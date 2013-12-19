#include "utility.h"
#include "header.h"

void test_equal(const SIMD_type &a, const SIMD_type &b)
{
	if (Store2String(a, 1) != Store2String(b, 1))
		cout << "Error: Not equal" << endl;
}

// Play with macros, ## means concatination
#define test_constant(fw) \
	test_equal(simd<fw>::ifh(d, a, b), llvm_ifh_##fw(d, a, b))

int main()
{	
	SIMD_type a, b, c, d;
	a = mvmd<32>::fill4(rand(), rand(), rand(), rand());		
	
	cout << "Playground running..." << endl;
	
	b = simd<32>::constant<122>();
	c = llvm_constant_32(122);
	test_equal(b, c);

	b = simd<16>::constant<56>();
	c = llvm_constant_16(56);
	test_equal(b, c);

	b = simd<64>::constant<12232>();
	c = llvm_constant_64(12232);
	test_equal(b, c);
		
	d = simd<2>::constant<0>();
	test_constant(8);
	test_constant(16);
	test_constant(32);
	test_constant(64);
	test_constant(128);

	return 0;
}

