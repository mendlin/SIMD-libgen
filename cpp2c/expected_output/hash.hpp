#ifndef HASH_H
#define HASH_H

/*=============================================================================
  hash.hpp - Hash Utilities.
  Created on: 18-December-2011
  Author: Ken Herdy
=============================================================================*/

// #define HASH_HPP_DEBUG

//#define NDEBUG // if NDEBUG then disable assertions

#include "bitblock.h"
#include <cassert>
#include <stdint.h>
#include <iostream>

///////////////////////////////////////////////////////////////////////////////
//
// WARNING: Pad or Perish
//
// 'bit_slice' and 'byte_slice' slice forward via a static cast to the
// uint64_t type at the position of the base address + bit_idx
// and require up to sizeof(uint64_t) bytes of additional padding.
//
///////////////////////////////////////////////////////////////////////////////

static int32_t bytes2bits(int32_t bytes) { return bytes * 8; }
static int32_t bits2bytes(int32_t bits) /*{ return (bits + 8) / (8); } */ { return ((bits & (8-1) != 0) ? (bits + 8) / (8) : (bits/8)); }
static IDISA_ALWAYS_INLINE uint64_t gen_mask(const uint32_t mask_bits);

//static IDISA_ALWAYS_INLINE uint64_t byte_slice(const uint8_t * base, const int32_t byte_idx, const uint32_t slice_bytes);
//static IDISA_ALWAYS_INLINE uint64_t byte_compress_hash(const uint8_t * h0, const uint8_t * h1, const int32_t byte_idx, const uint32_t slice_bytes, const uint32_t hash_bytes);

static IDISA_ALWAYS_INLINE uint64_t bit_slice(const uint8_t * base, const int32_t bit_idx, const uint32_t slice_bits);
static IDISA_ALWAYS_INLINE uint64_t bit_compress_hash(const uint8_t * h0, const uint8_t * h1, const int32_t bit_idx, const uint32_t slice_bits, const uint32_t hash_bits);

///////////////////////////////////////////////////////////////////////////////

static IDISA_ALWAYS_INLINE uint64_t gen_mask(const uint32_t mask_bits) {
    assert(mask_bits >= 0);

    const uint64_t ONE = 1;
    uint64_t mask = (ONE << mask_bits) - ONE;
#ifdef HASH_H_DEBUG
    print_register<uint64_t>("mask", mask);
#endif
    return mask;
}

//static IDISA_ALWAYS_INLINE uint64_t byte_slice(const uint8_t * base, const int32_t byte_idx, const uint32_t slice_bytes) {
//    assert(slice_bytes >= 0 && slice_bytes <= sizeof(uint64_t));
//    assert(byte_idx >= 0);

//    uint64_t shift = *((uint64_t *)(base + byte_idx));
//    uint64_t mask = gen_mask(bytes2bits(slice_bytes));
//    uint64_t r = shift & mask;

//#ifdef HASH_HPP_DEBUG
//    print_register<BitBlock>("base", *(BitBlock *)base);
//    std::cout << "byte index:" << byte_idx << std::endl;
//    print_register<BitBlock>("shift", *(BitBlock *)&shift);
//    print_register<uint64_t>("mask", mask);
//    print_register<uint64_t>("r", r);
//#endif

//    return r;
//}

static IDISA_ALWAYS_INLINE uint64_t bit_slice(const uint8_t * base, const int32_t bit_idx, const uint32_t slice_bits) {
    assert(slice_bits >= 0 && slice_bits <= bytes2bits(sizeof(uint64_t)));
    assert(bit_idx >= 0);

    uint64_t shift = *((uint64_t *)(base + (bit_idx/8))) >> (bit_idx & (8-1));
    uint64_t mask = gen_mask(slice_bits);
    uint64_t r = shift & mask;

#ifdef HASH_H_DEBUG
    print_register<uint64_t>("base", *(uint64_t *)base);
    std::cout << "           bit index = " << bit_idx << std::endl;
    print_register<uint64_t>("shift", *(uint64_t *)&shift);
    print_register<uint64_t>("mask", mask);
    print_register<uint64_t>("r", r);
#endif

    return r;
}

static IDISA_ALWAYS_INLINE uint64_t bit_compress_hash(const uint8_t * h0, const uint8_t * h1, const int32_t bit_idx, const uint32_t slice_bits, const uint32_t hash_bits) {

    assert(hash_bits > 0 && hash_bits <= 64);
    assert(slice_bits >= hash_bits);

    uint64_t x0 = bit_slice(h0,bit_idx,hash_bits);
    uint64_t x1 = bit_slice(h1,bit_idx+slice_bits-hash_bits,hash_bits);

    //assert(x0 != x1);
    uint64_t mask = gen_mask(slice_bits);
    uint64_t r = x0 ^ x1;

#ifdef HASH_H_DEBUG
    print_register<uint64_t>("h0", *(uint64_t *)(h0));
    print_register<uint64_t>("h1", *(uint64_t *)(h1));
    print_register<uint64_t>("x0", x0);
    print_register<uint64_t>("x1", x1);
    print_register<uint64_t>("r", r);
#endif

    return r  & mask;
}

#endif // HASH_H

/*
static IDISA_ALWAYS_INLINE uint64_t bit_expand_hash(const uint8_t * base, const uint8_t * base1, const int32_t offset, const uint32_t slice_size, const uint32_t hash_size);
static IDISA_ALWAYS_INLINE uint64_t bit_expand_hash(const uint8_t * base, const uint8_t * base1, const int32_t offset, const uint32_t slice_size, const uint32_t hash_size) {
    assert(slice_size > 0 && slice_size <= 64);
    //assert(slice_size <= hash_size);

    uint64_t x0 = bit_slice(base,offset,slice_size);
    uint64_t x1 = bit_slice(base1,offset,slice_size);
    uint64_t mask = gen_mask(hash_size);

    assert(x0 != x1);

    uint64_t t = x0 ^ x1;
    uint64_t r = t;
    int32_t shift = slice_size;

    print_register<uint64_t>("t", t);
    print_register<uint64_t>("r", r);

    while(shift > 0) {

#ifndef NDEBUG
    std::cout << "Stream offset (bit):  " << offset << std::endl;
    std::cout << "Symbol lgth (bits): " << slice_size << std::endl;
    std::cout << "Hash size (bits):   " << hash_size << std::endl;
    std::cout << "Shift (bits): " << shift << std::endl;

    print_register<uint64_t>("base", *(uint64_t *)base);
    print_register<uint64_t>("base1", *(uint64_t *)base1);
    print_register<uint64_t>("x0", x0);
    print_register<uint64_t>("x1", x1);
    print_register<uint64_t>("r", r);
#endif
	r = r | (r << (uint32_t)shift);
	shift -= slice_size;
	print_register<uint64_t>("r", r);
    }

    return r & mask;
}
*/
