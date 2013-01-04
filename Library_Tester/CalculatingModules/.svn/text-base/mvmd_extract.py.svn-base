
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

def GetResult(fw, pos, data):
    arg1 = data[0]
    (i, sz, ans) = (0, len(arg1), "")
    
    i = sz - (pos+1)*fw
    ans = arg1[-64:i+fw] if fw>64 else arg1[i:i+fw]
    
    return int(ans, 2)