
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	while i<sz:
		flag = 0
		if arg1[i]=="1" and arg2[i]=="0":
			flag = 1
		elif arg1[i] == arg2[i]:
			for j in range(1, fw):
				if arg1[i+j]=="1" and arg2[i+j]=="0":
					break
				elif arg1[i+j]=="0" and arg2[i+j]=="1":
					flag = 1
					break
		ans += "1"*fw if flag==1 else "0"*fw
		i += fw
	return ans
