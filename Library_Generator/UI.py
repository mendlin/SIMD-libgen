
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import sys
import copy
import os

import Utility
import Operation
import OperationSetAnalyzer
from Utility import configure

#from OperationSet import neededOps, neededFws, logicOps

def GetArchLang(args):
	uiInput = UiInput(args)
	return (uiInput.arch, uiInput.lang)

def WriteCodes(operationSetResult, arch, lang, outfile, whichContent):
	UiOutput(operationSetResult, arch, lang, outfile, whichContent)

def WriteStrategyCount(arch, strategyCount):
	fileOut = open(arch+"_strategy_count.ods", "w")
	fileOut.write("name")
	validFws = Utility.GetValidFieldWidth(configure.RegisterSize[arch])
	for fw in validFws:
		fileOut.write("\t" + str(fw))
	fileOut.write("\n")
	
	maxCt = 0
	
	for op in strategyCount:
		fileOut.write(op)
		for fw in validFws:
			fileOut.write("\t" + str(strategyCount[op][fw]))
			if strategyCount[op][fw] > maxCt:
				maxCt = strategyCount[op][fw]
		fileOut.write("\n")
	fileOut.write("max strategy count=" + str(maxCt) + "\n")
	fileOut.close()

def WriteStrategyComparisonInfo(operationSetResult, operationSet, arch, lang):
	fileOut = open(arch+"_strategy_cost.ods", "w")
	fileOut.write("name")
	validFws = Utility.GetValidFieldWidth(configure.RegisterSize[arch])
	for fw in validFws:
		fileOut.write("\t" + str(fw))
	fileOut.write("\n")
	
	(bestOpCount, bestOpCodes, maxCount) = (operationSetResult.optOpCount, operationSetResult.optOpCodes, operationSetResult.opMaxCount)
	
	#(bestOpCount, secBestOpCount, bestOpCodes, secBestOpCodes, tmpSecOptOpCount, maxCount) = (operationSetResult.optOpCount, operationSetResult.secOptOpCount, operationSetResult.optOpCodes, operationSetResult.secOptOpCodes, operationSetResult.tmpSecOptOpCount, operationSetResult.opMaxCount)
	for opName in Utility.definedOperations:
		fileOut.write(opName)
		for fw in validFws:
			fileOut.write("\t")
			op_fw = opName + "_" + str(fw)
			tmpAnalysisResult = OperationSetAnalyzer.AnalyzeSecBest(operationSet, op_fw)
			(secBestOpCount, secBestOpCodes, tmpSecOptOpCount) = (tmpAnalysisResult.secOptOpCount, tmpAnalysisResult.secOptOpCodes, tmpAnalysisResult.tmpSecOptOpCount)
			if op_fw in bestOpCount:
				fileOut.write(str(bestOpCount[op_fw]) + ", ")
			else:
				fileOut.write("N/A" + ", ")
			if op_fw in secBestOpCount:
				if secBestOpCount[op_fw] >= maxCount and tmpSecOptOpCount[op_fw] < maxCount:
					fileOut.write("SAME")
				else:
					fileOut.write(str(secBestOpCount[op_fw]))
			else:
				fileOut.write("N/A")
		fileOut.write("\n")
	fileOut.close()

	for opName in Utility.definedOperations:
		for fw in validFws:
			op_fw = opName + "_" + str(fw)
			tmpAnalysisResult = OperationSetAnalyzer.AnalyzeSecBest(operationSet, op_fw)
			(secBestOpCount, secBestOpCodes) = (tmpAnalysisResult.secOptOpCount, tmpAnalysisResult.secOptOpCodes)
			#tmpOperationSetResult = copy.deepcopy(operationSetResult)
			tmpAnalysisResult.optOpCount[op_fw] = secBestOpCount[op_fw]
			tmpAnalysisResult.optOpCodes[op_fw] = secBestOpCodes[op_fw]
			fileOutDir = os.getcwd() + "/tmp/" + arch + "/" 
			UiOutput(tmpAnalysisResult, arch, lang, fileOutDir + opName + "_" + str(fw) + ".h", "all")
			#os.system("rm " + fileOutDir + "*.db")
			#print "finished writing " + os.getcwd()+"/tmp/"+opName+"_"+str(fw)+".h"

class UiOutput:
	def __init__(self, operationSetResult, arch, lang, outfile, whichContent):
		
		if lang == configure.Language_C:
			self.WriteCCodes(operationSetResult, arch, lang, outfile, whichContent)
			self.WriteValidOperations(operationSetResult, arch, outfile)
		elif lang == configure.Language_CPP:
			self.WriteCodes(operationSetResult, arch, lang, outfile, whichContent)
			self.WriteValidOperations(operationSetResult, arch, outfile)
		
	def PreliminaryCodes(self, arch, lang, outfile, whichContent):
		codes = configure.cppCopyrightNotice
		if lang == configure.Language_C:
			codes += "#ifndef " + "_IDISA_" + arch.upper() + "_" + "C" + "_" + "H" + "\n"
			codes += "#define " + "_IDISA_" + arch.upper() + "_" + "C" + "_" + "H" + "\n"
			codes += '''#include "''' + configure.InstructionSetLibrary[arch] + '''"\n\n'''
			codes += "#include <stdint.h>\n"
			codes += "typedef " + configure.SIMD_type[arch] + " " + configure.Bitblock_type[arch] + ";\n"
			
		elif lang == configure.Language_CPP:
			#codes += "#ifndef " + "_IDISA_" + arch.upper() + "_" + "H" + "\n"
			codes += "#ifndef " + outfile.replace(".", "_").replace("/", "_").upper() + "\n"
			#codes += "#define " + "_IDISA_" + arch.upper() + "_" + "H" + "\n"
			codes += "#define " + outfile.replace(".", "_").replace("/", "_").upper() + "\n"

			
			if whichContent == configure.Body_Declaration:
				codes += configure.Macro_Idisa128_Hpp if "idisa128" in outfile.lower() else (configure.Macro_Idisa256_Hpp if "idisa256" in outfile.lower() else configure.Macro_Idisa_Hpp)
			elif whichContent == configure.Body_Implementation:
				codes += "#include <stdint.h>\n#include \"../config.hpp\"\n\n"
				codes += '''#include "''' + configure.InstructionSetLibrary[arch] + '''"\n\n'''
				if configure.ExtraImports.has_key(arch):
					for imp in configure.ExtraImports[arch]:
						codes += '''#include "''' + imp + '''"\n\n'''
				codes += "typedef " + configure.SIMD_type[arch] + " " + configure.Bitblock_type[arch] + ";\n"
			else:
				codes += "#include <stdint.h>\n"
				codes += '''#include "''' + configure.InstructionSetLibrary[arch] + '''"\n'''
				codes += "typedef " + configure.SIMD_type[arch] + " " + configure.Bitblock_type[arch] + ";\n"

			codes += \
"""			
template <uint32_t fw> struct FieldType {
   typedef int T;  //default for FieldType::T is int
};

template <> struct FieldType<1> {typedef uint8_t T;};
template <> struct FieldType<2> {typedef uint8_t T;};
template <> struct FieldType<4> {typedef uint8_t T;};
template <> struct FieldType<8> {typedef uint8_t T;};
template <> struct FieldType<16> {typedef uint16_t T;};
template <> struct FieldType<32> {typedef uint32_t T;};
template <> struct FieldType<64> {typedef uint64_t T;};
template <> struct FieldType<128> {typedef uint64_t T;};

"""
		else:
			pass
		return codes
	
	def FunctionDefinitions(self, optOpCodes, optOpNum, opMaxNum):
		functionDef = ""
		for op in neededOps:
			for fw in neededFws:
				op_fw = str(op) + "_" + str(fw)
				if op_fw in optOpNum and optOpNum[op_fw] < opMaxNum:
					if op_fw in optOpCodes:
						curCodes = optOpCodes[op_fw]
						functionDef += curCodes[:curCodes.find("\n")] + ";\n"
		return functionDef

	def WriteCodes(self, operationSetResult, arch, lang, outfile, whichContent):
		allClasses = ["simd", "hsimd", "esimd", "mvmd", "bitblock"]
		operationImp = {}
		operationDecla = {}
		
		#Output the header file
		#fileOut = open("idisa"+'_'+arch.lower()+'.h', 'w')
		fileOut = open(outfile, 'w')
		
		(optOpCount, optOpCodes, opMaxCount) = (operationSetResult.optOpCount, operationSetResult.optOpCodes, operationSetResult.opMaxCount)
		fileOut.write(self.PreliminaryCodes(arch, lang, outfile, whichContent))		

		for classType in allClasses:
			if whichContent == configure.Body_All:
				curClass = Utility.LibClass(classType, [], False if classType=="bitblock" else True)
			else:
				curClass = Utility.LibClass(classType, [], False if classType=="bitblock" else True, arch)
			operationImp[classType] = {}
			operationDecla[classType] = {}
			for opName in Utility.definedOperations:
				operationImp[classType][opName] = []
				operationDecla[classType][opName] = []
				
				operationTmp = Utility.definedOperations[opName][1]
				
				if operationTmp.classType == classType:
					#curClass.Append( Utility.LibFunction(operationTmp) )
					opSignatures = {}
					for fw in Utility.GetValidFieldWidth(configure.RegisterSize[arch]):
						operation = Utility.definedOperations[opName][fw]
						if optOpCount[operation.fullName + "_" + str(fw)] < opMaxCount:
							curOperation = Utility.LibFunction(operation, optOpCount[operation.fullName + "_" + str(fw)], optOpCodes[operation.fullName + "_" + str(fw)])
							curSignature = curOperation.ClassDeclarationToCppText()
							if curSignature not in opSignatures:
								opSignatures[curSignature] = True
								curClass.Append(curOperation)
							#curOperation.SetBodyContent(optOpCodes[operation.fullName + "_" + str(fw)])
							operationImp[classType][operation.fullName].append(curOperation.ToCppText())
							operationDecla[classType][operation.fullName].append(curOperation.FunctionDeclarationToCppText())
			
			if whichContent != configure.Body_Declaration:		
				fileOut.write(curClass.ToCppText())
		
		if whichContent != configure.Body_Declaration: 
			fileOut.write("//Declaration Part" + "\n")
		
			for opName in Utility.definedOperations:
				operationTmp = Utility.definedOperations[opName][1]
				if operationTmp.classType == "":
					#logic operations
					curOperation = Utility.LibFunction(operationTmp)
					if optOpCount[operationTmp.fullName + "_" + str(1)] < opMaxCount:
						fileOut.write(curOperation.FunctionDeclarationToCppText() + ";\n")
				
			for classType in allClasses:
				if classType == "bitblock":
					continue
				for op in operationDecla[classType]:
					for decla in operationDecla[classType][op]:
						fileOut.write(decla + ";\n")
			fileOut.write("\n")
		
		if whichContent != configure.Body_Declaration:
			fileOut.write("//Implementation Part" + "\n")
			#write pre-defined functions first
			for func in Utility.usedFunctionSupport:
				fileOut.write(Utility.functionSupport[func]["body"] + "\n")
		
			for opName in Utility.definedOperations:
				operationTmp = Utility.definedOperations[opName][1]
				if operationTmp.classType == "" and optOpCount[operationTmp.fullName + "_" + str(1)] < opMaxCount:
					#logic operations
					curOperation = Utility.LibFunction(operationTmp, optOpCount[operationTmp.fullName + "_" + str(1)], optOpCodes[operationTmp.fullName + "_" + str(1)])
					fileOut.write(curOperation.ToCppText() + "\n")
				
			for classType in allClasses:
				for op in operationImp[classType]:
					for imp in operationImp[classType][op]:
						fileOut.write(imp + "\n")
		
		fileOut.write("#endif\n")			
		fileOut.close()
		
		#Output the cpp file
		#fileOut = open(arch+"_"+lang+".cpp", "w")
		#fileOut.write('''#include "''' + arch+"_"+lang+".h" + '''"\n\n''')
		#for classType in allClasses:
		#	for op in operationImp[classType]:
		#		for imp in operationImp[classType][op]:
		#			fileOut.write(imp)
		#fileOut.close()
	
	def WriteValidOperations(self, operationSetResult, arch, outfile):
		#fileOut = open("idisa"+"_"+arch.lower()+".db", 'w')
		if ".hpp" in outfile:
			fileOut = open(outfile.replace(".hpp", ".db"), 'w')
		elif ".cpp" in outfile:
			fileOut = open(outfile.replace(".cpp", ".db"), 'w')
		else:
			fileOut = open(outfile.replace(".h", ".db"), 'w')		

		(optOpCount, opMaxCount) = (operationSetResult.optOpCount, operationSetResult.opMaxCount)
		opNameFilter = ["bitblock_load_aligned", "bitblock_load_unaligned", "bitblock_store_aligned", "bitblock_store_unaligned"]
		
		for opName in Utility.definedOperations:
			if opName in opNameFilter:
				continue
			thisOpName = ""
			thisOpFws = []
			thisOpCosts = []
			for fw in Utility.GetValidFieldWidth(configure.RegisterSize[arch]):
				operation = Utility.definedOperations[opName][fw]
				if optOpCount[operation.fullName + "_" + str(fw)] < opMaxCount:
					thisOpName = operation.fullName
					thisOpFws.append(fw)
					thisOpCosts.append(optOpCount[operation.fullName + "_" + str(fw)])
			
			if thisOpName != "" :
				fileOut.write(thisOpName+":\n")
				fileOut.write("fw=")
				for fw in thisOpFws:
					fileOut.write(str(fw) + " ")
				fileOut.write("\n")
				fileOut.write("cost=")
				for cost in thisOpCosts:
					fileOut.write(str(cost) + " ")
				fileOut.write("\n")

		fileOut.close()
	
	def WriteCCodes(self, operationSetResult, arch, lang, outfile, whichContent):			
		fileOut = open(outfile, "w")
		(optOpCount, optOpCodes, opMaxCount) = (operationSetResult.optOpCount, operationSetResult.optOpCodes, operationSetResult.opMaxCount)
		
		#oper = Utility.definedOperations["simd_add_8"]
		#print oper.CallingStatementToCText(8, oper.arguments, oper.):
		fileOut.write(self.PreliminaryCodes(arch, lang, outfile, whichContent))
		
		for func in Utility.usedFunctionSupport:
			fileOut.write(Utility.functionSupport[func]["body"] + "\n")

		fileOut.write("\n")
		fileOut.write("//Declaration Starts here\n");
		for op in Utility.definedOperations:
			for fw in Utility.definedOperations[op]:
				opr = Utility.definedOperations[op][fw]
				if optOpCount[op+"_"+str(fw)] < opMaxCount:					
					if (opr.opPattern == 1 or opr.opPattern == 4) and optOpCodes[op+"_"+str(fw)].count("\n") <= 1:
						libF = Utility.LibFunction(opr, optOpCount[op+"_"+str(fw)], optOpCodes[op+"_"+str(fw)])
						fileOut.write(libF.ToCMacro() + "\n")
					else:
						libF = Utility.LibFunction(opr, 0, optOpCodes[op+"_"+str(fw)])
						fileOut.write(libF.FunctionDeclarationToCText() + ";\n")

		fileOut.write("\n//Implementation Starts here\n");
		for op in Utility.definedOperations:
			for fw in Utility.definedOperations[op]:
				opr = Utility.definedOperations[op][fw]
				if optOpCount[op+"_"+str(fw)] < opMaxCount:
					if (opr.opPattern == 1 or opr.opPattern == 4) and optOpCodes[op+"_"+str(fw)].count("\n") <= 1:
						continue
					libF = Utility.LibFunction(opr, optOpCount[op+"_"+str(fw)], optOpCodes[op+"_"+str(fw)])
					fileOut.write(libF.ToCText())
		
		# for op in Utility.definedOperations:
		# 	for fw in Utility.definedOperations[op]:
		# 		opr = Utility.definedOperations[op][fw]
		# 		if optOpCount[op+"_"+str(fw)] < opMaxCount and optOpCodes[op+"_"+str(fw)].count("\n")>1:
		# 			libF = Utility.LibFunction(opr, optOpCount[op+"_"+str(fw)], optOpCodes[op+"_"+str(fw)])
		# 			fileOut.write(libF.ToCText())
		
		#opr = Utility.definedOperations["simd_add"][128]
		#libF = Utility.LibFunction(opr, 0, optOpCodes["simd_add_128"])
		#print libF.ToCText()
		
		fileOut.write("#endif\n")
		fileOut.close()
