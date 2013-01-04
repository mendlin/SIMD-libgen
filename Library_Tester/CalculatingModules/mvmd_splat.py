
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, j, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	
	i = sz - (j+1)*fw
	ans = arg1[i:i+fw] * int(sz/fw)

	return ans
