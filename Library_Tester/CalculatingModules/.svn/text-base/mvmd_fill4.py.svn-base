
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import utility

def GetResult(fw, data, regSize):
	(i, sz, ans) = (0, regSize, "")

	j = 0
	while i<sz:
		ans += utility.GetBinaryRepresentation(fw, data[j])
		j = (j+1)%4
		i += fw
	
	return ans
