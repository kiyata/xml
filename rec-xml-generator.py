from datetime import datetime
from random import seed
from random import randint
from src.feedTypes.ReconciliationFeedType import ReconciliationFeedType
import argparse


def main(feed_type, orgid, financial_year, month):
    rec_type = ReconciliationFeedType()
    file_name = filename(feed_type, orgid, financial_year, month)
    rec_type.generate_file_for(feed_type, orgid, file_name)
    print('rec file: {} generated correctly'.format(file_name))


def filename(feed_type, organisation, financial_year, month):
    file_template = 'output/{}_{}_{}_{}_{}_01.xml'
    return file_template.format(feed_type
                                , financial_year
                                , get_month(month)
                                , organisation
                                , datetime.now().strftime("%Y%m%dT%H%M"))


def get_month(month):
    if month is None:
        seed(1)
        return 'M' + (str(randint(1, 10))).zfill(2)
    else:
        return month


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--feed_type', '-f', help="feed type (AMBREC or INTREC)", type=str)
    parser.add_argument('--orgid', '-o', help="OrgSubmittingID, e.g. RH5", type= str)
    parser.add_argument('--financial_year', '-y', help="Financial year, e.g. FY_2020-21", type=str)
    parser.add_argument('--month', '-m', help="Month, e.g. M01", type=str, default='M01')
    args = parser.parse_args()
    main(args.feed_type, args.orgid, args.financial_year, args.month)
