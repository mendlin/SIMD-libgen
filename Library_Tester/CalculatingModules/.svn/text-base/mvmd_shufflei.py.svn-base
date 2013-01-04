
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import math

def GetResult(fw, m, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	
	#print "at shufflei", fw, m, data
	blockNum = int(sz/fw)
	maskBlockSz = int(math.log(blockNum, 2))
	mask = (1<<maskBlockSz)-1
	
	
	while i<blockNum:
		val = mask & (m>>((blockNum-i-1)*maskBlockSz))
		ans += arg1[(blockNum-val-1)*fw:(blockNum-val)*fw]
		i += 1
	
	return ans
