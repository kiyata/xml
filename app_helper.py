import json
from datetime import datetime
import random

from app_config import AppConfig
from src.feedTypes import IntegratedFeedTypes, AmbulanceFeedTypes, CsFeedTypes

# Common data values

MONTH_VALUES = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12"]
ALL_FEED_TAG = "ALL"


def feed_type_factory(feed_type):
    instance = None

    if feed_type == 'EC':
        instance = IntegratedFeedTypes.EmergencyCare()
    elif feed_type == 'APC':
        instance = IntegratedFeedTypes.AdmittedPatientCare()
    elif feed_type == 'OP':
        instance = IntegratedFeedTypes.Outpatient()
    elif feed_type == 'SWC':
        instance = IntegratedFeedTypes.SpecialistWareCare()
    elif feed_type == 'SI':
        instance = IntegratedFeedTypes.SupplementaryInformation()
    elif feed_type == 'MHCC':
        instance = IntegratedFeedTypes.CareContracts()
    elif feed_type == 'MHPS':
        instance = IntegratedFeedTypes.ProviderSpells()
    elif feed_type == 'AMB':
        instance = AmbulanceFeedTypes.Ambulance()
    elif feed_type == 'IAPT':
        instance = IntegratedFeedTypes.IAPT()
    elif feed_type == 'CSAPC':
        instance = CsFeedTypes.AdmittedPatientCare()
    elif feed_type == 'CSEC':
        instance = CsFeedTypes.EmergencyCare()
    elif feed_type == 'CSOP':
        instance = CsFeedTypes.Outpatient()
    elif feed_type == 'CSSI':
        instance = CsFeedTypes.SupplementaryInformation()
    elif feed_type == 'CSCC':
        instance = CsFeedTypes.CareContacts()

    if not instance:
        raise AttributeError("feed type provided empty or not valid")

    return instance

# def rec_type_factory(feed_type):
#     instance = None
#
#     if feed_type == 'AMBREC':
#         instance = IntegratedFeedTypes.EmergencyCare()
#     elif feed_type == 'INTREC':
#         instance = IntegratedFeedTypes.AdmittedPatientCare()
#     elif feed_type == 'CSREC':
#         instance = IntegratedFeedTypes.AdmittedPatientCare()
#     if not instance:
#         raise AttributeError("feed type provided empty or not valid")
#
#     return instance

# provide {field:value} elements to be feed into
# the activity generation.
def read_override_fields(feed_type, file_path):
    override_fields = {}
    # fields provided from a json file
    if file_path is not None:
        with open(file_path) as json_file:
            json_content = json.load(json_file)
            if feed_type in json_content:
                override_fields.update(json_content[feed_type])
            if ALL_FEED_TAG in json_content:
                override_fields.update(json_content["ALL"])

    return override_fields


def initialise_configuration(override_config_path):
    # if overrd config path is provided load the values to override them with
    # the default config.ini values.
    config_provided = {}
    if override_config_path:
        with open(override_config_path) as json_file:
            config_provided = json.load(json_file)
    # merge default config with provided config
    AppConfig(config_provided)


def random_month():
    return random.choice(MONTH_VALUES)


def filename(feed_type, month, org):
    config = AppConfig({})
    file_template = 'output/{}_{}_{}_{}_{}_01.xml'
    return file_template.format(feed_type
                                , config.financial_year()
                                , month
                                , org
                                , datetime.now().strftime("%Y%m%dT%H%M"))
