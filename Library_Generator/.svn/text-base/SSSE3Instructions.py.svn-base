
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *
from SSE3Instructions import SSE3BuiltIns

SSSE3BuiltIns = dict(SSE3BuiltIns.items() + \
{
	"simd_abs":\
	{
		"signature":["SIMD_type _mm_abs_epi$fw$(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"hsimd_add_hl":\
	{
		"signature":["SIMD_type _mm_hadd_epi$fw/2$(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32, 64]],
	},
	"mvmd_shuffle":\
	{
		"signature":["SIMD_type _mm_shuffle_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"_mm_hsub_epi16":\
	{
		"signature":["SIMD_type _mm_hsub_epi16(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"_mm_hsub_epi32":\
	{
		"signature":["SIMD_type _mm_hsub_epi32(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"_mm_sign_epi8":\
	{
		"signature":["SIMD_type _mm_sign_epi8(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"_mm_sign_epi16":\
	{
		"signature":["SIMD_type _mm_sign_epi16(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"_mm_sign_epi32":\
	{
		"signature":["SIMD_type _mm_sign_epi32(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
}.items())
