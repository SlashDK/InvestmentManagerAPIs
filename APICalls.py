import sys
import csv
import requests
import json

# name = list()
# for i in range (sys.argv[0]):
# name[i] = sys.argv[i]

def nameToTicker(companyName):
    with open('yahoo.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            row[1:] = map(lambda x: x.lower(),row[1:])
            if(companyName in row):
                print(row)
                return row[0][:-1]

# print(nameToTicker("microsoft"))

def APICalls(companyName):
	ticker = nameToTicker(companyName)
	endDate = "20150930"
	startDate = "20150815"
	callOneDay="""https://www.blackrock.com/tools/hackathon/performance?\
endDate=%s&identifiers=%s&outputDataExpression=resultMap%%5B\
'RETURNS'%%5D%%5B0%%5D.latestPerf%%5B'oneDay'%%5D&startDate=%s&useCache=true"""%(endDate,ticker,startDate)
	callFromStart = """https://www.blackrock.com/tools/hackathon/performance?\
endDate=%s&identifiers=%s&outputDataExpression=resultMap%%5B\
'RETURNS'%%5D%%5B0%%5D.latestPerf%%5B'sinceStartDate'%%5D&startDate=%s&useCache=true"""%(endDate,ticker,startDate) 
	r1=requests.get(callOneDay)
	r2=requests.get(callFromStart)
	# x=json.loads(r)
	return (r1.content,r2.content)

print(APICalls('apple'))