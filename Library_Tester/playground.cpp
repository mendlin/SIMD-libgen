#include "utility.h"

int main()
{
	SIMD_type a, b;
	a = simd<32>::constant<5>();
	b = simd<32>::constant<11>();
	string res = Store2String(a, 2);
	cout <<"a:"<<endl;
	cout <<res <<endl;
	cout <<"b:"<<endl;
	cout <<Store2String(b, 2) <<endl;

	SIMD_type alpha = _mm256_permute2x128_si256(b, a, (int32_t)(32));
	SIMD_type beta = _mm256_permute2x128_si256(b, a, (int32_t)(49));

	cout <<"alpha:"<<endl;
	cout <<Store2String(alpha, 2) <<endl;

	cout <<"beta:"<<endl;
	cout <<Store2String(beta, 2) <<endl;

	return 0;
}