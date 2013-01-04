
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(data):
	arg1 = data[0]
	for bit in arg1:
		if bit == '1':
			return 1
	return 0
