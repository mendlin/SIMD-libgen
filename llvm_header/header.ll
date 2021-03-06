define <16 x i8> @llvm_add_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = add <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_add_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = add <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_add_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = add <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <2 x i64> @llvm_add_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %res = add <2 x i64> %a, %b
    ret <2 x i64> %res
}
define <1 x i128> @llvm_add_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %res = add <1 x i128> %a, %b
    ret <1 x i128> %res
}
define <16 x i8> @llvm_sub_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = sub <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_sub_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = sub <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_sub_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = sub <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <2 x i64> @llvm_sub_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %res = sub <2 x i64> %a, %b
    ret <2 x i64> %res
}
define <1 x i128> @llvm_sub_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %res = sub <1 x i128> %a, %b
    ret <1 x i128> %res
}
define <16 x i8> @llvm_mul_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = mul <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_mul_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = mul <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_mul_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = mul <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <2 x i64> @llvm_mul_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %res = mul <2 x i64> %a, %b
    ret <2 x i64> %res
}
define <16 x i8> @llvm_and_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = and <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_and_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = and <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_and_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = and <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <2 x i64> @llvm_and_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %res = and <2 x i64> %a, %b
    ret <2 x i64> %res
}
define <1 x i128> @llvm_and_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %res = and <1 x i128> %a, %b
    ret <1 x i128> %res
}
define <16 x i8> @llvm_or_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = or <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_or_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = or <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_or_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = or <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <2 x i64> @llvm_or_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %res = or <2 x i64> %a, %b
    ret <2 x i64> %res
}
define <1 x i128> @llvm_or_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %res = or <1 x i128> %a, %b
    ret <1 x i128> %res
}
define <16 x i8> @llvm_xor_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = xor <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_xor_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = xor <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_xor_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = xor <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <2 x i64> @llvm_xor_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %res = xor <2 x i64> %a, %b
    ret <2 x i64> %res
}
define <1 x i128> @llvm_xor_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %res = xor <1 x i128> %a, %b
    ret <1 x i128> %res
}
define <16 x i8> @llvm_icmp_eq_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %cmp_res = icmp eq <16 x i8> %a, %b
	%res = sext <16 x i1> %cmp_res to <16 x i8>
    ret <16 x i8> %res
}
define <8 x i16> @llvm_icmp_eq_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %cmp_res = icmp eq <8 x i16> %a, %b
	%res = sext <8 x i1> %cmp_res to <8 x i16>
    ret <8 x i16> %res
}
define <4 x i32> @llvm_icmp_eq_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %cmp_res = icmp eq <4 x i32> %a, %b
	%res = sext <4 x i1> %cmp_res to <4 x i32>
    ret <4 x i32> %res
}
define <2 x i64> @llvm_icmp_eq_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %cmp_res = icmp eq <2 x i64> %a, %b
	%res = sext <2 x i1> %cmp_res to <2 x i64>
    ret <2 x i64> %res
}
define <1 x i128> @llvm_icmp_eq_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %cmp_res = icmp eq <1 x i128> %a, %b
	%res = sext <1 x i1> %cmp_res to <1 x i128>
    ret <1 x i128> %res
}
define <16 x i8> @llvm_icmp_sgt_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %cmp_res = icmp sgt <16 x i8> %a, %b
	%res = sext <16 x i1> %cmp_res to <16 x i8>
    ret <16 x i8> %res
}
define <8 x i16> @llvm_icmp_sgt_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %cmp_res = icmp sgt <8 x i16> %a, %b
	%res = sext <8 x i1> %cmp_res to <8 x i16>
    ret <8 x i16> %res
}
define <4 x i32> @llvm_icmp_sgt_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %cmp_res = icmp sgt <4 x i32> %a, %b
	%res = sext <4 x i1> %cmp_res to <4 x i32>
    ret <4 x i32> %res
}
define <2 x i64> @llvm_icmp_sgt_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %cmp_res = icmp sgt <2 x i64> %a, %b
	%res = sext <2 x i1> %cmp_res to <2 x i64>
    ret <2 x i64> %res
}
define <1 x i128> @llvm_icmp_sgt_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %cmp_res = icmp sgt <1 x i128> %a, %b
	%res = sext <1 x i1> %cmp_res to <1 x i128>
    ret <1 x i128> %res
}
define <16 x i8> @llvm_icmp_ugt_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %cmp_res = icmp ugt <16 x i8> %a, %b
	%res = sext <16 x i1> %cmp_res to <16 x i8>
    ret <16 x i8> %res
}
define <8 x i16> @llvm_icmp_ugt_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %cmp_res = icmp ugt <8 x i16> %a, %b
	%res = sext <8 x i1> %cmp_res to <8 x i16>
    ret <8 x i16> %res
}
define <4 x i32> @llvm_icmp_ugt_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %cmp_res = icmp ugt <4 x i32> %a, %b
	%res = sext <4 x i1> %cmp_res to <4 x i32>
    ret <4 x i32> %res
}
define <2 x i64> @llvm_icmp_ugt_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %cmp_res = icmp ugt <2 x i64> %a, %b
	%res = sext <2 x i1> %cmp_res to <2 x i64>
    ret <2 x i64> %res
}
define <1 x i128> @llvm_icmp_ugt_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %cmp_res = icmp ugt <1 x i128> %a, %b
	%res = sext <1 x i1> %cmp_res to <1 x i128>
    ret <1 x i128> %res
}
define <16 x i8> @llvm_icmp_slt_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %cmp_res = icmp slt <16 x i8> %a, %b
	%res = sext <16 x i1> %cmp_res to <16 x i8>
    ret <16 x i8> %res
}
define <8 x i16> @llvm_icmp_slt_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %cmp_res = icmp slt <8 x i16> %a, %b
	%res = sext <8 x i1> %cmp_res to <8 x i16>
    ret <8 x i16> %res
}
define <4 x i32> @llvm_icmp_slt_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %cmp_res = icmp slt <4 x i32> %a, %b
	%res = sext <4 x i1> %cmp_res to <4 x i32>
    ret <4 x i32> %res
}
define <2 x i64> @llvm_icmp_slt_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %cmp_res = icmp slt <2 x i64> %a, %b
	%res = sext <2 x i1> %cmp_res to <2 x i64>
    ret <2 x i64> %res
}
define <1 x i128> @llvm_icmp_slt_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %cmp_res = icmp slt <1 x i128> %a, %b
	%res = sext <1 x i1> %cmp_res to <1 x i128>
    ret <1 x i128> %res
}
define <16 x i8> @llvm_icmp_ult_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %cmp_res = icmp ult <16 x i8> %a, %b
	%res = sext <16 x i1> %cmp_res to <16 x i8>
    ret <16 x i8> %res
}
define <8 x i16> @llvm_icmp_ult_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %cmp_res = icmp ult <8 x i16> %a, %b
	%res = sext <8 x i1> %cmp_res to <8 x i16>
    ret <8 x i16> %res
}
define <4 x i32> @llvm_icmp_ult_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %cmp_res = icmp ult <4 x i32> %a, %b
	%res = sext <4 x i1> %cmp_res to <4 x i32>
    ret <4 x i32> %res
}
define <2 x i64> @llvm_icmp_ult_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %cmp_res = icmp ult <2 x i64> %a, %b
	%res = sext <2 x i1> %cmp_res to <2 x i64>
    ret <2 x i64> %res
}
define <1 x i128> @llvm_icmp_ult_128(<1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %cmp_res = icmp ult <1 x i128> %a, %b
	%res = sext <1 x i1> %cmp_res to <1 x i128>
    ret <1 x i128> %res
}
define <16 x i8> @llvm_shl_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = shl <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_shl_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = shl <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_shl_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = shl <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <16 x i8> @llvm_lshr_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = lshr <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_lshr_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = lshr <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_lshr_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = lshr <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <16 x i8> @llvm_ashr_8(<16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %res = ashr <16 x i8> %a, %b
    ret <16 x i8> %res
}
define <8 x i16> @llvm_ashr_16(<8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %res = ashr <8 x i16> %a, %b
    ret <8 x i16> %res
}
define <4 x i32> @llvm_ashr_32(<4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %res = ashr <4 x i32> %a, %b
    ret <4 x i32> %res
}
define <2 x i64> @llvm_ashr_64(<2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %res = ashr <2 x i64> %a, %b
    ret <2 x i64> %res
}
define i32 @llvm_extractelement_32(<4 x i32> %a, i32 %idx) alwaysinline {
entry:
    %res = extractelement <4 x i32> %a, i32 %idx
    ret i32 %res
}
define i16 @llvm_extractelement_16(<8 x i16> %a, i32 %idx) alwaysinline {
entry:
    %res = extractelement <8 x i16> %a, i32 %idx
    ret i16 %res
}
define i64 @llvm_extractelement_64(<2 x i64> %a, i32 %idx) alwaysinline {
entry:
    %res = extractelement <2 x i64> %a, i32 %idx
    ret i64 %res
}
define <4 x i32> @llvm_insertelement_32(<4 x i32> %a, i32 %val, i32 %idx) alwaysinline {
entry:
    %res = insertelement <4 x i32> %a, i32 %val, i32 %idx
    ret <4 x i32> %res
}
define <8 x i16> @llvm_insertelement_16(<8 x i16> %a, i16 %val, i32 %idx) alwaysinline {
entry:
    %res = insertelement <8 x i16> %a, i16 %val, i32 %idx
    ret <8 x i16> %res
}
define <2 x i64> @llvm_insertelement_64(<2 x i64> %a, i64 %val, i32 %idx) alwaysinline {
entry:
    %res = insertelement <2 x i64> %a, i64 %val, i32 %idx
    ret <2 x i64> %res
}
define <2 x i64> @llvm_load_aligned(<2 x i64>* %a) alwaysinline {
entry:
    %res = load <2 x i64>* %a, align 16
    ret <2 x i64> %res
}
define <2 x i64> @llvm_load_unaligned(<2 x i64>* %a) alwaysinline {
entry:
    %res = load <2 x i64>* %a, align 1
    ret <2 x i64> %res
}
define void @llvm_store_aligned(<2 x i64> %a, <2 x i64>* %addr) alwaysinline {
entry:
  store <2 x i64> %a, <2 x i64>* %addr, align 16
  ret void
}
define void @llvm_store_unaligned(<2 x i64> %a, <2 x i64>* %addr) alwaysinline {
entry:
  store <2 x i64> %a, <2 x i64>* %addr, align 1
  ret void
}
define <16 x i8> @llvm_ifh_8(<16 x i8> %mask, <16 x i8> %a, <16 x i8> %b) alwaysinline {
entry:
    %0 = icmp slt <16 x i8> %mask, <i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0, i8 0>
    %1 = select <16 x i1> %0, <16 x i8> %a, <16 x i8> %b
    ret <16 x i8> %1
}
define <8 x i16> @llvm_ifh_16(<8 x i16> %mask, <8 x i16> %a, <8 x i16> %b) alwaysinline {
entry:
    %0 = icmp slt <8 x i16> %mask, <i16 0, i16 0, i16 0, i16 0, i16 0, i16 0, i16 0, i16 0>
    %1 = select <8 x i1> %0, <8 x i16> %a, <8 x i16> %b
    ret <8 x i16> %1
}
define <4 x i32> @llvm_ifh_32(<4 x i32> %mask, <4 x i32> %a, <4 x i32> %b) alwaysinline {
entry:
    %0 = icmp slt <4 x i32> %mask, <i32 0, i32 0, i32 0, i32 0>
    %1 = select <4 x i1> %0, <4 x i32> %a, <4 x i32> %b
    ret <4 x i32> %1
}
define <2 x i64> @llvm_ifh_64(<2 x i64> %mask, <2 x i64> %a, <2 x i64> %b) alwaysinline {
entry:
    %0 = icmp slt <2 x i64> %mask, <i64 0, i64 0>
    %1 = select <2 x i1> %0, <2 x i64> %a, <2 x i64> %b
    ret <2 x i64> %1
}
define <1 x i128> @llvm_ifh_128(<1 x i128> %mask, <1 x i128> %a, <1 x i128> %b) alwaysinline {
entry:
    %0 = icmp slt <1 x i128> %mask, <i128 0>
    %1 = select <1 x i1> %0, <1 x i128> %a, <1 x i128> %b
    ret <1 x i128> %1
}
define <4 x i32> @llvm_constant_32(i32 %val) alwaysinline {
entry:
  %0 = insertelement <4 x i32> undef, i32 %val, i32 0
  %1 = shufflevector <4 x i32> %0, <4 x i32> undef, <4 x i32> <i32 0, i32 0, i32 0, i32 0>
  ret <4 x i32> %1
}
define <8 x i16> @llvm_constant_16(i16 %val) alwaysinline {
entry:
  %0 = insertelement <8 x i16> undef, i16 %val, i32 0
  %1 = shufflevector <8 x i16> %0, <8 x i16> undef, <8 x i32> <i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0, i32 0>
  ret <8 x i16> %1
}
define <2 x i64> @llvm_constant_64(i64 %val) alwaysinline {
entry:
  %0 = insertelement <2 x i64> undef, i64 %val, i32 0
  %1 = shufflevector <2 x i64> %0, <2 x i64> undef, <2 x i32> <i32 0, i32 0>
  ret <2 x i64> %1
}
