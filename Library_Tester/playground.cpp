#include "utility.h"

int main()
{
	SIMD_type a, b, c, d, e;	
	// b = simd<32>::constant<11>();
	string str = "1001000000000000010001001111101000010101111000011100010010010101100110111000101001011010111001000111100110100110100101001100000011110010010101101010110001101000000000001000111100011000011010001001011111001111100010010011011010001110101101100010101111110101";
	b = LoadfromString(str, 2);

	cout <<"b:"<<endl;
	cout <<Store2String(b, 2) <<endl;

	// a = bitblock::slli<0>(b);
	c = simd<128>::slli<0>(b);
	d = simd<128>::srli<128>(b);

	cout << ((256-0) & 127) <<endl;

	cout <<"d:"<<endl;
	cout <<Store2String(d, 2) <<endl;

	a = avx_move_lo128_to_hi128(d);

	cout <<"a:"<<endl;
	cout <<Store2String(a, 2) <<endl;

	return 0;
}