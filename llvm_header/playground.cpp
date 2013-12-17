#include "utility.h"
#include "header.h"

int main()
{	
	SIMD_type a, b, c;	
	a = mvmd<32>::fill4(rand(), rand(), rand(), rand());
	// a = simd<32>::constant<2>();
	b = simd<32>::constant<2>();
	
	cout << "Playground running..." << endl;
	
	c = llvm_add_8(a, b);
	cout << Store2String(c, 1) << endl;	

	return 0;
}

