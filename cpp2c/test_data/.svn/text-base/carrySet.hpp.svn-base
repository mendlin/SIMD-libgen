#ifndef CARRYQ_HPP_
#define CARRYQ_HPP_

/*=============================================================================
  carrySet.hpp - PabloJ compiler support for carry introduction.
  Ken Herdy, Robert D. Cameron
  Copyright (C) 2012, Robert D. Cameron, Kenneth S. Herdy.
    Licensed to the public under the Open Software License 3.0.
    Licensed to International Characters Inc.
       under the Academic Free License version 3.0.
  June 2012
=============================================================================*/

#include <string.h>
#include <stdint.h>
#include <iostream>

#include "bitblock.hpp"
#include "stdio.h"

///////////////////////////////////////////////////////////////////////////////
//
// Method variants.
//
// BitBlock_op_ci_co() 	- standard block non while loop statement and in final block if ignore the carry out
// BitBlock_op_co() 	- standard block while loop and in final block while loop if ignore carry out
// BitBlock_op_ci()	- final block non while loop statement
// BitBlock_op()	- final while loop statement
//
// BitBlock_op_ci(), BitBlock_op() methods not implemented to reduce the total number of
// methods and Pablo compiler complexity.
//

#define interpose32(x,y,pos) interpose32_<pos>(x,y)	
template<uint32_t n>
IDISA_ALWAYS_INLINE BitBlock interpose32_(BitBlock s, BitBlock s32) {
	return simd_or(simd<32>::slli<n>(s), simd<32>::srli<32-n>(s32));
}

template<uint32_t n>
IDISA_ALWAYS_INLINE BitBlock interpose64_(BitBlock s, BitBlock s64) {
	return simd_or(simd<64>::slli<n>(s), simd<64>::srli<64-n>(s64));
}

template <uint16_t CarryCount, uint16_t AdvanceNCount> class CarrySet;

#define LocalCarryCombine(carrySet, localCarry, carryNo, carryCount)\
	carrySet.carryCombine(localCarry.cq, carryNo, carryCount);  

#define CarryDeclare(name, carry1_count, carryN_count)\
CarrySet<carry1_count, carryN_count> name;

// Array of BitBlock implementation.
template <uint16_t CarryCount, uint16_t AdvanceNCount>
class CarrySet {

public:

    #define Carry0 simd<BLOCK_SIZE>::constant<0>()
    #define Carry1 simd<BLOCK_SIZE>::constant<1>()
  
	BitBlock cq[CarryCount + AdvanceNCount];
	//BitBlock pending64[AdvanceNCount];
	CarrySet()
	{

  	    memset (cq, 0, sizeof(BitBlock) * (CarryCount + AdvanceNCount));

	    //memset(pending64, 0, sizeof(BitBlock) * AdvanceNCount);
	}
	~CarrySet() {}

	IDISA_ALWAYS_INLINE bool carryTest(uint16_t carryno, uint16_t carry_count)
	{
		  BitBlock c1 = cq[carryno];
		  int ubound = carryno + carry_count;
		  for (int i = carryno + 1; i < ubound ; i++) {
			c1 = carryOr(c1, cq[i]);
		  }
		  return testCarry(c1);
	}

	IDISA_ALWAYS_INLINE BitBlock carryRange(uint16_t carryno, uint16_t carry_count)
	{
		  BitBlock c1 = cq[carryno];
		  int ubound = carryno + carry_count;
		  for (int i = carryno + 1; i < ubound ; i++) {
			c1 = carryOr(c1, cq[i]);
		  }
		  return c1;
	}

	IDISA_ALWAYS_INLINE void carryDequeueEnqueue(uint16_t carryno, uint16_t carry_count)
	{
		return;
	}

	IDISA_ALWAYS_INLINE void carryAdjust(uint16_t carry_count)
	{
		return;
	}

	IDISA_ALWAYS_INLINE void carryCombine(BitBlock local_cq[], uint16_t carryno, uint16_t carry_count)
	{
		  for (int i = 0; i < carry_count; i++) {
		    cq[carryno+i] = carryOr(cq[carryno+i], local_cq[i]);
		  }
	}

	IDISA_ALWAYS_INLINE BitBlock & getCarry(uint16_t carryno) 
	{
		return cq[carryno]; // carry2bitblock(cq[carryno]);
	}

	IDISA_ALWAYS_INLINE BitBlock & getPending64(uint16_t advance_n_blkno) 
	{
		return cq[CarryCount + advance_n_blkno];
	}

	IDISA_ALWAYS_INLINE void setCarry(BitBlock carryVal, uint16_t carryno)
	{
		cq[carryno] = carryVal;
	}

	IDISA_ALWAYS_INLINE BitBlock carryFlip(uint16_t carryno) const
	{
		return simd_xor(cq[carryno], Carry1);
	}

	IDISA_ALWAYS_INLINE bool testCarry(BitBlock carry) const
	{
		return bitblock::any(carry);
	}

	IDISA_ALWAYS_INLINE BitBlock carryOr(BitBlock carry1, BitBlock carry2) const
	{
		return simd_or(carry1, carry2);
	}

	
#undef Carry0
#undef Carry1

};

#endif // CARRYQ_HPP_
