

# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *
from Utility import configure

AVXBuiltIns = \
{
	"simd_and":\
	{
		"signature":["SIMD_type _mm256_and_ps(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_andc":\
	{
		"signature":["SIMD_type _mm256_andnot_ps(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_or":\
	{
		"signature":["SIMD_type _mm256_or_ps(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_xor":\
	{
		"signature":["SIMD_type _mm256_xor_ps(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_ifh":\
	{
		"signature":["SIMD_type (SIMD_type)_mm256_blendv_pd(SIMD_type arg3, SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"__m256d", "arg2":"__m256d", "arg3":"__m256d"},
		"return_type":"SIMD_type",
		"fws":[[64]],
	},
	"simd_add":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_add_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_sub":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_sub_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_umult":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_mul_epu$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"simd_mult":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_mullo_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"simd_eq":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_cmpeq_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_gt":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_cmpgt_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_max":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_max_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_umax":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_max_epu$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_min":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_min_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_umin":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_min_epu$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_srli":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_srli_epi$fw$, arg1, sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32, 64]],
	},
	"simd_slli":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_slli_epi$fw$, arg1, sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32, 64]],
	},
	"simd_srai":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_srai_epi$fw$, arg1, sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"simd_constant":\
	{
		"signature":["SIMD_type (SIMD_type)_mm256_set1_epi$fw$(int val)"],
		"args_type":{"val":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_abs":\
	{
		"signature":[configure.AVXBuiltInVecWrapper + "(_mm_abs_epi$fw$, arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"hsimd_add_hl":\
	{
		"signature":[configure.AVXBuiltInHorWrapper + "(_mm_hadd_epi$fw/2$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32, 64]],
	},
	"hsimd_packus":\
	{
		"signature":[configure.AVXBuiltInHorWrapper + "(_mm_packus_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"hsimd_packss":\
	{
		"signature":[configure.AVXBuiltInHorWrapper + "(_mm_packs_epi$fw$, arg1, arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"mvmd_fill":\
	{
		"signature":["SIMD_type (SIMD_type)_mm256_set1_epi$fw$(int val1)"],
		"args_type":{"val1":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"mvmd_fill4":\
	{
		"signature":["SIMD_type (SIMD_type)_mm256_set_epi$fw$(int val1, int val2, int val3, int val4, int val1, int val2, int val3, int val4)"],
		"args_type":{"val1":"signed_int(32)", "val2":"signed_int(32)", "val3":"signed_int(32)", "val4":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"mvmd_fill8":\
	{
		"signature":["SIMD_type (SIMD_type)_mm256_set_epi$fw$(int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8, int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8)"],
		"args_type":{"val1":"signed_int(32)", "val2":"signed_int(32)", "val3":"signed_int(32)", "val4":"signed_int(32)", \
					"val5":"signed_int(32)", "val6":"signed_int(32)", "val7":"signed_int(32)", "val8":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"mvmd_fill16":\
	{
		"signature":["SIMD_type (SIMD_type)_mm256_set_epi$fw$(int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8, int val9, int val10, int val11, int val12, int val13, int val14, int val15, int val16, int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8, int val9, int val10, int val11, int val12, int val13, int val14, int val15, int val16)"],
		"args_type":{"val1":"signed_int(32)", "val2":"signed_int(32)", "val3":"signed_int(32)", "val4":"signed_int(32)", \
					"val5":"signed_int(32)", "val6":"signed_int(32)", "val7":"signed_int(32)", "val8":"signed_int(32)", \
					"val9":"signed_int(32)", "val10":"signed_int(32)", "val11":"signed_int(32)", "val12":"signed_int(32)", \
					"val13":"signed_int(32)", "val14":"signed_int(32)", "val15":"signed_int(32)", "val16":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"bitblock_load_aligned":\
	{
		"signature":["SIMD_type _mm256_load_ps(float* arg1)"],
		"args_type":{"arg1":"float*"},
		"return_type":"SIMD_type",
		"fws":[[256]],
	},
	"bitblock_store_aligned":\
	{
		"signature":["void _mm256_store_ps(float* arg2, SIMD_type arg1)"],
		"args_type":{"arg2":"float*", "arg1":"SIMD_type"},
		"return_type":"void",
		"fws":[[256]],
	},
	"bitblock_load_unaligned":\
	{
		"signature":["SIMD_type _mm256_loadu_ps(float* arg1)"],
		"args_type":{"arg1":"float*"},
		"return_type":"SIMD_type",
		"fws":[[256]],
	},
	"bitblock_store_unaligned":\
	{
		"signature":["void _mm256_storeu_ps(float* arg2, SIMD_type arg1)"],
		"args_type":{"arg2":"float*", "arg1":"SIMD_type"},
		"return_type":"void",
		"fws":[[256]],
	},
	"_mm256_set_epi32":\
	{
		"signature":["SIMD_type _mm256_set_epi32(int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8)"],
		"args_type":{"val1":"signed_int(32)", "val2":"signed_int(32)", "val3":"signed_int(32)", "val4":"signed_int(32)", \
					"val5":"signed_int(32)", "val6":"signed_int(32)", "val7":"signed_int(32)", "val8":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"_mm256_castsi128_si256":\
	{
		"signature":["SIMD_type _mm256_castsi128_si256(__m128i arg1)"],
		"args_type":{"arg1":"__m128i"},
		"return_type":"SIMD_type",
		"fws":[[256]],
	},
	"_mm_sad_epu8":\
	{
		"signature":["__m128i _mm_sad_epu8(__m128i arg1, __m128i arg2)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[8]],
	},
	"_mm_set1_epi32":\
	{
		"signature":["__m128i _mm_set1_epi32(int val1)"],
		"args_type":{"val1":"signed_int(32)"},
		"return_type":"__m128i",
		"fws":[[32]],
	},
	"_mm_extract_epi8":\
	{
		"signature":["int _mm_extract_epi8(__m128i arg1, int pos)"],
		"args_type":{"arg1":"__m128i", "pos":"signed_int(32)"},
		"return_type":"signed_int(32)",
		"fws":[[8]],
	},
	"_mm_extract_epi16":\
	{
		"signature":["int _mm_extract_epi16(__m128i arg1, int pos)"],
		"args_type":{"arg1":"__m128i", "pos":"signed_int(32)"},
		"return_type":"signed_int(32)",
		"fws":[[16]],
	},
	"_mm_extract_epi32":\
	{
		"signature":["int _mm_extract_epi32(__m128i arg1, int pos)"],
		"args_type":{"arg1":"__m128i", "pos":"signed_int(32)"},
		"return_type":"signed_int(32)",
		"fws":[[32]],
	},
	"_mm256_testz_si256":\
	{
		"signature":["int _mm256_testz_si256(SIMD_type arg1, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"signed_int(32)",
		"fws":[[256]],
	},
	"_mm_movemask_epi8":\
	{
		"signature":["int _mm_movemask_epi8(__m128i arg1)"],
		"args_type":{"arg1":"__m128i"},
		"return_type":"signed_int(32)",
		"fws":[[8]],
	},
	"_mm_unpackhi_epi8":\
	{
		"signature":["__m128i _mm_unpackhi_epi8(__m128i arg2, __m128i arg1)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[8]],
	},
	"_mm_unpackhi_epi16":\
	{
		"signature":["__m128i _mm_unpackhi_epi16(__m128i arg2, __m128i arg1)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[16]],
	},
	"_mm_unpackhi_epi32":\
	{
		"signature":["__m128i _mm_unpackhi_epi32(__m128i arg2, __m128i arg1)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[32]],
	},
	"_mm_unpackhi_epi64":\
	{
		"signature":["__m128i _mm_unpackhi_epi64(__m128i arg2, __m128i arg1)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[64]],
	},
	"_mm_unpacklo_epi8":\
	{
		"signature":["__m128i _mm_unpacklo_epi8(__m128i arg2, __m128i arg1)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[8]],
	},
	"_mm_unpacklo_epi16":\
	{
		"signature":["__m128i _mm_unpacklo_epi16(__m128i arg2, __m128i arg1)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[16]],
	},
	"_mm_unpacklo_epi32":\
	{
		"signature":["__m128i _mm_unpacklo_epi32(__m128i arg2, __m128i arg1)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[32]],
	},
	"_mm_unpacklo_epi64":\
	{
		"signature":["__m128i _mm_unpacklo_epi64(__m128i arg2, __m128i arg1)"],
		"args_type":{"arg1":"__m128i", "arg2":"__m128i"},
		"return_type":"__m128i",
		"fws":[[64]],
	},
	
}
