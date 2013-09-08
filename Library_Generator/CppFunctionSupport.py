

# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *
from Utility import configure

Functions = \
{
	# Keys are mainly used as function names within all the strategies. 
	# But if the name after "#define" is different from the key,
	# That name will be the function name.

	"shufflemask2":\
	{
	"body":r'''
#define shufflemask2(s1, s2) ((s1<<1) | s2)''',
	"platform":["all"],
	"returnType":IntType,
	"cost":0
	},

	"shufflemask4":\
	{
	"body":r'''
#define shufflemask4(s1, s2, s3, s4) \
	((s1<<6) | (s2<<4) | (s3<<2) | s4)''',
	"platform":["all"],
	"returnType":IntType,
	"cost":0
	},

	"shufflemask8":\
	{
	"body":r'''
#define shufflemask8(s1, s2, s3, s4, s5, s6, s7, s8) \
	((s1<<21) | (s2<<18) | (s3<<15) | (s4<<12) | (s5<<9) | (s6<<6) | (s7<<3) | s8)''',
	"platform":["all"],
	"returnType":IntType,
	"cost":0
	},

	"shufflemask16":\
	{
	"body":r'''
#define shufflemask16(s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16) \
	(((long long)s1<<60) | ((long long)s2<<56) | ((long long)s3<<52) | ((long long)s4<<48) | ((long long)s5<<44) | ((long long)s6<<40) | ((long long)s7<<36) | ((long long)s8<<32) | ((long long)s9<<28) | ((long long)s10<<24) | ((long long)s11<<20) | ((long long)s12<<16) | ((long long)s13<<12) | ((long long)s14<<8) | ((long long)s15<<4) | ((long long)s16))''',
	"platform":["all"],
	"returnType":LongType,
	"cost":0
	},

	"shufflemask4_from_shufflemask2":\
	{
	"body":r'''
#define shufflemask4_from_shufflemask2(msk) \
	(msk==3 ? 238 : (msk==2 ? 228 : (msk==1 ? 78 : 68)))''',
	"platform":["all"],
	"returnType":IntType,
	"cost":0
	},

	"shufflemask8_to_shufflemask4":\
	{
	"body":r'''
#define shufflemask8_to_shufflemask4(msk) \
	((msk&3) | (((msk>>3)&3)<<2) | (((msk>>6)&3)<<4) | (((msk>>9)&3)<<6) | (((msk>>12)&3)<<8) | (((msk>>15)&3)<<10) | (((msk>>18)&3)<<12) | (((msk>>21)&3)<<14))''',
	"platform":["all"],
	"returnType":IntType,
	"cost":0
	},

	"shuffle8_demasking":\
	{
	"body":r'''
inline void shuffle8_demasking(int mask, int &s1, int &s2, int &s3, int &s4, int &s5, int &s6, int &s7, int &s8)
{
	const int v = 7;
	s1 = v&(mask>>21); s2 = v&(mask>>18); s3 = v&(mask>>15); s4 = v&(mask>>12);
	s5 = v&(mask>>9); s6 = v&(mask>>6); s7 = v&(mask>>3); s8 = v&mask;
}''',
	"platform":["all"],
	"returnType":NoneType,
	"cost":0
	},
	
	"avx_select_hi128":\
	{
	"body":r'''
#define avx_select_hi128(x) \
	((__m128i)(_mm256_extractf128_ps(x, 1)))''',
	"platform":[configure.AVX],
	"returnType":configure.SIMD_type[configure.SSE2],
	"cost":1,
	},

	# it's function name is still avx_select_hi128
	"avx2_select_hi128":\
	{
	"body":r'''
#define avx_select_hi128(x) \
	(_mm256_extractf128_si256(x, 1))''',
	"platform":[configure.AVX2],
	"returnType":"__m128i",
	"cost":1,
	},	
	
	"avx_select_lo128":\
	{
	"body":r'''
#define avx_select_lo128(x) \
	((__m128i) _mm256_castps256_ps128(x))''',
	"platform":[configure.AVX],
	"returnType":configure.SIMD_type[configure.SSE2],
	"cost":0,
	},

	"avx2_select_lo128":\
	{
	"body":r'''
#define avx_select_lo128(x) \
	_mm256_castsi256_si128(x)''',
	"platform":[configure.AVX2],
	"returnType":configure.SIMD_type[configure.SSE2],
	"cost":0,
	},

	"avx_general_combine256":\
	{
	"body":r'''
#define avx_general_combine256(x, y) \
   (_mm256_insertf128_ps(_mm256_castps128_ps256((__m128) y), (__m128) x, 1))''',
	"platform":[configure.AVX],
	"returnType":configure.SIMD_type[configure.AVX],
	"cost":1,
	},

	"avx2_general_combine256":\
	{
	"body":r'''
#define avx_general_combine256(x, y) \
    (_mm256_insertf128_si256(_mm256_castsi128_si256(y), x, 1))''',
	"platform":[configure.AVX2],
	"returnType":configure.SIMD_type[configure.AVX2],
	"cost":1,
	},	
	
	"avx_byte_shift_left":\
	{
	"body":r'''
#define avx_byte_shift_left(x, y) \
	((SIMD_type)avx_general_combine256(_mm_slli_si128(avx_select_hi128(x), y), _mm_slli_si128(avx_select_lo128(x), y)))''',
	"platform":[configure.AVX],
	"returnType":configure.SIMD_type[configure.AVX],
	"cost":4,
	},

	"avx2_byte_shift_left":\
	{
	"body":r'''
#define avx_byte_shift_left(x, y) \
	((SIMD_type)avx_general_combine256(_mm_slli_si128(avx_select_hi128(x), y), _mm_slli_si128(avx_select_lo128(x), y)))''',
	"platform":[configure.AVX2],
	"returnType":configure.SIMD_type[configure.AVX2],
	"cost":4,
	},

	"avx_byte_shift_right":\
	{
	"body":r'''
#define avx_byte_shift_right(x, y) \
	((SIMD_type)avx_general_combine256(_mm_srli_si128(avx_select_hi128(x), y), _mm_srli_si128(avx_select_lo128(x), y)))''',
	"platform":[configure.AVX],
	"returnType":configure.SIMD_type[configure.AVX],
	"cost":4,
	},

	"avx2_byte_shift_right":\
	{
	"body":r'''
#define avx_byte_shift_right(x, y) \
	((SIMD_type)avx_general_combine256(_mm_srli_si128(avx_select_hi128(x), y), _mm_srli_si128(avx_select_lo128(x), y)))''',
	"platform":[configure.AVX2],
	"returnType":configure.SIMD_type[configure.AVX2],
	"cost":4,
	},	
	
	"avx_move_lo128_to_hi128":\
	{
	"body":r'''
#define avx_move_lo128_to_hi128(x) \
	_mm256_permute2f128_ps(x, x, 0 + 8)''',
	"platform":[configure.AVX],
	"returnType":configure.SIMD_type[configure.AVX],
	"cost":1,
	},

	"avx2_move_lo128_to_hi128":\
	{
	"body":r'''
#define avx_move_lo128_to_hi128(x) \
	_mm256_permute2f128_si256(x, x, 0 + 8)''',
	"platform":[configure.AVX2],
	"returnType":configure.SIMD_type[configure.AVX2],
	"cost":1,
	},
	
	"avx_move_hi128_to_lo128":\
	{
	"body":r'''
#define avx_move_hi128_to_lo128(x) \
	_mm256_permute2f128_ps(x, x, 1 + 128)''',
	"platform":[configure.AVX],
	"returnType":configure.SIMD_type[configure.AVX],
	"cost":1,
	},

	"avx2_move_hi128_to_lo128":\
	{
	"body":r'''
#define avx_move_hi128_to_lo128(x) \
	_mm256_permute2f128_si256(x, x, 1 + 128)''',
	"platform":[configure.AVX2],
	"returnType":configure.SIMD_type[configure.AVX2],
	"cost":1,
	},
	
	"neon_shift_left_64_bits":\
	{
	"body":r'''
#define neon_shift_left_64_bits(x) \
	vextq_u64(vdupq_n_u64(0), (SIMD_type)(x), 1)''',
	"platform":[configure.NEON],
	"returnType":configure.SIMD_type[configure.NEON],
	"cost":2,
	},

	"neon_shift_right_64_bits":\
	{
	"body":r'''
#define neon_shift_right_64_bits(x) \
	vextq_u64((SIMD_type)(x), vdupq_n_u64(0), 1)''',
	"platform":[configure.NEON],
	"returnType":configure.SIMD_type[configure.NEON],
	"cost":2,
	},
}
