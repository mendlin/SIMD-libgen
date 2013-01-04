
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_gt
import simd_ifh

def GetResult(fw, data):
	gtAns = simd_gt.GetResult(fw, data)
	return simd_ifh.GetResult(1, [gtAns, data[0], data[1]])
