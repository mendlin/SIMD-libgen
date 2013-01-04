
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_add

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (fw, len(arg1), "")
	while i<sz:
		tmpMult = int(arg1[i:i+fw], 2) * int(arg2[i:i+fw], 2)
		tmpMult = bin(tmpMult)[2:]
		tmpMultLen = len(tmpMult)
		ans += tmpMult[-2*fw:] if tmpMultLen>=2*fw else "0"*(2*fw-tmpMultLen)+tmpMult
		i += 2*fw
	return ans

