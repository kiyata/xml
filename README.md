# PLICS - XML Data Generator

# Python version 3.9

## Setup
- `git clone https://git.digital.nhs.uk/DMS/plics/plics-tools/plics-xml-gen.git `
- `python setup.py install`


## Help
- `python activity-xml-generator.py --help` 
- `python activity-xml-generator.py random  --help`
- `python activity-xml-generator.py from-csv  --help`
- `python activity-xml-generator.py validate-xml  --help`


## Create random data
- `python activity-xml-generator.py random [OPTIONS] FEED_TYPE ORGANISATION`

Arguments:
  FEED_TYPE     feed type code [EC, APC, OP, SWC, SI, MHCC, MHPS, AMB, IAPT, CSAPC, CSEC, CSCC, CSOP, CSSI]
                [required]

  ORGANISATION  organisation code between 3 and 5 alphanumeric. ex. ORG01
                [required]


Options:
  --month TEXT          allowed values M01, M02 ... M12  [default: (dynamic)]
  --activities INTEGER  number of activities  [default: 10]
  --overr-config TEXT   file path to override config.ini values (check sample
                        file on resource > samples)

  --overr-fields TEXT   file path to override fields values (check sample file
                        on resource > samples)

  --help                Show this message and exit.


### command random examples
* basic call with only mandatory fields
`python activity-xml-generator.py random EC ORG01`

* a specific amount of activities for example 10.000:<br/>
 `python activity-xml-generator.py random EC ORG01 --activities 10000`

* providing the exact month<br/>
`python activity-xml-generator.py random EC ORG01 --month M10`

Note: all the options can be provided in combination.


### --overr-fields  (override fields file path)

Define field-values-path parameter to inject a json file and provide just the wanted values for a field.

`python activity-xml-generator.py random EC ORG01 --overr-fields resources/samples/field-override.json`

field-override.json file content

```
{
  "ALL" : {
    "OrgId" : [ "RX9", "X26"]
  },
  "EC" : {
    "HRG" : ["HRG1","HRG2"],
    "DepTyp" : ["01"]
  }
}
```

Because each run works on just one feed type, we can gather just the fields that belongs to the selected feed type.

ALL Section will apply to any feed type.

### --overr-config (override config file path)

The application contains config.ini file with all the basic configurations for each run, these can be overridden providing a json file that refers what to change.

For example, if we need to create activities with one cost and one resource we would provide a json file like this one:

config-file.json file content

```
{
  "activity": {
    "min-resources": "1",
    "max-resources": "1",
    "min-costs": "1",
    "max-costs": "1"
  }
}
```
`python activity-xml-generator.py random EC ORG01 --overr-config resources/samples/config-file.json`

## Command from-csv
`python activity-xml-generator.py from-csv EC ORG01 resources/samples/csv-files/si-example.csv`


## Other development tools

## Generating REC files
`python rec-xml-generator.py --feed_type=CSREC --orgid=RH5 --financial_year=FY_2020-21 --month=M01`

#### Unique identifiers
Unique identifiers helps to create id's

    from src.helpers.UniqueIdentifier import UniqueIdentifier
    
    costActivityId = UniqueIdentifier('CAC')
    
    costActivityId.next()
    
    # The result from this method will be CAC001, CAC002 ...