import sys
import csv

# name = list()
# for i in range (sys.argv[0]):
# 	name[i] = sys.argv[i]

def nameToTicker(companyName):
    with open('yahoo.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            row[1:] = map(lambda x: x.lower(),row[1:])
            if(companyName in row):
                print(row)
                return row[0][:-1]

print(nameToTicker("microsoft"))