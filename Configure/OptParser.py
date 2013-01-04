
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 


from optparse import OptionParser

def GetOptParser():
	parser = OptionParser()
	
	parser.add_option("-g", "--generator", dest="use_generator", 
						action="store_true", default=False,
						help="generate idisa library for a certain architecture")
	
	parser.add_option("-t", "--tester", dest="use_tester",
						action="store_true", default=False,
						help="test the idisa library")
	
	parser.add_option("-a", "--architecture", dest="arch",
						help="architecture information")
	
	parser.add_option("-l", "--language", dest="lang",
						help="idisa language information")
	
	parser.add_option("-f", "--file", dest="idisa_file",
						help="idisa file information")
	
	parser.add_option("-b", "--body", dest="body", default="all",
						help="which content do you want to output into the idisa file")
	
	parser.add_option("-s", "--strategy_count", dest="strategy_count",
						action="store_true", default=False,
						help="get the strategy count information for each operation")
	
	parser.add_option("-c", "--strategy_comparison", dest="strategy_comparison",
						action="store_true", default=False,
						help="get the strategy comparison information for each operation")
	
	parser.add_option("-i", "--instruction_count", dest="instruction_count",
						action="store_true", default=False,
						help="get the instruction count information for each operation")
	
	parser.add_option("-o", "--test_option", dest="test_option",
						help="options for tester")
	return parser
