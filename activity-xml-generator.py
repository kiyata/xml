import ntpath
import os
import logging
import uuid

import typer
from xmlschema import XMLSchemaValidationError

import app_helper

app = typer.Typer()

logger = logging.getLogger('XML-GEN')
logger.setLevel(logging.DEBUG)

def setup_logger():
    # create file handler which logs even debug messages
    fh = logging.FileHandler('app.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


setup_logger()

running_identifier = uuid.uuid4()

feed_type_helper = "feed type code [EC, APC, OP, SWC, SI, MHCC, MHPS, AMB, IAPT, CSAPC, CSEC, CSCC, CSOP, CSSI]"
organisation_help = "organisation code between 3 and 5 alphanumeric. ex. ORG01"
csv_file_helper = "file path to csv file (check sample file on resource > samples)"
month_helper = "allowed values M01, M02 ... M12"
overr_config_helper = "file path to override config.ini values (check sample file on resources > samples)"
overr_fields_helper = "file path to override fields values (check sample file on resources > samples)"

@app.command()
def random(
        feed_type: str = typer.Argument(..., help=feed_type_helper)
        , organisation: str = typer.Argument(..., help=organisation_help)
        , month: str = typer.Option(app_helper.random_month, help=csv_file_helper)
        , activities: int = typer.Option(10, help=month_helper)
        , overr_config: str = typer.Option(None, help=overr_config_helper)
        , overr_fields: str = typer.Option(None, help=overr_fields_helper)
):
    log_info(f'command: {random.__name__}, parameters: {locals()}')
    validate_parameters_or_exit(organisation, month)

    # Initialise AppConfig from config.ini and override config provided fields if required
    app_helper.initialise_configuration(overr_config)

    months = month.split(",")
    for month in months:
        filename = app_helper.filename(feed_type, month, organisation)

        feed_gen = app_helper.feed_type_factory(feed_type)
        fields_provided = app_helper.read_override_fields(feed_type, overr_fields)
        feed_gen.generate_random_file(activities, organisation, filename, month, fields_provided)

        typer.echo(f'file: {filename} generated successfully')
        logger.info(f'run_id: {running_identifier}, file: {filename} generated successfully')


@app.command()
def from_csv(
        feed_type: str = typer.Argument(..., help=feed_type_helper)
        , organisation: str = typer.Argument(..., help=organisation_help)
        , csv_file: str = typer.Argument(..., help=csv_file_helper)
        , month: str = typer.Option(app_helper.random_month, help=csv_file_helper)
        , activities: int = typer.Option(10, help=month_helper)
        , overr_config: str = typer.Option(None, help=overr_config_helper)
        , overr_fields: str = typer.Option(None, help=overr_fields_helper)
):
    log_info(f'command: {from_csv.__name__}, parameters: {locals()}')
    validate_parameters_or_exit(organisation, month)

    # Initialise AppConfig from config.ini and override config provided fields if required
    app_helper.initialise_configuration(overr_config)

    filename = app_helper.filename(feed_type, month, organisation)

    feed_gen = app_helper.feed_type_factory(feed_type)
    fields_provided = app_helper.read_override_fields(feed_type, overr_fields)
    feed_gen.generate_file_from_partial_csv(csv_file, organisation, filename, month, fields_provided)

    typer.echo(f'file: {filename} generated successfully')
    log_info(f'file: {filename} generated successfully')


def validate_parameters_or_exit(organisation, months):
    if len(organisation) < 3 or len(organisation) > 5:
        log_error("organisation must be between 3 and 5")
        raise typer.Exit()
    _months = months.split(",")
    for month in _months:
        if month not in app_helper.MONTH_VALUES:
            log_error(f"Invalid month {month}")
            raise typer.Exit()


@app.command()
def validate_xml(file_path: str = typer.Argument(...,
                                                 help="file path to validate (ex. output/APC_FY2020-21_M05_ORG01_20210604T1639_01.xml)")):
    log_info(f'command: {validate_xml.__name__}, parameters: {locals()}')
    if not os.path.isfile(file_path):
        log_error(f"file {file_path} not found")
        return

    filename = ntpath.basename(file_path)
    feed_type_code = filename.split("_")[0]

    if feed_type_code in ('REC', 'INTREC', 'AMBREC', 'CSREC'):
        log_warn(f'feed-type:[{feed_type_code}] filename:[{filename}] not validated.')
        return

    try:
        feed_type = app_helper.feed_type_factory(feed_type_code)
        feed_type.validate_xml(file_path)
        log_info(f'feed-type:[{feed_type_code}] filename:[{filename}] is valid.')
    except XMLSchemaValidationError as err:
        print(err)


def log_info(message):
    logger.info(f'run_id: {running_identifier}, {message}')


def log_error(message):
    logger.error(f'run_id: {running_identifier}, {message}')


def log_warn(message):
    logger.warning(f'run_id: {running_identifier}, {message}')


if __name__ == '__main__':
    app()
