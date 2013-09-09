
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from Utility import configure

def StrategyPool(curRegSize):
	strategies = \
	{
		"add1":\
		{
		"body":r'''return simd_xor(arg1, arg2)''',
		"Ops":["simd_add", "simd_sub"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		"umin1":\
		{
		"body":r'''return simd_and(arg1, arg2)''',
		"Ops":["simd_max", "simd_umin", "simd_mult"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		"umax1":\
		{
		"body":r'''return simd_or(arg1, arg2)''',
		"Ops":["simd_min", "simd_umax"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		"ult1":\
		{
		"body":r'''return simd_andc(arg2, arg1)''',
		"Ops":["simd_ult", "simd_gt"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		"ugt1":\
		{
		"body":r'''return simd_andc(arg1, arg2)''',
		"Ops":["simd_lt", "simd_ugt"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},

		"eq1":\
		{
		"body":r'''return simd_not(simd_xor(arg1, arg2))''',
		"Ops":["simd_eq"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		"ctz1":\
		{
		"body":r'''return simd_not(arg1)''',
		"Ops":["simd_ctz"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},

		"unsigned_predicate_using_signed":\
		{
		"body":r'''high_bit = simd_constant(fw, 1<<(fw-1))
return simd_signed_op(fw, simd_xor(arg1, high_bit), simd_xor(arg2, high_bit))''',
		"Ops":["simd_ugt", "simd_ult"],
		"Fws":range(1, 64+1),
		"Platforms":[configure.ALL],
		},

		"signed_predicate_using_unsigned":\
		{
		"body":r'''high_bit = simd_constant(fw, 1<<(fw-1))
return simd_uop(fw, simd_xor(arg1, high_bit), simd_xor(arg2, high_bit))''',
		"Ops":["simd_gt", "simd_lt"],
		"Fws":range(1, 64+1),
		"Platforms":[configure.ALL],
		},

		"unsigned_value_using_signed":\
		{
		"body":r'''high_bit = simd_constant(fw, 1<<(fw-1))
return simd_xor(simd_signed_op(fw, simd_xor(arg1, high_bit), simd_xor(arg2, high_bit)), high_bit)''',
		"Ops":["simd_umax", "simd_umin"],
		"Fws":range(1, 64+1),
		"Platforms":[configure.ALL],
		},

		"signed_value_using_unsigned":\
		{
		"body":r'''high_bit = simd_constant(fw, 1<<(fw-1))
return simd_xor(simd_uop(fw, simd_xor(arg1, high_bit), simd_xor(arg2, high_bit)), high_bit)''',
		"Ops":["simd_max", "simd_min"],
		"Fws":range(1, 64+1),
		"Platforms":[configure.ALL],
		},

		"in_place_if_doubling":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(2*fw), simd_op(2*fw, arg1, simd_and(simd_himask(2*fw), arg2)), simd_op(2*fw, arg1, arg2))''',
		"Ops":["simd_add", "simd_sub"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"in_place_hmask_post_lmask_pre":\
		{
		"body":r'''
return simd_or(simd_and(simd_himask(2*fw), simd_op(2*fw, arg1, arg2)), simd_op(2*fw, simd_and(simd_lomask(2*fw), arg1), simd_and(simd_lomask(2*fw), arg2)))''',
		"Ops":["simd_umax", "simd_umin"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"in_place_or_doubling":\
		{
		"body":r'''
return simd_or(simd_and(simd_himask(2*fw), simd_op(2*fw, simd_and(simd_himask(2*fw), arg1), simd_and(simd_himask(2*fw), arg2))), simd_and(simd_lomask(2*fw), simd_op(2*fw, simd_and(simd_lomask(2*fw), arg1), simd_and(simd_lomask(2*fw), arg2))))''',
		"Ops":["simd_eq", "simd_ugt", "simd_ult", "simd_umax", "simd_umin"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"in_place_sign_extension_doubling":\
		{
		"body":r'''
return simd_or(simd_and(simd_himask(2*fw), simd_op(2*fw, simd_and(simd_himask(2*fw), arg1), simd_and(simd_himask(2*fw), arg2))), simd_and(simd_op(2*fw, simd_or(simd_and(arg1, simd_lomask(2*fw)), simd_sub(2*fw, simd_constant(2*fw, 0), simd_and(simd_constant(2*fw, 1<<(fw-1)), arg1))), simd_or(simd_and(arg2, simd_lomask(2*fw)), simd_sub(2*fw, simd_constant(2*fw, 0), simd_and(simd_constant(2*fw, 1<<(fw-1)), arg2)))), simd_lomask(2*fw)))''',
		"Ops":["simd_gt", "simd_lt", "simd_max", "simd_min"],
		"Fws":range(2, 32+1),
		"Platforms":[configure.ALL],
		},
	
		"shift_if_doubling":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(2*fw), simd_op(2*fw, simd_and(simd_himask(2*fw), arg1), simd_and(simd_himask(2*fw), arg2)), simd_srli(2*fw, fw, simd_op(2*fw, simd_slli(2*fw, fw, arg1), simd_slli(2*fw, fw, arg2))))''',
		"Ops":["simd_gt", "simd_lt", "simd_max", "simd_min"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"predicate_shift_if_doubling_gt":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(2*fw), simd_op(2*fw, simd_and(simd_himask(2*fw), arg1), arg2), simd_op(2*fw, simd_slli(2*fw, fw, arg1), simd_slli(2*fw, fw, arg2)))''',
		"Ops":["simd_gt", "simd_ugt"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"predicate_shift_if_doubling_lt":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(2*fw), simd_op(2*fw, arg1, simd_and(simd_himask(2*fw), arg2)), simd_op(2*fw, simd_slli(2*fw, fw, arg1), simd_slli(2*fw, fw, arg2)))''',
		"Ops":["simd_lt", "simd_ult"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"predicate_if_doubling_ugt":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(2*fw), simd_op(2*fw, simd_and(simd_himask(2*fw), arg1), arg2), simd_op(2*fw, simd_andc(arg1, simd_himask(2*fw)), simd_andc(arg2, simd_himask(2*fw))))''',
		"Ops":["simd_ugt"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"predicate_if_doubling_ult":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(2*fw), simd_op(2*fw, arg1, simd_and(simd_himask(2*fw), arg2)), simd_op(2*fw, simd_andc(arg1, simd_himask(2*fw)), simd_andc(arg2, simd_himask(2*fw))))''',
		"Ops":["simd_ult"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"umult_doubling":\
		{
		"body":r'''
loMask = simd_lomask(2*fw)
tmpAns1 = simd_umult(2*fw, simd_and(loMask, arg1), simd_and(loMask, arg2))
tmpAns2 = simd_umult(2*fw, simd_and(loMask, simd_srli(4*fw, 2*fw, arg1)), simd_and(loMask, simd_srli(4*fw, 2*fw, arg2)))
return simd_or(tmpAns1, simd_slli(4*fw, 2*fw, tmpAns2))''',
		"Ops":["simd_umult"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"mult_doubling":\
		{
		"body":r'''
loMask = simd_lomask(2*fw)
tmpAns1 = simd_mult(2*fw, simd_and(loMask, arg1), simd_and(loMask, arg2))
tmpAns2 = simd_mult(2*fw, simd_srli(2*fw, fw, arg1), simd_srli(2*fw, fw, arg2))
return simd_ifh(1, loMask, tmpAns1, simd_slli(2*fw, fw, tmpAns2))''',
		"Ops":["simd_mult"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"umult_halving":\
		{
		"body":r'''
loMask1 = simd_lomask(2*fw)
arg11 = simd_and(arg1, loMask1)
arg22 = simd_and(arg2, loMask1)
loMask2 = simd_lomask(fw)
arg1_low = simd_and(arg11, loMask2)
arg1_high = simd_srli(fw, fw/2, arg11)
arg2_low = simd_and(arg22, loMask2)
arg2_high = simd_srli(fw, fw/2, arg22)
tmpAns1 = simd_umult(fw/2, arg1_low, arg2_low)
tmpAns2 = simd_slli(2*fw, fw/2, simd_umult(fw/2, arg1_low, arg2_high))
tmpAns3 = simd_slli(2*fw, fw/2, simd_umult(fw/2, arg1_high, arg2_low))
tmpAns4 = simd_slli(2*fw, fw, simd_umult(fw/2, arg1_high, arg2_high))
return simd_add(2*fw, tmpAns1, simd_add(2*fw, tmpAns2, simd_add(2*fw, tmpAns3, tmpAns4)))''',
		"Ops":["simd_umult"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"mult_halving":\
		{
		"body":r'''
loMask = simd_lomask(fw)
arg1_low = simd_and(arg1, loMask)
arg1_high = simd_srli(fw, fw/2, arg1)
arg2_low = simd_and(arg2, loMask)
arg2_high = simd_srli(fw, fw/2, arg2)
tmpAns1 = simd_umult(fw/2, arg1_low, arg2_low)
tmpAns2 = simd_slli(fw, fw/2, simd_umult(fw/2, arg1_low, arg2_high))
tmpAns3 = simd_slli(fw, fw/2, simd_umult(fw/2, arg1_high, arg2_low))
return simd_add(fw, tmpAns1, simd_add(fw, tmpAns2, tmpAns3))''',
		"Ops":["simd_mult"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"mult_32_using_Multiply_Packed_Signed_Dword_Integers":\
		{
		"body":r'''
return simd_or(simd_slli(2*fw, fw, _mm_mul_epi32(simd_srli(2*fw, fw, arg1), simd_srli(2*fw, fw, arg2))), simd_and(simd_lomask(2*fw), _mm_mul_epi32(arg1, arg2)))''',
		"Ops":["simd_mult"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"add_halving":\
		{
		"body":r'''
ans = simd_add(fw/2, arg1, arg2)
carryMask = simd_or(simd_and(arg1, arg2), simd_and(simd_xor(arg1, arg2), simd_not(ans)))
loMask = simd_lomask(fw)
carry = simd_slli(fw, 1, simd_and(carryMask, loMask))
return simd_ifh(1, loMask, ans, simd_add(fw/2, ans, carry))''',
		"Ops":["simd_add"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"add_another_halving":\
		{
		"body":r'''
partial = simd_add(fw/2, arg1, arg2)
carryMask = simd_or(simd_and(arg1, arg2), simd_andc(simd_xor(arg1, arg2), partial))
carry = simd_slli(fw, fw/2, simd_srli(fw/2, fw/2-1, carryMask))
return simd_add(fw/2, partial, carry)''',
		"Ops":["simd_add"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},

		"sub_halving":\
		{
		"body":r'''
ans = simd_sub(fw/2, arg1, arg2)
borrowMask = simd_or(simd_andc(arg2, arg1), simd_and(simd_not(simd_xor(arg1, arg2)), ans))
loMask = simd_lomask(fw)
borrow = simd_slli(fw, 1, simd_and(borrowMask, loMask))
return simd_ifh(1, loMask, ans, simd_sub(fw/2, ans, borrow))''', 
		"Ops":["simd_sub"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"sub_another_halving":\
		{
		"body":r'''
partial = simd_sub(fw/2, arg1, arg2)
borrowMask = simd_or(simd_andc(arg2, arg1), simd_andc(partial, simd_xor(arg1, arg2)))
borrow = simd_slli(fw, fw/2, simd_srli(fw/2, fw/2-1, borrowMask))
return simd_sub(fw/2, partial, borrow)''',
		"Ops":["simd_sub"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},

		"eq_halving":\
		{
		"body":r'''
tmpAns = simd_eq(fw/2, arg1, arg2)
loMask = simd_and(tmpAns, simd_srli(fw, fw/2, tmpAns))
hiMask = simd_slli(fw, fw/2, loMask)
return simd_or(loMask, hiMask)''',
		"Ops":["simd_eq"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"gt_lt_halving":\
		{
		"body":r'''
hiAns = simd_op(fw/2, arg1, arg2)
loAns = simd_uop(fw/2, arg1, arg2)
mask = simd_and(loAns, simd_srli(fw, fw/2, simd_eq(fw/2, arg1, arg2)))
mask = simd_or(mask, simd_slli(fw, fw/2, mask))
return simd_or(simd_srai(fw, fw/2, hiAns), mask)''',
		"Ops":["simd_gt", "simd_lt"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},

		"ugt_ult_halving":\
		{
		"body":r'''
tmpAns = simd_op(fw/2, arg1, arg2)
mask = simd_and(tmpAns, simd_srli(fw, fw/2, simd_eq(fw/2, arg1, arg2)))
mask = simd_or(mask, simd_slli(fw, fw/2, mask))
return simd_or(simd_srai(fw, fw/2, tmpAns), mask)''',
		"Ops":["simd_ugt", "simd_ult"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"max_min_halving":\
		{
		"body":r'''
hiAns = simd_op(fw/2, arg1, arg2)
loAns = simd_uop(fw/2, arg1, arg2)
eqMask1 = simd_srli(fw, fw/2, simd_eq(fw/2, hiAns, arg1))
eqMask2 = simd_srli(fw, fw/2, simd_eq(fw/2, hiAns, arg2))
return simd_ifh(1, simd_himask(fw), hiAns, simd_ifh(1, eqMask1, simd_ifh(1, eqMask2, loAns, arg1), arg2))''',
		"Ops":["simd_max", "simd_min"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"max_gt_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_gt(fw, arg1, arg2), arg1, arg2)''',
		"Ops":["simd_max"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"max_lt_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_lt(fw, arg1, arg2), arg2, arg1)''',
		"Ops":["simd_max"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"min_lt_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_lt(fw, arg1, arg2), arg1, arg2)''',
		"Ops":["simd_min"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"min_gt_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_gt(fw, arg1, arg2), arg2, arg1)''',
		"Ops":["simd_min"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},

		"umax_umin_halving":\
		{
		"body":r'''
tmpAns = simd_op(fw/2, arg1, arg2)
eqMask1 = simd_srli(fw, fw/2, simd_eq(fw/2, tmpAns, arg1))
eqMask2 = simd_srli(fw, fw/2, simd_eq(fw/2, tmpAns, arg2))
return simd_ifh(1, simd_himask(fw), tmpAns, simd_ifh(1, eqMask1, simd_ifh(1, eqMask2, tmpAns, arg1), arg2))''',
		"Ops":["simd_umax", "simd_umin"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},

		"srai_halving":\
		{
		"body":r'''
return simd_or(simd_and(simd_himask(fw), simd_srai(fw/2, sh if sh<fw/2 else fw/2, arg1)), simd_srli(fw, sh, arg1) if sh<=fw/2 else simd_srai(fw/2, sh-(fw/2), simd_srli(fw, fw/2, arg1)))''',
		"Ops":["simd_srai"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"ugt_blend":\
		{
		"body":r'''
return simd_and(simd_srai(fw, fw-1, simd_or(simd_and(arg1, simd_not(arg2)), simd_and(simd_not(simd_xor(arg1, arg2)), simd_not(simd_sub(fw, arg1, arg2))))), simd_not(simd_eq(fw, arg1, arg2)))''',
		"Ops":["simd_ugt"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"lt_blend":\
		{
		"body":r'''
return simd_and(simd_not(simd_gt(fw, arg1, arg2)), simd_not(simd_eq(fw, arg1, arg2)))''',
		"Ops":["simd_lt"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"ult_blend":\
		{
		"body":r'''
return simd_and(simd_srai(fw, fw-1, simd_or(simd_and(simd_not(arg1), arg2), simd_and(simd_not(simd_xor(arg1, arg2)), simd_sub(fw, arg1, arg2)))), simd_not(simd_eq(fw, arg1, arg2)))''',
		"Ops":["simd_ult"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"abs_blend":\
		{
		"body":r'''
gtMask = simd_gt(fw, arg1, simd_constant(fw, 0))
return simd_ifh(1, gtMask, arg1, simd_sub(fw, gtMask, arg1))''',
		"Ops":["simd_abs"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"abs_halving":\
		{
		"body":r'''
eqMask = simd_eq(fw, simd_ifh(1, simd_himask(fw), simd_abs(fw/2, arg1), arg1), arg1)
return simd_ifh(1, eqMask, arg1, simd_sub(fw, eqMask, arg1))''',
		"Ops":["simd_abs"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"neg_blend":\
		{
		"body":r'''
return simd_sub(fw, simd_constant(fw, 0), arg1)''',
		"Ops":["simd_neg"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"neg_8_Packed SIGN":\
		{
		"body":r'''
return _mm_sign_epi8(arg1, simd_constant(fw, -1))''',
		"Ops":["simd_neg"],
		"Fws":[8],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"neg_16_Packed SIGN":\
		{
		"body":r'''
return _mm_sign_epi16(arg1, simd_constant(fw, -1))''',
		"Ops":["simd_neg"],
		"Fws":[16],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"neg_32_Packed SIGN":\
		{
		"body":r'''
return _mm_sign_epi32(arg1, simd_constant(fw, -1))''',
		"Ops":["simd_neg"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
			
		"srai_2_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_eq(32, simd_constant(32, sh), simd_constant(32, 0)), arg1, simd_or(simd_and(simd_himask(2), arg1), simd_srli(fw, 1, arg1)))''',
		"Ops":["simd_srai"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"srai_2_blend_1":\
		{
		"body":r'''
return arg1 if sh==0 else simd_or(simd_and(simd_himask(2), arg1), simd_srli(fw, 1, arg1))''',
		"Ops":["simd_srai"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"srai_blend_subtract":\
		{
		"body":r'''
tmp = simd_srli(fw, (fw-1 if sh>=fw else 0 if sh<0 else sh), arg1)
return simd_or(tmp, simd_sub(fw, simd_constant(fw, 0), simd_and(simd_constant(fw, 1<<(fw-(fw-1 if sh>=fw else 0 if sh<0 else sh)-1)), tmp)))''',
		"Ops":["simd_srai"],
		"Fws":[2, 4, 8, 16, 32],
		"Platforms":[configure.ALL],
		},
		
		"srai_blend_substract_1":\
		{
		"body":r'''
tmp = simd_srli(fw, (fw-1 if sh>=fw else 0 if sh<0 else sh), arg1)
return simd_or(tmp, simd_sub(fw, simd_constant(fw, 0), simd_and(simd_slli(fw, (fw-(fw-1 if sh>=fw else 0 if sh<0 else sh)-1), simd_constant(fw, 1)), tmp)))''',
		"Ops":["simd_srai"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},

		"srai_8_neon":\
		{
		"body":r'''
return arg1 if sh==0 else IDISA_CASTING("SIMD_type", vshrq_n_s8(arg1, sh))''',
		"Ops":["simd_srai"],
		"Fws":[8],
		"Platforms":[configure.NEON],
		},
		
		"srai_16_neon":\
		{
		"body":r'''
return arg1 if sh==0 else IDISA_CASTING("SIMD_type", vshrq_n_s16(arg1, sh))''',
		"Ops":["simd_srai"],
		"Fws":[16],
		"Platforms":[configure.NEON],
		},
		
		"srai_32_neon":\
		{
		"body":r'''
return arg1 if sh==0 else IDISA_CASTING("SIMD_type", vshrq_n_s32(arg1, sh))''',
		"Ops":["simd_srai"],
		"Fws":[32],
		"Platforms":[configure.NEON],
		},
		
		"srai_64_neon":\
		{
		"body":r'''
return arg1 if sh==0 else IDISA_CASTING("SIMD_type", vshrq_n_s64(arg1, sh))''',
		"Ops":["simd_srai"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},
		
		"slli_increment_blend":\
		{
		"body":r'''
return simd_and(simd_slli(32, sh, arg1), simd_constant(fw, (((1<<fw)-1)<<sh)&((1<<fw)-1)))''',
		"Ops":["simd_slli"],
		"Fws":[2, 4, 8],
		"Platforms":[configure.ALL],
		},
	
		"vsll_64_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(128), _mm_sll_epi64(arg1, simd_and(_mm_srli_si128(shift_mask, 8), _mm_cvtsi32_si128(63))), _mm_sll_epi64(arg1, simd_and(shift_mask, _mm_cvtsi32_si128(63))))''',
		"Ops":["simd_vsll"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"vsll_128_blend":\
		{
		"body":r'''
shift = simd_and(shift_mask, _mm_cvtsi32_si128(127))
return simd_or(_mm_sll_epi64(arg1, shift), simd_or(_mm_slli_si128(_mm_sll_epi64(arg1, simd_sub(32, shift, _mm_cvtsi32_si128(64))), 8),  _mm_slli_si128(_mm_srl_epi64(arg1, simd_sub(32, _mm_cvtsi32_si128(64), shift)), 8)))''',
		"Ops":["simd_vsll"],
		"Fws":[128],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

# doesn't work...		
#		"sll_64_neon":\
#		{
#		"body":r'''
#shift = IDISA_CASTING("int64x2_t", simd_or(shift_mask, vextq_u64(shift_mask, shift_mask, 1)))
#return vshlq_u64(arg1, shift)''',
#		"Ops":["simd_sll"],
#		"Fws":[64],
#		"Platforms":[configure.NEON],
#		},
		
		"slli_128_blend":\
		{
		"body":r'''
return	_mm_slli_si128(arg1, sh/8) if (sh%8==0) else (simd_slli(64, (sh)&0x3F, _mm_slli_si128(arg1, 8)) if (sh>=64) else simd_or(simd_slli(64, sh, arg1), _mm_slli_si128(simd_srli(64, (128-sh)&0x3F, arg1), 8)))''',
		"Ops":["simd_slli"],
		"Fws":[128],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"slli_128_avx":\
		{
		"body":r'''
return avx_byte_shift_left(arg1, (sh)/8) if (sh%8==0) else (simd_slli(64, (sh)&0x3F, avx_byte_shift_left(arg1, 8)) if (sh>=64) else simd_or(simd_slli(64, sh, arg1), avx_byte_shift_left(simd_srli(64, (128-sh)&0x3F, arg1), 8)))''',
		"Ops":["simd_slli"],
		"Fws":[128],
		"Platforms":configure.AVX_SERIES,
		},

		# This strategy is wrong. Together with simd_srli_256, when sh = 0
		"slli_256_avx":\
		{
		"body":r'''
return simd_or(simd_slli(128, sh, arg1), avx_move_lo128_to_hi128(simd_srli(128, (128-sh), arg1))) if (sh<128) else simd_slli(128, sh-128, avx_move_lo128_to_hi128(arg1))''',
		"Ops":["simd_slli"],
		"Fws":[256],
		"Platforms":configure.AVX_SERIES,
		},

		"slli_8_neon":\
		{
		"body":r'''
return simd_constant(32, 0) if sh==8 else IDISA_CASTING("SIMD_type", vshlq_n_u8(arg1, sh))''',
		"Ops":["simd_slli"],
		"Fws":[8],
		"Platforms":[configure.NEON],
		},
		
		"slli_16_neon":\
		{
		"body":r'''
return simd_constant(32, 0) if sh==16 else IDISA_CASTING("SIMD_type", vshlq_n_u16(arg1, sh))''',
		"Ops":["simd_slli"],
		"Fws":[16],
		"Platforms":[configure.NEON],
		},
		
		"slli_32_neon":\
		{
		"body":r'''
return simd_constant(32, 0) if sh==32 else IDISA_CASTING("SIMD_type", vshlq_n_u32(arg1, sh))''',
		"Ops":["simd_slli"],
		"Fws":[32],
		"Platforms":[configure.NEON],
		},
		
		"slli_64_neon":\
		{
		"body":r'''
return simd_constant(32, 0) if sh==64 else IDISA_CASTING("SIMD_type", vshlq_n_u64(arg1, sh))''',
		"Ops":["simd_slli"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},
		
		"slli_128_neon":\
		{
		"body":r'''
return simd_constant(32, 0) if sh==128 else (simd_slli(64, (sh)&0x3F, neon_shift_left_64_bits(arg1)) if sh>=64 else simd_or(neon_shift_left_64_bits(simd_srli(64, 64 - sh, arg1)), simd_slli(64, sh, arg1)))''',
		"Ops":["simd_slli"],
		"Fws":[128],
		"Platforms":[configure.NEON],
		},
		
		"vsrl_64_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(128), _mm_srl_epi64(arg1, simd_and(_mm_srli_si128(shift_mask, 8), _mm_cvtsi32_si128(63))), _mm_srl_epi64(arg1, simd_and(shift_mask, _mm_cvtsi32_si128(63))))''',
		"Ops":["simd_vsrl"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"vsrl_128_blend":\
		{
		"body":r'''
shift = simd_and(shift_mask, _mm_cvtsi32_si128(127))
return simd_or(_mm_srl_epi64(arg1, shift), simd_or(_mm_srli_si128(_mm_srl_epi64(arg1, simd_sub(32, shift, _mm_cvtsi32_si128(64))), 8),  _mm_srli_si128(_mm_sll_epi64(arg1, simd_sub(32, _mm_cvtsi32_si128(64), shift)), 8)))''',
		"Ops":["simd_vsrl"],
		"Fws":[128],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		# TODO checking
		"srl_256_blend":\
		{
		"body":r'''
shift = _mm_cvtsi128_si32(avx_select_lo128(shift_mask))
n = shift / 64
arg2 = mvmd_srli(64, 1, arg1) if n==1 else (mvmd_srli(64, 2, arg1) if n==2 else (mvmd_srli(64, 3, arg1) if n==3 else arg1))
return simd_constant(32, 0) if n>=4 else (simd_or(_mm256_srl_epi64(arg2, _mm_cvtsi32_si128(shift & 63)), mvmd_srli(64, 1, _mm256_sll_epi64(arg2, _mm_cvtsi32_si128(64 - (shift & 63))))) if (shift & 63) > 0 else arg2)		
		''',
		"Ops":["simd_srl"],
		"Fws":[256],
		"Platforms":[configure.AVX2],
		},

		# TODO checking
		"sll_256_blend":\
		{
		"body":r'''
shift = _mm_cvtsi128_si32(avx_select_lo128(shift_mask))
n = shift / 64
arg2 = mvmd_slli(64, 1, arg1) if n==1 else (mvmd_slli(64, 2, arg1) if n==2 else (mvmd_slli(64, 3, arg1) if n==3 else arg1))
return simd_constant(32, 0) if n>=4 else (simd_or(_mm256_sll_epi64(arg2, _mm_cvtsi32_si128(shift & 63)), mvmd_slli(64, 1, _mm256_srl_epi64(arg2, _mm_cvtsi32_si128(64 - (shift & 63))))) if (shift & 63) > 0 else arg2)		
		''',
		"Ops":["simd_sll"],
		"Fws":[256],
		"Platforms":[configure.AVX2],
		},
	
		"srli_increment_blend":\
		{
		"body":r'''
return simd_and(simd_srli(32, sh, arg1), simd_constant(fw, ((1<<fw)-1)>>sh))''',
		"Ops":["simd_srli"],
		"Fws":[2, 4, 8],
		"Platforms":[configure.ALL],
		},
	
		"srli_128_blend":\
		{
		"body":r'''
return	_mm_srli_si128(arg1, sh/8) if (sh%8==0) else (simd_srli(64, (sh)&0x3F, _mm_srli_si128(arg1, 8)) if (sh>=64) else simd_or(simd_srli(64, sh, arg1), _mm_srli_si128(simd_slli(64, (128-sh)&0x3F, arg1), 8)))''',
		"Ops":["simd_srli"],
		"Fws":[128],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"srli_128_avx":\
		{
		"body":r'''
return avx_byte_shift_right(arg1, (sh)/8) if (sh%8==0) else (simd_srli(64, (sh)&0x3F, avx_byte_shift_right(arg1, 8)) if (sh>=64) else simd_or(simd_srli(64, sh, arg1), avx_byte_shift_right(simd_slli(64, (128-sh)&0x3F, arg1), 8)))''',
		"Ops":["simd_srli"],
		"Fws":[128],
		"Platforms":configure.AVX_SERIES,
		},

		"srli_256_avx":\
		{
		"body":r'''
return simd_or(simd_srli(128, sh, arg1), simd_slli(128, (128-sh), IDISA_CASTING("SIMD_type", _mm256_castsi128_si256(avx_select_hi128(arg1))))) if (sh<128) else simd_srli(128, (sh - 128), avx_move_hi128_to_lo128(arg1))''', 
		"Ops":["simd_srli"],
		"Fws":[256],
		"Platforms":configure.AVX_SERIES,
		},

		"srli_8_neon":\
		{
		"body":r'''
return arg1 if sh==0 else IDISA_CASTING("SIMD_type", vshrq_n_u8(arg1, sh))''',
		"Ops":["simd_srli"],
		"Fws":[8],
		"Platforms":[configure.NEON],
		},
		
		"srli_16_neon":\
		{
		"body":r'''
return arg1 if sh==0 else IDISA_CASTING("SIMD_type", vshrq_n_u16(arg1, sh))''',
		"Ops":["simd_srli"],
		"Fws":[16],
		"Platforms":[configure.NEON],
		},
		
		"srli_32_neon":\
		{
		"body":r'''
return arg1 if sh==0 else IDISA_CASTING("SIMD_type", vshrq_n_u32(arg1, sh))''',
		"Ops":["simd_srli"],
		"Fws":[32],
		"Platforms":[configure.NEON],
		},
		
		"srli_64_neon":\
		{
		"body":r'''
return arg1 if sh==0 else IDISA_CASTING("SIMD_type", vshrq_n_u64(arg1, sh))''',
		"Ops":["simd_srli"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},
		
		"srli_128_neon":\
		{
		"body":r'''
return neon_shift_right_64_bits(arg1) if sh==64 else (simd_srli(64, (sh)&0x3F, neon_shift_right_64_bits(arg1)) if sh>64 else simd_or(neon_shift_right_64_bits(simd_slli(64, 64 - sh, arg1)), simd_srli(64, sh, arg1)))''',
		"Ops":["simd_srli"],
		"Fws":[128],
		"Platforms":[configure.NEON],
		},
	  
		"not_blend":\
		{
		"body":r'''
return simd_xor(arg1, simd_constant(32, -1))''',
		"Ops":["simd_not"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
	
		"nor_blend":\
		{
		"body":r'''
return simd_not(simd_or(arg1, arg2))''',
		"Ops":["simd_nor"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		
		"popcount_1_blend":\
		{
		"body":r'''
return arg1''',
		"Ops":["simd_popcount"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		
		"popcount_halving":\
		{
		"body":r'''
return simd_add_hl(fw, simd_popcount(fw/2, arg1))''',
		"Ops":["simd_popcount"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"popcount_regSize_blend":\
		{
		"body":r'''
tmpAns = simd_popcount(curRegSize/2, arg1)
return simd_add(curRegSize/2, simd_and(tmpAns, simd_lomask(curRegSize)), simd_srli(curRegSize, curRegSize/2, tmpAns))''',
		"Ops":["simd_popcount"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},
		
		"popcount_64_sum_of_abs":\
		{
		"body":r'''
return _mm_sad_epu8(simd_popcount(8, arg1), simd_constant(8, 0))''',
		"Ops":["simd_popcount"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"popcount_64_avx":\
		{
		"body":r'''
tmpAns = simd_popcount(8, arg1)
return avx_general_combine256(_mm_sad_epu8(avx_select_hi128(tmpAns), _mm_set1_epi32(0)), _mm_sad_epu8(avx_select_lo128(tmpAns), _mm_set1_epi32(0)))''',
		"Ops":["simd_popcount"],
		"Fws":[64],
		"Platforms":configure.AVX_SERIES,
		},
		
		"ctz_blend":\
		{
		"body":r'''
return simd_popcount(fw, simd_andc(simd_sub(fw, arg1, simd_constant(fw, 1)), arg1))''',
		"Ops":["simd_ctz"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"ctz_1_blend":\
		{
		"body":r'''
return simd_not(arg1)''',
		"Ops":["simd_ctz"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
	
		"if_1":\
		{
		"body":r'''
return simd_or(simd_and(arg2, arg1), simd_andc(arg3, arg1))''',
		"Ops":["simd_ifh"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		
		"if_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_gt(fw, simd_constant(fw, 0), arg1), arg2, arg3)''',
		"Ops":["simd_ifh"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"if_havling":\
		{
		"body":r'''
return simd_ifh(fw/2, simd_ifh(1, simd_himask(fw), arg1, simd_srli(fw, fw/2, arg1)), arg2, arg3)''',
		"Ops":["simd_ifh"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"if_8_using_Variable_Blend_Packed_Bytes":\
		{
		"body":r'''
return _mm_blendv_epi8(arg3, arg2, arg1)''',
		"Ops":["simd_ifh"],
		"Fws":[8],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"if_curRegsize_avx":\
		{
		"body":r'''
ifMask = simd_eq(curRegSize, simd_constant(32, 0), simd_and(IDISA_CASTING("SIMD_type", _mm256_set_epi32(-2147483648, 0, 0, 0, 0, 0, 0, 0)), arg1))
return simd_ifh(1, ifMask, arg3, arg2)''',
		"Ops":["simd_ifh"],
		"Fws":[curRegSize],
		"Platforms":configure.AVX_SERIES,
		},

		"lomask_blend":\
		{
		"body":r'''
return simd_constant(fw, (1<<(fw/2))-1)''',
		"Ops":["simd_lomask"],
		"Fws":range(2, 32+1),
		"Platforms":[configure.ALL],
		},

		"lomask_64_blend":\
		{
		"body":r'''
return _mm_set_epi32(0,-1, 0, -1)''',
		"Ops":["simd_lomask"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"lomask_64_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(0, -1, 0, -1, 0, -1, 0, -1))''',
		"Ops":["simd_lomask"],
		"Fws":[64],
		"Platforms":configure.AVX_SERIES,
		},

		"lomask_64_neon":\
		{
		"body":r'''
return simd_constant(64, 4294967295L)''',
		"Ops":["simd_lomask"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},
	
		"lomask_128_blend":\
		{
		"body":r'''
return _mm_set_epi32(0, 0, -1, -1)''',
		"Ops":["simd_lomask"],
		"Fws":[128],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"lomask_128_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(0, 0, -1, -1, 0, 0,-1, -1))''',
		"Ops":["simd_lomask"],
		"Fws":[128],
		"Platforms":configure.AVX_SERIES,
		},

		"lomask_256_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(0, 0, 0, 0,-1,-1,-1,-1))''',
		"Ops":["simd_lomask"],
		"Fws":[256],
		"Platforms":configure.AVX_SERIES,
		},

		"lomask_128_neon":\
		{
		"body":r'''
return vsetq_lane_u64(-1, simd_constant(64, 0), 0)''',
		"Ops":["simd_lomask"],
		"Fws":[128],
		"Platforms":[configure.NEON],
		},

		"himask_blend":\
		{
		"body":r'''
return simd_constant(fw, (0-(1<<(fw/2)))&((1<<fw)-1))''',
		"Ops":["simd_himask"],
		"Fws":range(2, 16+1),
		"Platforms":[configure.ALL],
		},

		"himask_32_blend":\
		{
		"body":r'''
return simd_constant(fw, -65536)''',
		"Ops":["simd_himask"],
		"Fws":[32],
		"Platforms":[configure.ALL],
		},

		"himask_64_blend":\
		{
		"body":r'''
return _mm_set_epi32(-1, 0, -1, 0)''',
		"Ops":["simd_himask"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"himask_64_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(-1, 0, -1, 0, -1, 0, -1, 0))''',
		"Ops":["simd_himask"],
		"Fws":[64],
		"Platforms":configure.AVX_SERIES,
		},
		
		"himask_64_neon":\
		{
		"body":r'''
return simd_constant(64, 18446744069414584320L)''',
		"Ops":["simd_himask"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},

		"himask_128_blend":\
		{
		"body":r'''
return _mm_set_epi32(-1, -1, 0, 0)''',
		"Ops":["simd_himask"],
		"Fws":[128],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"himask_128_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(-1,-1, 0, 0,-1,-1, 0, 0))''',
		"Ops":["simd_himask"],
		"Fws":[128],
		"Platforms":configure.AVX_SERIES,
		},
	
		"himask_256_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(-1,-1,-1,-1, 0, 0, 0, 0))''',
		"Ops":["simd_himask"],
		"Fws":[256],
		"Platforms":configure.AVX_SERIES,
		},

		"himask_128_neon":\
		{
		"body":r'''
return vsetq_lane_u64(-1, simd_constant(64, 0), 1)''',
		"Ops":["simd_himask"],
		"Fws":[128],
		"Platforms":[configure.NEON],
		},
	
		"constant_doubling":\
		{
		"body":r'''
return simd_constant(2*fw, (val<<fw)|(val^(-1<<fw))) if val<0 else simd_constant(2*fw, (val<<fw)|val)
''',
		"Ops":["simd_constant"],
		"Fws":range(2, 16+1),
		"Platforms":[configure.ALL],
		},

		"constant_1_blend":\
		{
		#simd<1>::constant only accepts 0 or 1
		"body":r'''
return simd_constant(32, -1*val)
''',
		"Ops":["simd_constant"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},

		"constant_64_blend":\
		{
		"body":r'''
return _mm_set_epi32(val>>32, val, val>>32, val)
''',
		"Ops":["simd_constant"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"constant_64_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(val>>32, val, val>>32, val, val>>32, val, val>>32, val))''',
		"Ops":["simd_constant"],
		"Fws":[64],
		"Platforms":configure.AVX_SERIES,
		},
	
		"constant_128_blend":\
		{
		"body":r'''
return _mm_set_epi32(0, 0, val>>32, val)
''',
		"Ops":["simd_constant"],
		"Fws":[128],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"constant_128_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(0, 0, val>>32, val, 0, 0, val>>32, val))''',
		"Ops":["simd_constant"],
		"Fws":[128],
		"Platforms":configure.AVX_SERIES,
		},
	
		"constant_256_avx":\
		{
		"body":r'''
return IDISA_CASTING("SIMD_type", _mm256_set_epi32(0, 0, 0, 0, 0, 0, val>>32, val))''',
		"Ops":["simd_constant"],
		"Fws":[256],
		"Platforms":configure.AVX_SERIES,
		},
	
		"constant_128_neon":\
		{
		"body":r'''
return vsetq_lane_u64(0, simd_constant(64, val), 1)''',
		"Ops":["simd_constant"],
		"Fws":[128],
		"Platforms":[configure.NEON],
		},

		"hsimd_add_hl":\
		{
		"body":r'''
return simd_add(fw/2, hsimd_packh(fw, arg1, arg2), hsimd_packl(fw, arg1, arg2))
''',
		"Ops":["hsimd_add_hl"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"simd_add_hl_2":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), simd_and(simd_slli(16, 1, arg1), arg1), simd_xor(simd_srli(16, 1, arg1), arg1))''',
		"Ops":["simd_add_hl"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_add_hl_2_sub":\
		{
		"body":r'''
return simd_sub(16, arg1, simd_and(simd_lomask(fw), simd_srli(16, 1, arg1)))''',
		"Ops":["simd_add_hl"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_add_hl":\
		{
		"body":r'''
return simd_add(fw, simd_srli(fw, fw/2, arg1), simd_and(arg1, simd_lomask(fw)))
''',
		"Ops":["simd_add_hl"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"simd_add_hl_doubling":\
		{
		"body":r'''
return simd_add(2*fw, simd_srli(fw, fw/2, arg1), simd_and(arg1, simd_lomask(fw)))
''',
		"Ops":["simd_add_hl"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
#		"simd_add_hl_half_add":\
#		{
#		"body":r'''
#return simd_add(fw/2, simd_srli(fw, fw/2, arg1), simd_and(arg1, simd_lomask(fw)))''',
#		"Ops":["simd_add_hl"],
#		"Fws":range(4, curRegSize+1),
#		},
		
		"simd_add_hl_4_8":\
		{
		"body":r'''
return simd_add(fw, simd_and(simd_srli(16, fw/2, arg1), simd_lomask(fw)), simd_and(arg1, simd_lomask(fw)))
''',
		"Ops":["simd_add_hl"],
		"Fws":[4, 8],
		"Platforms":[configure.ALL],
		},
		
		"simd_xor_hl":\
		{
		"body":r'''
return simd_xor(simd_srli(fw, fw/2, arg1), simd_and(arg1, simd_lomask(fw)))
''',
		"Ops":["simd_xor_hl"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"hsimd_min_hl":\
		{
		"body":r'''
return simd_min(fw/2, hsimd_packh(fw, arg1, arg2), hsimd_packl(fw, arg1, arg2))''',
		"Ops":["hsimd_min_hl"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"hsimd_min_hl_regsize":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(curRegSize), simd_min(fw/2, arg1, simd_slli(fw, fw/2, arg1)), simd_min(fw/2, simd_srli(fw, fw/2, arg2), arg2))''',
		"Ops":["hsimd_min_hl"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},
		
		"hsimd_umin_hl":\
		{
		"body":r'''
return simd_umin(fw/2, hsimd_packh(fw, arg1, arg2), hsimd_packl(fw, arg1, arg2))''',
		"Ops":["hsimd_umin_hl"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"hsimd_umin_hl_regsize":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(curRegSize), simd_umin(fw/2, arg1, simd_slli(fw, fw/2, arg1)), simd_umin(fw/2, simd_srli(fw, fw/2, arg2), arg2))''',
		"Ops":["hsimd_umin_hl"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},

		"packh_blend":\
		{
		"body":r'''
return hsimd_packl(fw, simd_srli(64, fw/2, arg1), simd_srli(64, fw/2, arg2))
''',
		"Ops":["hsimd_packh"],
		"Fws":range(2, 64+1),
		"Platforms":[configure.ALL],
		},
		
		"packh_packus_blend":\
		{
		"body":r'''
return hsimd_packus(fw, simd_srli(fw, fw/2, arg1), simd_srli(fw, fw/2, arg2))
''',
		"Ops":["hsimd_packh"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"packh_regSize_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), arg1, simd_srli(fw, fw/2, arg2))
''',
		"Ops":["hsimd_packh"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},
		
		"packh_32_using_Packed_Horizontal_Subtract":\
		{
		"body":r'''
return _mm_hsub_epi16(simd_srli(fw, fw/2, arg2), simd_srli(fw, fw/2, arg1))''',
		"Ops":["hsimd_packh"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"packh_32_using_Packed_Horizontal_Subtract_and_Packed_SIGN":\
		{
		"body":r'''
return simd_neg(fw/2, _mm_hsub_epi16(simd_and(arg2, simd_himask(fw)), simd_and(arg1, simd_himask(fw))))''',
		"Ops":["hsimd_packh"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"packh_64_using_Packed_Horizontal_Subtract":\
		{
		"body":r'''
return _mm_hsub_epi32(simd_srli(fw, fw/2, arg2), simd_srli(fw, fw/2, arg1))''',
		"Ops":["hsimd_packh"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"packh_64_using_Packed_Horizontal_Subtract_and_Packed_SIGN":\
		{
		"body":r'''
return simd_neg(fw/2, _mm_hsub_epi32(simd_and(arg2, simd_himask(fw)), simd_and(arg1, simd_himask(fw))))''',
		"Ops":["hsimd_packh"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"packh_64_neon":\
		{
		"body":r'''
tmpArg1 = simd_and(simd_himask(fw), arg1)
tmpArg2 = simd_and(simd_himask(fw), arg2)
return vcombine_u64(vorr_u64(vshr_n_u64(vget_low_u64(tmpArg2), fw/2), vget_high_u64(tmpArg2)), vorr_u64(vshr_n_u64(vget_low_u64(tmpArg1), fw/2), vget_high_u64(tmpArg1)))
''',
		"Ops":["hsimd_packh"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},
		
		"packl_double":\
		{
		"body":r'''
return hsimd_packl(2*fw, simd_ifh(1, simd_himask(fw), simd_srli(curRegSize, fw/2, arg1), arg1), simd_ifh(1, simd_himask(fw), simd_srli(curRegSize, fw/2, arg2), arg2))
''',
		"Ops":["hsimd_packl"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},

		"packl_double_ifh64":\
		{
		"body":r'''
return hsimd_packl(2*fw, simd_ifh(64, simd_himask(fw), simd_srli(curRegSize, fw/2, arg1), arg1), simd_ifh(64, simd_himask(fw), simd_srli(curRegSize, fw/2, arg2), arg2))
''',
		"Ops":["hsimd_packl"],
		"Fws":[128],
		"Platforms":[configure.ALL],
		},

		"packl_blend":\
		{
		"body":r'''
return hsimd_packus(fw, simd_and(arg1, simd_lomask(fw)), simd_and(arg2, simd_lomask(fw)))
''',
		"Ops":["hsimd_packl"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"packl_64_blend":\
		{
		"body":r'''
return simd_or(mvmd_shufflei(32, shufflemask4(2,0,3,3), simd_andc(arg1, simd_himask(64))), mvmd_shufflei(32, shufflemask4(3, 3, 2, 0), simd_andc(arg2, simd_himask(64))))
''',
		"Ops":["hsimd_packl"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"packl_regSize_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), simd_slli(fw, fw/2, arg1), arg2)
''',
		"Ops":["hsimd_packl"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},
	
		"packl_32_using_Packed_Horizontal_Subtract":\
		{
		"body":r'''
return _mm_hsub_epi16(simd_and(arg2, simd_lomask(fw)), simd_and(arg1, simd_lomask(fw)))''',
		"Ops":["hsimd_packl"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"packl_64_using_Packed_Horizontal_Subtract":\
		{
		"body":r'''
return _mm_hsub_epi32(simd_and(arg2, simd_lomask(fw)), simd_and(arg1, simd_lomask(fw)))''',
		"Ops":["hsimd_packl"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"packl_64_neon":\
		{
		"body":r'''
tmpArg1 = simd_and(simd_lomask(fw), arg1)
tmpArg2 = simd_and(simd_lomask(fw), arg2)
return vcombine_u64(vorr_u64(vshl_n_u64(vget_high_u64(tmpArg2), fw/2), vget_low_u64(tmpArg2)), vorr_u64(vshl_n_u64(vget_high_u64(tmpArg1), fw/2), vget_low_u64(tmpArg1)))
''',
		"Ops":["hsimd_packl"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},

		"packus_packl_blend":\
		{
		"body":r'''
arg11 = simd_ifh(fw, arg1, simd_constant(fw, 0), arg1)
arg12 = simd_and(simd_lomask(fw), arg11)
arg21 = simd_ifh(fw, arg2, simd_constant(fw, 0), arg2)
arg22 = simd_and(simd_lomask(fw), arg21)
return hsimd_packl(fw, simd_ifh(1, simd_eq(fw, arg12, arg11), arg12, simd_lomask(fw)), simd_ifh(1, simd_eq(fw, arg22, arg21), arg22, simd_lomask(fw)))''',
		"Ops":["hsimd_packus"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"packus_blend":\
		{
		"body":r'''
hiPart = hsimd_packh(fw, arg1, arg2)
return simd_ifh(fw/2, hiPart, simd_constant(fw/2, 0), simd_or(simd_gt(fw/2, hiPart, simd_constant(fw/2, 0)), hsimd_packl(fw, arg1, arg2)))''',
		"Ops":["hsimd_packus"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"packss_packl_blend":\
		{
		"body":r'''
hiBound = simd_srli(fw, 1, simd_lomask(fw))
loBound = simd_not(hiBound)
return hsimd_packl(fw, simd_ifh(1, simd_gt(fw, arg1, hiBound), hiBound, simd_ifh(1, simd_gt(fw, arg1, loBound), arg1, loBound)), simd_ifh(1, simd_gt(fw, arg2, hiBound), hiBound, simd_ifh(1, simd_gt(fw, arg2, loBound), arg2, loBound)))''',
		"Ops":["hsimd_packss"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"signmask_halving_packh":\
		{
		"body":r'''
return hsimd_signmask(fw/2, hsimd_packh(fw, simd_constant(fw, 0), arg1))''',
		"Ops":["hsimd_signmask"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},

		"signmask_halving_packss":\
		{
		"body":r'''
return hsimd_signmask(fw/2, hsimd_packss(fw, simd_constant(fw, 0), arg1))''',
		"Ops":["hsimd_signmask"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"signmask_doubling":\
		{
		"body":r'''
tmpAns1 = hsimd_signmask(2*fw, esimd_mergeh(fw, arg1, simd_constant(fw, 0)))
tmpAns2 = hsimd_signmask(2*fw, esimd_mergel(fw, arg1, simd_constant(fw, 0)))
return (tmpAns1<<(curRegSize/(2*fw))) + tmpAns2''',
		"Ops":["hsimd_signmask"],
		"Fws":range(curRegSize/32, curRegSize+1),
		"Platforms":[configure.ALL],
		},
	
		"signmask_32_SSE":\
		{
		"body":r'''return  _mm_movemask_ps(IDISA_CASTING("_mm_castsi128_ps",arg1))''',
		"Ops":["hsimd_signmask"],
		"Fws":[32],
		"Platforms":([configure.SSE2]),
		},

		"signmask_64_SSE":\
		{
		"body":r'''return  _mm_movemask_pd(IDISA_CASTING("_mm_castsi128_pd",arg1))''',
		"Ops":["hsimd_signmask"],
		"Fws":[64],
		"Platforms":([arch for arch in configure.SSE_SERIES]),
		},

		"signmask_avx":\
		{
		"body":r'''
return (IDISA_CASTING("uint64_t", _mm_movemask_epi8(IDISA_CASTING("__m128i", avx_select_hi128(arg1))))<<16) | IDISA_CASTING("uint64_t", _mm_movemask_epi8(IDISA_CASTING("__m128i", avx_select_lo128(arg1))))''',
		"Ops":["hsimd_signmask"],
		"Fws":[8],
		"Platforms":[configure.AVX],
		},

		# TODO checking
		"signmask_avx2_32":\
		{
		"body":r'''
return _mm256_movemask_ps(_mm256_castsi256_ps(arg1))''',
		"Ops":["hsimd_signmask"],
		"Fws":[32],
		"Platforms":[configure.AVX2],
		},

		# TODO checking
		"signmask_avx2_64":\
		{
		"body":r'''
return _mm256_movemask_pd(_mm256_castsi256_pd(arg1))''',
		"Ops":["hsimd_signmask"],
		"Fws":[64],
		"Platforms":[configure.AVX2],
		},
		
		"signmask_16_general_128bit":\
		{
		"body":r'''
return ((mvmd_extract(16, 7, arg1) >> 8) & 128) | ((mvmd_extract(16, 6, arg1) >> 9) & 64) | ((mvmd_extract(16, 5, arg1) >> 10) & 32) | ((mvmd_extract(16, 4, arg1) >> 11) & 16) | ((mvmd_extract(16, 3, arg1) >> 12) & 8) | ((mvmd_extract(16, 2, arg1) >> 13) & 4) | ((mvmd_extract(16, 1, arg1) >> 14) & 2) | (mvmd_extract(16, 0, arg1) >> 15)''',
		"Ops":["hsimd_signmask"],
		"Fws":[16],
		"Platforms":([configure.NEON] + [arch for arch in configure.SSE_SERIES]),
		},
		
		"signmask_32_general_128bit":\
		{
		"body":r'''
return ((mvmd_extract(32, 3, arg1) >> 28) & 8) | ((mvmd_extract(32, 2, arg1) >> 29) & 4) | ((mvmd_extract(32, 1, arg1) >> 30) & 2) | (mvmd_extract(32, 0, arg1) >> 31)''',
		"Ops":["hsimd_signmask"],
		"Fws":[32],
		"Platforms":([configure.NEON] + [arch for arch in configure.SSE_SERIES]),
		},
	
		"signmask_64_general_128bit":\
		{
		"body":r'''
return ((mvmd_extract(64, 1, arg1) >> 62) & 2) | (mvmd_extract(64, 0, arg1) >> 63)''',
		"Ops":["hsimd_signmask"],
		"Fws":[64],
		"Platforms":([configure.NEON] + [arch for arch in configure.SSE_SERIES]),
		},
	
		"merge_doubling":\
		{
		"body":r'''
return esimd_op(2*fw, simd_ifh(1, simd_himask(2*fw), arg1, simd_srli(2*fw, fw, arg2)), simd_ifh(1, simd_himask(2*fw), simd_slli(2*fw, fw, arg1), arg2))
''',
		"Ops":["esimd_mergel", "esimd_mergeh"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
	
		"merge_havling":\
		{
		"body":r'''
return esimd_op(fw/2, simd_ifh(1, simd_himask(fw), arg1, simd_srli(fw, fw/2, arg2)), simd_ifh(1, simd_himask(fw), simd_slli(fw, fw/2, arg1), arg2))
''',
		"Ops":["esimd_mergel", "esimd_mergeh"],
		"Fws":range(1, curRegSize/2+1),
		"Platforms":[configure.ALL],
		},
		
		"mergeh_avx_using_SSE_BuiltIns":\
		{
		"body":r'''
hiPart2 = avx_select_hi128(arg2)
hiPart1 = avx_select_hi128(arg1)
return avx_general_combine256(IDISA_PACK("_mm_unpackhi_epi$fw$", hiPart2, hiPart1), IDISA_PACK("_mm_unpacklo_epi$fw$", hiPart2, hiPart1))''',
		"Ops":["esimd_mergeh"],
		"Fws":[8, 16, 32, 64],
		"Platforms":configure.AVX_SERIES,
		},

		"mergel_avx_using_SSE_BuiltIns":\
		{
		"body":r'''
loPart2 = avx_select_lo128(arg2)
loPart1 = avx_select_lo128(arg1)
return avx_general_combine256(IDISA_PACK("_mm_unpackhi_epi$fw$", loPart2, loPart1), IDISA_PACK("_mm_unpacklo_epi$fw$", loPart2, loPart1))''',
		"Ops":["esimd_mergel"],
		"Fws":[8, 16, 32, 64],
		"Platforms":configure.AVX_SERIES,
		},

		"mergeh_64_neon":\
		{
		"body":r'''
return vcombine_u64(vget_high_u64(arg2), vget_high_u64(arg1))
''',
		"Ops":["esimd_mergeh"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},

		"mergel_64_neon":\
		{
		"body":r'''
return vcombine_u64(vget_low_u64(arg2), vget_low_u64(arg1))
''',
		"Ops":["esimd_mergel"],
		"Fws":[64],
		"Platforms":[configure.NEON],
		},
		
		"signextendh_blend":\
		{
		"body":r'''
return esimd_mergeh(2*fw, simd_srai(2*fw, fw, arg1), simd_srai(2*fw, fw, simd_slli(2*fw, fw, arg1)))''',
		"Ops":["esimd_signextendh"],
		"Fws":range(1, curRegSize/2),
		"Platforms":[configure.ALL],
		},
		
		"singextendh_half_curRegSize_blend":\
		{
		"body":r'''
return simd_srai(2*fw, fw, arg1)''',
		"Ops":["esimd_signextendh"],
		"Fws":[curRegSize/2],
		"Platforms":[configure.ALL],
		},
		
		"signextendh_using_signextendl":\
		{
		"body":r'''
return esimd_signextendl(fw, simd_srli(curRegSize, curRegSize/2, arg1))''',
		"Ops":["esimd_signextendh"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"signextendl_blend":\
		{
		"body":r'''
return esimd_mergel(2*fw, simd_srai(2*fw, fw, arg1), simd_srai(2*fw, fw, simd_slli(2*fw, fw, arg1)))''',
		"Ops":["esimd_signextendl"],
		"Fws":range(1, curRegSize/2),
		"Platforms":[configure.ALL],
		},
		
		"singextendl_half_curRegSize_blend":\
		{
		"body":r'''
return simd_srai(2*fw, fw, simd_slli(2*fw, fw, arg1))''',
		"Ops":["esimd_signextendl"],
		"Fws":[curRegSize/2],
		"Platforms":[configure.ALL],
		},
		
		"signextendl_8_using_Packed_Move_with_Sign_Extend":\
		{
		"body":r'''
return _mm_cvtepi8_epi16(arg1)''',
		"Ops":["esimd_signextendl"],
		"Fws":[8],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"signextendl_16_using_Packed_Move_with_Sign_Extend":\
		{
		"body":r'''
return _mm_cvtepi16_epi32(arg1)''',
		"Ops":["esimd_signextendl"],
		"Fws":[16],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"signextendl_32_using_Packed_Move_with_Sign_Extend":\
		{
		"body":r'''
return _mm_cvtepi32_epi64(arg1)''',
		"Ops":["esimd_signextendl"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"zeroextendh_blend":\
		{
		"body":r'''
return esimd_mergeh(2*fw, simd_srli(2*fw, fw, arg1), simd_and(simd_lomask(2*fw), arg1))''',
		"Ops":["esimd_zeroextendh"],
		"Fws":range(1, curRegSize/2),
		"Platforms":[configure.ALL],
		},
		
		"zeroextendh_half_curRegSize_blend":\
		{
		"body":r'''
return simd_srli(2*fw, fw, arg1)''',
		"Ops":["esimd_zeroextendh"],
		"Fws":[curRegSize/2],
		"Platforms":[configure.ALL],
		},
		
		"zeroextendh_using_zeroextendl":\
		{
		"body":r'''
return esimd_zeroextendl(fw, simd_srli(curRegSize, curRegSize/2, arg1))''',
		"Ops":["esimd_zeroextendh"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		},
		
		"zeroextendl_blend":\
		{
		"body":r'''
return esimd_mergel(2*fw, simd_srli(2*fw, fw, arg1), simd_and(simd_lomask(2*fw), arg1))''',
		"Ops":["esimd_zeroextendl"],
		"Fws":range(1, curRegSize/2),
		"Platforms":[configure.ALL],
		},
		
		"zeroextendl_half_curRegSize_blend":\
		{
		"body":r'''
return simd_and(simd_lomask(2*fw), arg1)''',
		"Ops":["esimd_zeroextendl"],
		"Fws":[curRegSize/2],
		"Platforms":[configure.ALL],
		},
		
		"zeroextendl_8_using_Packed_Move_with_Zero_Extend":\
		{
		"body":r'''
return _mm_cvtepu8_epi16(arg1)''',
		"Ops":["esimd_zeroextendl"],
		"Fws":[8],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"zeroextendl_16_using_Packed_Move_with_Zero_Extend":\
		{
		"body":r'''
return _mm_cvtepu16_epi32(arg1)''',
		"Ops":["esimd_zeroextendl"],
		"Fws":[16],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"zeroextendl_32_using_Packed_Move_with_Zero_Extend":\
		{
		"body":r'''
return _mm_cvtepu32_epi64(arg1)''',
		"Ops":["esimd_zeroextendl"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"fill_halving":\
		{
		"body":r'''
return mvmd_fill2(fw/2, (val1>>fw/2), val1 & ((1<<fw/2) -1))
''',
		"Ops":["mvmd_fill"],
		"Fws":[16,32,64],
		"Platforms":[configure.ALL],
		},

		"fill_halving2":\
		{
		"body":r'''
return mvmd_fill2(fw/2, 0, val1)
''',
		"Ops":["mvmd_fill"],
		"Fws":[128,256],
		"Platforms":[configure.ALL],
		},

# 		"fill_halving24":\
# 		{
# 		"body":r'''
# return mvmd_fill4(fw/2, 0, val1, 0, val2)
# ''',
# 		"Ops":["mvmd_fill2"],
# 		"Fws":[64,128,256],
# 		"Platforms":[configure.ALL],
# 		},	#This strategy seems wrong. Meng

		"fill_doubling":\
		{
		"body":r'''
return mvmd_fill(2*fw, (val1<<fw)|val1)
''',
		"Ops":["mvmd_fill"],
		"Fws":range(2, 16+1),
		"Platforms":[configure.ALL],
		},

		"fill_1_blend":\
		{
		#mvmd<1>::fill only accepts 0 or -1
		"body":r'''
return mvmd_fill(32, -1*val1)
''',
		"Ops":["mvmd_fill"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},

		"fill_64_blend":\
		{
		"body":r'''
return _mm_set_epi32(val1>>32, val1, val1>>32, val1)
''',
		"Ops":["mvmd_fill"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"fill_128_blend":\
		{
		"body":r'''
return _mm_set_epi32(0, 0, val1>>32, val1)
''',
		"Ops":["mvmd_fill"],
		"Fws":[128],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"fill2_blend":\
		{
		"body":r'''
return mvmd_fill(2*fw, (val1<<fw)|(val2&((1<<fw)-1)))''',
		"Ops":["mvmd_fill2"],
		"Fws":range(1, 16+1),
		"Platforms":[configure.ALL],
		},
		
		"fill2_himask_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(2*fw), mvmd_fill(fw, val1), mvmd_fill(fw, val2))''',
		"Ops":["mvmd_fill2"],
		"Fws":range(32, curRegSize/2+1),
		"Platforms":[configure.ALL],
		},
		
		"fill4_fill2_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(4*fw), mvmd_fill2(fw, val1, val2), mvmd_fill2(fw, val3, val4))''',
		"Ops":["mvmd_fill4"],
		"Fws":range(1, curRegSize/4+1),
		"Platforms":[configure.ALL],
		},
		
		"fill4_doubling":\
		{
		"body":r'''
return simd_or(mvmd_fill4(2*fw, val1<<fw, val3<<fw, val1<<fw, val3<<fw), mvmd_fill4(2*fw, val2&((1<<fw)-1), val4&((1<<fw)-1), val2&((1<<fw)-1), val4&((1<<fw)-1)))''',
		"Ops":["mvmd_fill4"],
		"Fws":range(1, curRegSize/8+1),
		"Platforms":[configure.ALL],
		},
		
		"fill8_fill4_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(8*fw), mvmd_fill4(fw, val1, val2, val3, val4), mvmd_fill4(fw, val5, val6, val7, val8))''',
		"Ops":["mvmd_fill8"],
		"Fws":range(1, curRegSize/8+1),
		"Platforms":[configure.ALL],
		},
		
		"fill8_doubling":\
		{
		"body":r'''
return simd_or(mvmd_fill8(2*fw, val1<<fw, val3<<fw, val5<<fw, val7<<fw, val1<<fw, val3<<fw, val5<<fw, val7<<fw), mvmd_fill8(2*fw, val2&((1<<fw)-1), val4&((1<<fw)-1), val6&((1<<fw)-1), val8&((1<<fw)-1), val2&((1<<fw)-1), val4&((1<<fw)-1), val6&((1<<fw)-1), val8&((1<<fw)-1)))''',
		"Ops":["mvmd_fill8"],
		"Fws":range(1, curRegSize/16+1),
		"Platforms":[configure.ALL],
		},
		
		"fill16_fill8_blend":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(16*fw), mvmd_fill8(fw, val1, val2, val3, val4, val5, val6, val7, val8), mvmd_fill8(fw, val9, val10, val11, val12, val13, val14, val15, val16))''',
		"Ops":["mvmd_fill16"],
		"Fws":range(1, curRegSize/16+1),
		"Platforms":[configure.ALL],
		},
		
		"fill16_doubling":\
		{
		"body":r'''
return simd_or(mvmd_fill16(2*fw, val1<<fw, val3<<fw, val5<<fw, val7<<fw, val9<<fw, val11<<fw, val13<<fw, val15<<fw, val1<<fw, val3<<fw, val5<<fw, val7<<fw, val9<<fw, val11<<fw, val13<<fw, val15<<fw), mvmd_fill16(2*fw, val2&((1<<fw)-1), val4&((1<<fw)-1), val6&((1<<fw)-1), val8&((1<<fw)-1), val10&((1<<fw)-1), val12&((1<<fw)-1), val14&((1<<fw)-1), val16&((1<<fw)-1), val2&((1<<fw)-1), val4&((1<<fw)-1), val6&((1<<fw)-1), val8&((1<<fw)-1), val10&((1<<fw)-1), val12&((1<<fw)-1), val14&((1<<fw)-1), val16&((1<<fw)-1)))''',
		"Ops":["mvmd_fill16"],
		"Fws":range(1, curRegSize/32+1),
		"Platforms":[configure.ALL],
		},
		
		"splat_1_blend":\
		{
		"body":r'''
return simd_sub(curRegSize, simd_constant(curRegSize, 0), simd_and(simd_constant(curRegSize, 1), simd_srli(curRegSize, pos, arg1)))''',
		"Ops":["mvmd_splat"],
		"Fws":[1],
		"Platforms":[configure.ALL],
		},
		
# 		"splat_doubling":\
# 		{
# 		"body":r'''
# tmpArg = simd_slli(2*fw, fw, arg1) if pos%2==0 else simd_srli(2*fw, fw, arg1)
# arg11 = simd_and(simd_lomask(2*fw), arg1) if pos%2==0 else simd_and(simd_himask(2*fw), arg1)
# return mvmd_splat(2*fw, pos/2, simd_or(tmpArg, arg11))''',
# 		"Ops":["mvmd_splat"],
# 		"Fws":range(1, curRegSize/2+1),
# 		"Platforms":[configure.ALL],
# 		},
		"splat_doubling":\
		{
		"body":r'''
return mvmd_splat(2*fw, pos/2, simd_or(simd_slli(2*fw, fw, arg1) if pos%2==0 else simd_srli(2*fw, fw, arg1), simd_and(simd_lomask(2*fw), arg1) if pos%2==0 else simd_and(simd_himask(2*fw), arg1)))''',
		"Ops":["mvmd_splat"],
		"Fws":range(1, curRegSize/2+1),
		"Platforms":[configure.ALL],
		},
		
		"splat_halving":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), mvmd_splat(fw/2, 2*pos+1, arg1), mvmd_splat(fw/2, 2*pos, arg1))''',
		"Ops":["mvmd_splat"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"splat_32_blend":\
		{
		"body":r'''
return mvmd_shufflei(32, shufflemask4(pos, pos, pos, pos), arg1)''',
		"Ops":["mvmd_splat"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"splat_general_neon":\
		{
		"body":r'''
return mvmd_fill(fw, mvmd_extract(fw, pos, arg1))''',
		"Ops":["mvmd_splat"],
		"Fws":[-1],
		"Platforms":[configure.NEON],
		},
		
		"splat_8_using_Extract_Byte":\
		{
		"body":r'''
return mvmd_fill(fw, _mm_extract_epi8(arg1, pos))''',
		"Ops":["mvmd_splat"],
		"Fws":[8],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"splat_8_avx_using_Extract_Byte":\
		{
		"body":r'''
return mvmd_fill(fw, _mm_extract_epi8(avx_select_lo128(arg1), pos)) if (pos<16) else mvmd_fill(fw, _mm_extract_epi8(avx_select_hi128(arg1), pos-16))''',
		"Ops":["mvmd_splat"],
		"Fws":[8],
		"Platforms":configure.AVX_SERIES,
		},
		
		"splat_16_using_Extract_Word":\
		{
		"body":r'''
return mvmd_fill(fw, _mm_extract_epi16(arg1, pos))''',
		"Ops":["mvmd_splat"],
		"Fws":[16],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"splat_16_avx_using_Extract_Byte":\
		{
		"body":r'''
return mvmd_fill(fw, _mm_extract_epi16(avx_select_lo128(arg1), pos)) if (pos<8) else mvmd_fill(fw, _mm_extract_epi16(avx_select_hi128(arg1), pos-8))''',
		"Ops":["mvmd_splat"],
		"Fws":[16],
		"Platforms":configure.AVX_SERIES,
		},

		"splat_32_using_Extract_Dword":\
		{
		"body":r'''
return mvmd_fill(fw, _mm_extract_epi32(arg1, pos))''',
		"Ops":["mvmd_splat"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"splat_32_avx_using_Extract_Dword":\
		{
		"body":r'''
return mvmd_fill(fw, _mm_extract_epi32(avx_select_lo128(arg1), pos)) if (pos<4) else mvmd_fill(fw, _mm_extract_epi32(avx_select_hi128(arg1), pos-4))''',
		"Ops":["mvmd_splat"],
		"Fws":[32],
		"Platforms":configure.AVX_SERIES,
		},
			
		"mvmd_slli_blend":\
		{
		"body":r'''
return simd_slli(curRegSize, sh*fw, arg1)''',
		"Ops":["mvmd_slli"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"mvmd_srli_blend":\
		{
		"body":r'''
return simd_srli(curRegSize, sh*fw, arg1)''',
		"Ops":["mvmd_srli"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"shufflei_64_blend":\
		{
		"body":r'''
return mvmd_shufflei(32, shufflemask4_from_shufflemask2(msk), arg1)''',
		"Ops":["mvmd_shufflei"],
		"Fws":[64],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
# 		"shufflei_16_blend":\
# 		{
# 		"body":r'''
# tmphi = _mm_shufflehi_epi16(arg1, shufflemask8_to_shufflemask4(msk)>>8)
# tmpAns = _mm_shufflelo_epi16(tmphi, shufflemask8_to_shufflemask4(msk)&255)
# tmplh = _mm_shufflehi_epi16(simd_slli(128, 64, arg1), shufflemask8_to_shufflemask4(msk)>>8)
# tmphl = _mm_shufflelo_epi16(simd_srli(128, 64, arg1), shufflemask8_to_shufflemask4(msk)&255)
# a1 = 0 if ((msk>>21)&4)==0 else ((1<<(fw+1))-1)
# a2 = 0 if ((msk>>18)&4)==0 else ((1<<(fw+1))-1)
# a3 = 0 if ((msk>>15)&4)==0 else ((1<<(fw+1))-1)
# a4 = 0 if ((msk>>12)&4)==0 else ((1<<(fw+1))-1)
# a5 = ((1<<(fw+1))-1) if ((msk>>9)&4)==0 else 0
# a6 = ((1<<(fw+1))-1) if ((msk>>6)&4)==0 else 0
# a7 = ((1<<(fw+1))-1) if ((msk>>3)&4)==0 else 0
# a8 = ((1<<(fw+1))-1) if (msk&4)==0 else 0
# return simd_ifh(1, mvmd_fill8(fw, a1, a2, a3, a4, a5, a6, a7, a8), tmpAns, simd_or(tmplh, tmphl))''',
# 		"Ops":["mvmd_shufflei"],
# 		"Fws":[16],
# 		"Platforms":[arch for arch in configure.SSE_SERIES],
# 		},

		# Changed to suit C generator
		"shufflei_16_blend":\
		{
		"body":r'''
return simd_ifh(1, mvmd_fill8(fw, 0 if ((msk>>21)&4)==0 else ((1<<(fw+1))-1), 0 if ((msk>>18)&4)==0 else ((1<<(fw+1))-1), 0 if ((msk>>15)&4)==0 else ((1<<(fw+1))-1), 0 if ((msk>>12)&4)==0 else ((1<<(fw+1))-1), ((1<<(fw+1))-1) if ((msk>>9)&4)==0 else 0, ((1<<(fw+1))-1) if ((msk>>6)&4)==0 else 0, ((1<<(fw+1))-1) if ((msk>>3)&4)==0 else 0, ((1<<(fw+1))-1) if (msk&4)==0 else 0), _mm_shufflelo_epi16(_mm_shufflehi_epi16(arg1, shufflemask8_to_shufflemask4(msk)>>8), shufflemask8_to_shufflemask4(msk)&255), simd_or(_mm_shufflehi_epi16(simd_slli(128, 64, arg1), shufflemask8_to_shufflemask4(msk)>>8), _mm_shufflelo_epi16(simd_srli(128, 64, arg1), shufflemask8_to_shufflemask4(msk)&255)))''',
		"Ops":["mvmd_shufflei"],
		"Fws":[16],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"dslli_blend":\
		{
		"body":r'''
return simd_or(mvmd_slli(fw, sh, arg1), mvmd_srli(fw, curRegSize/fw-sh, arg2))''',
		"Ops":["mvmd_dslli"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"dsrli_blend":\
		{
		"body":r'''
return simd_or(mvmd_srli(fw, sh, arg1), mvmd_slli(fw, curRegSize/fw-sh, arg2))''',
		"Ops":["mvmd_dsrli"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},
		
		"shuffle_halving":\
		{
		"body":r'''
tmp1 = simd_and(simd_constant(fw, curRegSize/fw-1), arg2)
msk1 = simd_add(fw, tmp1, tmp1)
msk2 = simd_add(fw, msk1, simd_constant(fw, 1))
msk = simd_or(msk1, simd_slli(fw, fw/2, msk2))
return simd_ifh(fw, arg2, simd_constant(fw, 0), mvmd_shuffle(fw/2, arg1, msk))''',
		"Ops":["mvmd_shuffle"],
		"Fws":range(2, curRegSize/2+1),
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"mvmd_extract_havling":\
		{
		"body":r'''
return (((IDISA_CASTING("uint64_t", mvmd_extract(fw/2, 2*pos+1, arg1)))<<(fw/2)) | mvmd_extract(fw/2, 2*pos, arg1))''',
		"Ops":["mvmd_extract"],
		"Fws":range(2, 64+1),
		"Platforms":[configure.ALL],
		},#IDISA_CASTING("uint64_t", ((1<<fw)-1)) & 
		
		"mvmd_extract_8_SSE":\
		{
		"body":r'''
return 255 & _mm_extract_epi8(arg1, pos)''',
		"Ops":["mvmd_extract"],
		"Fws":[8],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"mvmd_extract_8_AVX":\
		{
		"body":r'''
return (255 & _mm_extract_epi8(avx_select_lo128(arg1), pos)) if (pos<16) else (255 & _mm_extract_epi8(avx_select_hi128(arg1), pos-16))
''',
		"Ops":["mvmd_extract"],
		"Fws":[8],
		"Platforms":configure.AVX_SERIES,
		},
	
		"mvmd_extract_16_SSE":\
		{
		"body":r'''
return 65535 & _mm_extract_epi16(arg1, pos)''',
		"Ops":["mvmd_extract"],
		"Fws":[16],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"mvmd_extract_16_AVX":\
		{
		"body":r'''
return (65535 & _mm_extract_epi16(avx_select_lo128(arg1), pos)) if (pos<8) else (65535 & _mm_extract_epi16(avx_select_hi128(arg1), pos-8))
''',
		"Ops":["mvmd_extract"],
		"Fws":[16],
		"Platforms":configure.AVX_SERIES,
		},

		"mvmd_extract_32_SSE":\
		{
		"body":r'''
return IDISA_CASTING("uint64_t", (1<<32)-1) & _mm_extract_epi32(arg1, pos)''',
		"Ops":["mvmd_extract"],
		"Fws":[32],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},

		"mvmd_extract_32_AVX":\
		{
		"body":r'''
return (IDISA_CASTING("uint64_t", (1<<32)-1) & _mm_extract_epi32(avx_select_lo128(arg1), pos)) if (pos<4) else (IDISA_CASTING("uint64_t", (1<<32)-1) & _mm_extract_epi32(avx_select_hi128(arg1), pos-4))
''',
		"Ops":["mvmd_extract"],
		"Fws":[32],
		"Platforms":configure.AVX_SERIES,
		},

		"mvmd_extract_doubling":\
		{
		"body":r'''
return (mvmd_extract(2*fw, pos/2, arg1) & ((1<<fw)-1)) if pos%2==0 else (mvmd_extract(2*fw, pos/2, arg1)>>fw)''',
		"Ops":["mvmd_extract"],
		"Fws":range(1, 32+1),
		"Platforms":[configure.ALL],
		},
		
		"mvmd_sXli_halving":\
		{
		"body":r'''
return (mvmd_op(fw/2, sh*2, arg1))''',
		"Ops":["mvmd_slli", "mvmd_srli"],
		"Fws":[-1],
		"Platforms":[configure.ALL],
		}, 

		"simd_add_2_logic":\
		{
		#f0 = (a1b1)^(a0^b0)
		#f1 = a1^b1
		"body":r'''
tmp = simd_xor(arg1, arg2)
return simd_ifh(1, simd_himask(fw), simd_xor(tmp, simd_slli(curRegSize, 1, simd_and(arg1, arg2))), tmp)''',
		"Ops":["simd_add"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_sub_2_logic":\
		{
		"body":r'''
tmp = simd_xor(arg1, arg2)
return simd_ifh(1, simd_himask(fw), simd_xor(tmp, simd_slli(curRegSize, 1, simd_and(simd_not(arg1), arg2))), tmp)''',
		"Ops":["simd_sub"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_mult_2_logic":\
		{
		"body":r'''
tmp1 = simd_slli(curRegSize, 1, arg1)
tmp2 = simd_slli(curRegSize, 1, arg2)
return simd_ifh(1, simd_himask(fw), simd_or(simd_and(tmp1, simd_and(arg2, simd_or(simd_not(arg1), simd_not(tmp2)))), simd_and(arg1, simd_and(tmp2, simd_or(simd_not(tmp1), simd_not(arg2))))), simd_and(arg1, arg2))''',
		"Ops":["simd_mult"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_eq_2_logic":\
		{
		"body":r'''
tmp = simd_xor(arg1, arg2)
tmpAns = simd_and(simd_not(simd_slli(curRegSize, 1, tmp)), simd_not(tmp))
return simd_ifh(1, simd_himask(fw), tmpAns, simd_srli(curRegSize, 1, tmpAns))''',
		"Ops":["simd_eq"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_gt_2_logic":\
		{
		"body":r'''
tmp = simd_not(arg1)
tmpAns = simd_or(simd_and(tmp, arg2), simd_and(simd_slli(curRegSize, 1, simd_and(arg1, simd_not(arg2))), simd_or(tmp, arg2)))
return simd_ifh(1, simd_himask(fw), tmpAns, simd_srli(curRegSize, 1, tmpAns))''',
		"Ops":["simd_gt"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_ugt_2_logic":\
		{
		"body":r'''
tmp = simd_not(arg2)
tmpAns = simd_or(simd_and(arg1, tmp), simd_and(simd_slli(curRegSize, 1, simd_and(arg1, tmp)), simd_or(arg1, tmp)))
return simd_ifh(1, simd_himask(fw), tmpAns, simd_srli(curRegSize, 1, tmpAns))''',
		"Ops":["simd_ugt"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_lt_2_logic":\
		{
		"body":r'''
tmp = simd_not(arg2)
tmpAns = simd_or(simd_and(arg1, tmp), simd_and(simd_slli(curRegSize, 1, simd_and(simd_not(arg1), arg2)), simd_or(arg1, tmp)))
return simd_ifh(1, simd_himask(fw), tmpAns, simd_srli(curRegSize, 1, tmpAns))''',
		"Ops":["simd_lt"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_ult_2_logic":\
		{
		"body":r'''
tmp = simd_not(arg1)
tmpAns = simd_or(simd_and(tmp, arg2), simd_and(simd_slli(curRegSize, 1, simd_and(tmp, arg2)), simd_or(tmp, arg2)))
return simd_ifh(1, simd_himask(fw), tmpAns, simd_srli(curRegSize, 1, tmpAns))''',
		"Ops":["simd_ult"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_max_2_logic":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), simd_and(arg1, arg2), simd_or(simd_and(arg2, simd_srli(curRegSize, 1, simd_or(arg1, simd_not(arg2)))), simd_and(arg1, simd_srli(curRegSize, 1, simd_or(simd_not(arg1), arg2)))))''',
		"Ops":["simd_max"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_umax_2_logic":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), simd_or(arg1, arg2), simd_or(simd_and(arg2, simd_srli(curRegSize, 1, simd_or(simd_not(arg1), arg2))), simd_and(arg1, simd_srli(curRegSize, 1, simd_or(arg1, simd_not(arg2))))))''',
		"Ops":["simd_umax"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_min_2_logic":\
		{
		"body":r'''
tmp1 = simd_srli(curRegSize, 1, arg1)
tmp2 = simd_srli(curRegSize, 1, arg2)
return simd_ifh(1, simd_himask(fw), simd_or(arg1, arg2), simd_or(simd_and(arg1, simd_and(tmp1, simd_not(tmp2))), simd_and(arg2, simd_or(simd_and(simd_not(tmp1), tmp2), arg1))))''',
		"Ops":["simd_min"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_umin_2_logic":\
		{
		"body":r'''
tmp1 = simd_srli(curRegSize, 1, arg1)
tmp2 = simd_srli(curRegSize, 1, arg2)
return simd_ifh(1, simd_himask(fw), simd_and(arg1, arg2), simd_or(simd_and(simd_and(tmp1, simd_not(tmp2)), arg2), simd_and(arg1, simd_or(simd_and(simd_not(tmp1), tmp2), arg2))))''',
		"Ops":["simd_umin"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_abs_2_logic":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), simd_and(arg1, simd_slli(curRegSize, 1, simd_not(arg1))), arg1)''',
		"Ops":["simd_abs"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_neg_2_logic":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), simd_xor(arg1, simd_slli(curRegSize, 1, arg1)), arg1)''',
		"Ops":["simd_neg"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_add_hl_2_logic":\
		{
		"body":r'''
return simd_ifh(1, simd_himask(fw), simd_and(arg1, simd_slli(curRegSize, 1, arg1)), simd_xor(simd_srli(curRegSize, 1, arg1), arg1))''',
		"Ops":["simd_add_hl"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_xor_hl_2_logic":\
		{
		"body":r'''
return simd_and(simd_lomask(fw), simd_xor(simd_srli(curRegSize, 1, arg1), arg1))''',
		"Ops":["simd_xor_hl"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"simd_ctz_2_logic":\
		{
		"body":r'''
tmp = simd_not(arg1)
return simd_ifh(1, simd_himask(fw), simd_and(tmp, simd_slli(curRegSize, 1, tmp)), simd_and(simd_srli(curRegSize, 1, arg1), tmp))''',
		"Ops":["simd_ctz"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},
		
		"bitblock_any_movemask":\
		{
		"body":r'''
return hsimd_signmask(8, simd_eq(8, arg1, simd_constant(8, 0))) != 0xFFFF''',
		"Ops":["bitblock_any"],
		"Fws":[curRegSize],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
		
		"bitblock_any_avx":\
		{
		"body":r'''
return _mm256_testz_si256(IDISA_CASTING("__m256i", arg1), IDISA_CASTING("__m256i", arg1)) == 0''',
		"Ops":["bitblock_any"],
		"Fws":[curRegSize],
		"Platforms":configure.AVX_SERIES,
		},
	
		"bitblock_any_neon":\
		{
		"body":r'''
return hsimd_signmask(32, simd_eq(32, arg1, simd_constant(32, 0))) != 15''',
		"Ops":["bitblock_any"],
		"Fws":[curRegSize],
		"Platforms":[configure.NEON],
		},

#		"bitblock_any_using_PTEST":\
#		{
#		"body":r'''
#return _mm_testz_si128(arg1, simd_constant(8, -1)) != 0''',
#		"Ops":["bitblock_any"],
#		"Fws":[curRegSize]
#		},
		
		"bitblock_all_movemask":\
		{
		"body":r'''
return hsimd_signmask(8, simd_eq(8, arg1, simd_constant(8, -1))) == 0xFFFF''',
		"Ops":["bitblock_all"],
		"Fws":[curRegSize],
		"Platforms":[arch for arch in configure.SSE_SERIES],
		},
	
		"bitblock_all_avx_using_VPTEST":\
		{
		"body":r'''
return _mm256_testz_si256(IDISA_CASTING("__m256i", simd_not(arg1)), IDISA_CASTING("__m256i", simd_constant(8, -1))) == 1''',
		"Ops":["bitblock_all"],
		"Fws":[curRegSize],
		"Platforms":configure.AVX_SERIES,
		},
		
		"bitblock_all_neon":\
		{
		"body":r'''
return hsimd_signmask(32, simd_eq(32, arg1, simd_constant(32, -1))) == 15''',
		"Ops":["bitblock_all"],
		"Fws":[curRegSize],
		"Platforms":[configure.NEON],
		},

#		"bitblock_all_using_PTEST":\
#		{
#		"body":r'''
#return _mm_testz_si128(arg1, simd_constant(8, -1)) == 1''',
#		"Ops":["bitblock_all"],
#		"Fws":[curRegSize]
#		},
		"bitblock_popcount":\
		{
		"body":r'''
return mvmd_extract(64, 0, simd_popcount(curRegSize, arg1))''',
		"Ops":["bitblock_popcount"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},
	
		"bitblock_srl":\
		{
		"body":r'''
return simd_srl(curRegSize, arg1, arg2)''',
		"Ops":["bitblock_srl"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},
	
		"bitblock_sll":\
		{
		"body":r'''
return simd_sll(curRegSize, arg1, arg2)''',
		"Ops":["bitblock_sll"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},
		"bitblock_srli":\
		{
		"body":r'''
return simd_srli(curRegSize, sh, arg1)''',
		"Ops":["bitblock_srli"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},
	
		"bitblock_slli":\
		{
		"body":r'''
return simd_slli(curRegSize, sh, arg1)''',
		"Ops":["bitblock_slli"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},

		"simd_any":\
		{
		"body":r'''
return simd_ugt(fw, arg1, simd_constant(8, 0))''',
		"Ops":["simd_any"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},

		"simd_all":\
		{
		"body":r'''
return simd_eq(fw, arg1, simd_constant(8, 255))''',
		"Ops":["simd_all"],
		"Fws":range(2, curRegSize+1),
		"Platforms":[configure.ALL],
		},

		"simd_any_bitblock_any":\
		{
		"body":r'''
return simd_constant(8, 255) if bitblock_any(arg1) else simd_constant(8, 0)''',
		"Ops":["simd_any"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},

		"simd_all_bitblock_all":\
		{
		"body":r'''
return simd_constant(8, 255) if bitblock_all(arg1) else simd_constant(8, 0)''',
		"Ops":["simd_all"],
		"Fws":[curRegSize],
		"Platforms":[configure.ALL],
		},

		"simd_any_2_logic":\
		{
		"body":r'''
t0 = simd_srli(2, 1, arg1)
f0 = simd_or(t0, simd_and(arg1, simd_xor(t0, simd_constant(8, 255))))
return simd_or(f0, simd_slli(2,1,f0))''',
		"Ops":["simd_any"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},

		"simd_all_2_logic":\
		{
		"body":r'''
f0 = simd_and(arg1, simd_srli(2, 1, arg1))
return simd_or(f0, simd_slli(2,1,f0))''',
		"Ops":["simd_all"],
		"Fws":[2],
		"Platforms":[configure.ALL],
		},

		"hsimd_add_hl_avx2_32":\
		{
		"body":r'''
alpha = _mm256_permute2x128_si256(arg2, arg1, 32)
beta  = _mm256_permute2x128_si256(arg2, arg1, 49)
return _mm256_hadd_epi16(alpha, beta)
''',
		"Ops":["hsimd_add_hl"],
		"Fws":[32],
		"Platforms":[configure.AVX2],
		},

		"hsimd_add_hl_avx2_64":\
		{
		"body":r'''
alpha = _mm256_permute2x128_si256(arg2, arg1, 32)
beta  = _mm256_permute2x128_si256(arg2, arg1, 49)
return _mm256_hadd_epi32(alpha, beta)
''',
		"Ops":["hsimd_add_hl"],
		"Fws":[64],
		"Platforms":[configure.AVX2],
		},

		"hsimd_packus_avx2_16": \
		{
		"body":r'''
alpha = _mm256_permute2x128_si256(arg2, arg1, 32)
beta  = _mm256_permute2x128_si256(arg2, arg1, 49)
return _mm256_packus_epi16(alpha, beta)		
''',
		"Ops":["hsimd_packus"],
		"Fws":[16],
		"Platforms":[configure.AVX2],
		},

		"hsimd_packus_avx2_32": \
		{
		"body":r'''
alpha = _mm256_permute2x128_si256(arg2, arg1, 32)
beta  = _mm256_permute2x128_si256(arg2, arg1, 49)
return _mm256_packus_epi32(alpha, beta)		
''',
		"Ops":["hsimd_packus"],
		"Fws":[32],
		"Platforms":[configure.AVX2],
		},

		"hsimd_packss_avx2_16": \
		{
		"body":r'''
alpha = _mm256_permute2x128_si256(arg2, arg1, 32)
beta  = _mm256_permute2x128_si256(arg2, arg1, 49)
return _mm256_packs_epi16(alpha, beta)		
''',
		"Ops":["hsimd_packss"],
		"Fws":[16],
		"Platforms":[configure.AVX2],
		},

		"hsimd_packss_avx2_32": \
		{
		"body":r'''
alpha = _mm256_permute2x128_si256(arg2, arg1, 32)
beta  = _mm256_permute2x128_si256(arg2, arg1, 49)
return _mm256_packs_epi32(alpha, beta)		
''',
		"Ops":["hsimd_packss"],
		"Fws":[32],
		"Platforms":[configure.AVX2],
		},		
	}	
	
	return strategies
