
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	while i<sz:
		tmpAns = ""
		borrow = 0
		for j in range(i+fw-1, i-1, -1):
			tmp = int(arg1[j]) - int(arg2[j]) - borrow
			tmpAns = str((tmp+2)%2) + tmpAns
			borrow = 1 if tmp<0 else 0
		i += fw
		ans += tmpAns
	return ans
