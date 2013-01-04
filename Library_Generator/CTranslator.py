
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

#
# This C translator is not completed yet.
# Please refer to the C++ translator if you want to complete this C translator.
#

import ast
import re
from types import *

import Utility
from Operation import Operation

class CTranslator:
	'''Methods of CTranslator recursively traverse an AST and output source codes in C syntax.
There are two options to emit C codes, in marcos or in static inline functions
	'''
	def __init__(self, strategyBody, operation):
		self.operation = operation
		self.curFunc = []
		self.variablesTable = {}
		#codes store the C implementation of the current operation
		self.codes = ""
		#calls store all the operations which are called by the current operation in the format of class_func_fw
		self.calls = []
		#prevCall used to construct the tree structure of calling procedure
		self.prevCall = self.calls
		self.isCompileTimeConstant = True
		
		#print "cur strategy is ", strategyBody
		
		abstractSyntaxTree = ast.parse(strategyBody)
		body = self.Traverse(abstractSyntaxTree)["codes"]
		if body:
			#self.codes = "{\n" + body + "}\n"
			self.codes = body
		else:
			#The strategy can not be parsed correctly given this operation
			self.codes = ""
			self.calls = []
			print "The strategy " + strategyBody + " can not be parsed correctly given operation = " + operation.classType + "::" +  operation.name
		
	def IdentifyOperation(self, funcName):
		#print funName
		classType = ""
		opName = ""
		if "hsimd_" in funcName:
			classType = "hsimd"
			opName = funcName.replace('hsimd_', '')
		elif "esimd_" in funcName:
			classType = "esimd"
			opName = funcName.replace('esimd_', '')
		elif "mvmd_" in funcName:
			classType = "mvmd"
			opName = funcName.replace('mvmd_', '')
		elif "simd_" in funcName:
			classType = "simd"
			opName = funcName.replace('simd_', '')
		elif "bitblock_" in funcName:
			classType = "bitblock"
			opName = funcName.replace("bitblock_", "")
		#print opName, " maps to ", 
		if opName == 'op':
			#This is a general operation which should be replaced by one of the strategy's applicable operations
			#print self.operation.classType + "_" + self.operation.name
			return Utility.definedOperations[self.operation.classType + "_" + self.operation.name][self.operation.fieldWidth]
		elif opName == 'uop':
			#This is an unsigned version of the general operation
			#print self.operation.classType + "_" + "u" + self.operation.name
			return Utility.definedOperations[self.operation.classType + "_" + "u" + self.operation.name][self.operation.fieldWidth]
		elif opName == 'signed_op':
			#This is an signed version of an unsigned operation
			#The function name must begin with "u"
                        assert self.operation.name[0] == 'u', "signed_op can only be used for signed version of uop"
			#print self.operation.classType + "_" + "u" + self.operation.name
			return Utility.definedOperations[self.operation.classType + "_" + self.operation.name[1:]][self.operation.fieldWidth]
		else:
			#This is a specific operation, field width is set to 1
			#print classType + "_" + opName
			return Utility.definedOperations[classType + "_" + opName][1]

	def Traverse(self, tree):
		'''
		This method recursively traverses the ast and return well-formatted C++ codes
		It returns a tuple of source codes and associated return type
		'''
		#print "now at ", ast.dump(tree)
		codes = ""
		returnType = None
		if isinstance(tree, list):
			for ch in tree:
				listRet = self.Traverse(ch)
				codes += listRet["codes"]
				returnType = ListType
		else:
			#print "now at", ast.dump(tree)
			callMethod = getattr(self, 'Is'+tree.__class__.__name__)
			if callMethod:
				callRet = callMethod(tree)
				#print callRet["codes"], callRet["returnType"]
				if callRet["codes"]:
					codes += callRet["codes"]
					returnType = callRet["returnType"]
				else:
					print "This strategy can not be parsed and will be ignored!"
					return {"codes":None, "returnType":None}
			else:
				print "error!(there is no such *" + callMethod + "* function)"
				return {"codes":None, "returnType":None}

		#print "current codes are => " + codes
		
		return {"codes":codes, "returnType":returnType}
		
	def IsModule(self, tree):
		'''
		Process the tree node with 'Module' type
		A module doesn't return any return type information
		'''
		codes = ""
		for statement in tree.body:
			codes += "\t" + self.Traverse(statement)["codes"] + ";\n"
		return {"codes":codes, "returnType":ModuleType}
	
	def GetReturnType(self, returnType):
		#print "cur return type = ", returnType
		if returnType == IntType:
			return "int"
		elif returnType == LongType:
			return "long long"
		elif returnType == "SIMD_type":
			return "SIMD_type"
		else:
			return returnType
	
	def IsAssign(self, tree):
		'''
		process the tree node with 'Assign' type
		'''
		codes = ""
		returnType = None
		for target in tree.targets:
			variableName = self.Traverse(target)["codes"]
			#(variableValue, returnType) = self.Traverse(tree.value)
			valRet = self.Traverse(tree.value)
			variableValue = valRet["codes"]
			returnType = valRet["returnType"]
			if returnType and (variableName not in self.variablesTable):
				codes += self.GetReturnType(returnType) + " "
				self.variablesTable[variableName] = returnType
			codes += variableName
			codes += " = "
			codes += variableValue
		return {"codes":codes, "returnType":returnType}

	def IsReturn(self, tree):
		'''
		process the tree node with 'Return' type
		'''
		codes = "return"
		returnType = None
		if tree.value:
			#(tmpCodes, returnType) = self.Traverse(tree.value)
			valRet = self.Traverse(tree.value)
			codes += " " + valRet["codes"]
			returnType = valRet["returnType"]
		return {"codes":codes, "returnType":returnType}
	
	def IsIfExp(self, tree):
		'''
		Process the tree node with conditional operator 'IfExp'
		Must consider the branches due to the 'IfExp'
		It ignores the cost of test branch while keeping body branch and oresle branch
		'''
		
		testRet = self.Traverse(tree.test)
		
		#back up prevCall
		backupCall = self.prevCall
		self.prevCall.append([[], []])
		
		bodyCall = self.prevCall[-1][0]
		orelseCall = self.prevCall[-1][1]
		
		self.prevCall = bodyCall
		bodyRet = self.Traverse(tree.body)
		self.prevCall = orelseCall
		orBodyRet = self.Traverse(tree.orelse)
		
		#restore the prevCall
		self.prevCall = backupCall
		
		#codes = "(" + "(" + testCodes + ")" + " ? " + bodyCodes + " : " + orBodyCodes + ")"
		
		codes = "(" + "(" + testRet["codes"] + ")" + " ? " + bodyRet["codes"] + " : " + orBodyRet["codes"] + ")"
		returnType = bodyRet["returnType"]
		
		return {"codes":codes, "returnType":returnType}
	
	def IsCompare(self, tree):
		'''
		Process the tree node with 'compare' type
		'''
		leftCodes = self.Traverse(tree.left)["codes"]
		opCodes = 	self.binop[tree.ops[0].__class__.__name__]
		rightCodes = self.Traverse(tree.comparators[0])["codes"]
		
		codes = leftCodes + " " + opCodes + " " + rightCodes
		return {"codes":codes, "returnType":BooleanType}
		
	def IsName(self, tree):
		'''
		Process the tree node with 'Name' type
		'''
		codes = ""
		returnType = None
		if "simd_" in tree.id or "hsimd_" in tree.id or "esimd_" in tree.id or "mvmd_" in tree.id or "bitblock_" in tree.id:
			self.curFunc.append(self.IdentifyOperation(tree.id))
			codes = tree.id
			#codes now actually is an operation object
			returnType = self.curFunc[-1].returnType
		elif "fw" == tree.id:
			codes = repr(self.operation.fieldWidth)
			returnType = IntType
		elif "curRegSize" == tree.id:
			codes = repr(Utility.curRegisterSize)
			returnType = IntType
		else:
			codes = tree.id
			returnType = type(tree.id)
			
		return {"codes":codes, "returnType":returnType}

	def IsNum(self, tree):
		'''
		process the tree node with 'Num' type
		'''
		codes = repr(tree.n)
		return {"codes":codes, "returnType":IntType}

	binop = {"Add":"+", "Sub":"-", "Mult":"*", "Div":"/", "Mod":"%",\
			"LShift":"<<", "RShift":">>", "BitOr":"|", "BitXor":"^", "BitAnd":"&",\
			"FloorDiv":"//", "Pow": "**", "Eq":"==", "GtE":">=", "LtE":"<=",\
			"Gt":">", "Lt":"<", "NotEq":"!="}
	def IsBinOp(self, tree):
		'''
		process the tree node with 'Binop' type
		'''
		codes = self.Traverse(tree.left)["codes"]
		codes += self.binop[tree.op.__class__.__name__]
		codes += self.Traverse(tree.right)["codes"]
		
		try:
			codes = repr(eval(codes))
		except:
			pass
		
		codes = "(" + codes + ")"
		
		return {"codes":codes, "returnType":IntType}
	
	def CheckArgs(self, args):
		for arg in args:
			if "arg" in str(arg) or "shift_mask" in str(arg) or "val1" in str(arg):
				return False
		return True

	def IsCall(self, tree):
		'''
		process the tree node with 'Call' type
		'''
		codes = ""
		returnType = None
		preLen = len(self.curFunc)
		#Get the function name
		funcRet = self.Traverse(tree.func)
		funcName = funcRet["codes"]
		returnType = funcRet["returnType"]
		
		#Start to pack args
		sz = len(tree.args)
		argList = []
		for i in range(sz):
			argList.append(self.Traverse(tree.args[i])["codes"])

		if len(self.curFunc) > preLen and isinstance(self.curFunc[-1], Operation):
			#func now is a defined simd operation
			op = self.curFunc[-1]
			del self.curFunc[-1]
			if op.opPattern == 0:
				codes += op.CallingStatementToCText(argList[0], argList[1:])
				if self.isCompileTimeConstant == True:
					self.isCompileTimeConstant = self.CheckArgs(argList[1:])
			elif op.opPattern == 1:
				codes += op.CallingStatementToCText(argList[0], argList[2:], argList[1])
				if self.isCompileTimeConstant == True:
					self.isCompileTimeConstant = self.CheckArgs(argList[2:])
			elif op.opPattern == 2:
				codes += op.CallingStatementToCText(1, argList[0:])
				if self.isCompileTimeConstant == True:
					self.isCompileTimeConstant = self.CheckArgs(argList[0:])
			elif op.opPattern == 3:
				codes += op.CallingStatementToCText(Utility.curRegisterSize, argList[0:])
				if self.isCompileTimeConstant == True:
					self.isCompileTimeConstant = self.CheckArgs(argList[0:])
			
			#Add the op into calls in the format of class_op_fw
			if op.opPattern == 0 or op.opPattern == 1:
				#self.calls.append(op.fullName + "_" + str(eval(argList[0])))
				self.prevCall.append(op.fullName + "_" + str(eval(argList[0])))
			elif op.opPattern == 2:
				#logic operation always has field width 1
				#self.calls.append(op.fullName + "_" + str(1))
				self.prevCall.append(op.fullName + "_" + str(1))
			elif op.opPattern == 3:
				self.prevCall.append(op.fullName + "_" + str(Utility.curRegisterSize))
		else:
			#func is not a simd operation and then it must be one of functions specified in built-ins
			#print "else funcName", funcName
			if Utility.builtIns.IsOperationBuiltIn(funcName) == False and Utility.functionSupport.has_key(funcName) == False:
				print "This function " + funcName + " is unknown!"
				return {"codes":None, "returnType":None}
			
			codes = Utility.CallingStatement(funcName, argList)
			returnType = None
			if Utility.builtIns.IsOperationBuiltIn(funcName) == True:
				returnType = Utility.builtIns.GetOperationReturnType(funcName)
			elif Utility.functionSupport.has_key(funcName) == True:
				returnType = Utility.functionSupport[funcName]["returnType"]
				Utility.usedFunctionSupport[funcName] = True
			
			if self.isCompileTimeConstant == True:
				self.isCompileTimeConstant = self.CheckArgs(argList)
			#For other operations, just add its name as it is
			#self.calls.append(funcName)
			self.prevCall.append(funcName)
		#print "func is " + codes + " with type ", returnType
		return {"codes":codes, "returnType":returnType}
		
