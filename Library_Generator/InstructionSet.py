
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import sys

import SSE2Instructions
import SSE3Instructions
import SSSE3Instructions
import SSE4_1Instructions
import SSE4_2Instructions
import NEONInstructions
import AVXInstructions
import AVX2Instructions

from Utility import configure

def Load(arch):
	if arch == configure.SSE2:
		return SSE2Instructions.SSE2BuiltIns
	elif arch == configure.SSE3:
		return SSE3Instructions.SSE3BuiltIns
	elif arch == configure.SSSE3:
		return SSSE3Instructions.SSSE3BuiltIns
	elif arch == configure.SSE4_1:
		return SSE4_1Instructions.SSE4_1BuiltIns
	elif arch == configure.SSE4_2:
		return SSE4_2Instructions.SSE4_2BuiltIns
	elif arch == configure.AVX:
		return AVXInstructions.AVXBuiltIns
	elif arch == configure.AVX2:
		return AVX2Instructions.AVX2BuiltIns
	elif arch == configure.NEON:
		return NEONInstructions.NEONBuiltIns
	else:
		print "The generator doesn't support this arch =", arch
		sys.exit()

'''
Below lists all the built-in instructions used by each instruction set

*************************Intel SSE2*************************
1> PAND = _mm_and_si128 = simd_and
2> PANDN = _mm_andnot_si128 = simd_andc
3> POR = _mm_or_si128 = simd_or
4> PXOR = _mm_xor_si128 = simd_xor
5> PADDB = _mm_add_epi8 = simd_add_8
6> PADDW =  _mm_add_epi16 = simd_add_16
7> PADDD = _mm_add_epi32 = simd_add_32
8> PADDQ = _mm_add_epi64 = simd_add_64
9> PSUBB = _mm_sub_epi8 = simd_sub_8
10> PSUBW = _mm_sub_epi16 = simd_sub_16
11> PSUBD = _mm_sub_epi32 = simd_sub_32
12> PSUBQ = _mm_sub_epi64 = simd_sub_64
13> PMULUDQ = _mm_mul_epu32 = simd_umult_32
14> PMULLW = _mm_mullo_epi16 = simd_mult_16
15> PCMPEQB = _mm_cmpeq_epi8 = simd_eq_8
16> PCMPEQW = _mm_cmpeq_epi16 = simd_eq_16
17> PCMPEQD = _mm_cmpeq_epi32 = simd_eq_32
18> PCMPGTB = _mm_cmpgt_epi8 = simd_gt_8
19> PCMPGTW = _mm_cmpgt_epi16 = simd_gt_16
20> PCMPGTD = _mm_cmpgt_epi32 = simd_gt_32
21> PMAXSW = _mm_max_epi16 = simd_max_16
22> PMAXUB = _mm_max_epu8 = simd_umax_8
23> PMINSW = _mm_min_epi16 = simd_min_16
24> PMINUB = _mm_min_epu8 = simd_umin_8
25> PSRLW = _mm_srli_epi16 = simd_srli_16
26> PSRLD = _mm_srli_epi32 = simd_srli_32
27> PSRLQ = _mm_srli_epi64 = simd_srli_64
28> PSLLW = _mm_slli_epi16 = simd_slli_16
29> PSLLD = _mm_slli_epi32 = simd_slli_32
30> PSLLQ = _mm_slli_epi64 = simd_slli_64
31> PSRAW = _mm_srai_epi16 = simd_srai_16
32> PSRAD = _mm_srai_epi32 = simd_srai_32
33> *composite* = _mm_set1_epi8 = simd_constant_8/mvmd_fill_8
34> *composite* = _mm_set1_epi16 = simd_constant_16/mvmd_fill_16
35> *composite* = _mm_set1_epi32 = simd_constant_32/mvmd_fill_32
36> PACKUSWB = _mm_packus_epi16 = hsimd_packus_16
37> PACKSSWB = _mm_packs_epi16 = hsimd_packss_16
38> PACKSSDW = _mm_packs_epi32 = hsimd_packss_32
39> PMOVMSKB = _mm_movemask_epi8 = hsimd_signmask_8
40> PUNPCKHBW = _mm_unpackhi_epi8 = esimd_mergeh_8
41> PUNPCKHWD = _mm_unpackhi_epi16 = esimd_mergeh_16
42> PUNPCKHDQ = _mm_unpackhi_epi32 = esimd_mergeh_32
43> PUNPCKHQDQ = _mm_unpackhi_epi64 = esimd_mergeh_64
44> PUNPCKLBW = _mm_unpacklo_epi8 = esimd_mergel_8
45> PUNPCKLWD = _mm_unpacklo_epi16 = esimd_mergel_16
46> PUNPCKLDQ = _mm_unpacklo_epi32 = esimd_mergel_32
47> PUNPCKLQDQ = _mm_unpacklo_epi64 = esimd_mergel_64
48> *composite* = _mm_set_epi32 = mvmd_fill4
49> *composite* = _mm_set_epi16 = mvmd_fill8
50> *composite* = _mm_set_epi8 = mvmd_fill16
51> PSHUFD = _mm_shuffle_epi32 = mvmd_shufflei_32
52> PSLLQ = _mm_sll_epi64
53> PSLLDQ = _mm_slli_si128
54> 	PSRLQ = _mm_srl_epi64
55> PSRLDQ = _mm_srli_si128
56> MOVD = _mm_cvtsi32_si128
57> PSHUFHW = _mm_shufflehi_epi16
58> PSHUFLW = _mm_shufflelo_epi16
59> PSADBW = _mm_sad_epu8
79> MOVDQA = _mm_load_si128/_mm_store_si128 = bitblock_load_aligned/bitblock_store_aligned
80> MOVDQU = _mm_loadu_si128/_mm_storeu_si128 = bitblock_load_unaligned/bitblock_store_unaligned

*************************Intel SSE3*************************
60> LDDQU = _mm_lddqu_si128 = bitblock_load_unaligned

*************************Intel SSSE3*************************
61> PSHUFB = _mm_shuffle_epi8 = mvmd_shuffle_8
62> PHADDW = _mm_hadd_epi16 = hsimd_add_hl_32
63> PHADDD = _mm_hadd_epi32 = hsimd_add_hl_64
64> PABSB = _mm_abs_epi8 = simd_abs_8
65> PABSW = _mm_abs_epi16 = simd_abs_16
66> PABSD = _mm_abs_epi32 = simd_abs_32

*************************Intel SSE4.1*************************
67> PACKUSDW = _mm_packus_epi32 = hsimd_packus_32
68> PCMPEQQ = _mm_cmpeq_epi64 = simd_eq_64
69> PMAXSB = _mm_max_epi8 = simd_max_8
70> PMAXSD = _mm_max_epi32 = simd_max_32
71> PMAXUD = _mm_max_epu32 = simd_umax_32
72> PMAXUW = _mm_max_epu16 = simd_umax_16
73> PMINSB = _mm_min_epi8 = simd_min_8
74> PMINSD = _mm_min_epi32 = simd_min_32
75> PMINUD = _mm_min_epu32 = simd_umin_32
76> PMINUW = _mm_min_epu16 = simd_umin_16
77> PMULLUD = _mm_mullo_epi32 = simd_mult_32

*************************Intel SSE4.2*************************
78> PCMPGTQ = _mm_cmpgt_epi64 = simd_gt_64
81> ...

*************************Intel AVX*************************
_mm256_shuffle_ps

'''


#PHSUBW/PHSUBD - Packed Horizontal Subtract - SSSE3

#PSIGNB/PSIGNW/PSIGND - Packed SIGN - SSSE3
#negates each data element of the destination operand (the first operand) if the signed integer value of the corresponding data element in
#the source operand (the second operand) is less than zero.

#PBLENDVB - Variable Blend Packed Bytes - SSE4.1
#If a mask bit is 1, then the corresponding byte element in the source operand is
#copied to the destination, else the byte element in the destination operand is left unchanged.

#PBLENDW - Blend Packed Words - SSE4.1
#Conditionally copies word elements from the source operand (second operand) to the
#destination operand (first operand) depending on the immediate byte (third
#operand). Each bit of Imm8 correspond to a word element.
#If a bit is 1, then the corresponding word element in the source operand is copied
#to the destination, else the word element in the destination operand is left unchanged.

#PEXTRB/PEXTRD/PEXTRQ - Extract Byte/Dword/Qword - SSE4.1
#Extract a byte/dword/qword integer value from the source XMM register at a
#byte/dword/qword offset determined from imm8[3:0].

#PEXTRW - Extract Word - SSE2
#Copies the word in the source operand (second operand) specified by the count
#operand (third operand) to the destination operand (first operand).

#PHMINPOSUW - Packed Horizontal Word Minimum - SSE4.1
#Get the minimum value in a 128-bits register and also its index

#PINSRB/PINSRD/PINSRQ - Insert Byte/Dword/Qword - SSE4.1

#PINSRW - Insert Word - SSE2
#insert a word into a 128-bits register at a specified position

#PMOVSXBD/PMOVSXBQ/PMOVSXBW/PMOVSXWD/PMOVSXWQ/PMOVSXDQ - Packed Move with Sign Extend - SSE4.1
#This instruction performs a conversion of signed integers from x-bit to y-bit

#PMOVZXBD/PMOVZXBQ/PMOVZXBW/PMOVZXWD/PMPVZXWQ/PMOVZXDQ - Packed Move with Zero Extend - SSE4.1
#This instruction performs a conversion of unsigned integers from x-bit to y-bit

#PMULDQ - Multiply Packed Signed Dword Integers - SSE4.1
#r0 := low_half(a0 * b0)
#r1 := high_half(a0 * b0)
#r2 := low_half(a2 * b2)
#r3 := high_half(a2 * b2)

#PTEST - Logical Compare - SSE4.1
#This instruction performs a bitwise comparison between two 128-bit parameters, the result is all 0s or all 1s.
