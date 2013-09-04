
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0.

import sys

import UI
import Utility
from Utility import configure, OptParser
import Operation
import Strategy
from BuiltIns import BuiltIns
import OperationSet
import OperationSetAnalyzer

import ipdb

def operationInfo(definedOperations):
	# All options have full powers of 2 as field width
	ref_keys = [1, 2, 4, 8, 16, 32, 64, 128, 256]
	generators = ["SIMDBuiltinGenerator", "SIMDConstantBuiltinGenerator", "SIMDLogicBuiltinGenerator", "SIMDBitblockBuiltinGenerator", "SIMDBitblockImmediateBuiltinGenerator"]	
	return_type = {"bool": "BOOL", "uint64_t": "BITFIELD", "bitblock128_t": "BITBLOCK", "void": "VOID"}
	for op_key in sorted(definedOperations):
		op_val = definedOperations[op_key]
		op_detail = op_val.values()[0]
		op_pattern = op_detail.opPattern
		op_generator = generators[op_pattern]
		op_upperBound = "BITBLOCK_SIZE"	

		if op_pattern == 4:
			print op_key.upper(), "(makeAllSimpleSignatures(" + op_upperBound + ", new " + op_generator + "(), ",						
			print len(op_detail.arguments) * "BITBLOCK, ",			
			# print return_type[op_detail.returnType] + ")),"
			# print "args:"
			# for arg in op_detail.arguments:
			# 	print arg.type, ", ", 
			# print 		

def Init(arch, lang):
	'''Initialization work
	'''
	#Load function support
	Utility.functionSupport = Utility.LoadFunctionSupport(arch, lang)

	#Get all defined operations
	Utility.definedOperations = Operation.LoadDefinedOperations(configure.AllOperations, arch)

	#Get the built-ins given the information of architecture
	Utility.builtIns = BuiltIns(arch)

	#Get the size of current register
	Utility.curRegisterSize = configure.RegisterSize[arch]

	#Get all strategies
	Utility.strategies = Strategy.LoadStrategies(arch)	

def Main(arch, lang, outfile, whichContent, options):

	Init(arch, lang)

	operationSet = OperationSet.LoadOperationSet(arch, lang)

# This is for evaluation
#	if options.strategy_count:
#		strategyCount = OperationSet.LoadStrategyCount(arch, lang)
#		UI.WriteStrategyCount(arch, strategyCount)

	analysisResult = OperationSetAnalyzer.Analyze(operationSet)

# This is for evaluation
#	if options.strategy_comparison:
#		UI.WriteStrategyComparisonInfo(analysisResult, operationSet, arch, lang)

	UI.WriteCodes(analysisResult, arch, lang, outfile, whichContent)

if __name__ == '__main__':

	optParser = OptParser.GetOptParser()
	options, args = optParser.parse_args(sys.argv[1:])

	if options.use_generator:
		Utility.outputOpt = options.body.lower()
		Main(options.arch.upper(), options.lang.upper(), options.idisa_file, options.body.lower(), options)
	else:
		print "idisa doesn't know what to do...[no input]"


