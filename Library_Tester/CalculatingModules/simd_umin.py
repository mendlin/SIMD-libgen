
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_ult
import simd_ifh

def GetResult(fw, data):
	ultAns = simd_ult.GetResult(fw, data)
	return simd_ifh.GetResult(1, [ultAns, data[0], data[1]])
