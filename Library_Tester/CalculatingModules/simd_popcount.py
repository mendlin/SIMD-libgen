
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import utility

def GetResult(fw, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	
	while i<sz:
		ct = 0
		for j in range(fw):
			ct += 1 if arg1[i+j]=="1" else 0
		ans += utility.GetBinaryRepresentation(fw, ct)
		i += fw
	
	return ans
