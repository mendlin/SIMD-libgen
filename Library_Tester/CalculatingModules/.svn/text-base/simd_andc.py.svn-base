
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_not
import simd_and

def GetResult(fw, data):
    (arg1, arg2) = (data[0], data[1])
    
    data = [arg1, simd_not.GetResult(fw, [arg2])]
    
    return simd_and.GetResult(fw, data)
