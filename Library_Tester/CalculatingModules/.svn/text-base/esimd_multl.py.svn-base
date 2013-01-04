
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import utility

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	i = int(sz/2)
	while i<sz:
		tmpMult = utility.TwosComplement(fw, arg1[i:i+fw]) * utility.TwosComplement(fw, arg2[i:i+fw])
		#print tmpMult
		tmpMult = utility.GetBinaryRepresentation(2*fw+1, tmpMult)
		ans += tmpMult[-2*fw:]
		i += fw
	return ans
