import abc
import calendar
import csv
import random
import re
import xml.etree.cElementTree as ET
from datetime import datetime
from xml.etree import ElementTree

import xmlschema
from faker import Faker

from app_config import AppConfig
from src.keys import CostKeys
from src.helpers.SchemaGenerator import SchemaGenerator

fake = Faker(['en_GB'])


# noinspection PyPackageRequirements
class XmlBase(abc.ABC):
    cost_fieldset = [CostKeys.ActCstID, CostKeys.ActCnt, CostKeys.ResCstID, CostKeys.TotCst]

    period_start_end = []

    def __init__(self, feed_type, schema_base_path, root_attributes):
        self.feedTypeStr = feed_type
        self.fieldset = self.activity_fieldset()
        self.cost_fieldset = self.cost_fieldset
        self.config = AppConfig({})
        self.schema_generator = SchemaGenerator(schema_base_path)
        self.root_attributes = root_attributes

    @abc.abstractmethod
    def activity_fieldset(self):
        raise NotImplementedError("method not implemented")

    # noinspection PyPackageRequirements
    @abc.abstractmethod
    def new_random_activity(self, **params):
        raise NotImplementedError("method not implemented")

    @abc.abstractmethod
    def xsd_file_path(self):
        raise NotImplementedError("method not implemented")

    def validate_xml(self, file_path):
        schema = xmlschema.XMLSchema(self.xsd_file_path())
        errors = schema.iter_errors(file_path)
        for error in errors:
            print('------ FIELD ERROR ------')
            print('\n')
            print("Element: {}".format(error.elem.tag[error.elem.tag.rfind('}') + 1:]))
            print("value: {}".format(error.args[1]))
            print("xsdFacets: {}".format(error.args[0]))
            print("Reason: {}".format(error.reason))
            print('\n')

    @staticmethod
    def __prefix(tree, prefix):
        for elem in tree.iter():
            elem.tag = prefix + ":" + elem.tag
        return tree

    @staticmethod
    def __total_cost(element):
        total = 0
        for cost in element.findall(".//TotCst"):
            total += round(float(cost.text), 2)
        return round(total, 2)

    def load_period_start_end_from(self, month):
        # from month definition calc month number
        month_number = int(month[-2:]) - 1
        # from xsd get the start date from a financial Year
        fin_year_start_str = self.schema_generator.get_dates_from("DateOfFinYear_Type")[0]
        fin_year_start = datetime.strptime(fin_year_start_str, '%Y-%m-%d')
        # add the number of months provided to get the desired date
        period_start = self.__add_months(fin_year_start, month_number)
        # calculate the last day in this month
        last_day_month = calendar.monthrange(period_start.year, period_start.month)[1]
        # build the dates with those values
        start_date = datetime(period_start.year, period_start.month, 1)
        end_date = datetime(period_start.year, period_start.month, last_day_month)

        return [start_date.date().isoformat(), end_date.date().isoformat()]

    def __add_months(self, sourcedate, months):
        month = sourcedate.month - 1 + months
        year = sourcedate.year + month // 12
        month = month % 12 + 1
        day = min(sourcedate.day, calendar.monthrange(year, month)[1])
        return datetime(year, month, day)

    def has_headers(self, csv_file):
        with open(csv_file, 'r') as file:
            return csv.Sniffer().has_header(file.readline(1024))

    def load_activities_from(self, csv_file):
        activities = []
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            if self.has_headers(csv_file):
                remove_headers = next(reader, None)
            for row in reader:
                activities.append(self.__build_activity_cost(row))
        return activities

    def __build_activity_cost(self, row):
        activity = {}
        cost = {}
        activity_row = row[0:len(self.fieldset)]
        for x in range(len(activity_row)):
            activity[self.fieldset[x]] = activity_row[x]

        cost_row = row[len(self.fieldset):len(row)]
        for x in range(len(cost_row)):
            cost[self.cost_fieldset[x]] = cost_row[x]

        return activity, cost

    def load_partial_activity_from(self, csv_file):
        activities = []
        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            headers = next(reader, None)
            for row in reader:
                if len(row) == len(headers):
                    activity = {}
                    total_cost = None
                    for x in range(len(headers)):
                        if headers[x] in CostKeys.TotCst:
                            total_cost = row[x]
                        else:
                            activity[headers[x]] = row[x]
                    activities.append((activity, total_cost))
                else:
                    print("Ignoring invalid row: " + str(row))
        return activities

    def __populate_header(self, header, total_costs, n_activities, organisation):
        ET.SubElement(header, "OrgSubmittingID").text = organisation
        ET.SubElement(header, "FinYr").text = self.config.financial_year()
        ET.SubElement(header, "PeriodStartDate").text = self.period_start_end[0]
        ET.SubElement(header, "PeriodEndDate").text = self.period_start_end[1]
        ET.SubElement(header, "CreateDateTime").text = datetime.now().strftime("%Y-%m-%dT%H:%M:00")
        ET.SubElement(header, "FeedType").text = self.feedTypeStr
        ET.SubElement(header, "NoOfActivityRecords").text = str(n_activities)
        ET.SubElement(header, "TotalCosts").text = str(total_costs)

    @staticmethod
    def __insert_activity_from_cost(element, cost):
        cost_activity = ET.SubElement(element, "CstActivity")
        ET.SubElement(cost_activity, CostKeys.ActCstID).text = cost[CostKeys.ActCstID]
        ET.SubElement(cost_activity, CostKeys.ActCnt).text = cost[CostKeys.ActCnt]
        resource = ET.SubElement(cost_activity, "Resource")
        ET.SubElement(resource, CostKeys.ResCstID).text = cost[CostKeys.ResCstID]
        ET.SubElement(resource, CostKeys.TotCst).text = cost[CostKeys.TotCst]

    def __insert_activity_cost(self, activity_node, total_cost):
        if total_cost is not None:
            self.__insert_activity_cost_with_total_cost(activity_node, total_cost)
        else:
            self.__insert_random_costs(activity_node)

    # Create a random cost element which contains one resource
    # with the provided total cost.
    def __insert_activity_cost_with_total_cost(self, element, total_cost):
        rand_cost = {CostKeys.ActCstID: self.schema_generator.random_enumeration('CollectionActivityID_Type'),
                     CostKeys.ActCnt: str(fake.random_number(digits=4)),
                     CostKeys.ResCstID: self.schema_generator.random_enumeration('CollectionResourceID_Type'),
                     CostKeys.TotCst: total_cost}
        self.__insert_activity_from_cost(element, rand_cost)

    def __insert_random_activity_cost(self, element):
        cost_activity = ET.SubElement(element, "CstActivity")
        ET.SubElement(cost_activity, CostKeys.ActCstID).text = self.schema_generator.random_enumeration(
            'CollectionActivityID_Type')
        ET.SubElement(cost_activity, CostKeys.ActCnt).text = str(fake.random_number(digits=4))
        self.__insert_random_cost_resources(cost_activity)

    def __insert_random_activity_cost_resource(self, cost_activity_element):
        resource = ET.SubElement(cost_activity_element, "Resource")
        ET.SubElement(resource, CostKeys.ResCstID).text = self.schema_generator.random_enumeration(
            'CollectionResourceID_Type')
        ET.SubElement(resource, CostKeys.TotCst).text = str(
            fake.pydecimal(left_digits=3, right_digits=2, positive=True, min_value=1, max_value=999))

    def __insert_random_cost_resources(self, cost_activity_element):
        n_resources = random.randint(self.config.activity_min_resources(), self.config.activity_max_resources())
        for _ in range(n_resources):
            self.__insert_random_activity_cost_resource(cost_activity_element)

    def __insert_random_costs(self, element):
        n_costs = random.randint(self.config.activity_min_costs(), self.config.activity_max_costs())
        for _ in range(n_costs):
            self.__insert_random_activity_cost(element)

    @staticmethod
    def add_node(parent, node_name, dict_fields):
        node = ET.SubElement(parent, node_name)
        for key, value in dict_fields.items():
            # In order to add attributes we can send it inside the value
            # with double square bracket ex.: [[attribute=true]]
            if re.match("\[\[.*?\]\]", value):
                attr = value[value.find("[[") + 2:value.find("]]")].split('=')
                ET.SubElement(node, key, {attr[0]: attr[1]})
            else:
                ET.SubElement(node, key).text = value
        return node

    # random_choice_of function
    # Given a dictionary (fields) with multiple elements
    #  { "key_a" : "val_a",
    #    "key_b" : ["l1","l2"]}
    # Return one choice of each element
    #  { "key_a" : "val_a",
    #    "key_b" : "l2" }
    #
    @staticmethod
    def random_choice_of(fields):
        rnd = {}
        for key, value in fields.items():
            if isinstance(value, str):
                rnd[key] = value
            elif isinstance(value, list):
                rnd[key] = random.choice(value)
        return rnd

    def __update_provided_fields(self, activity, partial_activity):
        for key, value in partial_activity.items():
            if key in activity:
                activity.update({key: value})
            else:
                if self.config.rule_fail_when_field_not_exits():
                    raise NameError("key provided: {} is not a field on the selected activity".format(key))
        return activity

    #  RANDOM DATA
    #  All this data will be random and validated against the schemas
    #  provided

    def generate_random_file(self, n_activities, organisation, filename, month, fields_provided):
        self.period_start_end = self.load_period_start_end_from(month)
        xml_root = ET.Element("HCDSExtract", self.root_attributes)
        params = {CostKeys.OrgId: organisation}
        message_header = ET.SubElement(xml_root, "MessageHeader")
        message_body = ET.SubElement(xml_root, "MessageBody")
        for x in range(n_activities):
            activity = self.new_random_activity(**params)
            activity.update(self.random_choice_of(fields_provided))
            activity_node = self.add_node(message_body, "Activity", activity)
            self.__insert_random_costs(activity_node)
        self.__populate_header(message_header, self.__total_cost(message_body), n_activities, organisation)
        self.__write_file(xml_root, filename)

    #  FROM CSV FILE
    #  Generate a file from a CSV, this will help test strategy
    #  to feed into the application all the needed data for testing.
    #  The function expect one activity and one cost each row.

    def generate_file_from(self, csv_file, organisation, filename, month):
        self.period_start_end = self.load_period_start_end_from(month)
        xml_root = ET.Element("HCDSExtract", self.root_attributes)
        message_header = ET.SubElement(xml_root, "MessageHeader")
        message_body = ET.SubElement(xml_root, "MessageBody")
        activity_tuple = self.load_activities_from(csv_file)
        for activity, cost in activity_tuple:
            activity_node = self.add_node(message_body, "Activity", activity)
            self.__insert_activity_from_cost(activity_node, cost)
        self.__populate_header(message_header, self.__total_cost(message_body), len(activity_tuple), organisation)
        self.__write_file(xml_root, filename)

    #  FROM PARTIAL CSV FILE
    #  Generate a file from a partial CSV, provide a set of fields from
    #  and the remaining fields will be populated with random data.
    #  The function expect some columns from activity, the cost will be populated random

    def generate_file_from_partial_csv(self, csv_file, organisation, filename, month, fields_provided):
        self.period_start_end = self.load_period_start_end_from(month)
        xml_root = ET.Element("HCDSExtract", self.root_attributes)
        message_header = ET.SubElement(xml_root, "MessageHeader")
        message_body = ET.SubElement(xml_root, "MessageBody")
        params = {CostKeys.OrgId: organisation}
        partial_activities = self.load_partial_activity_from(csv_file)
        for partial_activity, totalCost in partial_activities:
            rnd_activity = self.new_random_activity(**params)
            rnd_activity.update(self.random_choice_of(fields_provided))
            activity = self.__update_provided_fields(
                rnd_activity,
                partial_activity
            )
            activity_node = self.add_node(message_body, "Activity", activity)
            self.__insert_activity_cost(activity_node, totalCost)

        self.__populate_header(message_header, self.__total_cost(message_body), len(partial_activities), organisation)
        self.__write_file(xml_root, filename)

    def __write_file(self, element, filename):
        xml_with_ns = ET.ElementTree(element)
        self.__prefix(xml_with_ns, "ns")
        if self.config.xml_output_formatted():
            xml_with_ns.write(filename, xml_declaration=True,
                              encoding='utf-8',
                              method='xml')
        else:
            self.__write_file_formatted(xml_with_ns, filename)

    @staticmethod
    def __write_file_formatted(xml_with_ns, filename):
        import lxml.etree as lxml_etree
        tree_content = ElementTree.tostring(xml_with_ns.getroot(), encoding="utf-8")
        tree_transformed = lxml_etree.fromstring(tree_content)
        content_formatted = lxml_etree.tostring(tree_transformed, pretty_print=True).decode("utf-8")
        f = open(filename, "w")
        f.write("<?xml version='1.0' encoding='utf-8'?>")
        f.write(content_formatted)
        f.close()
