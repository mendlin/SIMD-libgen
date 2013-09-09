
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_slli

def GetResult(fw, data):
	(arg1, count) = (data[0], data[1])
	return simd_slli.GetResult(fw, int(count[-32:], 2), [arg1])