import sys
import csv
import requests
import json

from flask import Flask
app = Flask(__name__)

def nameToTicker(companyName):
    with open('yahoo.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            row[1:] = map(lambda x: x.lower(),row[1:])
            if(companyName in row):
                return row[0][:-1]

# print(nameToTicker("microsoft"))
@app.route("/")
def APICalls(companyName="apple"):
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
	# r = requests.post("http://yoururl/post", data={'foo': 'bar'})
	return str((r1.content,r2.content))

print(APICalls('apple'))


if __name__ == "__main__":
    app.run()