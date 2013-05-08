
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import sys
import os
import math

os.chdir(sys.path[0])
#import the configure module
sys.path.append("../Configure/")

import configure
import OptParser
import BuiltIns
import re

#This dictionary stores all the simd operations with class_func as the format for keys
#It should be initialized by Operation.GetDefinedOperations() at Main()
#{class_func:{fw1:operation1, fw2:operation2, ...}}
definedOperations = {}

#This is the object created by class BuiltIns when the architecture information is given
#It should be created by BuiltIns.__init__() at Main()
builtIns = None

#This is all the strategy instances created by Strategy.LoadStrategies() at Main()
strategies = {}

#It records the register size of current architecture
curRegisterSize = 0

#it stores some functions which support codes generation
functionSupport = {}

#used function support
usedFunctionSupport = {}

outputOpt = configure.Body_All
#This is an interface for returning the calling statements of a function given its all arguments
#e.g. given function name = "foo" and arguments = [arg1, arg2], then it returns "foo(arg1, arg2)"
def CallingStatement(func, arch, args):
	if builtIns.IsOperationBuiltIn(func):
		builtInOp = BuiltIns.BuiltInOperation(arch, builtIns.builtInsTable[func]["signature"][0], builtIns.builtInsTable[func]["args_type"])
		builtInOp.arguments = args
		return builtInOp.GetCallingConvention()
	
	text = func
	text += "("
	argSz = len(args)
	for i in range(argSz):
		text += str(args[i])
		if i < argSz-1:
			text += ", "
	text += ")"
	return text

def GetValidFieldWidth(registerSz):
	ret = [1]
	fw = 2
	while fw<=registerSz:
		ret.append(fw)
		fw *= 2
	return ret

#Load some pre-defined functions
def LoadFunctionSupport(arch, lang):
	retFuncs = {}
	allFuncs = {}
	
	if lang == configure.Language_C:
		import CppFunctionSupport
		allFuncs = CppFunctionSupport.Functions
	elif lang == configure.Language_CPP:
		import CppFunctionSupport
		allFuncs = CppFunctionSupport.Functions

	for func in allFuncs:
		if "all" in allFuncs[func]["platform"] or arch in allFuncs[func]["platform"]:
			retFuncs[func] = allFuncs[func]
			retFuncs[func]["body"] = retFuncs[func]["body"].replace("(SIMD_type)", "("+configure.Bitblock_type[arch]+")")

	return retFuncs

def CleanBrackets(expr):
	if "(" not in expr or ")" not in expr:
		return expr
	lPos = expr.find("(")
	rPos = len(expr)-1
	while rPos >= 0 and expr[rPos] != ")":
		rPos -= 1
	return CleanBrackets(expr[lPos+1:rPos])

def EvalStr(expr, regSize, fw):
	expr = expr[expr.find("(")+1:-1]
	expr = expr.replace("fw", str(fw)).replace("curRegSize", str(regSize))
	return [eval(val) for val in expr.split(",", 1)]

def GetMinMax(expr):
	if isinstance(expr, str):
		fw = eval(''.join(ch for ch in expr if ch.isdigit()))
		fw = 64 if fw >= 64 else fw
		return (0, (2**fw)-1)
	elif isinstance(expr, list):
		return (expr[0], expr[-1])
	print expr
	assert True==False, "Unknown expr for GetMinMax!"

# This part is about definition of LibClass, LibFunction and LibVariable, in which,
# LibClass is the class to describe general interfaces of classes(such as simd, hsimd, esimd, mvmd);
# LibFunction is the class to describe general interfaces of functions(such as add, sub, pack, merge);
# LibVariable is the class to describe general interfaces of variables(it only has two fields, variable type & name)
class LibClass:
	def __init__(self, name, body=[], templatedClass=True, arch=""):
		self.name = name
		self.type = "class"
		self.body = []
		self.templatedClass = templatedClass
		self.regSize = str(configure.RegisterSize[arch]) if outputOpt != configure.Body_All else ""
		self.name = self.name + self.regSize
		
	def Append(self, element):
		self.body.append(element)
		
	def ToCppText(self):
		cppText = "template <uint32_t fw>\n" if self.templatedClass==True else ""
		cppText += self.type + " " + self.name + "\n"
		cppText += "{\n"
		#All functions are public member functions
		cppText += "public:\n"
		for item in self.body:
			if isinstance(item, LibFunction):
				cppText += "\t" + item.ClassDeclarationToCppText() + ";\n"
			else:
				print "function pattern unknown!"
		cppText += "};\n\n"
		return cppText

class LibFunction:
	def __init__(self, operation, cost=0, body=""):
		self.arch = operation.arch
		self.name = operation.name
		self.type = "function"
		self.classType = operation.classType
		self.returnType = operation.returnType
		self.fieldWidth = operation.fieldWidth
		self.opPattern = operation.opPattern
		self.arguments = operation.arguments
		self.templateArg = operation.templateArg
		self.cost = cost
		self.body = body
		self.regSize = str(configure.RegisterSize[self.arch]) if outputOpt != configure.Body_All else ""
		self.classType = self.classType + self.regSize
		self.inlineStr = "IDISA_ALWAYS_INLINE" if outputOpt != configure.Body_All else "inline"
		self.cpp_class_signature = operation.cpp_class_signature
	
	#def SetBodyContent(self, body):
	#	self.body = body
		
	def ArgumentsToCppText(self):
		text = ""
		for arg in self.arguments:
			text += arg.type + " " + arg.name + ", "
		return text[0:len(text)-2]
	
	def ClassDeclarationToCppText(self):
		# if we have provided a signature
		if self.cpp_class_signature != "":
			return self.cpp_class_signature.replace("inline ", self.inlineStr + " ")

		text = ""
		if self.opPattern == 0 or self.opPattern == 3:
			text += "static " + self.inlineStr + " " + self.returnType + " " + self.name + "(" + self.ArgumentsToCppText() + ")"
		elif self.opPattern == 1 or self.opPattern == 4:
			text += "template <" + self.templateArg.type + " " + self.templateArg.name + "> " + "static " + self.inlineStr + " " + self.returnType + " " + self.name + "(" + self.ArgumentsToCppText() + ")"
		return text# + " __attribute__ ((always_inline))"
	
	def FunctionDeclarationToCppText(self):
		#if we have provided a signature
		if self.cpp_class_signature != "":
			declare = ("template <> " if self.classType != "bitblock" else "") + self.ClassDeclarationToCppText()
			declare = declare.replace("static ", "")			
			declare = declare.replace("typename ", "")
			declare = re.sub(r'\bfw\b', str(self.fieldWidth), declare)
			if self.classType != "bitblock":			
				declare = re.sub(r'\b' + self.name + r'\b', "%s<%d>::%s" % (self.classType, self.fieldWidth, self.name), declare)			
			else:
				declare = re.sub(r'\b' + self.name + r'\b', "%s::%s" % (self.classType, self.name), declare)

			return declare			

		text = "template <> "
		if self.opPattern == 0:
			text += self.inlineStr + " " + self.returnType + " " + self.classType + "<" + str(self.fieldWidth) + ">" + "::" + self.name + "(" + self.ArgumentsToCppText() + ")"
		elif self.opPattern == 1:
			text += "template <" + self.templateArg.type + " " + self.templateArg.name + ">" + " " + self.inlineStr + " " + self.returnType + " " + self.classType + "<" + str(self.fieldWidth) + ">" + "::" + self.name + "(" + self.ArgumentsToCppText() + ")"
		elif self.opPattern == 2:
			text = self.inlineStr + " " + self.returnType + " " + self.name + "(" + self.ArgumentsToCppText() + ")"
		elif self.opPattern == 3:
			text = self.inlineStr + " " + self.returnType + " " + self.classType + "::" + self.name + "(" + self.ArgumentsToCppText() + ")"
		elif self.opPattern == 4:
			text = "template <" + self.templateArg.type + " " + self.templateArg.name + "> " + self.inlineStr + " " + self.returnType + " " + self.classType + "::" + self.name + "(" + self.ArgumentsToCppText() + ")"
		return text
		
	def ToCppText(self):
		cppText = "//The total number of operations is " + str(self.cost) + "\n"
		cppText += self.FunctionDeclarationToCppText() + "\n"
		cppText += self.body
		return cppText
	
	def CMarcoSignature(self):
		text = "#define "
		if self.opPattern == 2:
			text += self.name
		elif self.opPattern == 3 or self.opPattern == 4:
			text += self.classType + "_" + self.name		
		else:
			text += self.classType + "_" + self.name + "_" + str(self.fieldWidth)
		
		text += "("
		for arg in self.arguments:
			text += arg.name + ", "
		if self.opPattern == 1 or self.opPattern == 4:
			text += self.templateArg.name
		elif len(self.arguments) > 0:
			text = text[0:len(text)-2]
	
		text += ")"
		return text
	
	def CStaticInlineText(self):
		text = "static inline " + self.returnType + " "
		if self.opPattern == 2:
			text += self.name
		elif self.opPattern == 3 or self.opPattern == 4:
			text += self.classType + "_" + self.name
		else:
			text += self.classType + "_" + self.name + "_" + str(self.fieldWidth)
			
		text += "("
		for arg in self.arguments:
			text += arg.type + " " + arg.name + ", "
		if self.opPattern == 1 or self.opPattern == 4:
			text += self.templateArg.type + " " + self.templateArg.name
		elif len(self.arguments) > 0:
			text = text[0:len(text)-2]
		
		text += ")"
		return text
	
	def FunctionDeclarationToCText(self):
		text = ""
		#if self.body.count("\n") <= 1:
		#	text += self.CMarcoSignature()
		#else:
		text += self.CStaticInlineText()
		return text
	
	def ToCText(self):
		cText = "//The total number of operations is " + str(self.cost) + "\n"
		cText += self.FunctionDeclarationToCText()
		#if self.body.count("\n") <= 1:
		#	cText += self.body.replace("return", "").replace(";", "") + "\n"
		#else:
		cText += "\n{" + "\n\t" + self.body.strip() + "\n}\n"
		return cText

	def ToCMacro(self):
		cText = "//The total number of operations is " + str(self.cost) + "\n"
		cText += self.CMarcoSignature()
		cText += " \\\n\t" + self.body.replace("return", "").replace(";", "").strip() + "\n"
		return cText

class LibVariable:
	def __init__(self, variableType, variableName):
		self.type = variableType
		self.name = variableName
