
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import utility

def GetResult(fw, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	while i<sz:
		tmp = abs(utility.TwosComplement(fw, arg1[i:i+fw]))
		ans += utility.GetBinaryRepresentation(fw, tmp)
		i += fw
	return ans
	
