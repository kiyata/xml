import collections
import configparser

FILENAME = 'config.ini'


class AppConfig:
    class __AppConfig:
        def __init__(self, arg):
            self.val = arg

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, args):
        if not AppConfig.instance:
            instance_config = self.read_config_file()
            AppConfig.instance = AppConfig.__AppConfig(instance_config)
        # Hack to provide new config even the instance has been instantiated
        if len(args) > 0:
            instance_config = self.__merge_configs(self.read_config_file(), args)
            AppConfig.instance.val = instance_config

    def __getattr__(self, section, item):
        return self.instance.val[section][item]

    def rules_attr(self, item):
        return self.__getattr__('rules', item)

    def activity_attr(self, item):
        return self.__getattr__('activity', item)

    def file_attr(self, item):
        return self.__getattr__('file', item)

    def ambulance_attr(self, item):
        return self.__getattr__('ambulance', item)

    def integrated_attr(self, item):
        return self.__getattr__('integrated', item)

    def cs_attr(self, item):
        return self.__getattr__('cs', item)

    def rule_fail_when_field_not_exits(self):
        return self.rules_attr('fail-when-field-not-exists') == 'true'

    def xml_output_formatted(self):
        return self.rules_attr('xml_output_formatted') == 'true'

    def activity_min_resources(self):
        return int(self.activity_attr('min-resources'))

    def activity_max_resources(self):
        return int(self.activity_attr('max-resources'))

    def activity_min_costs(self):
        return int(self.activity_attr('min-costs'))

    def activity_max_costs(self):
        return int(self.activity_attr('max-costs'))

    def financial_year(self):
        return self.file_attr('financial-year')

    def amb_schema_path(self):
        return self.ambulance_attr('xml-schema-path')

    def amb_file_version(self):
        return self.ambulance_attr('xml-file-version')

    def amb_xmlns_ns(self):
        return self.ambulance_attr('xmlns-ns')

    def amb_schemas(self):
        return {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:ns": "http://Improvement.nhs.uk/HealthcareCostingDataSet/AMB/{}".format(self.amb_xmlns_ns())
        }
    def amb_base_schema_path(self):
        return '{}/HCDS_AMB_schema_base_elements_{}.xsd'.format(self.amb_schema_path(), self.amb_file_version())

    def integrated_schema_path(self):
        return self.integrated_attr('xml-schema-path')

    def integrated_file_version(self):
        return self.integrated_attr('xml-file-version')

    def integrated_xmlns_ns(self):
        return self.integrated_attr('xmlns-ns')

    def integrated_schemas(self):
        return {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:ns": "http://Improvement.nhs.uk/HealthcareCostingDataSet/{}".format(self.integrated_xmlns_ns())
        }

    # App defined paths

    def integrated_base_schema_path(self):
        return '{}/HCDS_schema_base_elements_{}.xsd'.format(self.integrated_schema_path(), self.integrated_file_version())

    def cs_schema_path(self):
        return self.cs_attr('xml-schema-path')

    def cs_file_version(self):
        return self.cs_attr('xml-file-version')

    def cs_xmlns_ns(self):
        return self.cs_attr('xmlns-ns')

    def cs_base_schema_path(self):
        return '{}/HCDS_CS_schema_base_elements_{}.xsd'.format(self.cs_schema_path(), self.cs_file_version())

    def cs_schemas(self):
        return {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xmlns:ns": "http://Improvement.nhs.uk/HealthcareCostingDataSet/CS/{}".format(self.cs_xmlns_ns())
        }
    @staticmethod
    def read_config_file():
        config = configparser.ConfigParser()
        config.read(FILENAME)
        dictionary = {}
        for section in config.sections():
            dictionary[section] = {}
            for option in config.options(section):
                dictionary[section][option] = config.get(section, option)
        return dictionary

    def __merge_configs(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.__merge_configs(d.get(k, {}), v)
            else:
                d[k] = v
        return d
