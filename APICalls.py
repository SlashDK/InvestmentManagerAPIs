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
@app.route('/<path:path>')
def APICalls(path="apple"):
    # return 'You want path: %s' % path
# def APICalls(companyName="apple"):
	ticker = nameToTicker(path)
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
	print(type(r1.content),r1.content)
	r1=str(r1.content)
	r1=r1[2:r1.find('.')+4]
	r2=str(r2.content)
	r2=r2[2:r2.find('.')+4]
	# r = requests.post("http://yoururl/post", data={'foo': 'bar'})
	obj = {u"oneDayChange": r1, u"sinceStartDateChange": r2}
	return json.dumps(obj)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000)
