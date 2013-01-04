
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import math

def GetResult(fw, data):
	(arg1, mask) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	
	blockNum = int(sz/fw)
	maskBlockSz = int(math.log(blockNum, 2))
	while i<sz:
		index = int(mask[i:i+fw][-maskBlockSz:], 2)
		ans += "0"*fw if mask[i]=="1" else \
			   arg1[(blockNum-index-1)*fw:(blockNum-index)*fw]
		i += fw
	
	return ans

'''
if __name__ == "__main__":
	mask = "011011000010"
	arg1 = "110111101100"
	
	print GetResult(3, [arg1, mask])
'''
