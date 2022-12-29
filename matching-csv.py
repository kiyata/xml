import csv
import argparse

def formatDate(datestring):
    return datestring[6:10] + "-" + datestring[3:5] + "-" + datestring[0:2]

def formatTime(timestring):
    return timestring[0:2] + ":" + timestring[2:4] + ":00"

opMapping={
    "CDSUNIQUEID": "CDSID",
    "ORGPPPID": "OrgId",
    "APPTDATE": "AppDate",
    "NEWNHSNO": "NHSNo",
    "DOB": "DoB",
    "HOMEADD": "Postcd",
    "SEX": "Gendr",
    "TRETSPEF": "Tfc",
    "PATPATHID": "PathId",
    "ATTENDID": "AttID"
}

ecMapping={
    "CDSUNIQUEID": "CDSID",
    "PROCODE3": "OrgId",
    "ARRIVALDATE": "ArrDate",
    "ARRIVALTIME": "ArrTime",
    "DEPDUR": "DepDate",
    "DEPDATE": "DepTime",
    "DEPTIME": "NHSNo",
    "DOB": "DoB",
    "HOMEADD": "Postcd",
    "SEX": "Gendr",
    "AEATTENDNO": "AttID"
}
apcMapping={
    "CDSUNIQUEID": "CDSID",
    "ORGPPPID": "OrgId",
    "EPISTART": "EpStDte",
    "EPIEND": "EpEnDte",
    "PROVSPNO": "HSpellNo",
    "EPIORDER": "EpiNo",
    "NEWNHSNO": "NHSNo",
    "DOB": "DoB",
    "HOMEADD": "Postcd",
    "SEX": "Gendr",
    "PATPATHID": "PathId"
}

def main(feed_type, input, output):
    mapping = ""
    if feed_type == 'OP':
        mapping = opMapping
    elif feed_type == 'EC':
        mapping = ecMapping
    elif feed_type == 'APC':
        mapping = apcMapping

    f = open(output, 'w', newline='', encoding='utf-8')
    writer = csv.writer(f)

    writer.writerow(mapping.values())
    with open(input, 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for line in reader:
            row = []
            for key in mapping:
                value = line[key].strip()
                row.append(value)

            writer.writerow(row)

    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--feed', '-f', help="feed type (APC)", type=str)
    parser.add_argument('--input', '-i', help="Input CSV file from CSDS or MHDS, e.g. op.csv", type=str)
    parser.add_argument('--output', '-o', help="Output file, e.g. op_output.csv", type=str)
    args = parser.parse_args()
    main(args.feed, args.input, args.output)

