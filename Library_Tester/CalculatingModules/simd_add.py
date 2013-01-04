
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	while i<sz:
		tmpAns = ""
		carry = 0
		for j in range(i+fw-1, i-1, -1):
			tmp = int(arg1[j]) + int(arg2[j]) + carry
			tmpAns = str(tmp%2) + tmpAns
			carry = int(tmp/2)
		i += fw
		ans += tmpAns
	return ans
