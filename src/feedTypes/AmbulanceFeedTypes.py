import exrex
from faker import Faker

from app_config import AppConfig
from src.keys import AmbKeys
from src.feedTypes.XmlBase import XmlBase
from src.helpers import random_date as random_date

fake = Faker(['en_GB'])

config = AppConfig({})


class Ambulance(XmlBase):

    def __init__(self):
        super().__init__('AMB', config.amb_base_schema_path(), config.amb_schemas())

    def activity_fieldset(self):
        return [AmbKeys.OrgId,
                AmbKeys.AMB_OrgCom,
                AmbKeys.AMB_NHSNoAmb,
                AmbKeys.AMB_NhsSt,
                AmbKeys.AMB_IncID,
                AmbKeys.AMB_CllSrce,
                AmbKeys.AMB_CllCat,
                AmbKeys.AMB_MltPat,
                AmbKeys.AMB_UntsMob,
                AmbKeys.AMB_UntsSc,
                AmbKeys.AMB_UntsHsp,
                AmbKeys.AMB_IncDateTime,
                AmbKeys.AMB_JobDur,
                AmbKeys.AMB_RTyp,
                AmbKeys.AMB_OrgHdvr,
                AmbKeys.AMB_IncCcy]

    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(8,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])
        return {
            AmbKeys.OrgId: params[AmbKeys.OrgId],
            AmbKeys.AMB_OrgCom: exrex.getone('[a-zA-Z0-9]{3,5}'),
            AmbKeys.AMB_NHSNoAmb: exrex.getone('[0-9]{10}'),
            AmbKeys.AMB_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatus_Type'),
            AmbKeys.AMB_IncID: str(fake.random_number(digits=20, fix_len=False)),
            AmbKeys.AMB_CllSrce: self.schema_generator.random_enumeration('CallSource_Type'),
            AmbKeys.AMB_CllCat: self.schema_generator.random_enumeration('CallCategory_Type'),
            AmbKeys.AMB_MltPat: self.schema_generator.random_enumeration('MultiPatientIncident_Type'),
            AmbKeys.AMB_UntsMob: str(fake.random_number(digits=2, fix_len=False)),
            AmbKeys.AMB_UntsSc: str(fake.random_number(digits=2, fix_len=False)),
            AmbKeys.AMB_UntsHsp: str(fake.random_number(digits=2, fix_len=False)),
            AmbKeys.AMB_IncDateTime: self.schema_generator.random_date_time_between("IncidentDateTime_Type"),
            AmbKeys.AMB_JobDur: str(fake.random_number(digits=6, fix_len=False)),
            AmbKeys.AMB_RTyp: exrex.getone(
                '(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|97|98|99)(\|(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|97|98|99)){0,9}'),
            AmbKeys.AMB_OrgHdvr: exrex.getone('[a-zA-Z0-9]{3,6}'),
            AmbKeys.AMB_IncCcy: self.schema_generator.random_enumeration("IncidentCurrency_Type")
        }

    def xsd_file_path(self):
        return '{}/HCDS_AMB_schema_extract_{}_{}.xsd'.format(self.config.amb_schema_path(), 'Incidents',
                                                             self.config.amb_file_version())
