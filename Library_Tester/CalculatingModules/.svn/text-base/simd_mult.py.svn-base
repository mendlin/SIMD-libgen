
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import utility

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	while i<sz:
		tmpMult = utility.TwosComplement(fw, arg1[i:i+fw]) * utility.TwosComplement(fw, arg2[i:i+fw])
		#print tmpMult
		tmpMult = utility.GetBinaryRepresentation(2*fw+1, tmpMult)
		ans += tmpMult[-fw:]
		i += fw
	return ans

'''
if __name__ == "__main__":
	a = "11010101"
	b = "00110111"
	
	c = GetResult(4, [a, b])
	
	print utility.TwosComplement(8, c)
	
	print c
'''
