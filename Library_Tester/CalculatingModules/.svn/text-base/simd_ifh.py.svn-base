
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	(mask, arg1, arg2) = (data[0], data[1], data[2])
	(i, sz, ans) = (0, len(arg1), "")
	while i<sz:
		selArg = arg1 if mask[i]=="1" else arg2
		for j in range(fw):
			ans += selArg[i+j]
		i += fw
	return ans
