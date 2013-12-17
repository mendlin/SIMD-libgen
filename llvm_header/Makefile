# 
# To test generated header files
# 
CPPFLAG = -O0 -I../Library_Tester/
SOURCE = playground

ir: $(SOURCE).cpp header.h
	clang++ $(CPPFLAG) -S -emit-llvm $(SOURCE).cpp -o $(SOURCE).ll 

with_ir_header: ir header.ll 
	llvm-link header.ll $(SOURCE).ll -o all.bc
	llvm-dis < all.bc > all.ll
	opt -std-compile-opts -std-link-opts -O3 all.bc -o optimized.bc
	llvm-dis < optimized.bc > optimized.ll

native: with_ir_header
	llc -filetype=obj optimized.bc
	g++ optimized.o -o optimized

run: $(SOURCE).cpp 
	clang++ $(CPPFLAG) $(SOURCE).cpp -o $(SOURCE) 

clean: 
	rm all.* optimized.* playground.ll playground *.bc *.pyc tester.ll tester
