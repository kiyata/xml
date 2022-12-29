import csv

openFile = open('apc_costs.csv', 'r')
csvFile = csv.reader(openFile)
header = next(csvFile)
headers = map((lambda x: '['+x+']'), header)
#insert = 'INSERT INTO [PLIC_INTEGRATED].[ic].[PLIC_HES_APC_Act_SQL] (' + ", ".join(headers) + ") VALUES "
insert = "INSERT INTO [PLIC_INTEGRATED].[ic].[PLIC_HES_APC_Cost_SQL] VALUES "
for row in csvFile:
    values = map((lambda x: "'"+x+"'"), row)
    print (insert +"("+ ", ".join(values) +");" )
openFile.close()
