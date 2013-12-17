llvm_test:
	clang++ -O0 -S -emit-llvm LLVM128_test.cpp -o p.ll 
	llvm-link ../llvm_header/header.ll p.ll -o all.bc
	opt -std-compile-opts -std-link-opts -O3 all.bc -o optimized.bc
	llc -filetype=obj optimized.bc 
	g++ optimized.o -o LLVM128_test

clean:
	rm -f all.* optimized.* p.ll
