# PLICS - XML Data Generator

Basic client to create XML test data for PLICS collections.

## Requirements

* Git

You need *Git* to clone the project, find all OS versions in this link:

https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

* Python (min ver. 3.7.7 , max ver 3.8.9)

In Ubuntu, Mint and Debian you can install Python 3 like this:

    $ sudo apt-get install python3 python3-pip

For other Linux flavors, macOS and Windows, packages are available at

http://www.python.org/getit/



## How to run it


Clone the project locally

    git clone https://git.digital.nhs.uk/DMS/plics/plics-tools/plics-xml-gen.git

To ensure the required python packages are installed, run the following setup file before the running the app:

    python setup.py install


### Using xml-gen.py Client

Once we have python and all the libraries ready, use the client *xm-gen.py* to run all the available commands.

    python xml-gen.py --help

The available commands are:
* random
* from-csv
* validate-xml

        python xml-gen.py <command>


### Access help for commands
To access each command help lines, type the command follow by --help

    python xml-gen.py random  --help
    python xml-gen.py from-csv  --help
    python xml-gen.py validate-xml  --help


### Command Random

Random functionality will provide a set of activities filled with random data provided from the xsd files or pattern generators.
First type the following command  ```` python xml-gen.py random  --help ```` to check which arguments needs to be provided and which options are available. *Arguments are mandatory and Options are optional*


```` 
Usage: xml-gen.py random [OPTIONS] FEED_TYPE ORGANISATION

Arguments:
  FEED_TYPE     feed type code [EC, APC, OP, SWC, SI, MHCC, MHPS, AMB, IAPT]
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
````

##### command random examples
* basic call with only mandatory fields

        python xml-gen.py random EC ORG01

* a specific amount of activities for example 10.000:

        python xml-gen.py random EC ORG01 --activities 10000

* providing the exact month

        python xml-gen.py random EC ORG01 --month M10

Note: all the options can be provided in combination.


## OPTIONS Explained

### --overr-fields  (override fields file path)

Define field-values-path parameter to inject a json file and provide just the wanted values for a field.

command example

    python xml-gen.py random EC ORG01 --overr-fields resources/samples/field-override.json

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

And call the following command:

    python xml-gen.py random EC ORG01 --overr-config resources/samples/config-file.json

## Command from-csv


Run command example :

    python xml-gen.py from-csv EC ORG01 resources/samples/csv-files/si-example.csv
python activity-xml-generator.py from-csv OP RH5 resources/samples/csv-files/op.csv


All the columns added in this csv will replace the fields in the activity, each row will represent one activity. The non specified fields will be randomly generated.
All costs will automatically be generated unless TotCst column is provided in the csv.


### csv file examples to generate activities for SI

#### si-example.csv
```
OrgId,CSIU,UnCur
OR1,1,PHCD00160
OR2,1,PHCD00190
```

this csv will produce the following xml

```
<?xml version='1.0' encoding='utf-8'?>
<ns:HCDSExtract xmlns:ns="http://Improvement.nhs.uk/HealthcareCostingDataSet/v2.0-1920"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ns:MessageHeader>
        <ns:OrgSubmittingID>ORG01</ns:OrgSubmittingID>
        <ns:FinYr>FY2019-20</ns:FinYr>
        <ns:PeriodStartDate>2019-11-01</ns:PeriodStartDate>
        <ns:PeriodEndDate>2019-11-30</ns:PeriodEndDate>
        <ns:CreateDateTime>2020-03-30T10:11:10</ns:CreateDateTime>
        <ns:FeedType>SI</ns:FeedType>
        <ns:NoOfActivityRecords>2</ns:NoOfActivityRecords>
        <ns:TotalCosts>3535.06</ns:TotalCosts>
    </ns:MessageHeader>
    <ns:MessageBody>
        <ns:Activity>
            <ns:OrgId>OR1</ns:OrgId>
            <ns:PLEMI>CUL8344856214550757056507257336036042415147966-762</ns:PLEMI>
            <ns:UnActDate>2020-01-07</ns:UnActDate>
            <ns:CSIU>1</ns:CSIU>
            <ns:UnCur>PHCD00160</ns:UnCur>
            <ns:CstActivity>
                <ns:ActCstID>PAT006</ns:ActCstID>
                <ns:ActCnt>54</ns:ActCnt>
                <ns:Resource>
                    <ns:ResCstID>CPF001</ns:ResCstID>
                    <ns:TotCst>671.76</ns:TotCst>
                </ns:Resource>
                <ns:Resource>
                    <ns:ResCstID>CPF032</ns:ResCstID>
                    <ns:TotCst>728.32</ns:TotCst>
                </ns:Resource>
                <ns:Resource>
                    <ns:ResCstID>CPF022</ns:ResCstID>
                    <ns:TotCst>183.22</ns:TotCst>
                </ns:Resource>
            </ns:CstActivity>
        </ns:Activity>
        <ns:Activity>
            <ns:OrgId>OR2</ns:OrgId>
            <ns:PLEMI>LDC1444458486529051852579487951896044283204684-403</ns:PLEMI>
            <ns:UnActDate>2019-07-25</ns:UnActDate>
            <ns:CSIU>1</ns:CSIU>
            <ns:UnCur>PHCD00190</ns:UnCur>
            <ns:CstActivity>
                <ns:ActCstID>DIM001</ns:ActCstID>
                <ns:ActCnt>29</ns:ActCnt>
                <ns:Resource>
                    <ns:ResCstID>CPF022</ns:ResCstID>
                    <ns:TotCst>981.7</ns:TotCst>
                </ns:Resource>
            </ns:CstActivity>
            <ns:CstActivity>
                <ns:ActCstID>DIM005</ns:ActCstID>
                <ns:ActCnt>84</ns:ActCnt>
                <ns:Resource>
                    <ns:ResCstID>CPF030</ns:ResCstID>
                    <ns:TotCst>607.59</ns:TotCst>
                </ns:Resource>
                <ns:Resource>
                    <ns:ResCstID>CPF023</ns:ResCstID>
                    <ns:TotCst>362.47</ns:TotCst>
                </ns:Resource>
            </ns:CstActivity>
        </ns:Activity>
    </ns:MessageBody>
</ns:HCDSExtract>
```

To provide a total cost in each activity add a column named **TotCst**

####si-example-with-cost.csv
```
OrgId,CSIU,UnCur,TotCst
OR1,1,PHCD00160,10
OR2,1,PHCD00190,20
```
this csv will produce the following xml
```
<?xml version='1.0' encoding='utf-8'?>
<ns:HCDSExtract xmlns:ns="http://Improvement.nhs.uk/HealthcareCostingDataSet/v2.0-1920"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ns:MessageHeader>
        <ns:OrgSubmittingID>ORG01</ns:OrgSubmittingID>
        <ns:FinYr>FY2019-20</ns:FinYr>
        <ns:PeriodStartDate>2019-06-01</ns:PeriodStartDate>
        <ns:PeriodEndDate>2019-06-30</ns:PeriodEndDate>
        <ns:CreateDateTime>2020-03-30T10:11:10</ns:CreateDateTime>
        <ns:FeedType>SI</ns:FeedType>
        <ns:NoOfActivityRecords>2</ns:NoOfActivityRecords>
        <ns:TotalCosts>30.0</ns:TotalCosts>
    </ns:MessageHeader>
    <ns:MessageBody>
        <ns:Activity>
            <ns:OrgId>OR1</ns:OrgId>
            <ns:PLEMI>QEZ4839113985607946530361079424112363625113417-864</ns:PLEMI>
            <ns:UnActDate>2019-05-21</ns:UnActDate>
            <ns:CSIU>1</ns:CSIU>
            <ns:UnCur>PHCD00160</ns:UnCur>
            <ns:CstActivity>
                <ns:ActCstID>26</ns:ActCstID>
                <ns:ActCnt>73</ns:ActCnt>
                <ns:Resource>
                    <ns:ResCstID>CPF022</ns:ResCstID>
                    <ns:TotCst>10</ns:TotCst>
                </ns:Resource>
            </ns:CstActivity>
        </ns:Activity>
        <ns:Activity>
            <ns:OrgId>OR2</ns:OrgId>
            <ns:PLEMI>NWH7556000130923615767637149644094414803333267-003</ns:PLEMI>
            <ns:UnActDate>2020-03-28</ns:UnActDate>
            <ns:CSIU>1</ns:CSIU>
            <ns:UnCur>PHCD00190</ns:UnCur>
            <ns:CstActivity>
                <ns:ActCstID>81</ns:ActCstID>
                <ns:ActCnt>53</ns:ActCnt>
                <ns:Resource>
                    <ns:ResCstID>CPF005</ns:ResCstID>
                    <ns:TotCst>20</ns:TotCst>
                </ns:Resource>
            </ns:CstActivity>
        </ns:Activity>
    </ns:MessageBody>
</ns:HCDSExtract>
```

### How to add attributes xml tags

In order to add attributes into a field we can provide a value wrapped with double squared brackets ([[attribute]]) and the attribute inside
Ex.: *[[xsi:nil=true]]*

attribute-nil-example.csv
```
OrgId,PLEMI
OR1,[[xsi:nil=true]]
```
This csv will produce the following file
```
<?xml version='1.0' encoding='utf-8'?>
<ns:HCDSExtract xmlns:ns="http://Improvement.nhs.uk/HealthcareCostingDataSet/v2.0-2021"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ns:MessageHeader>
        <ns:OrgSubmittingID>ORG01</ns:OrgSubmittingID>
        <ns:FinYr>FY2020-21</ns:FinYr>
        <ns:PeriodStartDate>2020-05-01</ns:PeriodStartDate>
        <ns:PeriodEndDate>2020-05-31</ns:PeriodEndDate>
        <ns:CreateDateTime>2021-06-10T16:17:00</ns:CreateDateTime>
        <ns:FeedType>SI</ns:FeedType>
        <ns:NoOfActivityRecords>1</ns:NoOfActivityRecords>
        <ns:TotalCosts>884.79</ns:TotalCosts>
    </ns:MessageHeader>
    <ns:MessageBody>
        <ns:Activity>
            <ns:OrgId>OR1</ns:OrgId>
            <ns:PLEMI xsi:nil="true"/>
            <ns:UnActDate>2020-11-08</ns:UnActDate>
            <ns:CSIU>3</ns:CSIU>
            <ns:UnCur>PHCD00389</ns:UnCur>
            <ns:CstActivity>
                <ns:ActCstID>ODT005</ns:ActCstID>
                <ns:ActCnt>6240</ns:ActCnt>
                <ns:Resource>
                    <ns:ResCstID>CPF023</ns:ResCstID>
                    <ns:TotCst>884.79</ns:TotCst>
                </ns:Resource>
            </ns:CstActivity>
        </ns:Activity>
    </ns:MessageBody>
</ns:HCDSExtract>

```

## Other development tools

#### Unique identifiers
Unique identifiers helps to create id's

    from src.helpers.UniqueIdentifier import UniqueIdentifier
    
    costActivityId = UniqueIdentifier('CAC')
    
    costActivityId.next()
    
    # The result from this method will be CAC001, CAC002 ...
    
    
## Generating REC files
python rec-xml-generator.py --feed_type=CSREC --orgid=RH5 --financial_year=FY_2020-21 --month=M01
