
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import copy

import BuiltIns
import Utility
from Utility import configure

staticOperationSet = None

def LoadOperationSet(arch, lang):
	global staticOperationSet
	if staticOperationSet == None:
		staticOperationSet = OperationSet(arch, lang)
	return staticOperationSet.operationSet

def LoadStrategyCount(arch, lang):
	global staticOperationSet
	if staticOperationSet == None:
		staticOperationSet = OperationSet(arch, lang)
	return staticOperationSet.strategyCount

class OperationSet:
	
	def __init__(self, arch, lang):
		#operationSet is a dictionary of all operations and their all possible implementations
		#The format of keys is class_op_fw, the format of values is a list of implementations
		self.strategyCount = {}
		self.operationSet = {}
		self.operationSet = self.AssembleOperationSet(arch, lang)
		
	
	def AssembleOperationSet(self, arch, lang):
		operationSet = {}
		strategies = Utility.strategies
		validFws = Utility.GetValidFieldWidth(configure.RegisterSize[arch])
		
		#initialize the strategy count
		for op in Utility.definedOperations:
			operation = Utility.definedOperations[op][1]
			self.strategyCount[operation.fullName] = {}
			for fw in validFws:
				self.strategyCount[operation.fullName][fw] = 0
		
		for op in Utility.definedOperations:
			for fw in validFws:
				operation = Utility.definedOperations[op][fw]
				#operation.fieldWidth = fw
				operationSet[operation.fullName + "_" + str(operation.fieldWidth)]  = []
				if Utility.builtIns.IsOperationBuiltIn(operation):
					content = {}
					if lang == configure.Language_CPP:
						content["body"] = Utility.builtIns.PackAnOperationInCpp(operation)
					elif lang == configure.Language_C:
						content["body"] = Utility.builtIns.PackAnOperationInC(operation)
					content["calls"] = [operation]
					content["isCompileTimeConstant"] = Utility.builtIns.IsCompileTimeConstant(operation)
					#print operation.fullName + "_" + str(operation.fieldWidth), " calls have ", operation.fullName, operation.fieldWidth
					operationSet[operation.fullName + "_" + str(operation.fieldWidth)].append(content)
					self.strategyCount[operation.fullName][fw] += 1
				if True:
				#Only assemble the built-in operations at this moment
					#continue
					for strgyId in strategies:
						strgy = strategies[strgyId]
						if strgy.DoesStrategySupport(operation) and strgy.DoesInstructionSetSupport(arch, strgy.body, strgy.platforms):
							#print strgy.body, operation.fullName
							#If strgy supports this operation, then we translate	the strgy with operation
							content = strgy.Parse(operation, lang)
							#Add the content returned by Translate routine into operationSet
							#The format of keys is class_name_fw
							#Content is a dictionary of two keys, the first is the code body(key = "body")
							#While the second is all the calling routines used by this strategy(key = "calls")
							operationSet[operation.fullName + "_" + str(operation.fieldWidth)].append(content)
							self.strategyCount[operation.fullName][fw] += 1
		return operationSet
