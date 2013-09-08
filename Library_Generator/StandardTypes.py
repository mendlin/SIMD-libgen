
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import sys
import math
from types import *

from Utility import configure

def GetUnsignedIntType(typeStr, regSize, fw="$fw$", truncated=True):
    valStr = typeStr[typeStr.find("(")+1:typeStr.find(")")] 
    if fw != "$fw$" or ("fw" not in valStr):
        val = eval(valStr.replace("fw", str(fw)).replace("curRegSize", str(regSize)))
        assert (val & (val-1)) == 0, "val is not a pow of 2!"
    else:
        val = fw

    if truncated and val != "$fw$":
        if val < 8:
            return "uint8_t"
        elif val > 64:
            return "uint64_t"
    return "uint" + str(val) + "_t"

def GetSignedIntType(typeStr, regSize, fw="$fw$", truncated=True):
    valStr = typeStr[typeStr.find("(")+1:typeStr.find(")")]
    if fw != "$fw$" or ("fw" not in valStr):
        val = eval(valStr.replace("fw", str(fw)).replace("curRegSize", str(regSize)))
        assert (val & (val-1)) == 0, "val is not a pow of 2!"
    else:
        val = fw
    
    if truncated and val != "$fw$":
        if val < 8:
            return "int8_t"
        elif val > 64:
            return "int64_t"
    return "int" + str(val) + "_t"

def Get64BitFloatingType(typeStr, regSize):
    return "__m256d"

def GetAppropriateType(valRange):
    maxVal = valRange[-1]
    if maxVal <= (2**8)-1:
        return "uint8_t"
    elif maxVal <= (2**16)-1:
        return "uint16_t"
    elif maxVal <= (2**32)-1:
        return "uint32_t"
    else:
        return "uint64_t"

def GetAppropriatePythonType(val):
    val = eval(val)
    if -(2**31) <= val and val <= (2**31)-1:
        return IntType
    elif -(2**63) <= val and val <= (2**63)-1:
        return LongType
    return LongType

def GetSIMDPointer(arch):
    return configure.Bitblock_type[arch] + "*"

def GetFloatConstantPointer():
    return "float const*"

def GetFloatPointer():
    return "float*"

def GetLoadType(arch):
    return "const " + configure.Load_type[arch]

def GetStoreType(arch):
    return configure.Store_type[arch]

def GetUInt64ConstantPointer():
    return "uint64_t const*"

def GetUInt64Pointer():
    return "uint64_t*"

def GetSIMDTypeConvert(argType, arch, argument):
    if argType == "SIMD_type":
        return argument

    if configure.SIMD_type[arch] != argType:        
        if arch == "AVX2" and argType == "__m128i" and not "(" in argument:            
            return "avx_select_lo128(%s)" % argument
    
    return argument

def GetNEONSignedType(fw=0, fwStr="fw"):
    if fw <= 0:
        return "int$" + fwStr + "$x$128/" + "(" + fwStr + ")" + "$_t"
    else:
        return "int" + str(fw) + "x" + str(128/fw) + "_t"

def GetNEONUnsignedType(fw=0, fwStr="fw"):
    if fw <= 0:
        return "uint$" + fwStr + "$x$128/" + "(" + fwStr + ")" + "$_t"
    else:
        return "uint" + str(fw) + "x" + str(128/fw) + "_t"

def IsLoadType(typeStr):
    return "load_type" == typeStr

def IsStoreType(typeStr):
    return "store_type" == typeStr

def Is64BitFloatingType(typeStr):
    return "__m256d" in typeStr
    
def IsSIMDPointer(typeStr):
    return "SIMD_type*" == typeStr

def IsFloatPointer(typeStr):
    return "float*" == typeStr

def IsFloatConstantPointer(typeStr):
    return "float const*" == typeStr

def IsSIMDType(typeStr):
    return "SIMD_type" == typeStr or "bitblock" in typeStr or "__m128i"  in typeStr or "__m128" in typeStr or "__m256" in typeStr

def IsUnsignedIntType(typeStr):
    return "unsigned_int" in typeStr

def IsSignedIntType(typeStr):
    return "signed_int" in typeStr and "unsigned_int" not in typeStr

def IsRangeType(typeStr):
    return "range" in typeStr

def IsUInt64Pointer(typeStr):
    return "uint64_t*" == typeStr

def IsUInt64ConstantPointer(typeStr):
    return "uint64_t const*" == typeStr

def IsExtactWidthIntType(typeStr):
    return "uint8_t" == typeStr or "uint16_t" == typeStr or "uint32_t" == typeStr or "uint64_t" == typeStr \
        or "int8_t" == typeStr or "int16_t" == typeStr or "int32_t" == typeStr or "int64_t" == typeStr

def IsNEONSignedType(typeStr):
    return "NEON_stype" in typeStr 

def IsNEONUnsignedType(typeStr):
    return "NEON_utype" in typeStr

def IsNEONType(typeStr):
    return "int8x16_t" == typeStr or "int16x8_t" == typeStr or "int32x4_t" == typeStr or \
        "int64x2_t" == typeStr or "uint8x16_t" == typeStr or "uint16x8_t" == typeStr or \
        "uint32x4_t" == typeStr or "uint64x2_t" == typeStr or \
        "uint64x1_t" == typeStr
