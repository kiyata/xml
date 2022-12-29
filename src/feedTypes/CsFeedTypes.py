import exrex
from faker import Faker

from app_config import AppConfig
from src.keys import CsKeys
from src.feedTypes.XmlBase import XmlBase
from src.helpers import random_date as random_date

fake = Faker(['en_GB'])

config = AppConfig({})


class EmergencyCare(XmlBase):

    def __init__(self):
        super().__init__('CSEC', config.cs_base_schema_path(), config.cs_schemas())

    def activity_fieldset(self):
        return [CsKeys.OrgId,
                CsKeys.PLEMI,
                CsKeys.EC_CDSID,
                CsKeys.EC_NHSNo,
                CsKeys.EC_NhsSt,
                CsKeys.EC_Postcd,
                CsKeys.EC_DoB,
                CsKeys.EC_Gendr,
                CsKeys.EC_AttID,
                CsKeys.EC_ArrDate,
                CsKeys.EC_ArrTime,
                CsKeys.EC_DepTyp,
                CsKeys.EC_DepDate,
                CsKeys.EC_DepTime,
                CsKeys.EC_HRG]
    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(8,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])
        return {
            CsKeys.OrgId: params[CsKeys.OrgId],
            CsKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            CsKeys.EC_CDSID: str(fake.random_number(digits=35, fix_len=False)),
            CsKeys.EC_NHSNo: str(fake.random_number(digits=10, fix_len=True)),
            CsKeys.EC_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatus_Type'),
            CsKeys.EC_Postcd: fake.postcode(),
            CsKeys.EC_DoB: str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)),
            CsKeys.EC_Gendr: self.schema_generator.random_enumeration('Gender_Type'),
            CsKeys.EC_AttID: str(fake.random_number(digits=12, fix_len=False)),
            CsKeys.EC_ArrDate: random_period[0].date().isoformat(),
            CsKeys.EC_ArrTime: random_period[0].time().isoformat(),
            CsKeys.EC_DepTyp: self.schema_generator.random_enumeration('CareStatus_Type'),
            CsKeys.EC_DepDate: random_period[1].date().isoformat(),
            CsKeys.EC_DepTime: random_period[1].time().isoformat(),
            CsKeys.EC_HRG: self.schema_generator.random_enumeration('HRGEC_Type')
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.cs_schema_path(), 'EmerCare',
                                                         self.config.cs_file_version())


class AdmittedPatientCare(XmlBase):

    def __init__(self):
        super().__init__('CSAPC', config.cs_base_schema_path(), config.cs_schemas())

    def activity_fieldset(self):
        return [CsKeys.OrgId,
                CsKeys.PLEMI,
                CsKeys.APC_CDSID,
                CsKeys.APC_NHSNo,
                CsKeys.APC_NhsSt,
                CsKeys.APC_Postcd,
                CsKeys.APC_DoB,
                CsKeys.APC_Gendr,
                CsKeys.APC_PathId,
                CsKeys.APC_PatOrgId,
                CsKeys.APC_Pod,
                CsKeys.APC_HSpellNo,
                CsKeys.APC_EpiNo,
                CsKeys.APC_EpStDte,
                CsKeys.APC_EpEnDte,
                CsKeys.APC_EpType,
                CsKeys.APC_Tfc,
                CsKeys.APC_CFBand,
                CsKeys.APC_EpGro,
                CsKeys.APC_HrgFce,
                CsKeys.APC_HrgSpl,
                CsKeys.APC_Alos]

    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(96,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])
        return {
            CsKeys.OrgId: params[CsKeys.OrgId],
            CsKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            CsKeys.APC_CDSID: str(fake.random_number(digits=35, fix_len=False)),
            CsKeys.APC_NHSNo: str(fake.random_number(digits=10, fix_len=True)),
            CsKeys.APC_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatus_Type'),
            CsKeys.APC_Postcd: fake.postcode(),
            CsKeys.APC_DoB: str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)),
            CsKeys.APC_Gendr: self.schema_generator.random_enumeration('Gender_Type'),
            CsKeys.APC_PathId: str(fake.random_number(digits=20, fix_len=False)),
            CsKeys.APC_PatOrgId: exrex.getone('([a-zA-Z0-9]{3,5})?'),
            CsKeys.APC_Pod: self.schema_generator.random_enumeration('PointOfDeliveryAPC_Type'),
            CsKeys.APC_HSpellNo: str(fake.random_number(digits=12, fix_len=False)),
            CsKeys.APC_EpiNo: exrex.getone('[0][1-9]|[1-7][0-9]|8[0-7]|9[8-9]'),
            CsKeys.APC_EpStDte: random_period[0].date().isoformat(),
            CsKeys.APC_EpEnDte: random_period[1].date().isoformat(),
            CsKeys.APC_EpType: self.schema_generator.random_enumeration('CompletionStatus_Type'),
            CsKeys.APC_Tfc: self.schema_generator.random_enumeration('TreatmentFunctionSpecialty_Type'),
            CsKeys.APC_CFBand: self.schema_generator.random_enumeration('CFBanding_Type'),
            CsKeys.APC_EpGro: self.schema_generator.random_enumeration('EpisodeGrouping_Type'),
            CsKeys.APC_HrgFce: self.schema_generator.random_enumeration('HRGAPC_Type'),
            CsKeys.APC_HrgSpl: self.schema_generator.random_enumeration('HRGAPC_Type'),
            CsKeys.APC_Alos: str(fake.random_number(digits=3, fix_len=False))
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.cs_schema_path(), 'AdmittedPatientCare',
                                                         self.config.cs_file_version())


class Outpatient(XmlBase):

    def __init__(self):
        super().__init__('CSOP', config.cs_base_schema_path(), config.cs_schemas())

    def activity_fieldset(self):
        return [
            CsKeys.OrgId,
            CsKeys.PLEMI,
            CsKeys.OP_CDSID,
            CsKeys.OP_NHSNo,
            CsKeys.OP_NhsSt,
            CsKeys.OP_Postcd,
            CsKeys.OP_DoB,
            CsKeys.OP_Gendr,
            CsKeys.OP_PathId,
            CsKeys.OP_PatOrgId,
            CsKeys.OP_Pod,
            CsKeys.OP_AttID,
            CsKeys.OP_AppDate,
            CsKeys.OP_AppTime,
            CsKeys.OP_Tfc,
            CsKeys.OP_CFBand,
            CsKeys.OP_WhConTyp,
            CsKeys.OP_HRG
        ]

    def new_random_activity(self, **params):
        return {
            CsKeys.OrgId: params[CsKeys.OrgId],
            CsKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            CsKeys.OP_CDSID: str(fake.random_number(digits=35, fix_len=False)),
            CsKeys.OP_NHSNo: str(fake.random_number(digits=10, fix_len=True)),
            CsKeys.OP_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatus_Type'),
            CsKeys.OP_Postcd: fake.postcode(),
            CsKeys.OP_DoB: str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)),
            CsKeys.OP_Gendr: self.schema_generator.random_enumeration('Gender_Type'),
            CsKeys.OP_PathId: str(fake.random_number(digits=20, fix_len=False)),
            CsKeys.OP_PatOrgId: exrex.getone('([a-zA-Z0-9]{3,5})?'),
            CsKeys.OP_Pod: self.schema_generator.random_enumeration('PointOfDeliveryOP_Type'),
            CsKeys.OP_AttID: str(fake.random_number(digits=12, fix_len=False)),
            CsKeys.OP_AppDate: self.schema_generator.random_date_between("DateOfFinYear_Type"),
            CsKeys.OP_AppTime: exrex.getone('(2[0-3]|1[0-9]|0[1-9]):[0-5][0-9]:[0-5][0-9]'),
            CsKeys.OP_Tfc: self.schema_generator.random_enumeration('TreatmentFunctionSpecialty_Type'),
            CsKeys.OP_CFBand: self.schema_generator.random_enumeration('CFBanding_Type'),
            CsKeys.OP_WhConTyp: self.schema_generator.random_enumeration('WheelchairContact_Type'),
            CsKeys.OP_HRG: self.schema_generator.random_enumeration('HRGOP_Type')
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.cs_schema_path(), 'Outpatient',
                                                         self.config.cs_file_version())


class SupplementaryInformation(XmlBase):

    def __init__(self):
        super().__init__('CSSI', config.cs_base_schema_path(), config.cs_schemas())

    def activity_fieldset(self):
        return [CsKeys.OrgId, CsKeys.PLEMI, CsKeys.SI_UnActDate, CsKeys.SI_CSIU, CsKeys.SI_UnCur]

    def new_random_activity(self, **params):
        return {
            CsKeys.OrgId: params[CsKeys.OrgId],
            CsKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            CsKeys.SI_UnActDate: self.schema_generator.random_date_between("DateOfFinYear_Type"),
            CsKeys.SI_CSIU: self.schema_generator.random_enumeration('UNBCurrencyScheme_Type'),
            CsKeys.SI_UnCur: self.schema_generator.random_enumeration('SupplInfoCurrency_Type')
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.cs_schema_path(), 'SupInf',
                                                         self.config.cs_file_version())

class CareContacts(XmlBase):

    def __init__(self):
        super().__init__('CSCC', config.cs_base_schema_path(), config.cs_schemas())

    def activity_fieldset(self):
        return [
            CsKeys.OrgId,
            CsKeys.PLEMI,
            CsKeys.CC_NHSNo,
            CsKeys.CC_NhsSt,
            CsKeys.CC_DoB,
            CsKeys.CC_Gendr,
            CsKeys.CC_SerReqID,
            CsKeys.CC_CareId,
            CsKeys.CC_CareDte,
            CsKeys.CC_ClinDuration,
            CsKeys.CC_TeamType,
            CsKeys.CC_CCSubject,
            CsKeys.CC_ConsultType,
            CsKeys.CC_CMedium,
            CsKeys.CC_LocCode,
            CsKeys.CC_GPTherapyInd,
            CsKeys.CC_ChsCcy
        ]

    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(8,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])
        rnd_cc_act = {
            CsKeys.OrgId: params[CsKeys.OrgId],
            CsKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            CsKeys.CC_NHSNo: str(fake.random_number(digits=10, fix_len=True)),
            CsKeys.CC_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatus_Type'),
            CsKeys.CC_DoB: str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)),
            CsKeys.CC_Gendr: self.schema_generator.random_enumeration('Gender_Type'),
            CsKeys.CC_SerReqID: str(fake.random_number(digits=20, fix_len=False)),
            CsKeys.CC_CareId: str(fake.random_number(digits=20, fix_len=False)),
            CsKeys.CC_CareDte: random_period[0].date().isoformat(),
            CsKeys.CC_ClinDuration: self.schema_generator.random_enumeration('ClinDuration_Type'),
            CsKeys.CC_TeamType: self.schema_generator.random_enumeration('TeamType_Type'),
            CsKeys.CC_ConsultType: self.schema_generator.random_enumeration('ConsultType_Type'),
            CsKeys.CC_CCSubject: self.schema_generator.random_enumeration('CCSubject_Type'),
            CsKeys.CC_CMedium: self.schema_generator.random_enumeration('CMedium_Type'),
            CsKeys.CC_LocCode: self.schema_generator.random_enumeration('LocCode_Type'),
            CsKeys.CC_GPTherapyInd: self.schema_generator.random_enumeration('GPTherapyInd_Type'),
            CsKeys.CC_ChsCcy: self.schema_generator.random_enumeration('ChsCcy_Type')
        }

        return rnd_cc_act

    def xsd_file_path(self):
        return '{}/HCDS_CC_schema_extract_{}_{}.xsd'.format(self.config.cs_schema_path(), 'CareContacts',
                                                            self.config.cs_file_version())