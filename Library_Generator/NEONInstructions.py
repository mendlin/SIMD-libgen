
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

from types import *

NEONBuiltIns = \
{
    "simd_not":\
    {
        "signature":["SIMD_type (SIMD_type)vmvnq_u32(uint32x4_t arg1)"],
        "args_type":{"arg1":"uint32x4_t"},
        "return_type":"SIMD_type",
        "fws":[[1]],
    },
    "simd_and":\
    {
        "signature":["SIMD_type vandq_u64(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
        "return_type":"SIMD_type",
        "fws":[[1]],
    },
    "simd_andc":\
    {
        "signature":["SIMD_type vbicq_u64(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
        "return_type":"SIMD_type",
        "fws":[[1]],
    },
    "simd_or":\
    {
        "signature":["SIMD_type vorrq_u64(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
        "return_type":"SIMD_type",
        "fws":[[1]],
    },
    "simd_xor":\
    {
        "signature":["SIMD_type veorq_u64(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
        "return_type":"SIMD_type",
        "fws":[[1]],
    },
    "simd_ifh":\
    {
        "signature":["SIMD_type vbslq_u64(SIMD_type arg1, SIMD_type arg2, SIMD_type arg3)"],
        "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type", "arg3":"SIMD_type"},
        "return_type":"SIMD_type",
        "fws":[[1]],
    },
    "simd_add":\
    {
        "signature":["SIMD_type (SIMD_type)vaddq_u$fw$(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"NEON_utype(fw)", "arg2":"NEON_utype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32, 64]],
    },
    "simd_sub":\
    {
        "signature":["SIMD_type (SIMD_type)vsubq_u$fw$(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"NEON_utype(fw)", "arg2":"NEON_utype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32, 64]],
    },
    "simd_mult":\
    {
        "signature":["SIMD_type (SIMD_type)vmulq_s$fw$(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"NEON_stype(fw)", "arg2":"NEON_stype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "simd_eq":\
    {
        "signature":["SIMD_type (SIMD_type)vceqq_u$fw$(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"NEON_utype(fw)", "arg2":"NEON_utype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "simd_gt":\
    {
        "signature":["SIMD_type (SIMD_type)vcgtq_s$fw$(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"NEON_stype(fw)", "arg2":"NEON_stype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "simd_lt":\
    {
        "signature":["SIMD_type (SIMD_type)vcltq_s$fw$(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"NEON_stype(fw)", "arg2":"NEON_stype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "simd_max":\
    {
        "signature":["SIMD_type (SIMD_type)vmaxq_s$fw$(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"NEON_stype(fw)", "arg2":"NEON_stype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "simd_min":\
    {
        "signature":["SIMD_type (SIMD_type)vminq_s$fw$(SIMD_type arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"NEON_stype(fw)", "arg2":"NEON_stype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
#    "simd_srli":\
#    {
#        "signature":["SIMD_type (SIMD_type)vshrq_n_u$fw$(SIMD_type arg1, int sh)"],
#        "args_type":{"arg1":"NEON_utype(fw)", "sh":"signed_int(32)"},
#        "return_type":"SIMD_type",
#        "fws":[[8, 16, 32, 64]],
#    },
#    "simd_slli":\
#    {
#        "signature":["SIMD_type (SIMD_type)vshlq_n_u$fw$(SIMD_type arg1, int sh)"],
#        "args_type":{"arg1":"NEON_utype(fw)", "sh":"signed_int(32)"},
#        "return_type":"SIMD_type",
#        "fws":[[8, 16, 32, 64]],
#    },
#    "simd_sll":\
#    {
#        "signature":["SIMD_type (SIMD_type)vshlq_u$fw$(SIMD_type arg1, SIMD_type shift_mask)"],
#        "args_type":{"arg1":"NEON_utype(fw)", "shift_mask":"NEON_stype(fw)"},
#        "return_type":"SIMD_type",
#        "fws":[[8, 16, 32, 64]],
#    },
#    "simd_srai":\
#    {
#        "signature":["SIMD_type (SIMD_type)vshrq_n_s$fw$(SIMD_type arg1, int sh)"],
#        "args_type":{"arg1":"NEON_stype(fw)", "sh":"signed_int(32)"},
#        "return_type":"SIMD_type",
#        "fws":[[8, 16, 32, 64]],
#    },
    "simd_constant":\
    {
        "signature":["SIMD_type (SIMD_type)vdupq_n_u$fw$(int val)"],
        "args_type":{"val":"unsigned_int(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32, 64]],
    },
    "simd_abs":\
    {
        "signature":["SIMD_type (SIMD_type)vabsq_s$fw$(SIMD_type arg1)"],
        "args_type":{"arg1":"NEON_stype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "simd_neg":\
    {
        "signature":["SIMD_type (SIMD_type)vnegq_s$fw$(SIMD_type arg1)"],
        "args_type":{"arg1":"NEON_stype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "simd_popcount":\
    {
        "signature":["SIMD_type (SIMD_type)vcntq_u$fw$(SIMD_type arg1)"],
        "args_type":{"arg1":"NEON_utype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8]],
    },
    "hsimd_packh":\
    {
        "signature":["SIMD_type (SIMD_type)(vuzpq_u$fw/2$(SIMD_type arg2, SIMD_type arg1).val[1])"],
        "args_type":{"arg1":"NEON_utype(fw/2)", "arg2":"NEON_utype(fw/2)"},
        "return_type":"SIMD_type",
        "fws":[[16, 32, 64]],
    },
    "hsimd_packl":\
    {
        "signature":["SIMD_type (SIMD_type)(vuzpq_u$fw/2$(SIMD_type arg2, SIMD_type arg1).val[0])"],
        "args_type":{"arg1":"NEON_utype(fw/2)", "arg2":"NEON_utype(fw/2)"},
        "return_type":"SIMD_type",
        "fws":[[16, 32, 64]],
    },
    "esimd_mergeh":\
    {
        "signature":["SIMD_type (SIMD_type)(vzipq_u$fw$(SIMD_type arg2, SIMD_type arg1).val[1])"],
        "args_type":{"arg1":"NEON_utype(fw)", "arg2":"NEON_utype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "esimd_mergel":\
    {
        "signature":["SIMD_type (SIMD_type)(vzipq_u$fw$(SIMD_type arg2, SIMD_type arg1).val[0])"],
        "args_type":{"arg1":"NEON_utype(fw)", "arg2":"NEON_utype(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32]],
    },
    "mvmd_fill":\
    {
        "signature":["SIMD_type (SIMD_type)vdupq_n_u$fw$(int val1)"],
        "args_type":{"val1":"unsigned_int(fw)"},
        "return_type":"SIMD_type",
        "fws":[[8, 16, 32, 64]],
    },
    "mvmd_extract":\
    {
        "signature":["int vgetq_lane_u$fw$(SIMD_type arg1, int pos)"],
        "args_type":{"arg1":"NEON_utype(fw)", "pos":"signed_int(32)"},
        "return_type":"unsigned_int(64)",
        "fws":[[8, 16, 32, 64]],
    },
    "bitblock_load_aligned":\
    {
        "signature":["SIMD_type vld1q_u64(uint64_t const* arg1)"],
        "args_type":{"arg1":"uint64_t const*"},
        "return_type":"SIMD_type",
        "fws":[[128]],
    },
    "bitblock_store_aligned":\
    {
        "signature":["void vst1q_u64(uint64_t* arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"uint64_t*", "arg2":"SIMD_type"},
        "return_type":"void",
        "fws":[[128]],
    },
    "bitblock_load_unaligned":\
    {
        "signature":["SIMD_type vld1q_u64(uint64_t const* arg1)"],
        "args_type":{"arg1":"uint64_t const*"},
        "return_type":"SIMD_type",
        "fws":[[128]],
    },
    "bitblock_store_unaligned":\
    {
        "signature":["void vst1q_u64(uint64_t* arg1, SIMD_type arg2)"],
        "args_type":{"arg1":"uint64_t*", "arg2":"SIMD_type"},
        "return_type":"void",
        "fws":[[128]],
    },
    "vsetq_lane_u64":\
    {
        "signature":["SIMD_type vsetq_lane_u64(int val, SIMD_type arg1, int pos)"],
        "args_type":{"val":"uint64_t", "arg1":"SIMD_type", "pos":"signed_int(32)"},
        "return_type":"SIMD_type",
        "fws":[[64]],
    },
    "vcombine_u64":\
    {
        "signature":["SIMD_type vcombine_u64(uint64x1_t low, uint64x1_t high)"],
        "args_type":{"low":"uint64x1_t", "high":"uint64x1_t"},
        "return_type":"SIMD_type",
        "fws":[[64]],
    },
    "vget_high_u64":\
    {
        "signature":["uint64x1_t vget_high_u64(SIMD_type arg1)"],
        "args_type":{"arg1":"SIMD_type"},
        "return_type":"uint64x1_t",
        "fws":[[64]],
    },
    "vget_low_u64":\
    {
        "signature":["uint64x1_t vget_low_u64(SIMD_type arg1)"],
        "args_type":{"arg1":"SIMD_type"},
        "return_type":"uint64x1_t",
        "fws":[[64]],
    },
    "vorr_u64":\
    {
        "signature":["uint64x1_t vorr_u64(uint64x1_t arg1, uint64x1_t arg2)"],
        "args_type":{"arg1":"uint64x1_t", "arg2":"uint64x1_t"},
        "return_type":"uint64x1_t",
        "fws":[[64]],
    },
    "vshl_n_u64":\
    {
        "signature":["uint64x1_t vshl_n_u64(uint64x1_t arg1, int sh)"],
        "args_type":{"arg1":"uint64x1_t", "sh":"signed_int(32)"},
        "return_type":"uint64x1_t",
        "fws":[[64]],
    },
    "vshr_n_u64":\
    {
        "signature":["uint64x1_t vshr_n_u64(uint64x1_t arg1, int sh)"],
        "args_type":{"arg1":"uint64x1_t", "sh":"signed_int(32)"},
        "return_type":"uint64x1_t",
        "fws":[[64]],
    },
    "vshrq_n_u8":\
    {
        "signature":["uint8x16_t vshrq_n_u8(uint8x16_t arg1, int sh)"],
        "args_type":{"arg1":"uint8x16_t", "sh":"signed_int(32)"},
        "return_type":"uint8x16_t",
        "fws":[[8]],
    },
    "vshrq_n_u16":\
    {
        "signature":["uint16x8_t vshrq_n_u16(uint16x8_t arg1, int sh)"],
        "args_type":{"arg1":"uint16x8_t", "sh":"signed_int(32)"},
        "return_type":"uint16x8_t",
        "fws":[[16]],
    },
    "vshrq_n_u32":\
    {
        "signature":["uint32x4_t vshrq_n_u32(uint32x4_t arg1, int sh)"],
        "args_type":{"arg1":"uint32x4_t", "sh":"signed_int(32)"},
        "return_type":"uint32x4_t",
        "fws":[[32]],
    },
    "vshrq_n_u64":\
    {
        "signature":["uint64x2_t vshrq_n_u64(uint64x2_t arg1, int sh)"],
        "args_type":{"arg1":"uint64x2_t", "sh":"signed_int(32)"},
        "return_type":"uint64x2_t",
        "fws":[[64]],
    },
    "vshlq_n_u8":\
    {
        "signature":["uint8x16_t vshlq_n_u8(uint8x16_t arg1, int sh)"],
        "args_type":{"arg1":"uint8x16_t", "sh":"signed_int(32)"},
        "return_type":"uint8x16_t",
        "fws":[[8]],
    },
    "vshlq_n_u16":\
    {
        "signature":["uint16x8_t vshlq_n_u16(uint16x8_t arg1, int sh)"],
        "args_type":{"arg1":"uint16x8_t", "sh":"signed_int(32)"},
        "return_type":"uint16x8_t",
        "fws":[[16]],
    },
    "vshlq_n_u32":\
    {
        "signature":["uint32x4_t vshlq_n_u32(uint32x4_t arg1, int sh)"],
        "args_type":{"arg1":"uint32x4_t", "sh":"signed_int(32)"},
        "return_type":"uint32x4_t",
        "fws":[[32]],
    },
    "vshlq_n_u64":\
    {
        "signature":["uint64x2_t vshlq_n_u64(uint64x2_t arg1, int sh)"],
        "args_type":{"arg1":"uint64x2_t", "sh":"signed_int(32)"},
        "return_type":"uint64x2_t",
        "fws":[[64]],
    },
    "vshrq_n_s8":\
    {
        "signature":["int8x16_t vshrq_n_s8(int8x16_t arg1, int sh)"],
        "args_type":{"arg1":"int8x16_t", "sh":"signed_int(32)"},
        "return_type":"int8x16_t",
        "fws":[[8]],
    },
    "vshrq_n_s16":\
    {
        "signature":["int16x8_t vshrq_n_s16(int16x8_t arg1, int sh)"],
        "args_type":{"arg1":"int16x8_t", "sh":"signed_int(32)"},
        "return_type":"int16x8_t",
        "fws":[[16]],
    },
    "vshrq_n_s32":\
    {
        "signature":["int32x4_t vshrq_n_s32(int32x4_t arg1, int sh)"],
        "args_type":{"arg1":"int32x4_t", "sh":"signed_int(32)"},
        "return_type":"int32x4_t",
        "fws":[[32]],
    },
    "vshrq_n_s64":\
    {
        "signature":["int64x2_t vshrq_n_s64(int64x2_t arg1, int sh)"],
        "args_type":{"arg1":"int64x2_t", "sh":"signed_int(32)"},
        "return_type":"int64x2_t",
        "fws":[[64]],
    },
    "vshlq_u64":\
    {
        "signature":["uint64x2_t vshlq_u64(uint64x2_t arg1, int64x2_t shift_mask)"],
        "args_type":{"arg1":"SIMD_type", "shift_mask":"int64x2_t"},
        "return_type":"SIMD_type",
        "fws":[[64]],
    },
    "vextq_u64":\
    {
        "signature":["uint64x2_t vextq_u64(uint64x2_t arg1, uint64x2_t arg2, int c)"],
        "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type", "c":"signed_int(32)"},
        "return_type":"SIMD_type",
        "fws":[[64]],
    },
}
