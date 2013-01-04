
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	halfFw = int(fw/2)

	i = halfFw
	#pack the data from low fw/2 part of each fw field in arg1
	while i<sz:
		for j in range(halfFw):
			ans += arg1[i+j]
		i += fw
	#pack the data from high fw/2 part of each fw field in arg2
	i = halfFw
	while i<sz:
		for j in range(halfFw):
			ans += arg2[i+j]
		i += fw
	return ans
