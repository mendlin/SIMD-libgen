/*  p2s - Serial to Parallel Bit Stream Transposition
    Copyright (c) 2007, 2008, 2010, Robert D. Cameron.
    Licensed to the public under the Open Software License 3.0.
    Licensed to International Characters Inc.
       under the Academic Free License version 3.0.

*/

#ifndef P2S_HPP
#define P2S_HPP

#include "idisa128.hpp"

#define BytePack BitBlock

/*
/* Given 8 parallel bitstream blocks p0, p1, ..., p7, inverse transpose
   the data into a block of bytes in 8 consecutive registers s0, s1, ..., s7.

   The following header shows the intent, although a macro is used for
   speed.
static inline void p2s(BitBlock p0, BitBlock p1, BitBlock p2, BitBlock p3, 
                       BitBlock p4, BitBlock p5, BitBlock p6, BitBlock p7,
                       BytePack& s0, BytePack& s1, BytePack& s2, BytePack& s3,
                       BytePack& s5, BytePack& s6, BytePack& s7, BytePack& s8,
                       );

*/

/* Different algorithms may be selected. */
#ifdef USE_P2S_IDEAL
#define P2S_ALGORITHM p2s_ideal
#endif

#ifndef P2S_ALGORITHM
#define P2S_ALGORITHM p2s_bytemerge
#endif

/*  p2s_ideal is an ideal parallel to serial transposition
    algorithm given an architecture with native support for
    esimd<{4,2,1}>::merge{h,l} operations, achieving transposition
    of 8 parallel bitblocks into 8 serial bytepacks in only 24 merge
    operations.
*/

#define p2s_ideal(p0,p1,p2,p3,p4,p5,p6,p7,s0,s1,s2,s3,s4,s5,s6,s7)  \
  do { \
	BitBlock bit01_r0,bit01_r1,bit23_r0,bit23_r1,bit45_r0,bit45_r1,bit67_r0,bit67_r1; \
	BitBlock bit0123_r0,bit0123_r1,bit0123_r2,bit0123_r3, \
	bit4567_r0,bit4567_r1,bit4567_r2,bit4567_r3; \
	bit01_r0= esimd<1>::mergeh(p0,p1) ; \
	bit01_r1= esimd<1>::mergel(p0,p1) ; \
	bit23_r0= esimd<1>::mergeh(p2,p3) ; \
	bit23_r1= esimd<1>::mergel(p2,p3) ; \
	bit45_r0= esimd<1>::mergeh(p4,p5) ; \
	bit45_r1= esimd<1>::mergel(p4,p5) ; \
	bit67_r0= esimd<1>::mergeh(p6,p7) ; \
	bit67_r1= esimd<1>::mergel(p6,p7) ; \
	bit0123_r0= esimd<2>::mergeh(bit01_r0,bit23_r0) ; \
	bit0123_r1= esimd<2>::mergel(bit01_r0,bit23_r0) ; \
	bit0123_r2= esimd<2>::mergeh(bit01_r1,bit23_r1) ; \
	bit0123_r3= esimd<2>::mergel(bit01_r1,bit23_r1) ; \
	bit4567_r0= esimd<2>::mergeh(bit45_r0,bit67_r0) ; \
	bit4567_r1= esimd<2>::mergel(bit45_r0,bit67_r0) ; \
	bit4567_r2= esimd<2>::mergeh(bit45_r1,bit67_r1) ; \
	bit4567_r3= esimd<2>::mergel(bit45_r1,bit67_r1) ; \
	s0= esimd<4>::mergeh(bit0123_r0,bit4567_r0) ; \
	s1= esimd<4>::mergel(bit0123_r0,bit4567_r0) ; \
	s2= esimd<4>::mergeh(bit0123_r1,bit4567_r1) ; \
	s3= esimd<4>::mergel(bit0123_r1,bit4567_r1) ; \
	s4= esimd<4>::mergeh(bit0123_r2,bit4567_r2) ; \
	s5= esimd<4>::mergel(bit0123_r2,bit4567_r2) ; \
	s6= esimd<4>::mergeh(bit0123_r3,bit4567_r3) ; \
	s7= esimd<4>::mergel(bit0123_r3,bit4567_r3) ; \
  } while(0) 

/*  p2s_bytemerge is a fast parallel to serial transposition
    algorithm given an architecture with esimd<8>::merge{h,l},
    but not at small field widths.
    MMX, SSE, Altivec ...
*/
  
#define p2s_step(p0,p1,hi_mask,shift,s0,s1)  \
  do { \
	BitBlock t0,t1; \
	t0= simd<1>::ifh(hi_mask,p0,simd<16>::srli<shift>(p1)) ; \
	t1= simd<1>::ifh(hi_mask,simd<16>::slli<shift>(p0),p1) ; \
	s0= esimd<8>::mergeh(t0,t1) ; \
	s1= esimd<8>::mergel(t0,t1) ; \
  } while(0)

#define p2s_bytemerge(p0,p1,p2,p3,p4,p5,p6,p7,s0,s1,s2,s3,s4,s5,s6,s7)  \
  do { \
	BitBlock bit00004444_0,bit22226666_0,bit00004444_1,bit22226666_1; \
	BitBlock bit11115555_0,bit33337777_0,bit11115555_1,bit33337777_1; \
	BitBlock bit00224466_0,bit00224466_1,bit00224466_2,bit00224466_3; \
	BitBlock bit11335577_0,bit11335577_1,bit11335577_2,bit11335577_3; \
	p2s_step(p0,p4,simd<8>::himask(),4,bit00004444_0,bit00004444_1);  \
	p2s_step(p1,p5,simd<8>::himask(),4,bit11115555_0,bit11115555_1);  \
	p2s_step(p2,p6,simd<8>::himask(),4,bit22226666_0,bit22226666_1);  \
	p2s_step(p3,p7,simd<8>::himask(),4,bit33337777_0,bit33337777_1);  \
	p2s_step(bit00004444_0,bit22226666_0,simd<4>::himask(),2,bit00224466_0,bit00224466_1);  \
	p2s_step(bit11115555_0,bit33337777_0,simd<4>::himask(),2,bit11335577_0,bit11335577_1);  \
	p2s_step(bit00004444_1,bit22226666_1,simd<4>::himask(),2,bit00224466_2,bit00224466_3);  \
	p2s_step(bit11115555_1,bit33337777_1,simd<4>::himask(),2,bit11335577_2,bit11335577_3);  \
	p2s_step(bit00224466_0,bit11335577_0,simd<2>::himask(),1,s0,s1);  \
	p2s_step(bit00224466_1,bit11335577_1,simd<2>::himask(),1,s2,s3);  \
	p2s_step(bit00224466_2,bit11335577_2,simd<2>::himask(),1,s4,s5);  \
	p2s_step(bit00224466_3,bit11335577_3,simd<2>::himask(),1,s6,s7);  \
  } while(0)

#define p2s(p0, p1, p2, p3, p4, p5, p6, p7, s0, s1, s2, s3, s4, s5, s6, s7)\
  P2S_ALGORITHM(p0, p1, p2, p3, p4, p5, p6, p7, s7, s6, s5, s4, s3, s2, s1, s0)

#endif // P2S_HPP

