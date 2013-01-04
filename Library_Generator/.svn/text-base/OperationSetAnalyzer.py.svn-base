
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import sys

import Utility
from BuiltIns import BuiltIns
from Operation import *

def Analyze(operationSet):
	return OperationSetAnalyzer(operationSet)

def AnalyzeSecBest(operationSet, class_op_fw):
	result = OperationSetAnalyzer(operationSet, class_op_fw, "")
	result.disabledOp = ""
	result.updateOpOnly = class_op_fw
	result.IterationAlgorithm(operationSet)
	return result
	
class OperationSetAnalyzer:

	def __init__(self, operationSet, disabledOp="", updateOpOnly=""):
		self.opMaxCount = 1000000.0
		self.optOpCodes = {}
		self.optOpCount = {}
		self.secOptOpCount = {}
		self.secOptOpCodes = {}
		self.tmpSecOptOpCount = {}
		self.realCompileTimeConstant = {}
		self.DoubleCheckCompileTimeConstant(operationSet)
		self.disabledOp = disabledOp
		self.updateOpOnly = updateOpOnly
		self.numOfBranches = 0
		for opId in operationSet:
			self.optOpCodes[opId] = ""
			self.optOpCount[opId] = self.opMaxCount
			self.secOptOpCodes[opId] = ""
			self.secOptOpCount[opId] = self.opMaxCount
			self.tmpSecOptOpCount[opId] = self.opMaxCount
		self.IterationAlgorithm(operationSet)
	
	def DoubleCheckCompileTimeConstant(self, operationSet):
		for class_op_fw in operationSet:
			for opUnit in operationSet[class_op_fw]:
				isCompileTimeConstant = opUnit["isCompileTimeConstant"]
				if isCompileTimeConstant == True:
					self.realCompileTimeConstant[class_op_fw] = False
		
		for class_op_fw in self.realCompileTimeConstant:
			secUnderLine = class_op_fw.find("_", class_op_fw.find("_")+1)
			class_op = class_op_fw[:secUnderLine]
			fw = int(class_op_fw[secUnderLine+1:])
			if Utility.builtIns.IsOperationBuiltIn(Utility.definedOperations[class_op][fw]):
				self.realCompileTimeConstant[class_op_fw] = True
	
	def CheckFunc(self, func):		
		if  Utility.builtIns.IsOperationBuiltIn(func):
			if isinstance(func, Operation):
				return func.estCost if func.estCost > 0.0 else 1.0
			else:
			#The cost for each built-in is set to 1 at this moment
				return 1.0
		elif Utility.functionSupport.has_key(func):
			#each function in function support has cost defined at functionSupport table
			return Utility.functionSupport[func]["cost"]
		elif (func not in self.optOpCount) or (self.optOpCount[func] >= self.opMaxCount):
			return self.opMaxCount
		else:
			return self.optOpCount[func]
	
	def CheckIfElseBranch(self, branch):
		'''
		Find the maximum cost between if branch and else branch
		'''
		ifBranch = branch[0]
		ifCost = 0
		if len(ifBranch)<=0:
			pass
		elif type(ifBranch[0]) != list:
			for func in ifBranch:
				ifCost += self.CheckFunc(func)
		else:
			ifCost += self.CheckIfElseBranch(ifBranch)

		elseBranch = branch[1]
		elseCost = 0
		if len(elseBranch) <= 0:
			pass
		elif type(elseBranch[0]) != list:
			for func in elseBranch:
				elseCost += self.CheckFunc(func)
		else:
			elseCost += self.CheckIfElseBranch(elseBranch[0])
		
		return ifCost if ifCost > elseCost else elseCost
		
	def CheckIfElseBranchAvg(self, branch):
		'''
		Find the average cost between if branch and else branch
		'''
		ifBranch = branch[0]
		ifCost = 0
		if len(ifBranch)<=0:
			pass
		elif type(ifBranch[0]) != list:
			for func in ifBranch:
				ifCost += self.CheckFunc(func)
			self.numOfBranches += 1
		else:
			ifCost += self.CheckIfElseBranchAvg(ifBranch)

		elseBranch = branch[1]
		elseCost = 0
		if len(elseBranch) <= 0:
			pass
		elif type(elseBranch[0]) != list:
			for func in elseBranch:
				elseCost += self.CheckFunc(func)
			self.numOfBranches += 1
		else:
			elseCost += self.CheckIfElseBranchAvg(elseBranch[0])
		
		return ifCost + elseCost
	
	def IsFuncIn(self, func, calls):
		if func in calls:
			return True
		for item in calls:
			if isinstance(item, list):
				return self.IsFuncIn(func, item)
		return False
				
	def OneIteration(self, operationSet):
		changed = False
		for class_op_fw in operationSet:
			for opUnit in operationSet[class_op_fw]:
				codes = opUnit["body"]
				calls = opUnit["calls"]
				isCompileTimeConstant = opUnit["isCompileTimeConstant"]
				
				opTotalNum = 0.0
				
				#calls is empty, cost should be 0
				if calls == None or len(calls) <= 0:
					opTotalNum = 0.0
				#if it is compile time constant and there is an implementation for it as well, set its cost to 0
				elif class_op_fw in self.realCompileTimeConstant and self.realCompileTimeConstant[class_op_fw]:
					opTotalNum = 0.0
				else:
					for func in calls:
						if type(func) != list:
							opTotalNum += self.CheckFunc(func)
						else:
							#we meet a if-else branch
							self.numOfBranches = 0
							
							# use the max cost of branches
							#opTotalNum += self.CheckIfElseBranch(func)
							
							# use the average cost of branches
							tmp = self.CheckIfElseBranchAvg(func)
							opTotalNum += (tmp * 1.0 / self.numOfBranches) if self.numOfBranches > 0 else 0
	
				if isCompileTimeConstant:
					opTotalNum = 0 if opTotalNum < self.opMaxCount else self.opMaxCount
				
				if self.disabledOp != "" and self.IsFuncIn(self.disabledOp, calls):
					continue
				
				if self.updateOpOnly != "" and class_op_fw != self.updateOpOnly:
					continue
				
				if opTotalNum < self.optOpCount[class_op_fw]:
					self.secOptOpCount[class_op_fw] = self.optOpCount[class_op_fw]
					self.secOptOpCodes[class_op_fw] = self.optOpCodes[class_op_fw]
					self.optOpCount[class_op_fw] = opTotalNum
					self.optOpCodes[class_op_fw] = codes
					changed = True
				elif opTotalNum == self.optOpCount[class_op_fw] and opTotalNum < self.tmpSecOptOpCount[class_op_fw]:
					self.tmpSecOptOpCount[class_op_fw] = opTotalNum
				elif opTotalNum < self.secOptOpCount[class_op_fw] and opTotalNum != self.optOpCount[class_op_fw]:
					self.secOptOpCount[class_op_fw] = opTotalNum
					self.secOptOpCodes[class_op_fw] = codes
		return changed

	def IterationAlgorithm(self, operationSet):
		changed = self.OneIteration(operationSet)
		while changed:
			changed = self.OneIteration(operationSet)

