
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_srli
import simd_and
import simd_sub

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[0])
	(i, sz, ans) = (0, len(arg1), "")
	
	halfFw = int(fw/2)
	arg1 = simd_srli.GetResult(fw, halfFw, [arg1])		
	
	mask = ("0"*halfFw + "1"*halfFw) * int(sz/fw)
	
	arg2 = simd_and.GetResult(fw, [arg2, mask])
	ans = simd_sub.GetResult(fw, [arg1, arg2])
	return ans
