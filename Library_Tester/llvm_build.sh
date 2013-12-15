# The first argument, $1 is executable name, $2 is source file name
echo "Build llvm-simd tests..."

clang++ -O3 -S -emit-llvm "$2" -o p.ll 
llvm-link ../llvm_header/header.ll p.ll -o all.bc
opt -std-compile-opts -std-link-opts -O3 all.bc -o optimized.bc
llc optimized.bc -o "$1"

rm p.ll all.bc optimized.bc