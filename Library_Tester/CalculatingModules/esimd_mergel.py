
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	
	i = int(sz/2)
	while i<sz:
		ans += arg1[i:i+fw] + arg2[i:i+fw]
		i += fw
	
	return ans
