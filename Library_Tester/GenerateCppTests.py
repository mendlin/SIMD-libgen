
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import os

import GenData
import TesterUtility
from TesterUtility import configure

maxTestCase = 100

normalFunc = r'''
void Testing_$opFullName$(int fw)
{
	string inFile = (string)"$cwd$/input/" + "$opFullName$" + "_" + Int2String(fw) + ".in";
	string outFile = (string)"$cwd$/output_temp/" + "$opFullName$" + "_" + Int2String(fw)+".out";
	vector< vector<string> > data = ReadTestData(inFile.c_str());
	vector<string> ans;
	int sz = data.size();
	for(int i=0; i<sz; i++)
	{
		vector<string> tuple = data[i];
		
		$arguments_init$

		$tmpAns_type$ tmpAns;
		switch(fw)
		{
			$test_body$
		
			default:
				break;
		}
		ans.push_back($store_tmpAns$);
	}
	WriteResult(outFile.c_str(), ans);
}
'''

templatedFunc = r'''
void Testing_$opFullName$(int fw)
{
	string inFile = (string)"$cwd$/input/" + "$opFullName$" + "_" + Int2String(fw) + ".in";
	string outFile = (string)"$cwd$/output_temp/" + "$opFullName$" + "_" + Int2String(fw)+".out";
	vector< vector<string> > data = ReadTestData(inFile.c_str());
	vector<string> ans;
	
	$arguments_init$
	
	switch(fw)
	{
		$test_body$
		
		default:
			break;
	}
	WriteResult(outFile.c_str(), ans);
}
'''

options_global = None

def TemplatedFuncMakeCppText(arch, operation, validOperations, testingData):
	text = templatedFunc
	oprdNum = len(operation.arguments)
	SIMD_type = configure.Bitblock_type[arch]

	arguments_init = ""
	for i in range(oprdNum):
		arguments_init += "\t" + SIMD_type + " arg" + str(i) + ";\n"
	
	test_body = ""
	for vop in validOperations[operation.fullName]:
		op_fw = operation.fullName + "_" + str(vop.fw)
		test_body += "\t\t" + "case " + str(vop.fw) + ":\n"
		for i in range(len(testingData[op_fw])):
			args = []
			for j in range(oprdNum):
				if operation.arguments[j].type == SIMD_type:
					test_body += "\t\t\t" + "arg$j$ = LoadfromString(data[$i$][$j$], $optId$);\n".replace("$j$", str(j)).replace("$i$", str(i)).replace("$optId$", str(TesterUtility.GetOptId(arch)))
				elif operation.arguments[j].type == "uint64_t":
					test_body += "\t\t\t" + "arg$j$ = DigitString2Int(data[$i$][$j$]);\n".replace("$j$", str(j)).replace("$i$", str(i))
				else:
					print "can't process this data type", operation.arguments[j].type
				args.append("arg"+str(j))
				
			if operation.returnType == SIMD_type:
				test_body += "\t\t\t" + "ans.push_back(Store2String($call_op$, $optId$));\n".replace("$call_op$", operation.CallingStatementToCppText(vop.fw, args, testingData[op_fw][i][-1], True)).replace("$optId$", str(TesterUtility.GetOptId(arch)))
			elif operation.returnType == "uint64_t":
				test_body += "\t\t\t" + "ans.push_back(Int2String($call_op$));\n".replace("$call_op$", operation.CallingStatementToCppText(vop.fw, args, testingData[op_fw][i][-1], True)).replace("$optId$", str(TesterUtility.GetOptId(arch)))
			else:
				assert False, "can't process this data type" + str(operation.returnType)
		test_body += "\t\t\t" + "break;\n"

	text = text.replace("$opFullName$", operation.fullName)
	if options_global.test_option == "neon_gen_data":
		text = text.replace("$cwd$/", "")
	else:
		text = text.replace("$cwd$", os.getcwd());
	text = text.replace("$arguments_init$", arguments_init)
	text = text.replace("$test_body$", test_body)
	
	return text

def NormalFuncMakeCppText(arch, operation, validOperations, testingData):
	text = normalFunc
	oprdNum = len(operation.arguments)
	SIMD_type = configure.Bitblock_type[arch]
	args = []
	arguments_init = ""
	for i in range(oprdNum):
		if operation.arguments[i].type == SIMD_type:
			arguments_init += "\t" + SIMD_type + " arg" + str(i) + " = " + "LoadfromString(tuple[$i$], $optId$);\n".replace("$i$", str(i)).replace("$optId$", str(TesterUtility.GetOptId(arch)))
		elif operation.arguments[i].type == "uint64_t":
			arguments_init += "\t" + "uint64_t arg" + str(i) + " = " + "DigitString2Int(tuple[$i$]);\n".replace("$i$", str(i))
		else:
			print "can't process this data type", operation.arguments[i].type
		args.append("arg"+str(i))
	
	test_body = ""
	for vop in validOperations[operation.fullName]:
		op_fw = operation.fullName + "_" + str(vop.fw)
		test_body += "\t\t" + "case " + str(vop.fw) + ":\n"
		test_body += "\t\t\t" + "tmpAns = $call_op$;\n".replace("$call_op$", operation.CallingStatementToCppText(vop.fw, args))
		test_body += "\t\t\t" + "break" + ";\n"
	
	text = text.replace("$opFullName$", operation.fullName)
	if options_global.test_option == "neon_gen_data":
		text = text.replace("$cwd$/", "")
	else:
		text = text.replace("$cwd$", os.getcwd());
	text = text.replace("$arguments_init$", arguments_init)
	text = text.replace("$test_body$", test_body)
	text = text.replace("$tmpAns_type$", operation.returnType)
	if operation.returnType == SIMD_type:
		text = text.replace("$store_tmpAns$", "Store2String(tmpAns, $optId$)".replace("$optId$", str(TesterUtility.GetOptId(arch))))
	elif operation.returnType == "uint64_t" or operation.returnType == "bool":
		text = text.replace("$store_tmpAns$", "Int2String(tmpAns)")
	else:
		print "can't process this data type", operation.returnType
	text = text.replace("$arch_opt$", str(TesterUtility.GetOptId(arch)))
	
	return text

def MakeCppText(arch, definedOperations, validOperations, testingData, options):
	
	global options_global
	options_global = options
	
	if options.test_option == "neon_gen_data":
		header = '''#include "lib/utility.h"\n'''
	else:
		header = '''#include "utility.h"\n'''
	
	funcDefs = ""
	for opFullName in validOperations:
		operation = definedOperations[opFullName][1]
		
		if operation.opPattern == 1 or operation.opPattern == 4:
			#operations with other types
			funcDefs += TemplatedFuncMakeCppText(arch, operation, validOperations, testingData)
		elif operation.opPattern == 0 or operation.opPattern == 2 or operation.opPattern == 3:
			#logic operations and normal operations
			funcDefs += NormalFuncMakeCppText(arch, operation, validOperations, testingData)
		else:
			print "unknown operation pattern!"
		
	mainBody = "int main()\n{\n"
	for opFullName in validOperations:
		operation = definedOperations[opFullName][1]
		#if operation.opPattern == 4: continue
		for vop in validOperations[opFullName]:
			mainBody += "\t" + "Testing_" + opFullName + "(" + str(vop.fw) + ")" + ";\n"
	mainBody += "\t" + "return 0" + ";\n}"
	
	return header + funcDefs + mainBody
	
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
						lowBound = operation.valueRange[key]["min"]
						upBound = operation.valueRange[key]["max"]
						templatedData = TesterUtility.GetRandomNums(lowBound, upBound, maxTestCase)
						break
					
					for i in range(len(templatedData)):
						testingData[opFullName + "_" + str(validOp.fw)][i].append(templatedData[i])
	
	print "finished generating test data."
	return testingData

def WriteCppText(arch, objFile, cppText):
	'''modify utility.h
	'''
	fileIn = open("utility.h", "r")
	utilityCodes = fileIn.readlines()
	utilityCodes[0] = '''#include "''' + "idisa_" + arch.lower() + '''.h"\n'''
	utilityCodes[1] = '''#define USE_SSE\n''' if arch in configure.SSE_SERIES else ('''#define USE_AVX\n''' if arch == configure.AVX else ('''#define USE_NEON\n''' if arch == configure.NEON else '''''')) 
	utilityCodes[2] = '''typedef ''' + configure.SIMD_type[arch] + " SIMD_type;\n"
	fileIn.close()
	fileIn = open("utility.h", "w")
	for code in utilityCodes:
		fileIn.write(code)
	fileIn.close()
	
	'''write c++ codes
	'''
	fileOut = open(objFile, "w")
	fileOut.write(cppText)
	fileOut.close()
