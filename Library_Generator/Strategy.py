
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import sys
import ast

from StrategyPool import *
import Utility
from Utility import configure
from CppTranslator import CppTranslator
from CTranslator import CTranslator
from IDISAFunctionSupport import IDISAFunction

def LoadStrategies(arch):
	strategies = {}
	allStrategies = StrategyPool(configure.RegisterSize[arch])
	for strgyId in allStrategies:
		strategies[strgyId] = Strategy(allStrategies[strgyId], arch, strgyId)
	return strategies

class Strategy:
	'''This is the class for defining a strategy.
	'''
	def __init__(self, strategy, arch, strgyId):
		#The id of this strategy
		self.strgyId = strgyId
		
		#The initial content of the strategy
		self.body = strategy["body"]
		
		#It is supposed to be a list of eligible operations which can use this strategy
		self.applicableOps = strategy["Ops"]
		
		#The information of supported platforms
		self.platforms = strategy["Platforms"]
		
		#ApplicableFws must be a range containing all the valid field widths
		if len(strategy["Fws"]) == 1:
			self.applicableFws = range(1, configure.RegisterSize[arch]+1) if strategy["Fws"][0] < 0 else range(strategy["Fws"][0], strategy["Fws"][0]+1)
		elif len(strategy["Fws"]) >= 2:
			self.applicableFws = strategy["Fws"]
		else:
			print "This strategy " + self.body + " is not well written!"
	
	def Parse(self, operation, lang):
		'''It parses the current strategy and returns the resulting source codes and function calls for the given operation and language setting.
		'''
		parsedResult = {"body":"", "calls":[]}
		translator = None
		#print "now is ", self.strgyId
		if lang == configure.Language_CPP:
			translator = CppTranslator(self.body, operation)
		elif lang == configure.Language_C:
			translator = CTranslator(self.body, operation)
		else:
			print "Failed! No such translator supported!"
			sys.exit()

		parsedResult["body"] = translator.codes
		parsedResult["calls"] = translator.calls
		parsedResult["isCompileTimeConstant"] = translator.isCompileTimeConstant

		return parsedResult

	def DoesStrategySupport(self, operation):
		#print operation.fullName, operation.fieldWidth, " <=> ", self.applicableOps, self.applicableFws
		return operation.fullName in self.applicableOps \
			and operation.fieldWidth in self.applicableFws

	def DoesInstructionSetSupport(self, arch, strategyBody, strategyPlatform):
		if configure.ALL in strategyPlatform or arch in strategyPlatform:
			pass
		else:
			return False
		
		nonSIMDCalls = NonSIMDCallsInStrategy(strategyBody).calls
		for call in nonSIMDCalls:
			if Utility.builtIns.IsOperationBuiltIn(call) or call in Utility.functionSupport or IDISAFunction.IsIDISAFunction(call):
				continue
			else:
				return False
		return True

class NonSIMDCallsInStrategy:
		def __init__(self, strategyBody):
			#print strategyBody
			#print "has", 
			self.calls = []
			self.Traverse(ast.parse(strategyBody))

		def Traverse(self, tree):
			if isinstance(tree, list):
				[Travese(ele) for ele in tree]
			else:
				callMethod = getattr(self, 'Is'+tree.__class__.__name__)
				if callMethod:
					#print callMethod
					return callMethod(tree)
		
		def IsModule(self, tree):
			[self.Traverse(statement) for statement in tree.body]
		
		def IsAssign(self, tree):
			for target in tree.targets:
				self.Traverse(target)
				self.Traverse(tree.value)
		
		def IsReturn(self, tree):
			if tree.value:
				self.Traverse(tree.value)
		
		def IsIfExp(self, tree):
			self.Traverse(tree.test)
			self.Traverse(tree.body)
			self.Traverse(tree.orelse)
		
		def IsCompare(self, tree):
			self.Traverse(tree.left)
			self.Traverse(tree.comparators[0])
		
		def IsName(self, tree):
			return tree.id
		
		def IsNum(self, tree):
			return repr(tree.n)
		
		def IsBinOp(self, tree):
			self.Traverse(tree.left)
			self.Traverse(tree.right)
		
		def IsStr(self, tree):
			return tree.s
		
		def IsCall(self, tree):
			funcName = self.Traverse(tree.func)
			if "simd_" not in funcName and "hsimd_" not in funcName and "esimd_" not in funcName and "mvmd_" not in funcName and "bitblock_" not in funcName:
				self.calls.append(funcName)
			sz = len(tree.args)
			for i in range(sz):
				self.Traverse(tree.args[i])
			