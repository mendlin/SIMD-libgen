IDISA_ALWAYS_INLINE bitblock256_t bitblock256::sll(bitblock256_t arg1, int shift)
{
	int n = shift / 64;
	if (n == 1)
		arg1 = mvmd256<64>::slli<1>(arg1);
	else if (n == 2)
		arg1 = mvmd256<64>::slli<2>(arg1);
	else if (n == 3)
		arg1 = mvmd256<64>::slli<3>(arg1);
	else if (n >= 4)
		return simd256<32>::constant<0>();

	if (shift & 63)
	{
		__m128i sh = _mm_cvtsi32_si128(shift & 63);
		__m128i subsh = _mm_cvtsi32_si128(64 - (shift & 63));

		return simd_or(_mm256_sll_epi64(arg1, sh), mvmd256<64>::slli<1>(_mm256_srl_epi64(arg1, subsh)));
	}

	return arg1;
}

IDISA_ALWAYS_INLINE bitblock256_t bitblock256::srl(bitblock256_t arg1, int shift)
{
	int n = shift / 64;
	if (n == 1)
		arg1 = mvmd256<64>::srli<1>(arg1);
	else if (n == 2)
		arg1 = mvmd256<64>::srli<2>(arg1);
	else if (n == 3)
		arg1 = mvmd256<64>::srli<3>(arg1);
	else if (n >= 4)
		return simd256<32>::constant<0>();

	if (shift & 63)
	{
		__m128i sh = _mm_cvtsi32_si128(shift & 63);
		__m128i subsh = _mm_cvtsi32_si128(64 - (shift & 63));

		return simd_or(_mm256_srl_epi64(arg1, sh), mvmd256<64>::srli<1>(_mm256_sll_epi64(arg1, subsh)));
	}

	return arg1;
}

IDISA_ALWAYS_INLINE bitblock256_t bitblock256::sll(bitblock256_t arg1, bitblock256_t shift)
{
	return bitblock256::sll(arg1, _mm_cvtsi128_si32(avx_select_lo128(shift)));
}

IDISA_ALWAYS_INLINE bitblock256_t bitblock256::srl(bitblock256_t arg1, bitblock256_t shift)
{
	return bitblock256::srl(arg1, _mm_cvtsi128_si32(avx_select_lo128(shift)));
}

// idisa_avx2.h
template <> inline bitblock256_t simd<256>::srl(bitblock256_t arg1, bitblock256_t shift_mask)
{		
	int shift = _mm_cvtsi128_si32(avx_select_lo128(simd_and(shift_mask, simd<256>::constant<255>())));

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