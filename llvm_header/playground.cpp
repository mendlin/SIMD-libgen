#include "utility.h"
#include "header.h"

int main()
{	
	// SIMD_type a, b, c;	
	SIMD_type c;
	// a = mvmd<32>::fill4(rand(), rand(), rand(), rand());
	// a = simd<32>::constant<2>();
	// b = simd<32>::constant<2>();
	
	// cout << "Playground running..." << endl;
	
	// c = llvm_constant_32(2);
	c = simd<32>::constant<2>();
	// cout << Store2String(b, 1) << endl;
	cout << Store2String(c, 1) << endl;	

	return 0;
}

