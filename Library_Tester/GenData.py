
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import random

from TesterUtility import configure

def Flip(bits, fw, num):
	flipPos = []
	for i in range(fw):
		flipPos.append(0)
	for i in range(num):
		pos = random.randint(1, fw-1)
		flipPos[pos] = 1 - flipPos[pos]
		
	retBits = ""
	for i in range(fw):
		if flipPos[i] == 1:
			if bits[i] == "0":
				retBits += "1"
			else:
				retBits += "0"
		else:
			retBits += bits[i]
	return retBits

def GenNormalSIMDTestingData(fw, regSize, oprdNum, casNum):
	testdata = []
	times = int(regSize/fw)
	basics = ["0"*fw, "1"*fw]
	
	for i in range(casNum-3):
		data = []
		for j in range(oprdNum):
			bits = ""
			for k in range(times):
				bits += Flip(basics[random.randint(0, 1)], fw, random.randint(0, fw-1))
			data.append(bits)
		testdata.append(data)
		
	#only 0 and -1
	data = []
	for i in range(oprdNum):
		bits = ""
		for k in range(times):
			bits += basics[i%2]
		data.append(bits)
	testdata.append(data)
		
	#only 0
	data = []
	for i in range(oprdNum):
		bits = ""
		for k in range(times):
			bits += basics[0]
		data.append(bits)
	testdata.append(data)
		
	#only -1
	data = []
	for i in range(oprdNum):
		bits = ""
		for k in range(times):
			bits += basics[1]
		data.append(bits)
	testdata.append(data)
	
	return testdata

def MakeRandomData(operation, regSize, casNum):
	oprdNum = len(operation.arguments)
	simdData = GenNormalSIMDTestingData(operation.fieldWidth, regSize, oprdNum, casNum)

	testdata = []
	for i in range(casNum):
		data = []
		j = 0
		for arg in operation.arguments:
			if arg.type == configure.Bitblock_type[operation.arch]:
				data.append(simdData[i][j])
				j += 1
			elif arg.type == "uint64_t":
				lowBound = operation.valueRange[arg.name]["min"]
				upBound = operation.valueRange[arg.name]["max"]
				data.append(random.randint(lowBound, upBound))
			else:
				print "unable to process this data type", arg.type
		testdata.append(data)
	
	return testdata
		
