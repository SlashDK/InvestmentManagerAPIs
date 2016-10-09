import sys
import csv
import requests
import json

from flask import Flask
app = Flask(__name__)

myPortfolio=[]

def gains(currDate):
	print(myPortfolio)
	origInvest=0
	portfolioGains=0
	for i in myPortfolio:
		print(i[1])
		origInvest+=int(i[1])
		callFromStart = """https://www.blackrock.com/tools/hackathon/performance?\
endDate=%s&identifiers=%s&outputDataExpression=resultMap%%5B\
'RETURNS'%%5D%%5B0%%5D.latestPerf%%5B'sinceStartDate'%%5D&startDate=%s&useCache=true"""%(currDate,i[0],i[2])
		r=requests.get(callFromStart)
		r=str(r.content)
		print(r)
		r=r[2:r.find('.')+4]
		r=float(r)*int(i[1])
		portfolioGains+=r
		print(portfolioGains)
	return (portfolioGains)*100/origInvest 

def portfolioCompanies():
	companies = ""
	print( myPortfolio)
	for i in myPortfolio:
		# print(i)
		companies=companies+" "+(i[3])
	return companies

def portfolioAdder(ticker,amount,date,path):
	myPortfolio.append((ticker,amount,date,path))

def nameToTicker(companyName):
    with open('companylist.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            row[1]=row[1].lower()
            if(companyName in row[1]):
                return row[0]
    return "invalid"

# print(nameToTicker("microsoft"))
@app.route("/")
@app.route('/<path:path>')
def APICalls(path="apple"):
    # return 'You want path: %s' % path
# def APICalls(companyName="apple"):
	startDate="20151007"
	add=""
	amount=1
	if ('/' in path):
		path,startDate,add,amount=path.split('/')
		print(path,add,startDate,amount)
	ticker = nameToTicker(path)
	if(ticker=="invalid"):
		ticker="BLUE"
	endDate = "20151008"
	if(add=="portfolio"):
		portfolioAdder(ticker,amount,startDate,path)
	if(add=="tell"):
		obj = {u"netGains": gains(endDate)}
		return json.dumps(obj)
	if(add=="tellcompanies"):
		print(str(portfolioCompanies))
		obj = {u"companies": portfolioCompanies()}
		return json.dumps(obj)
	callOneDay="""https://www.blackrock.com/tools/hackathon/performance?\
endDate=%s&identifiers=%s&outputDataExpression=resultMap%%5B\
'RETURNS'%%5D%%5B0%%5D.latestPerf%%5B'oneDay'%%5D&startDate=%s&useCache=true"""%(endDate,ticker,startDate)
	print(callOneDay)
	callFromStart = """https://www.blackrock.com/tools/hackathon/performance?\
endDate=%s&identifiers=%s&outputDataExpression=resultMap%%5B\
'RETURNS'%%5D%%5B0%%5D.latestPerf%%5B'sinceStartDate'%%5D&startDate=%s&useCache=true"""%(endDate,ticker,startDate) 
	callGraphData="""https://www.blackrock.com/tools/hackathon/performance?\
endDate=%s&identifiers=%s&outputDataExpression=resultMap%%5B\
'RETURNS'%%5D%%5B0%%5D.latestPerf%%5B'sinceStartDate'%%5D&startDate=%s&useCache=true"""%(endDate,ticker,startDate) 
	# print(callGraphData)
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
    app.run()
