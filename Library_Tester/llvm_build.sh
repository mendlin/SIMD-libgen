# The first argument, $1 is executable name
echo "Build llvm-simd tests..."
rm all.* optimized.* p.ll

clang++ -O3 -S -emit-llvm "$1".cpp -o p.ll 
llvm-link ../llvm_header/header.ll p.ll -o all.bc
opt -std-compile-opts -std-link-opts -O3 all.bc -o optimized.bc
