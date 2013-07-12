#ifndef BYTE_COMPARE_HPP
#define BYTE_COMPARE_HPP

/*=============================================================================
    byte_compare - Byte comparison methods.

    Copyright (C) 2011, Robert D. Cameron, Kenneth S. Herdy.
    Licensed to the public under the Open Software License 3.0.
    Licensed to International Characters Inc.
    under the Academic Free License version 3.0.

    Created on:
    Author: Ken Herdy
=============================================================================*/

///////////////////////////////////////////////////////////////////////////////
//
//   WARNING: L (Length)
//
//   for L is 1, choose T = uint8_t
//   for L in [2,3], choose T = uint16_t
//   for L in [4,7], choose T = uint32_t
//   for L in [8,15], choose T = uint64_t
//   for L in [16,), choose T = BitBlock
//
//   WARNING: sizeof(T) <= L in the due to pointer cast.
//		i.e !( (T*) p1 ^ (T*) p2) logic
//
///////////////////////////////////////////////////////////////////////////////

#include "bitblock.hpp"
#include <string.h>
#include <stdint.h>
#include <iostream>

template<class T, uint32_t L> IDISA_ALWAYS_INLINE bool overlap_compare(const uint8_t * x, const uint8_t * y);
template<class T> IDISA_ALWAYS_INLINE bool overlap_compare(const uint8_t * x, const uint8_t * y, uint32_t lgth);
template<class T> IDISA_ALWAYS_INLINE bool compare(const uint8_t * x, const uint8_t * y, const uint32_t offset);
IDISA_ALWAYS_INLINE bool mem_compare(const unsigned char * x, const unsigned char * y, uint32_t lgth);

// WARNING: sizeof(T) <= L
template<uint32_t L, class T>
IDISA_ALWAYS_INLINE bool overlap_compare(const uint8_t * x, const uint8_t * y) {

    bool accum = true;
    uint8_t * p_x = (uint8_t*)x;
    uint8_t * p_y = (uint8_t*)y;

    for(int i=0; i < L/sizeof(T); i++) {
	accum = accum && compare<T>(p_x,p_y,0);
	p_x+=sizeof(T);
	p_y+=sizeof(T);
    }
    if(L & (sizeof(T)-1)) {
	accum = accum && compare<T>(x,y,L-sizeof(T));
    }
    return accum;
}

// WARNING: sizeof(T) <= L
template<class T>
IDISA_ALWAYS_INLINE bool overlap_compare(const uint8_t * x, const uint8_t * y, uint32_t lgth) {

    bool accum = true;
    uint8_t * p_x = (uint8_t*)x;
    uint8_t * p_y = (uint8_t*)y;

    for(int i=0; i < lgth/sizeof(T); i++) {
	accum = accum && compare<T>(p_x,p_y,0);
	p_x+=sizeof(T);
	p_y+=sizeof(T);
    }
    if(lgth & (sizeof(T)-1)) {
	accum = accum && compare<T>(x,y,lgth-sizeof(T));
    }
    return accum;
}

// WARNING: sizeof(T) <= L
template<class T>
IDISA_ALWAYS_INLINE bool compare(const uint8_t * x, const uint8_t * y, const uint32_t offset) {
    return !((*((T*)((uint8_t *)x + offset))) ^
	     (*((T*)((uint8_t *)y + offset)))); // << offset
}

template<>
IDISA_ALWAYS_INLINE bool compare<BitBlock>(const uint8_t * x, const uint8_t * y, const uint32_t offset) {
    BitBlock temp = simd_xor(bitblock::load_unaligned((BitBlock*) ((uint8_t *)x + offset)),
			     bitblock::load_unaligned((BitBlock*) ((uint8_t *)y + offset))); // << shift offset
    return bitblock::all(simd_not(temp));
}

IDISA_ALWAYS_INLINE bool mem_compare(const unsigned char * x, const unsigned char * y, uint32_t lgth) {
	return (0 == memcmp(x, y, lgth));
}


#endif // BYTE_COMPARE_HPP


