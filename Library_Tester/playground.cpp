#include "utility.h"

static inline bitblock256_t bitblock_sll(bitblock256_t arg1, int shift)
{
	int n = shift / 64;
	if (n == 1)
		arg1 = mvmd<64>::slli<1>(arg1);
	else if (n == 2)
		arg1 = mvmd<64>::slli<2>(arg1);
	else if (n == 3)
		arg1 = mvmd<64>::slli<3>(arg1);
	else if (n >= 4)
		return simd<32>::constant<0>();

	if (shift & 63)
	{
		__m128i sh = _mm_cvtsi32_si128(shift & 63);
		__m128i subsh = _mm_cvtsi32_si128(64 - (shift & 63));

		return simd_or(_mm256_sll_epi64(arg1, sh), mvmd<64>::slli<1>(_mm256_srl_epi64(arg1, subsh)));
	}

	return arg1;
}

static inline bitblock256_t bitblock_srl(bitblock256_t arg1, int shift)
{
	int n = shift / 64;
	if (n == 1)
		arg1 = mvmd<64>::srli<1>(arg1);
	else if (n == 2)
		arg1 = mvmd<64>::srli<2>(arg1);
	else if (n == 3)
		arg1 = mvmd<64>::srli<3>(arg1);
	else if (n >= 4)
		return simd<32>::constant<0>();

	if (shift & 63)
	{
		__m128i sh = _mm_cvtsi32_si128(shift & 63);
		__m128i subsh = _mm_cvtsi32_si128(64 - (shift & 63));

		return simd_or(_mm256_srl_epi64(arg1, sh), mvmd<64>::srli<1>(_mm256_sll_epi64(arg1, subsh)));
	}

	return arg1;
}

union ubitblock {
        bitblock256_t _256;
        __m128i _128[sizeof(bitblock256_t)/sizeof(bitblock256_t)];
        uint64_t _64[sizeof(bitblock256_t)/sizeof(uint64_t)];
        uint32_t _32[sizeof(bitblock256_t)/sizeof(uint32_t)];
        uint16_t _16[sizeof(bitblock256_t)/sizeof(uint16_t)];
        uint8_t _8[sizeof(bitblock256_t)/sizeof(uint8_t)];
};

/* The type used to store a carry bit. */
typedef bitblock256_t carry_t;

static inline void add_ci_co(bitblock256_t x, bitblock256_t y, carry_t carry_in, carry_t & carry_out, bitblock256_t & sum);
static inline void sub_bi_bo(bitblock256_t x, bitblock256_t y, carry_t borrow_in, carry_t & borrow_out, bitblock256_t & difference);
static inline void adv_ci_co(bitblock256_t cursor, bitblock256_t carry_in, bitblock256_t & carry_out, bitblock256_t & rslt);

static inline bitblock256_t convert (uint64_t s);
static inline uint64_t convert(bitblock256_t v);

static inline void add_ci_co(bitblock256_t x, bitblock256_t y, carry_t carry_in, carry_t & carry_out, bitblock256_t & sum) {
  bitblock256_t all_ones = simd<1>::constant<1>();
  bitblock256_t gen = simd_and(x, y);
  bitblock256_t prop = simd_xor(x, y);
  bitblock256_t partial_sum = simd<64>::add(x, y);
  bitblock256_t carry = simd_or(gen, simd_andc(prop, partial_sum));
  bitblock256_t bubble = simd<64>::eq(partial_sum, all_ones);
  uint64_t carry_mask = hsimd<64>::signmask(carry) * 2 + convert(carry_in);
  uint64_t bubble_mask = hsimd<64>::signmask(bubble);
  uint64_t carry_scan_thru_bubbles = (carry_mask + bubble_mask) &~ bubble_mask;
  uint64_t increments = carry_scan_thru_bubbles | (carry_scan_thru_bubbles - carry_mask);
  carry_out = convert(increments >> 4);
  uint64_t spread = 0x0000200040008001 * increments & 0x0001000100010001;
  sum = simd<64>::add(partial_sum, _mm256_cvtepu8_epi64(avx_select_lo128(convert(spread))));
}

inline void sub_bi_bo(bitblock256_t x, bitblock256_t y, carry_t borrow_in, carry_t & borrow_out, bitblock256_t & difference){
	bitblock256_t gen = simd_andc(y, x);
	bitblock256_t prop = simd_not(simd_xor(x, y));
	bitblock256_t partial = simd<128>::sub(simd<128>::sub(x, y), borrow_in);
	bitblock256_t b1 = simd<256>::slli<128>(simd<128>::srli<127>(simd_or(gen, simd_and(prop, partial))));
	difference = simd<128>::sub(partial, b1);
	borrow_out = simd_or(gen, simd_and(prop, difference));
}

static inline void adv_ci_co(bitblock256_t cursor, bitblock256_t carry_in, bitblock256_t & carry_out, bitblock256_t & rslt){
	bitblock256_t shift_out = simd<64>::srli<63>(cursor);
	bitblock256_t low_bits = simd_or(mvmd<64>::slli<1>(shift_out), carry_in);
	carry_out = cursor;
	rslt = simd_or(simd<64>::add(cursor, cursor), low_bits);
}

static inline bitblock256_t convert(uint64_t s)
{
  ubitblock b = {b._256 = simd<128>::constant<0>()}; // = {0};
  b._64[0] = s;
  return b._256;
}

static inline uint64_t convert(bitblock256_t v)
{
  return (uint64_t) mvmd<64>::extract<0>(v);
}

int main()
{
	SIMD_type a, b, c, d, e, r;
	// b = simd<32>::constant<11>();
	string str = "1001000000000000010001001111101000010101111000011100010010010101100110111000101001011010111001000111100110100110100101001100000011110010010101101010110001101000000000001000111100011000011010001001011111001111100010010011011010001110101101100010101111110101";	

	a = LoadfromString(str, 2);
	b = LoadfromString(str, 2);
	c = simd<32>::constant<0>();

	add_ci_co(a, b, c, d, r);

	cout << "a: "<<endl << Store2String(a, 2) <<endl;
	cout << "r: "<<endl << Store2String(r, 2) <<endl;
	cout << "d: "<<endl << Store2String(d, 2) <<endl;

	b = avx_move_hi128_to_lo128(a);

	cout <<"b:"<<endl;
	cout <<Store2String(b, 2) <<endl;
	return 0;
}

