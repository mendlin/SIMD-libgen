
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_slli

def GetResult(sh, data):
    arg1, regSize = data[0], len(data[0])
    return simd_slli.GetResult(regSize, sh, [arg1])