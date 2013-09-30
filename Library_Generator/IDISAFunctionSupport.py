
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import Utility
from Utility import configure

class IDISAFunction:
    
    def __init__(self, arch):
	self.arch = arch
	pass

    @staticmethod
    def IsIDISAFunction(funcName):
	callMethod = None
	try:
	    callMethod = getattr(IDISAFunction, "Is" + funcName.upper())
	except:
	    pass
	return True if callMethod else False
    
    @staticmethod
    def Parse(self, funcName, argsList, fw=0):
	callMethod = getattr(self, "Is" + funcName.upper())
	argsList.append(fw)    
	if callMethod:
	    return callMethod(argsList)
	else:
	    print "No such IDISA function", funcName

    def IsIDISA_CASTING(self, argsList):
	assert len(argsList)-1 == 2, "IDISA_CASTING can't accept these many arguments!"
	castExpr = str(argsList[0])
	if castExpr == "_mm_castsi128_ps":  
		return (castExpr + "(" + str(argsList[1]) + ")", "__m128")
	if castExpr == "_mm256_castsi256_ps":
		return (castExpr + "(" + str(argsList[1]) + ")", "__m256")
	if castExpr == "_mm_castsi128_pd":                  
		return (castExpr + "(" + str(argsList[1]) + ")", "__m128d")
	if castExpr == "_mm256_castsi256_pd":
		return (castExpr + "(" + str(argsList[1]) + ")", "__m256d")
	if castExpr == "_mm256_castsi128_si256":
		return (castExpr + "(" + str(argsList[1]) + ")", "__m256i")

	returnType = configure.Bitblock_type[self.arch] if castExpr == "SIMD_type" else castExpr
	#codes = "reinterpret_cast" + "<" + returnType + ">(" + str(argsList[1]) + ")"
	codes = "((" + returnType + ")(" + str(argsList[1]) + "))"
	return (codes, returnType)
    
    def IsIDISA_PACK(self, argsList):
	func = argsList[0]
	fw = argsList[-1]
	assert "$fw$" in func, "No $fw$ in function name!"
	func = func.replace("$fw$", str(fw))
	assert Utility.builtIns.IsOperationBuiltIn(func) == True, "This " + func + " is not a built-in!" 
	
	returnType = Utility.builtIns.GetOperationReturnType(func)
	codes = func + "("
	for arg in argsList[1:-2]:
		codes += arg + "," + " "
	codes += argsList[-2] + ")"
	return (codes, returnType)
