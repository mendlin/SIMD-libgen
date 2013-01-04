
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import os
import sys

import TesterUtility
from TesterUtility import Operation, configure
import ParseIdisaDB

oneOperandTestingRepr = r'''
s1 = $simd_op$(t1);
s2 = $simd_op$(t2);
s3 = $simd_op$(t3);
s4 = $simd_op$(t4);
t1 = $simd_op$(s1);
t2 = $simd_op$(s2);
t3 = $simd_op$(s3);
t4 = $simd_op$(s4);
'''

twoOperandTestingRepr = r'''
s1 = $simd_op$(t1, t2);
s2 = $simd_op$(t3, t4);
t1 = $simd_op$(s1, t2);
t3 = $simd_op$(s2, t4);
'''

threeOperandTestingRepr = r'''
s1 = $simd_op$(t1, t2, t3);
s2 = $simd_op$(t2, t1, t3);
s3 = $simd_op$(t3, t1, t2);
t1 = $simd_op$(s1, t2, t3);
t2 = $simd_op$(s2, t1, t3);
t3 = $simd_op$(s3, t2, t3);
'''

commonText = r'''
#include "../i386_timer.h"
#include "../utility.h"
#include <iostream>
#include <fstream>
#include <cstdlib>

$global_variable$

int main()
{
	std::cout << "$op$" << " test begins..." << std::endl;
	ofstream fout;
	fout.open("test.out");
	srand(time(NULL));
	timestamp_t x;
	timestamp_t y;
	double cyc = 1e10;
	
	$variable_init$
	
	for(int i=0; i<$testCase$; i++)
	{
		x = read_cycle_counter();
		
		$operation_list$
		
		y = read_cycle_counter();
		double z = (y-x)*1.0/$opCount$;
		cyc = cyc < z ? cyc : z;
	}
	
	fout << cyc << std::endl;
	
	$write_variable$
	
	fout.close();
	std::cout << "$op$" << " test ends..." << std::endl;
	return 0;
}
'''

outputDir = os.getcwd() + "/perf_out/"
gccCommand = "g++ $arch$ -O3 -o $des$ $src$ --param inline-unit-growth=100000 --param large-function-growth=5000"
gccAssemblyCommand = "g++ $arch$ -O3 -S $des$ $src$ --param inline-unit-growth=100000 --param large-function-growth=5000"

repeatTime = 100
testCases = 20

def ParseTestingStr(testingStr):
	varTable = {}
	newLineCount = 0
	newTestingStr = ""
	while True:
		newLinePos = testingStr.find("\n")
		if newLinePos == -1:
			break
		if newLinePos > 1:
			varStr = testingStr[0:newLinePos]
			varStr = varStr[0:varStr.find(" =")]
			newTestingStr += testingStr[0:newLinePos] + '''asm volatile("" : "=x"($var$) : "0"($var$));'''.replace("$var$", varStr) + "\n"
		tmpStr = testingStr[0:newLinePos]
		#print "tmpStr = ", tmpStr
		if len(tmpStr) > 1:
			newLineCount += 1
			varStr = tmpStr[0:tmpStr.find("=")].strip()
			if varStr not in varTable:
				varTable[varStr] = 0
			tmpStr = tmpStr[tmpStr.find("(")+1:tmpStr.find(")")]
			varList = [varStr.strip() for varStr in tmpStr.split(",")]
			for varStr in varList:
				try:
					eval(varStr)
				except:
					if varStr not in varTable:
						varTable[varStr] = 1
		testingStr = testingStr[newLinePos+1:]
	
	return (varTable, newLineCount, newTestingStr)

def PackAnOperation(testingRepr, operation):
	'''All the arguments of the operation should be SIMD_type
	'''
	(varTable, newLineCount, newTestingStr) = ParseTestingStr(testingRepr)
	(opClassType, opName) = TesterUtility.ParseOp(operation.fullName)
	
	#prepare for the variable definition part
	variable_init = ""
	for var in varTable:
		if varTable[var] == 1:
			variable_init += "SIMD_type " + var + " = LoadfromInt(rand(), 1);\n"
	for var in varTable:
		if varTable[var] == 0:
			variable_init += "SIMD_type " + var + ";\n"
	
	#prepare for the operation list which is used for testing performance
	operation_list = ""
	for i in range(repeatTime):
		if operation.opPattern == 0:
		#class<fw>::op(...)
			operation_list += newTestingStr.replace("$simd_op$", opClassType + "<" + str(operation.fieldWidth) + ">" + "::" + opName)
		elif operation.opPattern == 1:
		#class<fw>::op<constant>(...)
			#print operation.fullName, operation.fieldWidth
			constantVals = []
			for key in operation.valueRange:
				constantVals = TesterUtility.GetRandomNums(operation.valueRange[key]["min"], operation.valueRange[key]["max"], newLineCount)
				#only one constant for an operation
				break
			testingStrTmp = newTestingStr
			#print "newlinecount=", newLineCount, "constantvals=", constantVals, "testingStr=", newTestingStr
			for i in range(newLineCount):
				sPos = testingStrTmp.find("$simd_op$")
				ePos = sPos + len("$simd_op$")
				testingStrTmp = testingStrTmp[0:sPos] + opClassType + "<" + str(operation.fieldWidth) + ">" + "::" + opName + "<" + str(constantVals[i]) + ">" + testingStrTmp[ePos:]
			operation_list += testingStrTmp
	
	#the operation count of the operation_list
	opCount = str(newLineCount*repeatTime)
	
	#output all used variables in order to enforce gcc not to optimize out some codes
	write_variable = ""
	for var in varTable:
		write_variable += "fout << Store2String(" + var + ", 1) << std::endl;\n"
	
	#finalize the cpp text
	cppText = commonText.replace("$global_variable$", "")
	cppText = cppText.replace("$op$", operation.fullName + "_" + str(operation.fieldWidth))
	cppText = cppText.replace("$variable_init$", variable_init)
	cppText = cppText.replace("$testCase$", str(testCases))
	cppText = cppText.replace("$operation_list$", operation_list)
	cppText = cppText.replace("$opCount$", opCount)
	cppText = cppText.replace("$write_variable$", write_variable)
	
	return cppText

def GetGccCommand(cmd, arch, des, src):
	cmd = cmd.replace("$des$", des).replace("$src$", src)
	if arch == configure.SSE2:
		return cmd.replace("$arch$", "-msse2")
	else:
		print "It doesn't support this architecture " + arch
		sys.exit()

def WriteAndTest(operation, cppText):
	cppSrcFile = outputDir + operation.fullName + "_" + str(operation.fieldWidth) + "_" + "test.cpp"
	cppDesFile = outputDir + operation.fullName + "_" + str(operation.fieldWidth) + "_" + "test"
	fout = open(cppSrcFile, "w")
	fout.write(cppText)
	fout.close()

	if os.system(GetGccCommand(gccCommand, operation.arch, cppDesFile, cppSrcFile)) != 0:
		print "gcc can't compile this cpp file!"
		return -1
	
	if os.system(GetGccCommand(gccAssemblyCommand, operation.arch, "", cppSrcFile)) != 0:
		print "gcc can't generate the assembly codes!"
		return -1
	else:
		os.system("mv " + operation.fullName + "_" + str(operation.fieldWidth) + "_" + "test.s" + " perf_out/")
	
	if os.system("." + "/perf_out/" + operation.fullName + "_" + str(operation.fieldWidth) + "_" + "test") != 0:
		print "error occured when executing " + op
	else:
		fin = open("test.out", "r")
		cycInfo = fin.readline()
		fin.close()
		return float(cycInfo)
	return -1

definedOperations = {}
validOperations = {}

def Init(arch):
	global definedOperations, validOperations
	definedOperations = Operation.LoadDefinedOperations(configure.AllOperations, arch)
	validOperations = ParseIdisaDB.Parse("idisa_" + arch.lower() + ".db")

def LogicOperationPerfTest(operation):
	print "We don't test performance for logic operation " + str(operation.fullName) + " at this moment!"
	return -1

def NormalOperationPerfTest(operation):
	numOfArgs = len(operation.arguments)
	cppText = ""
	
	if numOfArgs == 0:
		print "This operation " + operation.fullName + " is supposed to be a compile-time constant."
		return 0
	elif numOfArgs == 1:
		cppText = PackAnOperation(oneOperandTestingRepr, operation)
	elif numOfArgs == 2:
		cppText = PackAnOperation(twoOperandTestingRepr, operation)
	elif numOfArgs == 3:
		cppText = PackAnOperation(threeOperandTestingRepr, operation)
	else:
		print "We can't support an operation with more than 3 arguments."
		return -1

	cycInfo = WriteAndTest(operation, cppText)
	return cycInfo

def PackAnOperationWithAllSameTypeOfArguments(numOfArgs, operation):
	global_variable = "static " + str(operation.arguments[0].type) + " data[" + str(numOfArgs*repeatTime) + "]" + ";\n"
	
	(opClassType, opName) = TesterUtility.ParseOp(operation.fullName)
	
	variable_init = ""
	if "int" in operation.arguments[0].type:
		for key in operation.valueRange:
			variable_init += "GetRandomNums(" + str(operation.valueRange[key]["min"]) + ", " + str(operation.valueRange[key]["max"]) + ", " + "data" + ", " + str(numOfArgs*repeatTime) + ")" + ";\n"
			break
	elif "SIMD_type" in operation.arguments[0].type:
		variable_init += "GetRandomSIMD_typeNums(data" + ", " + str(numOfArgs*repeatTime) + ", " + str(TesterUtility.GetOptId(operation.arch)) + ")" + ";\n"
	variable_init += ("int" if operation.returnType=="bool" else operation.returnType) + " s;"
		
	k = 0
	operation_list = ""
	for i in range(repeatTime):
		operation_list += "s = " + opClassType + ("<" + str(operation.fieldWidth) + ">" if operation.opPattern == 0 else "") + "::" + opName
		operation_list += "("
		for j in range(numOfArgs):
			operation_list += "data[" + str(k) + "]" + ","
			k += 1
		operation_list = operation_list[:-1]
		operation_list += ")" + ";" + '''asm volatile("" : "=x"(s) : "0"(s));''' + "\n"
	
	opCount = str(repeatTime)
	
	write_variable = ""
	if operation.returnType == "SIMD_type":
		write_variable = "fout << Store2String(s, 1) << std::endl;\n"
	else:
		write_variable = "fout << s << std::endl;\n"
	
	#finalize the cpp text
	cppText = commonText.replace("$global_variable$", global_variable)
	cppText = cppText.replace("$op$", operation.fullName + "_" + str(operation.fieldWidth))
	cppText = cppText.replace("$variable_init$", variable_init)
	cppText = cppText.replace("$testCase$", str(testCases))
	cppText = cppText.replace("$operation_list$", operation_list)
	cppText = cppText.replace("$opCount$", opCount)
	cppText = cppText.replace("$write_variable$", write_variable)
	
	return cppText
	
def OperationWithAllSameTypeOfArgumentsPerfTest(operation):
	numOfArgs = len(operation.arguments)
	cppText = PackAnOperationWithAllSameTypeOfArguments(numOfArgs, operation)
	
	cycInfo = WriteAndTest(operation, cppText)
	return cycInfo
	
def IsNormalOperation(operation):
	for arg in operation.arguments:
		if "SIMD_type" not in arg.type:
			return False
	if "SIMD_type" not in operation.returnType:
		return False
	return True

def IsOperationWithAllSameTypeOfArugments(operation):
	numOfArgs = len(operation.arguments)
	if numOfArgs <= 0:
		return True
	argType = operation.arguments[0].type
	for arg in operation.arguments:
		if argType != arg.type:
			return False
	return True

def WriteResults2Table(arch, cycInfo, validOperations):
	fOut = open("cycInfo.ods", "w")
	regSize = configure.RegisterSize[arch]
	fws = [1]
	while fws[-1] < regSize:
		fws.append(fws[-1]*2)
	
	fOut.write("\t")
	for fw in fws:
		fOut.write(str(fw) + "\t")
	fOut.write("\n")
	
	for op in cycInfo:
		fOut.write(op+" estimated "+"\t")
		for fw in fws:
			for vOp in validOperations[op]:
				if str(fw) == str(vOp.fw):
					fOut.write(str(vOp.cost))
					break
			fOut.write("\t")
		fOut.write("\n")
		fOut.write(op+"\t")
		for fw in fws:
			if fw in cycInfo[op]:
				fOut.write(str(cycInfo[op][fw]) + "\t")
			else:
				fOut.write("-1" + "\t")
		fOut.write("\n")
	fOut.close()

if __name__ == "__main__":
	Init(configure.SSE2)
	
	#validOperations = {"bitblock_any":[ParseIdisaDB.ValidOperation("bitblock_any", 128)], "bitblock_all":[ParseIdisaDB.ValidOperation("bitblock_all", 128)], "mvmd_fill4":[ParseIdisaDB.ValidOperation("mvmd_fill4", 32)]}
	
	cycInfo = {}
	for op in validOperations:
		for vOperation in validOperations[op]:
			fw = vOperation.fw
			operation = definedOperations[op][fw]
			cyc = 0
			print operation.fullName + "_" + str(operation.fieldWidth)
			if operation.opPattern == 2:
				#operation is a logic operation
				cyc = LogicOperationPerfTest(operation)
			elif IsNormalOperation(operation) == True:
				#operation is a normal operation
				cyc = NormalOperationPerfTest(operation)
				#cycInfo[operation.fullName + "_" + str(operation.fieldWidth)] = cyc
			elif IsOperationWithAllSameTypeOfArugments(operation) == True:
				#basically, these operations are mvmd_fill operations
				cyc = OperationWithAllSameTypeOfArgumentsPerfTest(operation)
				#cycInfo[operation.fullName + "_" + str(operation.fieldWidth)] = cyc
			else:
				#other types of operations
				print "other types of operations"
			
			if operation.fullName not in cycInfo:
				cycInfo[operation.fullName] = {operation.fieldWidth:cyc}
			else:
				cycInfo[operation.fullName][operation.fieldWidth] = cyc
			print "cyc=", cyc
	
	fout = open("cycle_info.out", "w")
	for op in cycInfo:
		for fw in cycInfo[op]:
			fout.write(op + "_" + str(fw) + "\t" + str(cycInfo[op][fw]) + "\n")
	fout.close()
	
	WriteResults2Table(configure.SSE2, cycInfo, validOperations)
