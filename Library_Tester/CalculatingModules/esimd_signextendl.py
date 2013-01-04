
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	
	i = int(sz/2)
	while i<sz:
		ans += "0"*fw if arg1[i]=="0" else "1"*fw
		ans += arg1[i:i+fw]
		i += fw
	return ans
