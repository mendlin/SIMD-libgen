
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_ugt
import simd_ifh

def GetResult(fw, data):
	ugtAns = simd_ugt.GetResult(fw, data)
	return simd_ifh.GetResult(1, [ugtAns, data[0], data[1]])
