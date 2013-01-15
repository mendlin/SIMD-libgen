
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import re
import sys
import traceback
import math

import StandardTypes
import Utility
from Utility import configure

def LoadDefinedOperations(allOperations, arch):
	definedOperations = {}
	for opName in allOperations:
		#print allOperations[opName]
		
		operationTmp = Operation(allOperations[opName], arch)
		definedOperations[operationTmp.fullName] = {}
		fws = Utility.GetValidFieldWidth(configure.RegisterSize[arch])
		for fw in fws:
			#Get an operation object given the information of operation description and architecture
			operation = Operation(allOperations[opName], arch, fw)
			#Add this operation object into the operationSet dictionary
			definedOperations[operation.fullName][fw] = operation
			#ouput debug information
			# DebugOut(operation)
	
	#sys.exit()
	
	return definedOperations

def DebugOut(operation):
	print "full name=", operation.fullName
	print "return_type=", operation.returnType
	print "arguments="
	for arg in operation.arguments:
		print arg.type, arg.name
	print "templated arguments="
	print operation.templateArg.type, operation.templateArg.name
	print "value range="
	print operation.valueRange

class Operation:
	r'''The class Operation which describes the basic form of an operation.
An operation contains operation name, field width, operation type, operation pattern, return type, arguments and template arguments.
	'''
	def __init__(self, opDescription, arch, fw=0):
		'''
		the constructor for Operation
		'''
		self.name = ""
		self.arch = arch
		self.fieldWidth = fw
		self.classType = ""
		self.opPattern = -1
		self.returnType = ""
		self.arguments = []
		self.templateArg = Utility.LibVariable("", "")
		self.ParseOpDescription(opDescription["signature"], arch)
		self.fullName = ""
		self.valueRange = {}
		self.estCost = 0
		
		#fullName looks like "class_op"
		if self.classType not in self.name:
			self.fullName = self.classType + "_" + self.name
		else:
			self.fullName = self.name
		
		#call GetValueRange after we get the value for fullName
		if fw > 0:
			self.PostParsing(opDescription)
		
		self.newClassType = self.classType + (str(configure.RegisterSize[arch]) if Utility.outputOpt != configure.Body_All else "")

		self.cpp_class_signature = ""
		if "cpp_class_signature" in opDescription:
			self.cpp_class_signature = opDescription["cpp_class_signature"].replace("SIMD_type", configure.Bitblock_type[self.arch])
	
	def PostParsing(self, opDescription): 
		regSize = configure.RegisterSize[self.arch]
		return_type = opDescription["return_type"]
		args_type = opDescription["args_type"]
		int_type = "unsigned_int(64)"
		
		if StandardTypes.IsSIMDType(return_type):
			self.returnType = configure.Bitblock_type[self.arch]
		elif StandardTypes.IsUnsignedIntType(return_type):
			# uint64_t is the standard type for integers throughout the idisa libraries
			self.returnType = StandardTypes.GetUnsignedIntType(int_type, regSize)
		
		newArgs = []
		for i in range(len(self.arguments)):
			arg = self.arguments[i]
			argType = args_type[arg.name]
			if StandardTypes.IsUnsignedIntType(argType):
				(minV, maxV) = Utility.GetMinMax(StandardTypes.GetUnsignedIntType(argType, regSize, self.fieldWidth, False))
				self.valueRange[arg.name] = {"min":minV, "max":maxV}
				argType = StandardTypes.GetUnsignedIntType(int_type, regSize)
			elif StandardTypes.IsRangeType(argType):
				# for non-templated arguments, find an appropriate type
				(minV, maxV) = Utility.GetMinMax(Utility.EvalStr(argType, regSize, self.fieldWidth))
				self.valueRange[arg.name] = {"min":minV, "max":maxV}
				argType = StandardTypes.GetUnsignedIntType(int_type, regSize)
			elif StandardTypes.IsSIMDPointer(argType):
				argType = configure.Bitblock_type[self.arch] + "*"
			elif StandardTypes.IsFloatConstantPointer(argType):
				argType = StandardTypes.GetFloatConstantPointer()
			elif StandardTypes.IsFloatPointer(argType):
				argType = StandardTypes.GetFloatPointer()
			elif StandardTypes.IsLoadType(argType):
				argType = StandardTypes.GetLoadType(self.arch)
			elif StandardTypes.IsStoreType(argType):
				argType = StandardTypes.GetStoreType(self.arch)
			else:
				#it must be a SIMD_type
				argType = configure.Bitblock_type[self.arch]
			self.arguments[i].type = argType
		
		if self.opPattern == 1 or self.opPattern == 4:
			self.templateArg.type = StandardTypes.GetUnsignedIntType(int_type, regSize)
			argType = args_type[self.templateArg.name]
			if StandardTypes.IsUnsignedIntType(argType):
				(minV, maxV) = Utility.GetMinMax(StandardTypes.GetUnsignedIntType(argType, regSize, self.fieldWidth, False))
				self.valueRange[self.templateArg.name] = {"min":minV, "max":maxV}
			elif StandardTypes.IsRangeType(argType):
				(minV, maxV) = Utility.GetMinMax(Utility.EvalStr(argType, regSize, self.fieldWidth))
				self.valueRange[self.templateArg.name] = {"min":minV, "max":maxV}
	
	def ParseOpDescription(self, opDescription, arch):
		r'''Parse the operation description string to get classType, opPattern and the list of arguments
		'''
		returnTypeMatchObj = re.search("([a-zA-Z_]+) ", opDescription)
		try:
			self.returnType = returnTypeMatchObj.group(1)
			#print self.returnType
		except Exception, e:
			traceback_print_exc()
			sys.exit()
			
		typeNameMatchObj = re.search("([a-zA-Z]+)(<[a-zA-Z]+>)*::", opDescription)
		#print typeNameMatchObj.group(0, 1, 2)
		try:
			self.classType = typeNameMatchObj.group(1)
		except Exception, e:
			#print "At Operation -> ParseOpDescription:\n\tThe operation description = " +\
			#	opDescription + " is not valid.\n\tThe problems maybe '::' is not included or the class is not templated class."
			#traceback.print_exc()
			#sys.exit()
			#This operation has no class type which means it's a logic operation
			pass
		
		funcMatchObj = re.search("([a-zA-Z_0-9]+)<*([a-zA-Z]+)*>*\(", opDescription)
		#print funcMatchObj.group(0, 1, 2)
		try:
			self.name = funcMatchObj.group(1)
			if self.classType == "":
			#This operation is a logic operation
				self.opPattern = 2
			elif funcMatchObj.group(2) and typeNameMatchObj.group(2):
				self.opPattern = 1
				self.templateArg.type = "int"
				self.templateArg.name = funcMatchObj.group(2)
			elif funcMatchObj.group(2):
				self.opPattern = 4
				self.templateArg.type = "int"
				self.templateArg.name = funcMatchObj.group(2)
			elif typeNameMatchObj.group(2):
				self.opPattern = 0
			else:
				self.opPattern = 3
		except Exception, e:
			#print "At Operation -> PraseOpDescription:\n\tCan't match the function name!"
			traceback.print_exc()
			sys.exit()
		
		leftBracketMatchObj = re.search("\(", opDescription)
		rightBracketMatchObj = re.search("\)", opDescription)
		try:
			args = opDescription[leftBracketMatchObj.start()+1:rightBracketMatchObj.start()]
			if len(args) > 0:
				args = re.split(",", args)
				for arg in args:
					arg0 = arg.strip()
					spacePos, lastSpacePos = 0, 0
					while arg0.find(" ", spacePos) != -1:
						lastSpacePos = arg0.find(" ", spacePos)
						spacePos = lastSpacePos + 1
					#argPart0 is the data type of the first argument, it could be SIMD_type or SIMD_type*
					argPart0 = arg0[:lastSpacePos].strip()
					#argPart1 is the name of the first argument, it could be any variable name or '&'+variable_name
					argPart1 = arg0[lastSpacePos+1:].strip()
					self.arguments.append( Utility.LibVariable(argPart0, argPart1) )
		except Exception, e:
			traceback.print_exc()
			sys.exit()
	
	def CallingPrefixToCppText(self):
		if self.opPattern == 2:
		#This is a logic operation, return its name as the calling prefix
			return self.name
		cppText = self.classType
		if self.opPattern == 1:  # Have a field-width parameter
			cppText += "<" + "$fw$" + ">"
		cppText += "::" + self.name
		if self.opPattern == 1 or self.opPattern == 4:  # Have a template arg
			cppText += "<" + "$" + self.templateArg.name + "$" + ">"
		return cppText
	
	def CallingStatementToCppText(self, fw, args=[], templateArg="", testingFlag=False):
		#print "in args ", args, " self args", self.arguments, " cur op ", self.name, "curlen= ", len(args)
		if len(args) != len(self.arguments):
			print "The operation " + self.newClassType + "::" + self.name + " doesn't accept this many arguments!"
			sys.exit()
		
		cppText = self.newClassType + "<" + str(fw) + ">" + "::" + self.name
		if self.opPattern == 1:
			#simd<fw>::op<val>(...)
			if testingFlag:
				cppText += "<" + "(" + str(self.templateArg.type) + ")" + "(" + str(templateArg) + "ULL)" + ">"
			else:
				cppText += "<" + str(templateArg) + ">"
		if self.opPattern == 4:
			#bitblock::op<val>(...)
			if testingFlag:
				cppText = self.newClassType + "::" + self.name + "<" + "(" + str(self.templateArg.type) + ")" + "(" + str(templateArg) + "ULL)" + ">"
			else:
				cppText = self.newClassType + "::" + self.name + "<" + str(templateArg) + ">"
		elif self.opPattern == 2:
			cppText = self.name
		elif self.opPattern == 3:
			cppText = self.newClassType + "::" + self.name
		
		cppText += "("
		for i in range(len(args)):
			arg = args[i]
			if StandardTypes.IsSIMDType(self.arguments[i].type):
				cppText += str(arg) + ", "
			else:
				#cppText += "(" + str(self.arguments[i].type) + ")" + "(" + str(arg) + ")" + ", "
				cppText += str(arg) + ", "
		if len(args) > 0:
		#if there is at least one argument
			cppText = cppText[0:len(cppText)-2]
		cppText += ")"
		
		#print "return cppText= ", cppText
		return cppText
	
	def CallingStatementToCText(self, fw, args=[], templateArg=""):
		if len(args) != len(self.arguments):
			print "The operation " + self.classType + "::" + self.name + " doesn't accept this many arguments!"
			sys.exit()
		
		fw = Utility.CleanBrackets(str(fw))
			
		cText = ""
		if self.opPattern == 0 or self.opPattern == 1:
			cText = self.classType + "_" + self.name + "_" + str(fw)
		elif self.opPattern == 2:
			cText = self.name
		elif self.opPattern == 3:
			cText = self.classType + "_" + self.name
		
		cText += "("
		for arg in args:
			cText += str(arg) + ", "
		if self.opPattern == 1 or self.opPattern == 4:
			cText += str(templateArg) + ", "
		
		if len(args) > 0 or self.opPattern == 1:
		#if there is at least one argument
			cText = cText[0:len(cText)-2]
		cText += ")"
		
		return cText
