# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *

SSE2BuiltIns = \
{
	"simd_and":\
	{
		"signature":["SIMD_type _mm_and_si128(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_andc":\
	{
		"signature":["SIMD_type _mm_andnot_si128(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_or":\
	{
		"signature":["SIMD_type _mm_or_si128(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_xor":\
	{
		"signature":["SIMD_type _mm_xor_si128(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_add":\
	{
		"signature":["SIMD_type _mm_add_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_sub":\
	{
		"signature":["SIMD_type _mm_sub_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"simd_umult":\
	{
		"signature":["SIMD_type _mm_mul_epu$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"simd_mult":\
	{
		"signature":["SIMD_type _mm_mullo_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"simd_eq":\
	{
		"signature":["SIMD_type _mm_cmpeq_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_gt":\
	{
		"signature":["SIMD_type _mm_cmpgt_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"simd_max":\
	{
		"signature":["SIMD_type _mm_max_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"simd_umax":\
	{
		"signature":["SIMD_type _mm_max_epu$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"simd_min":\
	{
		"signature":["SIMD_type _mm_min_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"simd_umin":\
	{
		"signature":["SIMD_type _mm_min_epu$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"simd_srli":\
	{
		"signature":["SIMD_type _mm_srli_epi$fw$(SIMD_type arg1, int sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32, 64]],
	},
	"simd_slli":\
	{
		"signature":["SIMD_type _mm_slli_epi$fw$(SIMD_type arg1, int sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32, 64]],
	},
	"simd_srai":\
	{
		"signature":["SIMD_type _mm_srai_epi$fw$(SIMD_type arg1, int sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"simd_constant":\
	{
		"signature":["SIMD_type _mm_set1_epi$fw$(int val)"],
		"args_type":{"val":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"hsimd_packus":\
	{
		"signature":["SIMD_type _mm_packus_epi$fw$(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"hsimd_packss":\
	{
		"signature":["SIMD_type _mm_packs_epi$fw$(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[16, 32]],
	},
	"hsimd_signmask":\
	{
		"signature":["int _mm_movemask_epi$fw$(SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type"},
		"return_type":"signed_int(32)",
		"fws":[[8]],
	},
	"esimd_mergeh":\
	{
		"signature":["SIMD_type _mm_unpackhi_epi$fw$(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"esimd_mergel":\
	{
		"signature":["SIMD_type _mm_unpacklo_epi$fw$(SIMD_type arg2, SIMD_type arg1)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
	"mvmd_srli":\
	{
		"signature":["SIMD_type _mm_srli_si128(SIMD_type arg1, int sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"mvmd_slli":\
	{
		"signature":["SIMD_type _mm_slli_si128(SIMD_type arg1, int sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},	
	"mvmd_fill":\
	{
		"signature":["SIMD_type _mm_set1_epi$fw$(int val1)"],
		"args_type":{"val1":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32]],
	},
	"mvmd_fill4":\
	{
		"signature":["SIMD_type _mm_set_epi$fw$(int val1, int val2, int val3, int val4)"],
		"args_type":{"val1":"signed_int(32)", "val2":"signed_int(32)", "val3":"signed_int(32)", "val4":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"mvmd_fill8":\
	{
		"signature":["SIMD_type _mm_set_epi$fw$(int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8)"],
		"args_type":{"val1":"signed_int(32)", "val2":"signed_int(32)", "val3":"signed_int(32)", "val4":"signed_int(32)", \
					"val5":"signed_int(32)", "val6":"signed_int(32)", "val7":"signed_int(32)", "val8":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"mvmd_fill16":\
	{
		"signature":["SIMD_type _mm_set_epi$fw$(int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8, \
					int val9, int val10, int val11, int val12, int val13, int val14, int val15, int val16)"],
		"args_type":{"val1":"signed_int(32)", "val2":"signed_int(32)", "val3":"signed_int(32)", "val4":"signed_int(32)", \
					"val5":"signed_int(32)", "val6":"signed_int(32)", "val7":"signed_int(32)", "val8":"signed_int(32)", \
					"val9":"signed_int(32)", "val10":"signed_int(32)", "val11":"signed_int(32)", "val12":"signed_int(32)", \
					"val13":"signed_int(32)", "val14":"signed_int(32)", "val15":"signed_int(32)", "val16":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},

	"mvmd_shufflei":\
	{
		"signature":["SIMD_type _mm_shuffle_epi$fw$(SIMD_type arg1, int msk)"],
		"args_type":{"arg1":"SIMD_type", "msk":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},

	"mvmd_insert":\
	{
		"signature":["SIMD_type _mm_insert_epi16(SIMD_type arg1, int arg2, int pos)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"signed_int(32)", "pos":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},

	"bitblock_load_aligned":\
	{
		"signature":["SIMD_type _mm_load_si128(SIMD_type* arg1)"],
		"args_type":{"arg1":"SIMD_type*"},
		"return_type":"SIMD_type",
		"fws":[[128]],
	},
	"bitblock_store_aligned":\
	{
		"signature":["void _mm_store_si128(SIMD_type* arg2, SIMD_type arg1)"],
		"args_type":{"arg2":"SIMD_type*", "arg1":"SIMD_type"},
		"return_type":"void",
		"fws":[[128]],
	},
	"bitblock_load_unaligned":\
	{
		"signature":["SIMD_type _mm_loadu_si128(SIMD_type* arg1)"],
		"args_type":{"arg1":"SIMD_type*"},
		"return_type":"SIMD_type",
		"fws":[[128]],
	},
	"bitblock_store_unaligned":\
	{
		"signature":["void _mm_storeu_si128(SIMD_type* arg2, SIMD_type arg1)"],
		"args_type":{"arg2":"SIMD_type*", "arg1":"SIMD_type"},
		"return_type":"void",
		"fws":[[128]],
	},
	"_mm_sll_epi64":\
	{
		"signature":["SIMD_type _mm_sll_epi64(SIMD_type arg1, SIMD_type sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[64]],
	},
	"_mm_slli_si128":\
	{
		"signature":["SIMD_type _mm_slli_si128(SIMD_type arg1, int sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[128]],
	},
	"_mm_srl_epi64":\
	{
		"signature":["SIMD_type _mm_srl_epi64(SIMD_type arg1, SIMD_type sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[64]],
	},
	"_mm_srli_si128":\
	{
		"signature":["SIMD_type _mm_srli_si128(SIMD_type arg1, int sh)"],
		"args_type":{"arg1":"SIMD_type", "sh":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[128]],
	},
	"_mm_set_epi32":\
	{
		"signature":["SIMD_type _mm_set_epi32(int val1, int val2, int val3, int val4)"],
		"args_type":{"val1":"signed_int(32)", "val2":"signed_int(32)", "val3":"signed_int(32)", "val4":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"_mm_set1_epi32":\
	{
		"signature":["SIMD_type _mm_set1_epi32(int val1)"],
		"args_type":{"val1":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[32]],
	},
	"_mm_cvtsi32_si128":\
	{
		"signature":["SIMD_type _mm_cvtsi32_si128(int val1)"],
		"args_type":{"val1":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[128]],
	},
	"_mm_shufflehi_epi16":\
	{
		"signature":["SIMD_type _mm_shufflehi_epi16(SIMD_type arg1, int msk)"],
		"args_type":{"arg1":"SIMD_type", "msk":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"_mm_shufflelo_epi16":\
	{
		"signature":["SIMD_type _mm_shufflelo_epi16(SIMD_type arg1, int msk)"],
		"args_type":{"arg1":"SIMD_type", "msk":"signed_int(32)"},
		"return_type":"SIMD_type",
		"fws":[[16]],
	},
	"_mm_sad_epu8":\
	{
		"signature":["SIMD_type _mm_sad_epu8(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8]],
	},
	"_mm_extract_epi16":\
	{
		"signature":["int _mm_extract_epi16(SIMD_type arg1, int pos)"],
		"args_type":{"arg1":"SIMD_type", "pos":"signed_int(32)"},
		"return_type":"signed_int(32)",
		"fws":[[16]],
	},
	"_mm_movemask_ps":\
	{
		"signature":["int _mm_movemask_ps(__m128 arg1)"],
		"args_type":{"arg1":"__m128"},
		"return_type":"signed_int(32)",
		"fws":[[32]],
	},
	"_mm_movemask_pd":\
	{
		"signature":["int _mm_movemask_pd(__m128 arg1)"],
		"args_type":{"arg1":"__m128"},
		"return_type":"signed_int(32)",
		"fws":[[64]],
	},
}
