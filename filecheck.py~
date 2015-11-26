import os
from decimal import Decimal

def checkIfInHome(fileName):
	k = os.getcwd() #saves the current working directory
	os.system('cd /home')
	os.system('find /home -type f -name '+fileName+' 2>/dev/null |cat>temp')
	f = open('temp','r')
	fileSet = set()
	for line in f:
		if 'Permission denied' not in line:
			fileSet.add(line.rstrip('\n'))
	fileSet = list(fileSet)
	return fileSet

def checkIfInHomeDir(dirName):
	k = os.getcwd() #saves the current working directory
	os.system('cd /home')
	os.system('find /home -type d -name '+dirName+' 2>/dev/null |cat>temp')
	f = open('temp','r')
	dirSet = set()
	for line in f:
		if 'Permission denied' not in line:
			dirSet.add(line.rstrip('\n'))
	dirSet = list(dirSet)
	return dirSet

def isFileName(userName,fileName):
	os.system('find /home/'+userName+' -type f -name '+fileName+' 2>/dev/null |cat>temp')
	os.system('wc -l<temp >count')
	countL=''
	f = open('count','r')
	for line in f:
		countL = line.strip('\n')
	countL = Decimal(countL)
	os.system('rm temp')
	os.system('rm count')
	if countL>=1:
		return True
	else:
		return False

def isDirName(userName,fileName):
	os.system('find /home/'+userName+' -type d -name '+fileName+' 2>/dev/null |cat>temp')
	os.system('wc -l<temp >count')
	countL=''
	f = open('count','r')
	for line in f:
		countL = line.strip('\n')
	countL = Decimal(countL)
	os.system('rm temp')
	os.system('rm count')
	if countL>=1:
		return True
	else:
		return False
