
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, sh, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	
	blockNum = int(sz/fw)
	while i<blockNum:
		ans += arg1[(i-sh)*fw:(i-sh+1)*fw] if (i-sh)>=0 else "0"*fw
		i += 1
	
	return ans
