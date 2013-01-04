
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_slli

def GetResult(fw, data):
	(arg1, count) = (data[0], data[1])
	(i, sz, ans) = (0, len(arg1), "")
	
	while i<sz:
		sh = int(count[i:i+fw], 2) if fw<=32 else int(count[i+fw-32:i+fw], 2)
		sh &= (fw - 1)
		ans += simd_slli.GetResult(fw, sh, [arg1[i:i+fw]])
		i += fw
	
	return ans
