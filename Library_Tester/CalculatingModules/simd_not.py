
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, data):
	arg1 = data[0]
	(i, sz, ans) = (0, len(arg1), "")
	#print fw, data
	while i<sz:
		for j in range(fw):
			curPos = i+j
			#print "curPos = ", curPos
			if(arg1[curPos]=="1"):
				ans += "0"
			else:
				ans += "1"
		i += fw
	return ans
