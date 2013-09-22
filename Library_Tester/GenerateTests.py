
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import os
import ipdb

import GenData
import TesterUtility
from TesterUtility import configure

# Number of test cases. For development, use small number to test faster.
maxTestCase = 50

def MakeTestdata(arch, definedOperations, validOperations):
	testingData = {}
	regSize = configure.RegisterSize[arch]
	
	print "generating test data..."		
	
	for opFullName in validOperations:
		operation = definedOperations[opFullName][1]
		oprdNum = len(operation.arguments)
		
		if operation.opPattern == 2:
			#logic operations
			testingData[opFullName + "_" + str(1)] = GenData.MakeRandomData(operation, regSize, maxTestCase)
		elif operation.opPattern == 3:
			#bitblock operations
			testingData[opFullName + "_" + str(regSize)] = GenData.MakeRandomData(operation, regSize, maxTestCase)
		elif operation.opPattern == 4:
			testingData[opFullName + "_" + str(regSize)] = GenData.MakeRandomData(operation, regSize, maxTestCase)
			templatedData = []
			for key in operation.valueRange:
				lowBound = operation.valueRange[key]["min"]
				upBound = operation.valueRange[key]["max"]
				templatedData = TesterUtility.GetRandomNums(lowBound, upBound, maxTestCase)
				break
			for i in range(len(templatedData)):
				testingData[opFullName + "_" + str(regSize)][i].append(templatedData[i])
		else:			
			#operations with other types
			for validOp in validOperations[opFullName]:
				operation = definedOperations[opFullName][validOp.fw]				

				if operation.opPattern == 0:
					#normal operations
					testingData[opFullName + "_" + str(validOp.fw)] = GenData.MakeRandomData(operation, regSize, maxTestCase)
				elif operation.opPattern == 1:
					#operations with a templated argument
					testingData[opFullName + "_" + str(validOp.fw)] = GenData.MakeRandomData(operation, regSize, maxTestCase)
					
					templatedData = []
					for key in operation.valueRange:
						if "arg" in key:
							# we want templated values only. Args can also appear in the valueRange
							continue
						lowBound = operation.valueRange[key]["min"]
						upBound = operation.valueRange[key]["max"]
						templatedData = TesterUtility.GetRandomNums(lowBound, upBound, maxTestCase)						
					
					for i in range(len(templatedData)):
						testingData[opFullName + "_" + str(validOp.fw)][i].append(templatedData[i])
	
	print "finished generating test data."
	return testingData
