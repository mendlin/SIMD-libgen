# Copyright (c) 2011, Meng Lin, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import utility

def GetResult(fw, pos, data):
	(arg1, arg2) = (data[0], data[1])

	sz = len(arg1)    
	i = sz - (pos+1)*fw    
	
	ans = arg1[0:i] + utility.GetBinaryRepresentation(fw, arg2) + arg1[i+fw:sz]

	return ans