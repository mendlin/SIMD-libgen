
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import simd_sub
import simd_not

def GetBinaryRepresentation(fw, val):
	ret = bin(abs(val))[2:]
	ans = "0"*(fw-len(ret)) + ret
	#print "val = ", val, " ret = ", ret, "len of ret=", len(ret)," ans = ", ans, "fw=", fw
	if val<0:
	#val is a negative number
	#use two's complement
		ans = simd_not.GetResult(fw, [ans])
		ret = ""
		carry = 1
		for i in range(fw-1, -1, -1):
			tmpSum = int(ans[i]) + carry
			tmp = tmpSum % 2
			carry = int(tmpSum / 2)
			ret = str(tmp) + ret
		ans = ret
	return ans

def TwosComplement(fw, binStr):
	if binStr[0] == '0':
		return int(binStr, 2)
	
	one = "0"*(fw-1) + "1"
	binStr = simd_not.GetResult(fw, [simd_sub.GetResult(fw, [binStr, one])])
	
	return -1 * int(binStr, 2)

def UnsignedSaturation0(fw, block):
	'''get a new block with fw/2 wide by applying unsigned saturation on block
	'''
	upBound = (1<<(fw/2)) - 1
	val = int(block, 2)
	val = upBound if val>upBound else val
	return GetBinaryRepresentation(fw/2, val)

def UnsignedSaturation(fw, block):
	'''get a new block with fw/2 wide by applying unsigned saturation on block
	'''
	upBound = (1<<(fw/2)) - 1
	val = TwosComplement(fw, block)
	val = upBound if val>upBound else val if val>=0 else 0
	return GetBinaryRepresentation(fw/2, val)
	
def SignedSaturation(fw, block):
	'''get a new block with fw/2 wide by applying signed saturation on block
	'''
	val = TwosComplement(fw, block)
	#print "initial val = ", val, "block = ", block, "initial fw=", fw
	fw = int(fw/2)
	upBound = (1<<(fw-1)) - 1
	lowBound = -1*(1<<(fw-1))
	val = lowBound if val<lowBound else upBound if val>upBound else val
	return GetBinaryRepresentation(fw, val)
	
