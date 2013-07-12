#ifndef BITBLOCK128_H_
#define BITBLOCK128_H_
/*=============================================================================
    bitblock128 - Specific 128 bit IDISA implementations.

    Copyright (C) 2011, Robert D. Cameron, Kenneth S. Herdy, Hua Huang and Nigel Medforth.
    Licensed to the public under the Open Software License 3.0.
    Licensed to International Characters Inc.
       under the Academic Free License version 3.0.

=============================================================================*/

#include "idisa128_c.h"
#include "builtins.h"

union ubitblock {
	bitblock128_t _128;
	uint64_t _64[sizeof(bitblock128_t)/sizeof(uint64_t)];
	uint32_t _32[sizeof(bitblock128_t)/sizeof(uint32_t)];
	uint16_t _16[sizeof(bitblock128_t)/sizeof(uint16_t)];
	uint8_t _8[sizeof(bitblock128_t)/sizeof(uint8_t)];
};

static IDISA_ALWAYS_INLINE void add_ci_co(bitblock128_t x, bitblock128_t y, bitblock128_t carry_in, bitblock128_t & carry_out, bitblock128_t & sum);
static IDISA_ALWAYS_INLINE void sub_bi_bo(bitblock128_t x, bitblock128_t y, bitblock128_t borrow_in, bitblock128_t & borrow_out, bitblock128_t & difference);
static IDISA_ALWAYS_INLINE void adv_ci_co(bitblock128_t cursor, bitblock128_t carry_in, bitblock128_t & carry_out, bitblock128_t & rslt);

/* The type used to store a carry bit. */
typedef bitblock128_t carry_t;





static IDISA_ALWAYS_INLINE bitblock128_t carry2bitblock(carry_t carry);
static IDISA_ALWAYS_INLINE carry_t bitblock2carry(bitblock128_t carry);

static IDISA_ALWAYS_INLINE void adc(bitblock128_t x, bitblock128_t y, carry_t & carry, bitblock128_t & sum);
static IDISA_ALWAYS_INLINE void sbb(bitblock128_t x, bitblock128_t y, carry_t & borrow, bitblock128_t & difference);
static IDISA_ALWAYS_INLINE void advance_with_carry(bitblock128_t cursor, carry_t & carry, bitblock128_t & rslt);

static IDISA_ALWAYS_INLINE void adc(bitblock128_t x, bitblock128_t y, carry_t carry_in, carry_t & carry_out, bitblock128_t & sum);
static IDISA_ALWAYS_INLINE void sbb(bitblock128_t x, bitblock128_t y, carry_t borrow_in, carry_t & borrow_out, bitblock128_t & difference);
static IDISA_ALWAYS_INLINE void advance_with_carry(bitblock128_t cursor, carry_t carry_in, carry_t & carry_out, bitblock128_t & rslt);

static IDISA_ALWAYS_INLINE bitblock128_t convert (uint64_t s);
static IDISA_ALWAYS_INLINE uint64_t convert (bitblock128_t v);

static IDISA_ALWAYS_INLINE bitblock128_t carry2bitblock(carry_t carry) {  return carry;} 
static IDISA_ALWAYS_INLINE carry_t bitblock2carry(bitblock128_t carry) {  return carry;}




static IDISA_ALWAYS_INLINE void add_ci_co(bitblock128_t x, bitblock128_t y, bitblock128_t carry_in, bitblock128_t & carry_out, bitblock128_t & sum) {
	bitblock128_t gen = simd_and(x, y);
	bitblock128_t prop = simd_or(x, y);
	bitblock128_t partial = simd_add_64(simd_add_64(x, y), carry_in);
	bitblock128_t c1 = simd_slli_128(64, simd_srli_64(63, simd_or(gen, simd_andc(prop, partial))));
	sum = simd_add_64(c1, partial);
	carry_out = simd_or(gen, simd_andc(prop, sum));
}
static IDISA_ALWAYS_INLINE void sub_bi_bo(bitblock128_t x, bitblock128_t y, bitblock128_t borrow_in, bitblock128_t & borrow_out, bitblock128_t & difference){
	bitblock128_t gen = simd_andc(y, x);
	bitblock128_t prop = simd_not(simd_xor(x, y));
	bitblock128_t partial = simd_sub_64(simd_sub_64(x, y), borrow_in);
	bitblock128_t b1 = simd_slli_128(64, simd_srli_64(63, simd_or(gen, simd_and(prop, partial))));
	difference = simd_sub_64(partial, b1);
	borrow_out = simd_or(gen, simd_and(prop, difference));
}
static IDISA_ALWAYS_INLINE void adv_ci_co(bitblock128_t cursor, bitblock128_t carry_in, bitblock128_t & carry_out, bitblock128_t & rslt){
	bitblock128_t shift_out = simd_srli_64(63, cursor);
	bitblock128_t low_bits = esimd_mergel_64(shift_out, carry_in);
	carry_out = cursor;
	rslt = simd_or(simd_add_64(cursor, cursor), low_bits);
}

IDISA_ALWAYS_INLINE void adc(bitblock128_t x, bitblock128_t y, carry_t & carry, bitblock128_t & sum)
{
	bitblock128_t gen = simd_and(x, y);
	bitblock128_t prop = simd_or(x, y);
	bitblock128_t partial = simd_add_64(simd_add_64(x, y), carry2bitblock(carry));
	bitblock128_t c1 = simd_slli_128(64, simd_srli_64(63, simd_or(gen, simd_andc(prop, partial))));
	sum = simd_add_64(c1, partial);
	carry = bitblock2carry(simd_srli_128(127, simd_or(gen, simd_andc(prop, sum))));
}

IDISA_ALWAYS_INLINE void adc(bitblock128_t x, bitblock128_t y, carry_t carry_in, carry_t & carry_out, bitblock128_t & sum)
{
	bitblock128_t co;
	add_ci_co(x, y, carry2bitblock(carry_in), co, sum);
        carry_out = bitblock2carry(simd_srli_128(127, co));
}

IDISA_ALWAYS_INLINE void sbb(bitblock128_t x, bitblock128_t y, carry_t & borrow, bitblock128_t & difference)
{
	bitblock128_t gen = simd_andc(y, x);
	bitblock128_t prop = simd_not(simd_xor(x, y));
	bitblock128_t partial = simd_sub_64(simd_sub_64(x, y), carry2bitblock(borrow));
	bitblock128_t b1 = simd_slli_128(64, simd_srli_64(63, simd_or(gen, simd_and(prop, partial))));
	difference = simd_sub_64(partial, b1);
	borrow = bitblock2carry(simd_srli_128(127, simd_or(gen, simd_and(prop, difference))));
}

IDISA_ALWAYS_INLINE void sbb(bitblock128_t x, bitblock128_t y, carry_t borrow_in, carry_t & borrow_out, bitblock128_t & difference)
{
	bitblock128_t bo;
	sub_bi_bo(x, y, carry2bitblock(borrow_in), bo, difference);
	borrow_out = bitblock2carry(simd_srli_128(127, bo));
}

IDISA_ALWAYS_INLINE void advance_with_carry(bitblock128_t cursor, carry_t & carry, bitblock128_t & rslt)
{
bitblock128_t shift_out = simd_srli_64(63, cursor);
bitblock128_t low_bits = esimd_mergel_64(shift_out, carry2bitblock(carry));
carry = bitblock2carry(simd_srli_128(64, shift_out));
rslt = simd_or(simd_add_64(cursor, cursor), low_bits);
}

IDISA_ALWAYS_INLINE void advance_with_carry(bitblock128_t cursor, carry_t carry_in, carry_t & carry_out, bitblock128_t & rslt)
{
bitblock128_t shift_out = simd_srli_64(63, cursor);
bitblock128_t low_bits = esimd_mergel_64(shift_out, carry2bitblock(carry_in));
carry_out = bitblock2carry(simd_srli_128(64, shift_out));
rslt = simd_or(simd_add_64(cursor, cursor), low_bits);
}

IDISA_ALWAYS_INLINE bitblock128_t convert(uint64_t s)
{
	ubitblock b;
	b._128 = simd_constant_128(0);
	b._64[0] = s;
	return b._128;
}

IDISA_ALWAYS_INLINE uint64_t convert (bitblock128_t v)
{
	return (uint64_t) mvmd_extract_64(0, v);
}

#endif // BITBLOCK128_H_
