
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import hsimd_packl
import hsimd_packh
import simd_umin

def GetResult(fw, data):
	(arg1, arg2) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	
	arg11 = hsimd_packh.GetResult(fw, [arg1, arg2])
	arg22 = hsimd_packl.GetResult(fw, [arg1, arg2])
	
	ans = simd_umin.GetResult(fw/2, [arg11, arg22])
	return ans
