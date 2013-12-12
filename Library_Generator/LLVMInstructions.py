

# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *
from Utility import configure

LLVMBuiltIns = \
{
	"simd_and":\
	{
		"signature":["SIMD_type _mm256_and_si256(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_andc":\
	{
		"signature":["SIMD_type _mm256_andnot_si256(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_or":\
	{
		"signature":["SIMD_type _mm256_or_si256(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_xor":\
	{
		"signature":["SIMD_type _mm256_xor_si256(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},	
	"simd_ifh":\
	{
		"signature":["SIMD_type _mm256_blendv_epi8(SIMD_type arg3, SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type", "arg3":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"simd_add":\
	{
		"signature":["SIMD_type _mm256_add_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_sub":\
	{
		"signature":["t _mm256_sub_epi$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},

	# CAUSION: Simd umult is not exactly what we want. 
	# For _mm256_mul_epu32:
	#   Multiply the low unsigned 32-bit integers from each packed 64-bit element in a and b, 
	#   and store the unsigned 64-bit results in dst.
	"simd_umult":\
	{
		"signature":["t _mm256_mul_epu32(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},	
	"simd_mult":\
	{
		"signature":["t _mm256_mullo_epi$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"simd_eq":\
	{
		"signature":["t _mm256_cmpeq_epi$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_gt":\
	{
		"signature":["t _mm256_cmpgt_epi$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_max":\
	{
		"signature":["t _mm256_max_epi$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_umax":\
	{
		"signature":["t _mm256_max_epu$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_min":\
	{
		"signature":["t _mm256_min_epi$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_umin":\
	{
		"signature":["t _mm256_min_epu$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_srli":\
	{
		"signature":["t _mm256_srli_epi$fw$(t arg1, t sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32, 64]],
	},

	"simd_srl":\
	{
		"signature":["t _mm256_srl_epi$fw$(t arg1, __m128i shift_mask)"],
		"args_type":{"arg1":"SIMD_type", "shift_mask":"__m128i"},
		"return_type":"SIMD_type",
		"fws":[[16, 32, 64]],
	},

	"simd_slli":\
	{
		"signature":["t _mm256_slli_epi$fw$(t arg1, t sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32, 64]],
	},

	"simd_sll":\
	{
		"signature":["t _mm256_sll_epi$fw$(t arg1, t shift_mask)"],
		"args_type":{"arg1":"SIMD_type", "shift_mask":"__m128i"},
		"return_type":"SIMD_type",
		"fws":[[16, 32, 64]],
	},

	"simd_srai":\
	{
		"signature":["t _mm256_srai_epi$fw$(t arg1, t sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},

	"simd_sra":\
	{
		"signature":["t _mm256_sra_epi$fw$(t arg1, t shift_mask)"],
		"args_type":{"arg1":"SIMD_type", "shift_mask":"__m128i"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},

	"simd_constant":\
	{
		"signature":["SIMD_type _mm256_set1_epi$fw$(int val)"],
		"args_type":{"val":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_abs":\
	{
		"signature":["t _mm256_abs_epi$fw$(t arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
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
		"signature":["SIMD_type _mm256_load_si256(SIMD_type* arg1)"],
		"args_type":{"arg1":"SIMD_type*"},
		"return_type":"SIMD_type",
		"fws":[[256]],
	},
	"bitblock_store_aligned":\
	{
		"signature":["void _mm256_store_si256(SIMD_type* arg2, SIMD_type arg1)"],
		"args_type":{"arg2":"SIMD_type*", "arg1":"SIMD_type"},
		"return_type":"void",
		"fws":[[256]],
	},
	"bitblock_load_unaligned":\
	{
		"signature":["SIMD_type _mm256_loadu_si256(SIMD_type* arg1)"],
		"args_type":{"arg1":"SIMD_type*"},
		"return_type":"SIMD_type",
		"fws":[[256]],
	},
	"bitblock_store_unaligned":\
	{
		"signature":["void _mm256_storeu_si256(SIMD_type* arg2, SIMD_type arg1)"],
		"args_type":{"arg2":"SIMD_type*", "arg1":"SIMD_type"},
		"return_type":"void",
		"fws":[[256]],
	},

	"hsimd_signmask":\
	{
		"signature":["int _mm256_movemask_epi8(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"int",
		"fws":[[8]],	
	}
}

