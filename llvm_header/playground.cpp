#include "utility.h"
#include "header.h"

int main()
{	
	SIMD_type a, b, c;		
	// a = mvmd<32>::fill4(rand(), rand(), rand(), rand());
	// a = simd<32>::constant<2>();
	// b = simd<32>::constant<2>();
	
	// cout << "Playground running..." << endl;
	
	// c = llvm_constant_32(2);	
	// c = simd<2>::constant<0>();
	for (int i = 0; i < 100; i++)
	{
		c = llvm_constant_32(15);
		cout << Store2String(c, 1) << endl;	
	}
		
	// b = simd<32>::constant<15>();

	// c = simd<32>::ifh(c, a, b);
	// c = llvm_ifh_32(c, a, b);
	// // cout << Store2String(b, 1) << endl;
	// cout << Store2String(a, 1) << endl;
	// cout << Store2String(b, 1) << endl;

	return 0;
}

