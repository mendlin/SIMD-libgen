
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_srl

def GetResult(data):
    (arg1, count) = (data[0], data[1])
    (i, regSize, ans) = (0, len(arg1), "")
    
    return simd_srl.GetResult(regSize, data)
