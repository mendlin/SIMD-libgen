
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import CalculatingModules

def GetResult(operation, testingData, regSize):
	calcModule = getattr(CalculatingModules, operation.fullName)
	oprdNum = len(operation.arguments)
	results = []
	
	for data in testingData:
		ret = ""
		if operation.opPattern == 2:
			#logic operations
			ret = calcModule.GetResult(1, data)
		elif operation.opPattern == 0:
			#normal operations
			if oprdNum == 0:
				ret = calcModule.GetResult(operation.fieldWidth, regSize)
			elif "fill" in operation.fullName:
				ret = calcModule.GetResult(operation.fieldWidth, data, regSize)
			else:
				ret = calcModule.GetResult(operation.fieldWidth, data)
		elif operation.opPattern == 1:
			#operations with other types
			if oprdNum == 0:
				ret = calcModule.GetResult(operation.fieldWidth, data[-1], regSize)
			else:
				ret = calcModule.GetResult(operation.fieldWidth, data[-1], data)
		elif operation.opPattern == 3:
			#bitblock operations
			ret = calcModule.GetResult(data)
		elif operation.opPattern == 4:
			#bitblock srli/slli operations
			ret = calcModule.GetResult(data[-1], data)
			#pass
		else:
			print "unknown operation!"

		results.append(ret)
	
	return results
