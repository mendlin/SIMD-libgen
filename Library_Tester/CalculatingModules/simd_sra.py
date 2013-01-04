
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_srai

def GetResult(fw, data):
	(arg1, count) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	count = int(count[-32:], 2)
	ans = simd_srai.GetResult(fw, count, [arg1])
	return ans
