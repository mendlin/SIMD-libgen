
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_slli

def GetResult(data):
    (arg1, count) = (data[0], data[1])
    (i, regSize, ans) = (0, len(arg1), "")
    
    while i<regSize:
        sh = int(count[i:i+regSize], 2) if regSize<=32 else int(count[i+regSize-32:i+regSize], 2)
	sh &= regSize -1
        ans += simd_slli.GetResult(regSize, sh, [arg1[i:i+regSize]])
        i += regSize
    
    return ans
