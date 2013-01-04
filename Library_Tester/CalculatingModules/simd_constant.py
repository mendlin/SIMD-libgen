
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import utility

def GetResult(fw, val, regSize):
	(i, sz, ans) = (0, regSize, "")
	block = utility.GetBinaryRepresentation(fw, val)
	while i<sz:
		ans += block
		i += fw
	return ans
