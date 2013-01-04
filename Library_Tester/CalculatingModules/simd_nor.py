
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_not
import simd_or

def GetResult(fw, data):
	data = [simd_or.GetResult(fw, data)]
	return simd_not.GetResult(fw, data)
