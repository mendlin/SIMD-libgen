
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, sh, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	sh = fw if sh>fw else sh if sh>=0 else 0
	while i<sz:
		ans += sh*arg1[i:i+1] + arg1[i:i+fw-sh]
		i += fw
	return ans
