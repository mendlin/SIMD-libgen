
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 


# This is a list of all operations. 
# The definition of each operation must follow one of the below formats
# format_1(only for logic operations): opPattern = 2
#     simd_op(data_type arg, ...)
# format_2: opPattern = 0
#     class_name<fw>::op(data_type arg, ...)
# format_3: opPattern = 1
#     class_name<fw>::op<x>(data_type arg, ...)
# format_4: opPattern = 3
#     class_name::op(data_type arg, ...)
# format_5: opPattern = 4
#     class_name::op<x>(data_type arg, ...)

AllOperations = \
{
    #logic operations
    "and":\
    {
     "signature":"SIMD_type simd_and(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "andc":\
    {
     "signature":"SIMD_type simd_andc(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "or":\
    {
     "signature":"SIMD_type simd_or(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "xor":\
    {
     "signature":"SIMD_type simd_xor(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "not":\
    {
     "signature":"SIMD_type simd_not(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "nor":\
    {
     "signature":"SIMD_type simd_nor(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_ifh":\
    {
     "signature":"SIMD_type simd<fw>::ifh(SIMD_type arg1, SIMD_type arg2, SIMD_type arg3)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type", "arg3":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"static inline SIMD_type ifh(SIMD_type arg1, SIMD_type arg2, SIMD_type arg3)"
    },

    #constant and masking operations
    "simd_lomask":\
    {
     "signature":"SIMD_type simd<fw>::lomask()",
     "args_type":{},
     "return_type":"SIMD_type",
    },
    
    "simd_himask":\
    {
     "signature":"SIMD_type simd<fw>::himask()",
     "args_type":{},
     "return_type":"SIMD_type",
    },
    
    "simd_constant":\
    {
     "signature":"SIMD_type simd<fw>::constant<val>()",
     "args_type":{"val":"unsigned_int(fw)"},
     "return_type":"SIMD_type",
     "cpp_class_signature": "template <typename FieldType<fw>::T val> static inline SIMD_type constant()",
    },
    
    #shifting operations
    "simd_srli":\
    {
     "signature":"SIMD_type simd<fw>::srli<sh>(SIMD_type arg1)",
     "args_type":{"sh":"range(0, fw)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type srli(SIMD_type arg1)",
    },
    
    "simd_vsrl":\
    {
     "signature":"SIMD_type simd<fw>::vsrl(SIMD_type arg1, SIMD_type shift_mask)",
     "args_type":{"arg1":"SIMD_type", "shift_mask":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_slli":\
    {
     "signature":"SIMD_type simd<fw>::slli<sh>(SIMD_type arg1)",
     "args_type":{"sh":"range(0, fw)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type slli(SIMD_type arg1)",
    },
    
    "simd_vsll":\
    {
     "signature":"SIMD_type simd<fw>::vsll(SIMD_type arg1, SIMD_type shift_mask)",
     "args_type":{"arg1":"SIMD_type", "shift_mask":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_srai":\
    {
     "signature":"SIMD_type simd<fw>::srai<sh>(SIMD_type arg1)",
     "args_type":{"sh":"range(0, fw)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type srai(SIMD_type arg1)",
    },
    
    "simd_vsra":\
    {
     "signature":"SIMD_type simd<fw>::vsra(SIMD_type arg1, SIMD_type shift_mask)",
     "args_type":{"arg1":"SIMD_type", "shift_mask":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    #vertical operations
    "simd_add":\
    {
     "signature":"SIMD_type simd<fw>::add(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_sub":\
    {
     "signature":"SIMD_type simd<fw>::sub(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    # simd_umult may be defined differently from ordinary sense, use with care.     
    "simd_umult":\
    {
     "signature":"SIMD_type simd<fw>::umult(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_mult":\
    {
     "signature":"SIMD_type simd<fw>::mult(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_eq":\
    {
     "signature":"SIMD_type simd<fw>::eq(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_gt":\
    {
     "signature":"SIMD_type simd<fw>::gt(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_ugt":\
    {
     "signature":"SIMD_type simd<fw>::ugt(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_lt":\
    {
     "signature":"SIMD_type simd<fw>::lt(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_ult":\
    {
     "signature":"SIMD_type simd<fw>::ult(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_max":\
    {
     "signature":"SIMD_type simd<fw>::max(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
     # Force class signature and other signature will be infered from this one. 
     "cpp_class_signature": "static inline SIMD_type max(SIMD_type arg1, SIMD_type arg2)",
    },
    
    "simd_umax":\
    {
     "signature":"SIMD_type simd<fw>::umax(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_min":\
    {
     "signature":"SIMD_type simd<fw>::min(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_umin":\
    {
     "signature":"SIMD_type simd<fw>::umin(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_abs":\
    {
     "signature":"SIMD_type simd<fw>::abs(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_neg":\
    {
     "signature":"SIMD_type simd<fw>::neg(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_add_hl":\
    {
     "signature":"SIMD_type simd<fw>::add_hl(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_sub_hl":\
    {
     "signature":"SIMD_type simd<fw>::sub_hl(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_xor_hl":\
    {
     "signature":"SIMD_type simd<fw>::xor_hl(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_popcount":\
    {
     "signature":"SIMD_type simd<fw>::popcount(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "simd_ctz":\
    {
     "signature":"SIMD_type simd<fw>::ctz(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },

    "simd_any":\
    {
     "signature":"SIMD_type simd<fw>::any(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },

    "simd_all":\
    {
     "signature":"SIMD_type simd<fw>::all(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },

    #horizontal operations
    "hsimd_add_hl":\
    {
     "signature":"SIMD_type hsimd<fw>::add_hl(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "hsimd_min_hl":\
    {
     "signature":"SIMD_type hsimd<fw>::min_hl(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "hsimd_umin_hl":\
    {
     "signature":"SIMD_type hsimd<fw>::umin_hl(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "hsimd_packh":\
    {
     "signature":"SIMD_type hsimd<fw>::packh(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "hsimd_packl":\
    {
     "signature":"SIMD_type hsimd<fw>::packl(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "hsimd_packus":\
    {
     "signature":"SIMD_type hsimd<fw>::packus(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "hsimd_packss":\
    {
     "signature":"SIMD_type hsimd<fw>::packss(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "hsimd_signmask":\
    {
     "signature":"int hsimd<fw>::signmask(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"unsigned_int(64)",
     "cpp_class_signature": "static inline typename FieldType<regw/fw>::T signmask(SIMD_type arg1)"
    },

    #expanding operations
    "esimd_mergeh":\
    {
     "signature":"SIMD_type esimd<fw>::mergeh(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "esimd_mergel":\
    {
     "signature":"SIMD_type esimd<fw>::mergel(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    #"esimd_merge":\
    #{
    # "signature":"void esimd<fw>::merge(SIMD_type arg1, SIMD_type arg2, SIMD_type &u, SIMD_type &v)",
    #},
    
    "esimd_multh":\
    {
     "signature":"SIMD_type esimd<fw>::multh(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "esimd_multl":\
    {
     "signature":"SIMD_type esimd<fw>::multl(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "esimd_signextendh":\
    {
     "signature":"SIMD_type esimd<fw>::signextendh(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "esimd_signextendl":\
    {
     "signature":"SIMD_type esimd<fw>::signextendl(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "esimd_zeroextendh":\
    {
     "signature":"SIMD_type esimd<fw>::zeroextendh(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "esimd_zeroextendl":\
    {
     "signature":"SIMD_type esimd<fw>::zeroextendl(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"SIMD_type",
    },

    #movement operations
    "mvmd_fill":\
    {
     "signature":"SIMD_type mvmd<fw>::fill(int val1)",
     "args_type":{"val1":"unsigned_int(fw)"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"static inline SIMD_type fill(typename FieldType<fw>::T val1)",
    },
    
    "mvmd_fill2":\
    {
     "signature":"SIMD_type mvmd<fw>::fill2(int val1, int val2)",
     "args_type":{"val1":"unsigned_int(fw)", "val2":"unsigned_int(fw)"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"static inline SIMD_type fill2(typename FieldType<fw>::T val1, typename FieldType<fw>::T val2)",
    },
    
    "mvmd_fill4":\
    {
     "signature":"SIMD_type mvmd<fw>::fill4(int val1, int val2, int val3, int val4)",
     "args_type":{"val1":"unsigned_int(fw)", "val2":"unsigned_int(fw)", "val3":"unsigned_int(fw)", "val4":"unsigned_int(fw)"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"static inline SIMD_type fill4(typename FieldType<fw>::T val1, typename FieldType<fw>::T val2, typename FieldType<fw>::T val3, typename FieldType<fw>::T val4)",
    },
    
    "mvmd_fill8":\
    {
     "signature":"SIMD_type mvmd<fw>::fill8(int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8)",
     "args_type":{"val1":"unsigned_int(fw)", "val2":"unsigned_int(fw)", "val3":"unsigned_int(fw)", "val4":"unsigned_int(fw)", "val5":"unsigned_int(fw)", "val6":"unsigned_int(fw)", "val7":"unsigned_int(fw)", "val8":"unsigned_int(fw)"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"static inline SIMD_type fill8(typename FieldType<fw>::T val1, typename FieldType<fw>::T val2, typename FieldType<fw>::T val3, typename FieldType<fw>::T val4, typename FieldType<fw>::T val5, typename FieldType<fw>::T val6, typename FieldType<fw>::T val7, typename FieldType<fw>::T val8)",
    },
    
    "mvmd_fill16":\
    {
     "signature":"SIMD_type mvmd<fw>::fill16(int val1, int val2, int val3, int val4, int val5, int val6, int val7, int val8, int val9, int val10, int val11, int val12, int val13, int val14, int val15, int val16)",
     "args_type":{"val1":"unsigned_int(fw)", "val2":"unsigned_int(fw)", "val3":"unsigned_int(fw)", "val4":"unsigned_int(fw)", "val5":"unsigned_int(fw)", "val6":"unsigned_int(fw)", "val7":"unsigned_int(fw)", "val8":"unsigned_int(fw)",
                  "val9":"unsigned_int(fw)", "val10":"unsigned_int(fw)", "val11":"unsigned_int(fw)", "val12":"unsigned_int(fw)", "val13":"unsigned_int(fw)", "val14":"unsigned_int(fw)", "val15":"unsigned_int(fw)", "val16":"unsigned_int(fw)"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"static inline SIMD_type fill16(typename FieldType<fw>::T val1, typename FieldType<fw>::T val2, typename FieldType<fw>::T val3, typename FieldType<fw>::T val4, \
typename FieldType<fw>::T val5, typename FieldType<fw>::T val6, typename FieldType<fw>::T val7, typename FieldType<fw>::T val8, \
typename FieldType<fw>::T val9, typename FieldType<fw>::T val10, typename FieldType<fw>::T val11, typename FieldType<fw>::T val12, \
typename FieldType<fw>::T val13, typename FieldType<fw>::T val14, typename FieldType<fw>::T val15, typename FieldType<fw>::T val16)",
    },
    
    "mvmd_splat":\
    {
     "signature":"SIMD_type mvmd<fw>::splat<pos>(SIMD_type arg1)",
     "args_type":{"pos":"range(0, curRegSize/fw-1)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t pos> static inline SIMD_type splat(SIMD_type arg1)"
    },
    
    "mvmd__slli":\
    {
     "signature":"SIMD_type mvmd<fw>::slli<sh>(SIMD_type arg1)",
     "args_type":{"sh":"range(0, curRegSize/fw)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type slli(SIMD_type arg1)",
    },
    
    "mvmd__srli":\
    {
     "signature":"SIMD_type mvmd<fw>::srli<sh>(SIMD_type arg1)",
     "args_type":{"sh":"range(0, curRegSize/fw)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type srli(SIMD_type arg1)",
    },
    
    "mvmd_shufflei":\
    {
     "signature":"SIMD_type mvmd<fw>::shufflei<msk>(SIMD_type arg1)",
     "args_type":{"msk":"range(0, 2**((curRegSize/fw)*int(math.log(curRegSize/fw, 2)))-1)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",     
    },
    
    "mvmd_dslli":\
    {
     "signature":"SIMD_type mvmd<fw>::dslli<sh>(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"sh":"range(0, curRegSize/fw)", "arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type dslli(SIMD_type arg1, SIMD_type arg2)"
    },
    
    "mvmd_dsrli":\
    {
     "signature":"SIMD_type mvmd<fw>::dsrli<sh>(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"sh":"range(0, curRegSize/fw)", "arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type dsrli(SIMD_type arg1, SIMD_type arg2)",
    },
    
    "mvmd_shuffle":\
    {
     "signature":"SIMD_type mvmd<fw>::shuffle(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "mvmd_extract":\
    {
     "signature":"int mvmd<fw>::extract<pos>(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type", "pos":"range(0, curRegSize/fw-1)"},
     "return_type":"unsigned_int(64)",
     "cpp_class_signature":"template <uint8_t pos> static inline typename FieldType<fw>::T extract(SIMD_type arg1)",
    },

    #bitblock operations
    "bitblock_any":\
    {
     "signature":"bool bitblock::any(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"bool",
    },
    
    "bitblock_all":\
    {
     "signature":"bool bitblock::all(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"bool",
    },
    
    "bitblock_popcount":\
    {
     "signature":"int bitblock::popcount(SIMD_type arg1)",
     "args_type":{"arg1":"SIMD_type"},
     "return_type":"unsigned_int(64)",
     "cpp_class_signature":"static inline uint16_t popcount(SIMD_type arg1)"
    },
    
    "bitblock_srl":\
    {
     "signature":"SIMD_type bitblock::srl(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    
    "bitblock_sll":\
    {
     "signature":"SIMD_type bitblock::sll(SIMD_type arg1, SIMD_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"SIMD_type"},
     "return_type":"SIMD_type",
    },
    "bitblock_srli":\
    {
     "signature":"SIMD_type bitblock::srli<sh>(SIMD_type arg1)",
     "args_type":{"sh":"range(0, fw)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type srli(SIMD_type arg1)",
    },
    
    "bitblock_slli":\
    {
     "signature":"SIMD_type bitblock::slli<sh>(SIMD_type arg1)",
     "args_type":{"sh":"range(0, fw)", "arg1":"SIMD_type"},
     "return_type":"SIMD_type",
     "cpp_class_signature":"template <uint16_t sh> static inline SIMD_type slli(SIMD_type arg1)"
    },
    "bitblock_load_aligned":\
    {
     "signature":"SIMD_type bitblock::load_aligned(load_type arg1)",
     "args_type":{"arg1":"load_type"},
     "return_type":"SIMD_type",
    },
    "bitblock_load_unaligned":\
    {
     "signature":"SIMD_type bitblock::load_unaligned(load_type arg1)",
     "args_type":{"arg1":"load_type"},
     "return_type":"SIMD_type",
    },
    
    "bitblock_store_aligned":\
    {
     "signature":"void bitblock::store_aligned(SIMD_type arg1, store_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"store_type"},
     "return_type":"void",
    },
    "bitblock_store_unaligned":\
    {
     "signature":"void bitblock::store_unaligned(SIMD_type arg1, store_type arg2)",
     "args_type":{"arg1":"SIMD_type", "arg2":"store_type"},
     "return_type":"void",
    },
}
