
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *
from SSSE3Instructions import SSSE3BuiltIns

SSE4_1BuiltIns = dict(SSSE3BuiltIns.items() +\
{
	"simd_mult":\
	{
		"signature":["SIMD_type _mm_mullo_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"simd_eq":\
	{
		"signature":["SIMD_type _mm_cmpeq_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_max":\
	{
		"signature":["SIMD_type _mm_max_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_umax":\
	{
		"signature":["SIMD_type _mm_max_epu$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_min":\
	{
		"signature":["SIMD_type _mm_min_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_umin":\
	{
		"signature":["SIMD_type _mm_min_epu$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"hsimd_packus":\
	{
		"signature":["SIMD_type _mm_packus_epi$fw$(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"_mm_blendv_epi8":\
	{
		"signature":["SIMD_type _mm_blendv_epi8(SIMD_type arg3, SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type", "arg3":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"_mm_extract_epi8":\
	{
		"signature":["int _mm_extract_epi8(SIMD_type arg1, int pos)"],
		"args_type":{"arg1":"SIMD_type", "pos":"signed_int(32)"},
		"return_type":"signed_int(32)",
		"fws":[[8]],
	},
	"_mm_extract_epi32":\
	{
		"signature":["int _mm_extract_epi32(SIMD_type arg1, int pos)"],
		"args_type":{"arg1":"SIMD_type", "pos":"signed_int(32)"},
		"return_type":"signed_int(32)",
		"fws":[[32]],
	},
	"_mm_cvtepi8_epi16":\
	{
		"signature":["SIMD_type _mm_cvtepi8_epi16(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"_mm_cvtepi16_epi32":\
	{
		"signature":["SIMD_type _mm_cvtepi16_epi32(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"_mm_cvtepi32_epi64":\
	{
		"signature":["SIMD_type _mm_cvtepi32_epi64(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"_mm_cvtepu8_epi16":
	{
		"signature":["SIMD_type _mm_cvtepu8_epi16(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"_mm_cvtepu16_epi32":
	{
		"signature":["SIMD_type _mm_cvtepu16_epi32(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"_mm_cvtepu32_epi64":
	{
		"signature":["SIMD_type _mm_cvtepu32_epi64(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"_mm_mul_epi32":
	{
		"signature":["SIMD_type _mm_mul_epi32(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
}.items())
