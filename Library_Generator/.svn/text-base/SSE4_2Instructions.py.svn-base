
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *
from SSE4_1Instructions import SSE4_1BuiltIns

SSE4_2BuiltIns = dict(SSE4_1BuiltIns.items() +\
{
	"simd_gt":\
	{
		"signature":["SIMD_type _mm_cmpgt_epi$fw$(SIMD_type arg1, SIMD_type arg2)"],
		"args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
		"return_type":"SIMD_type",
		"fws":[[8, 16, 32, 64]],
	},
}.items())
