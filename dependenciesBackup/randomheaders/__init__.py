import random
import csv
import os

file_name = os.path.dirname(os.path.realpath(__file__)) + '/UserAgent.csv'
UserAgentCSV = open(file_name, 'r')
UserAgentList = csv.reader(UserAgentCSV)
UserAgentList = [row for row in UserAgentList]
UserAgentList = [l[0] for l in UserAgentList]
random.shuffle(UserAgentList)

def LoadHeader():
	return {'User-Agent': random.choice(UserAgentList)}
