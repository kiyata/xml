import datetime as dt
import xml.etree.cElementTree as ET

from faker import Faker

from src.helpers import random_date as random_date

fake = Faker(['en_GB'])


class SchemaGenerator:
    collections = {}

    def __init__(self, schema_base_path):
        self.root = ET.parse(schema_base_path).getroot()

    @staticmethod
    def __extract_tag_name(element):
        return element.tag[element.tag.rfind('}') + 1:]

    def is_tag_enumeration(self, element):
        return self.__extract_tag_name(element) == 'enumeration'

    @staticmethod
    def __validate_date(date_text, pattern):
        try:
            dt.datetime.strptime(date_text, pattern)
            return True
        except ValueError:
            raise ValueError("Incorrect data format, should be {}".format(pattern))

    def __enumerations(self, tag_name):
        items = []
        for element in self.root.find('.//*[@name="{}"]'.format(tag_name)).iter():
            if self.is_tag_enumeration(element):
                items.append(element.attrib.get('value'))
        if not items:
            raise ValueError("no values found with tag name {}".format(tag_name))
        return items

    def __date_between(self, tag_name, expected_format):
        items = []
        for element in self.root.find('.//*[@name="{}"]'.format(tag_name)).iter():
            date = element.attrib.get('value')
            if date and self.__validate_date(date, expected_format):
                items.append(date)
        return items

    def get_dates_from(self, tag_name):
        if tag_name not in self.collections:
            self.collections[tag_name] = self.__date_between(tag_name, '%Y-%m-%d')
        return self.collections[tag_name]

    def random_enumeration(self, tag_name):
        if tag_name not in self.collections:
            self.collections[tag_name] = self.__enumerations(tag_name)
        return fake.random.choice(self.collections[tag_name])

    def random_date_between(self, tag_name):
        if tag_name not in self.collections:
            self.collections[tag_name] = self.__date_between(tag_name, '%Y-%m-%d')
        dates = self.collections[tag_name]
        return random_date.date_between(dates[0], dates[1])

    def random_date_time_between(self, tag_name):
        if tag_name not in self.collections:
            self.collections[tag_name] = self.__date_between(tag_name, '%Y-%m-%dT%H:%M:%S')
        dates = self.collections[tag_name]
        return random_date.date_time_between(dates[0], dates[1])
