

# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *
from Utility import configure

LLVMBuiltIns = \
{
	"simd_and":\
	{
		"signature":["SIMD_type llvm_and_128(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_or":\
	{
		"signature":["SIMD_type llvm_or_128(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_xor":\
	{
		"signature":["SIMD_type llvm_xor_128(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[1]],
	},
	"simd_add":\
	{
		"signature":["SIMD_type llvm_add_$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},
	"simd_sub":\
	{
		"signature":["t llvm_sub_$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},
	"simd_umult":\
	{
		"signature":["t llvm_mul_$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},	
	"simd_mult":\
	{
		"signature":["t llvm_mul_$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},
	"simd_eq":\
	{
		"signature":["t llvm_icmp_eq_$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},
	"simd_gt":\
	{
		"signature":["t llvm_icmp_sgt_$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},
	"simd_ugt":\
	{
		"signature":["t llvm_icmp_ugt_$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},
	"simd_lt":\
	{
		"signature":["t llvm_icmp_slt_$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},
	"simd_ult":\
	{
		"signature":["t llvm_icmp_ult_$fw$(t arg1, t arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},	
	"simd_vsrl":\
	{
		"signature":["t llvm_lshr_$fw$(t arg1, __m128i shift_mask)"],
		"args_type":{"arg1":"SIMD_type", "shift_mask":"__m128i"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},	
	"simd_vsra":\
	{
		"signature":["t llvm_ashr_$fw$(t arg1, __m128i shift_mask)"],
		"args_type":{"arg1":"SIMD_type", "shift_mask":"__m128i"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},
	"simd_vsll":\
	{
		"signature":["t llvm_shl_$fw$(t arg1, t shift_mask)"],
		"args_type":{"arg1":"SIMD_type", "shift_mask":"__m128i"},
		"return_type":"SIMD_type",
		"fws":[[2, 4, 8, 16, 32, 64, 128]],
	},	
	"bitblock_load_aligned":\
	{
		"signature":["SIMD_type llvm_load_aligned(SIMD_type* arg1)"],
		"args_type":{"arg1":"SIMD_type*"},
		"return_type":"SIMD_type",
		"fws":[[128]],
	},
	"bitblock_store_aligned":\
	{
		"signature":["void llvm_store_aligned(SIMD_type arg1, SIMD_type* arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type*"},
		"return_type":"void",
		"fws":[[128]],
	},
	"bitblock_load_unaligned":\
	{
		"signature":["SIMD_type llvm_load_unaligned(SIMD_type* arg1)"],
		"args_type":{"arg1":"SIMD_type*"},
		"return_type":"SIMD_type",
		"fws":[[128]],
	},
	"bitblock_store_unaligned":\
	{
		"signature":["void llvm_store_unaligned(SIMD_type arg1, SIMD_type* arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type*"},
		"return_type":"void",
		"fws":[[128]],
	}
}

