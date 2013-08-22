
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	while i<sz:
		flag = 1
		for j in range(fw):
			if arg1[i+j] == "0":
				# all fail
				flag = 0
				break
		ans += "1" * fw if flag == 1 else "0" * fw		
		i += fw
	return ans
