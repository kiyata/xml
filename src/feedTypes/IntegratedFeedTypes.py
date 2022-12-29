import exrex
from faker import Faker

from app_config import AppConfig
from src.keys import IntKeys
from src.feedTypes.XmlBase import XmlBase
from src.helpers import random_date as random_date

fake = Faker(['en_GB'])

config = AppConfig({})


class EmergencyCare(XmlBase):

    def __init__(self):
        super().__init__('EC', config.integrated_base_schema_path(), config.integrated_schemas())

    def activity_fieldset(self):
        return [IntKeys.OrgId,
                IntKeys.PLEMI,
                IntKeys.EC_CDSID,
                IntKeys.EC_NHSNo,
                IntKeys.EC_NhsSt,
                IntKeys.EC_Postcd,
                IntKeys.EC_DoB,
                IntKeys.EC_Gendr,
                IntKeys.EC_AttID,
                IntKeys.EC_ArrDate,
                IntKeys.EC_ArrTime,
                IntKeys.EC_DepTyp,
                IntKeys.EC_DepDate,
                IntKeys.EC_DepTime,
                IntKeys.EC_HRG]

    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(8,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])
        return {
            IntKeys.OrgId: params[IntKeys.OrgId],
            IntKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            IntKeys.EC_CDSID: str(fake.random_number(digits=35, fix_len=False)),
            IntKeys.EC_NHSNo: str(fake.random_number(digits=10, fix_len=True)),
            IntKeys.EC_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatus_Type'),
            IntKeys.EC_Postcd: fake.postcode(),
            IntKeys.EC_DoB: str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)),
            IntKeys.EC_Gendr: self.schema_generator.random_enumeration('Gender_Type'),
            IntKeys.EC_AttID: str(fake.random_number(digits=12, fix_len=False)),
            IntKeys.EC_ArrDate: random_period[0].date().isoformat(),
            IntKeys.EC_ArrTime: random_period[0].time().isoformat(),
            IntKeys.EC_DepTyp: self.schema_generator.random_enumeration('CareStatus_Type'),
            IntKeys.EC_DepDate: random_period[1].date().isoformat(),
            IntKeys.EC_DepTime: random_period[1].time().isoformat(),
            IntKeys.EC_HRG: self.schema_generator.random_enumeration('HRGEC_Type')
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.integrated_schema_path(), 'EmerCare',
                                                         self.config.integrated_file_version())


class AdmittedPatientCare(XmlBase):

    def __init__(self):
        super().__init__('APC', config.integrated_base_schema_path(), config.integrated_schemas())

    def activity_fieldset(self):
        return [IntKeys.OrgId,
                IntKeys.PLEMI,
                IntKeys.APC_CDSID,
                IntKeys.APC_NHSNo,
                IntKeys.APC_NhsSt,
                IntKeys.APC_Postcd,
                IntKeys.APC_DoB,
                IntKeys.APC_Gendr,
                IntKeys.APC_PathId,
                IntKeys.APC_PatOrgId,
                IntKeys.APC_Pod,
                IntKeys.APC_HSpellNo,
                IntKeys.APC_EpiNo,
                IntKeys.APC_EpStDte,
                IntKeys.APC_EpEnDte,
                IntKeys.APC_EpType,
                IntKeys.APC_Tfc,
                IntKeys.APC_CFBand,
                IntKeys.APC_HrgFce,
                IntKeys.APC_HrgSpl,
                IntKeys.APC_Alos]

    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(96,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])
        return {
            IntKeys.OrgId: params[IntKeys.OrgId],
            IntKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            IntKeys.APC_CDSID: str(fake.random_number(digits=35, fix_len=False)),
            IntKeys.APC_NHSNo: str(fake.random_number(digits=10, fix_len=True)),
            IntKeys.APC_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatus_Type'),
            IntKeys.APC_Postcd: fake.postcode(),
            IntKeys.APC_DoB: str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)),
            IntKeys.APC_Gendr: self.schema_generator.random_enumeration('Gender_Type'),
            IntKeys.APC_PathId: str(fake.random_number(digits=20, fix_len=False)),
            IntKeys.APC_PatOrgId: exrex.getone('([a-zA-Z0-9]{3,5})?'),
            IntKeys.APC_Pod: self.schema_generator.random_enumeration('PointOfDeliveryAPC_Type'),
            IntKeys.APC_HSpellNo: str(fake.random_number(digits=12, fix_len=False)),
            IntKeys.APC_EpiNo: exrex.getone('[0][1-9]|[1-7][0-9]|8[0-7]|9[8-9]'),
            IntKeys.APC_EpStDte: random_period[0].date().isoformat(),
            IntKeys.APC_EpEnDte: random_period[1].date().isoformat(),
            IntKeys.APC_EpType: self.schema_generator.random_enumeration('CompletionStatus_Type'),
            IntKeys.APC_Tfc: self.schema_generator.random_enumeration('TreatmentFunctionSpecialty_Type'),
            IntKeys.APC_CFBand: self.schema_generator.random_enumeration('CFBanding_Type'),
            IntKeys.APC_HrgFce: self.schema_generator.random_enumeration('HRGAPC_Type'),
            IntKeys.APC_HrgSpl: self.schema_generator.random_enumeration('HRGAPC_Type'),
            IntKeys.APC_Alos: str(fake.random_number(digits=3, fix_len=False))
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.integrated_schema_path(), 'AdmittedPatientCare',
                                                         self.config.integrated_file_version())


class Outpatient(XmlBase):

    def __init__(self):
        super().__init__('OP', config.integrated_base_schema_path(), config.integrated_schemas())

    def activity_fieldset(self):
        return [
            IntKeys.OrgId, IntKeys.PLEMI,
            IntKeys.OP_CDSID, IntKeys.OP_NHSNo,
            IntKeys.OP_NhsSt, IntKeys.OP_Postcd,
            IntKeys.OP_DoB, IntKeys.OP_Gendr,
            IntKeys.OP_PathId, IntKeys.OP_PatOrgId,
            IntKeys.OP_Pod, IntKeys.OP_AttID,
            IntKeys.OP_AppDate, IntKeys.OP_AppTime,
            IntKeys.OP_Tfc, IntKeys.OP_CFBand,
            IntKeys.OP_HRG
        ]

    def new_random_activity(self, **params):
        return {
            IntKeys.OrgId: params[IntKeys.OrgId],
            IntKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            IntKeys.OP_CDSID: str(fake.random_number(digits=35, fix_len=False)),
            IntKeys.OP_NHSNo: str(fake.random_number(digits=10, fix_len=True)),
            IntKeys.OP_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatus_Type'),
            IntKeys.OP_Postcd: fake.postcode(),
            IntKeys.OP_DoB: str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)),
            IntKeys.OP_Gendr: self.schema_generator.random_enumeration('Gender_Type'),
            IntKeys.OP_PathId: str(fake.random_number(digits=20, fix_len=False)),
            IntKeys.OP_PatOrgId: exrex.getone('([a-zA-Z0-9]{3,5})?'),
            IntKeys.OP_Pod: self.schema_generator.random_enumeration('PointOfDeliveryOP_Type'),
            IntKeys.OP_AttID: str(fake.random_number(digits=12, fix_len=False)),
            IntKeys.OP_AppDate: self.schema_generator.random_date_between("DateOfFinYear_Type"),
            IntKeys.OP_AppTime: exrex.getone('(2[0-3]|1[0-9]|0[1-9]):[0-5][0-9]:[0-5][0-9]'),
            IntKeys.OP_Tfc: self.schema_generator.random_enumeration('TreatmentFunctionSpecialty_Type'),
            IntKeys.OP_CFBand: self.schema_generator.random_enumeration('CFBanding_Type'),
            IntKeys.OP_HRG: self.schema_generator.random_enumeration('HRGOP_Type')
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.integrated_schema_path(), 'Outpatient',
                                                         self.config.integrated_file_version())


class SpecialistWareCare(XmlBase):

    def __init__(self):
        super().__init__('SWC', config.integrated_base_schema_path(), config.integrated_schemas())

    def activity_fieldset(self):
        return [IntKeys.OrgId,
                IntKeys.PLEMI,
                IntKeys.SWC_UnAct,
                IntKeys.SWC_CCLI,
                IntKeys.SWC_CCUF,
                IntKeys.SWC_UnActDate,
                IntKeys.SWC_CCPerType,
                IntKeys.SWC_OrgsSupp,
                IntKeys.SWC_UnHRG]

    def new_random_activity(self, **params):
        return {
            IntKeys.OrgId: params[IntKeys.OrgId],
            IntKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            IntKeys.SWC_UnAct: self.schema_generator.random_enumeration('UNBActivity_Type'),
            IntKeys.SWC_CCLI: exrex.getone('[A-Z0-9]{8}'),
            IntKeys.SWC_CCUF: self.schema_generator.random_enumeration('CriticalCareUnit_Type'),
            IntKeys.SWC_UnActDate: self.schema_generator.random_date_between("DateOfFinYear_Type"),
            IntKeys.SWC_CCPerType: self.schema_generator.random_enumeration('CompletionStatus_Type'),
            IntKeys.SWC_OrgsSupp: self.schema_generator.random_enumeration('OrgansSupported_Type'),
            IntKeys.SWC_UnHRG: self.schema_generator.random_enumeration('UNBHRG_Type')
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.integrated_schema_path(), 'SpecWard',
                                                         self.config.integrated_file_version())


class SupplementaryInformation(XmlBase):

    def __init__(self):
        super().__init__('SI', config.integrated_base_schema_path(), config.integrated_schemas())

    def activity_fieldset(self):
        return [IntKeys.OrgId, IntKeys.PLEMI, IntKeys.SI_UnActDate, IntKeys.SI_CSIU, IntKeys.SI_UnCur]

    def new_random_activity(self, **params):
        return {
            IntKeys.OrgId: params[IntKeys.OrgId],
            IntKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            IntKeys.SI_UnActDate: self.schema_generator.random_date_between("DateOfFinYear_Type"),
            IntKeys.SI_CSIU: self.schema_generator.random_enumeration('UNBCurrencyScheme_Type'),
            IntKeys.SI_UnCur: self.schema_generator.random_enumeration('SupplInfoCurrency_Type')
        }

    def xsd_file_path(self):
        return '{}/HCDS_schema_extract_{}_{}.xsd'.format(self.config.integrated_schema_path(), 'SupInf',
                                                         self.config.integrated_file_version())

class CareContracts(XmlBase):

    def __init__(self):
        super().__init__('MHCC', config.integrated_base_schema_path(), config.integrated_schemas())

    def activity_fieldset(self):
        return [IntKeys.OrgId,
                IntKeys.PLEMI,
                IntKeys.MHCC_SerReqID,
                IntKeys.MHCC_CareId,
                IntKeys.MHCC_CareDte,
                IntKeys.MHCC_Attendance,
                IntKeys.MHCC_PatCAS,
                IntKeys.MHCC_Cluster]

    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(8,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])

        rnd_ps_act = {
            IntKeys.OrgId: params[IntKeys.OrgId],
            IntKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            IntKeys.MHCC_SerReqID: str(fake.random_number(digits=20, fix_len=False)),
            IntKeys.MHCC_CareId: str(fake.random_number(digits=20, fix_len=False)),
            IntKeys.MHCC_CareDte: random_period[0].date().isoformat(),
            IntKeys.MHCC_Attendance: self.schema_generator.random_enumeration('Attendance_Type'),
            IntKeys.MHCC_PatCAS: self.schema_generator.random_enumeration('CareStatus_Type'),
            IntKeys.MHCC_Cluster: self.schema_generator.random_enumeration('Cluster_Type')
        }

        # Ammend logic where Cluster does not exist if PatCas is different than 01
        if rnd_ps_act[IntKeys.MHCC_PatCAS] not in '01':
            rnd_ps_act[IntKeys.MHCC_Cluster] = ''

        return rnd_ps_act

    def xsd_file_path(self):
        return '{}/HCDS_MH_schema_extract_{}_{}.xsd'.format(self.config.integrated_schema_path(), 'CareContacts',
                                                            self.config.integrated_file_version())


class ProviderSpells(XmlBase):

    def __init__(self):
        super().__init__('MHPS', config.integrated_base_schema_path(), config.integrated_schemas())

    def activity_fieldset(self):
        return [IntKeys.OrgId,
                IntKeys.PLEMI,
                IntKeys.MHPS_SerReqID,
                IntKeys.MHPS_HSpellNo,
                IntKeys.MHPS_HSpllStDte,
                IntKeys.MHPS_HSpllDisDte,
                IntKeys.MHPS_SpllType,
                IntKeys.MHPS_PatCAS,
                IntKeys.MHPS_PatCASStDte,
                IntKeys.MHPS_PatCASEndDte,
                IntKeys.MHPS_Cluster,
                IntKeys.MHPS_StartDateCareClust,
                IntKeys.MHPS_EndDateCareClust]

    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(1480,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])

        rnd_ps_act = {
            IntKeys.OrgId: params[IntKeys.OrgId],
            IntKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            IntKeys.MHPS_SerReqID: str(fake.random_number(digits=20, fix_len=False)),
            IntKeys.MHPS_HSpellNo: str(fake.random_number(digits=12, fix_len=False)),
            IntKeys.MHPS_HSpllStDte: random_period[0].date().isoformat(),
            IntKeys.MHPS_HSpllDisDte: random_period[1].date().isoformat(),
            IntKeys.MHPS_SpllType: self.schema_generator.random_enumeration('CompletionStatus_Type'),
            IntKeys.MHPS_PatCAS: self.schema_generator.random_enumeration('CareStatus_Type'),
            IntKeys.MHPS_PatCASStDte: random_period[0].date().isoformat(),
            IntKeys.MHPS_PatCASEndDte: random_period[1].date().isoformat(),
            IntKeys.MHPS_Cluster: self.schema_generator.random_enumeration('Cluster_Type'),
            IntKeys.MHPS_StartDateCareClust: random_period[0].date().isoformat(),
            IntKeys.MHPS_EndDateCareClust: random_period[1].date().isoformat()

        }

        # Amend logic where Cluster does not exist if PatCas is different than 01
        if rnd_ps_act[IntKeys.MHPS_PatCAS] not in '01':
            rnd_ps_act[IntKeys.MHPS_Cluster] = ''
            rnd_ps_act[IntKeys.MHPS_StartDateCareClust] = ''
            rnd_ps_act[IntKeys.MHPS_EndDateCareClust] = ''

        return rnd_ps_act

    def xsd_file_path(self):
        return '{}/HCDS_MH_schema_extract_{}_{}.xsd'.format(self.config.integrated_schema_path(), 'ProviderSpells',
                                                            self.config.integrated_file_version())

class IAPT(XmlBase):

    def __init__(self):
        super().__init__('IAPT', config.integrated_base_schema_path(), config.integrated_schemas())

    def activity_fieldset(self):
        return [IntKeys.OrgId,
                IntKeys.PLEMI,
                IntKeys.IAPT_NHSNo,
                IntKeys.IAPT_NhsSt,
                IntKeys.IAPT_Postcd,
                IntKeys.IAPT_DoB,
                IntKeys.IAPT_Gendr,
                IntKeys.IAPT_LptID,
                IntKeys.IAPT_SerReqID,
                IntKeys.IAPT_CareConDate,
                IntKeys.IAPT_CareConTime,
                IntKeys.IAPT_Attendance,
                IntKeys.IAPT_PatCAS,
                IntKeys.IAPT_Cluster]

    def new_random_activity(self, **params):
        random_period = random_date.hours_period_time_between(8,
                                                              self.period_start_end[0],
                                                              self.period_start_end[1])

        rnd_ps_act = {
            IntKeys.OrgId: params[IntKeys.OrgId],
            IntKeys.PLEMI: exrex.getone('[A-Z]{3}[0-9]{43}-[0-9]{3}'),
            IntKeys.IAPT_NHSNo: exrex.getone('([0-9]{10})?'),
            IntKeys.IAPT_NhsSt: self.schema_generator.random_enumeration('NHSNumberStatusNN_Type'),
            IntKeys.IAPT_Postcd: fake.postcode(),
            IntKeys.IAPT_DoB: str(fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)),
            IntKeys.IAPT_Gendr: self.schema_generator.random_enumeration('Gender_Type'),
            IntKeys.IAPT_LptID: str(fake.random_number(digits=20, fix_len=False)),
            IntKeys.IAPT_SerReqID: str(fake.random_number(digits=20, fix_len=False)),
            IntKeys.IAPT_CareConID: str(fake.random_number(digits=20, fix_len=False)),
            IntKeys.IAPT_CareConDate: random_period[0].date().isoformat(),
            IntKeys.IAPT_CareConTime: random_period[0].time().isoformat(),
            IntKeys.IAPT_Attendance: self.schema_generator.random_enumeration('Attendance_Type'),
            IntKeys.IAPT_PatCAS: self.schema_generator.random_enumeration('CareStatus_Type'),
            IntKeys.IAPT_Cluster: self.schema_generator.random_enumeration('Cluster_Type'),
        }

        # Ammend logic where Cluster does not exist if PatCas is different than 01
        if rnd_ps_act[IntKeys.IAPT_PatCAS] not in '01':
            rnd_ps_act[IntKeys.IAPT_Cluster] = ''

        return rnd_ps_act

    def xsd_file_path(self):
        return '{}/HCDS_IAPT_schema_extract_{}_{}.xsd'.format(self.config.integrated_schema_path(), 'IAPT',
                                                              self.config.integrated_file_version())
