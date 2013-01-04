
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_lt
import simd_ifh

def GetResult(fw, data):
	ltAns = simd_lt.GetResult(fw, data)
	return simd_ifh.GetResult(1, [ltAns, data[0], data[1]])
