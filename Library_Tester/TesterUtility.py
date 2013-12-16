
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import random
import os
import sys

os.chdir(sys.path[0])
#import the configure module
sys.path.append("../Configure/")
import configure
import OptParser

#import the Operation module from Library Generator
sys.path.append("../Library_Generator/")
import Operation

#This is the dictionary for storing testing data
#"class_op_fw" : [test0, test1, ...]
#testingData = {}

def GetArgsText(oprdNum):
	txt = "("
	for i in range(oprdNum):
		txt += "arg" + str(i)
		txt += ", " if i < oprdNum-1 else ""
	txt += ")"
	return txt

def GetOptId(arch):
	arch = arch.lower()
	if "mmx" in arch:
		return 0
	elif "sse" in arch:
		return 1
	elif "avx" in arch:
		return 2
	elif "neon" in arch:
		return 3
	elif "llvm128" in arch:
		return 1

	print "WARNING: GetOptId, arch not recognized"
	return -1

def GetRandomNums(low, up, ct):
	ret = []
	for i in range(ct):
		ret.append(random.randint(low, up))
	return ret

def ParseOp(op):
	dashPos = op.find("_")
	return (op[0:dashPos], op[dashPos+1:])
