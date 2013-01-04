
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import utility

def GetResult(fw, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	
	while i<sz:
		ans += arg1[i]
		i += fw
	ans = ("" if len(ans) >= 64 else "0"*(64-len(ans))) + ans
	#the result should be a 64-bits unsigned integer
	return int(ans, 2)

'''
if __name__ == "__main__":
	
	a = "10100001"
	print GetResult(2, [a])
'''
