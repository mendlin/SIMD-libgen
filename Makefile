
GENERATOR_DIR = Library_Generator
TESTER_DIR = Library_Tester
CONFIGURE_DIR = Configure
LIB_DIR = ../lib
IDISA_LIB_DIR = idisa_lib
IDISA_LIB_CPP_DIR = $(IDISA_LIB_DIR)/idisa_cpp
IDISA_LIB_C_DIR = $(IDISA_LIB_DIR)/idisa_c
LIB_CPP_DIR = $(LIB_DIR)/idisa_cpp

IDISA_GENERATOR = $(GENERATOR_DIR)/LibraryGenerator.py
IDISA_TESTER = $(TESTER_DIR)/LibraryTester.py

IDISA_SSE2_C_LIB = idisa_sse2_c
IDISA_SSE2_CPP_LIB = idisa_sse2

IDISA_SSE3_CPP_LIB = idisa_sse3

IDISA_SSSE3_CPP_LIB = idisa_ssse3

IDISA_SSE4_1_CPP_LIB = idisa_sse4_1

IDISA_SSE4_2_CPP_LIB = idisa_sse4_2

IDISA_NEON_CPP_LIB = idisa_neon

IDISA_AVX_CPP_LIB = idisa_avx
IDISA_AVX2_CPP_LIB = idisa_avx2

IDISA128 = idisa128

IDISA256 = idisa256

IDISA = idisa

BODY_DECLARATION = declaration

BODY_IMPLEMENTATION = implementation

playground: Library_Tester/playground.cpp
	# g++ -o playground -mavx2 -march=core-avx2 Library_Tester/playground.cpp	
	g++ -o playground -msse2 Library_Tester/playground.cpp		

sse2:
	python $(IDISA_GENERATOR) -a sse2 -l cpp -f $(IDISA_SSE2_CPP_LIB).h -g
sse2_c:
	python $(IDISA_GENERATOR) -a sse2 -l c -f $(IDISA_SSE2_C_LIB).h -g
sse2_test:
	python $(IDISA_TESTER) -a sse2 -l cpp -f $(IDISA_SSE2_CPP_LIB) -t
sse2_c_test:
	python $(IDISA_TESTER) -a sse2 -l c -f $(IDISA_SSE2_C_LIB) -t

#sse2_strategy_count:
#	python $(IDISA_GENERATOR) -a sse2 -l cpp -f $(IDISA_SSE2_CPP_LIB).h -g --strategy_count = True

#sse2_strategy_compare:
#	python $(IDISA_GENERATOR) -a sse2 -l cpp -f $(IDISA_SSE2_CPP_LIB).h -g --strategy_comparison = True

#sse2_instruction_count:
#	python $(IDISA_TESTER) -a sse2 -l cpp -f $(IDISA_SSE2_CPP_LIB) -t --instruction_count = True

sse3:
	python $(IDISA_GENERATOR) -a sse3 -l cpp -f $(IDISA_SSE3_CPP_LIB).h -g
sse3_c:
	python $(IDISA_GENERATOR) -a sse3 -l c -f $(IDISA_SSE3_CPP_LIB)_c.h -g
sse3_test:
	python $(IDISA_TESTER) -a sse3 -l cpp -f $(IDISA_SSE3_CPP_LIB) -t
sse3_c_test:
	python $(IDISA_TESTER) -a sse3 -l c -f $(IDISA_SSE3_CPP_LIB)_c -t

ssse3:
	python $(IDISA_GENERATOR) -a ssse3 -l cpp -f $(IDISA_SSSE3_CPP_LIB).h -g
ssse3_test:
	python $(IDISA_TESTER) -a ssse3 -l cpp -f $(IDISA_SSSE3_CPP_LIB) -t
ssse3_c:
	python $(IDISA_GENERATOR) -a ssse3 -l c -f $(IDISA_SSSE3_CPP_LIB)_c.h -g
ssse3_c_test:
	python $(IDISA_TESTER) -a ssse3 -l c -f $(IDISA_SSSE3_CPP_LIB)_c -t	

sse4_1:
	python $(IDISA_GENERATOR) -a sse4_1 -l cpp -f $(IDISA_SSE4_1_CPP_LIB).h -g
sse4_1_test:
	python $(IDISA_TESTER) -a sse4_1 -l cpp -f $(IDISA_SSE4_1_CPP_LIB) -t
sse4_1_c:
	python $(IDISA_GENERATOR) -a sse4_1 -l c -f $(IDISA_SSE4_1_CPP_LIB)_c.h -g
sse4_1_c_test:
	python $(IDISA_TESTER) -a sse4_1 -l c -f $(IDISA_SSE4_1_CPP_LIB)_c -t

sse4_2:
	python $(IDISA_GENERATOR) -a sse4_2 -l cpp -f $(IDISA_SSE4_2_CPP_LIB).h -g
sse4_2_test:
	python $(IDISA_TESTER) -a sse4_2 -l cpp -f $(IDISA_SSE4_2_CPP_LIB) -t
sse4_2_c:
	python $(IDISA_GENERATOR) -a sse4_2 -l c -f $(IDISA_SSE4_2_CPP_LIB)_c.h -g
sse4_2_c_test:
	python $(IDISA_TESTER) -a sse4_2 -l c -f $(IDISA_SSE4_2_CPP_LIB)_c -t	

neon:
	python $(IDISA_GENERATOR) -a neon -l cpp -f $(IDISA_NEON_CPP_LIB).h -g

#neon_strategy_count:
#	python $(IDISA_GENERATOR) -a neon -l cpp -f $(IDISA_NEON_CPP_LIB).h -g --strategy_count = True

#neon_generate_data:
#	python $(IDISA_TESTER) -a neon -l cpp -f $(IDISA_NEON_CPP_LIB) -t -o neon_gen_data

#neon_test:
#	python $(IDISA_TESTER) -a neon -l cpp -f $(IDISA_NEON_CPP_LIB) -t -o neon_test_data

avx:
	python $(IDISA_GENERATOR) -a avx -l cpp -f $(IDISA_AVX_CPP_LIB).h -g
avx_test:
	python $(IDISA_TESTER) -a avx -l cpp -f $(IDISA_AVX_CPP_LIB) -t
avx2:
	python $(IDISA_GENERATOR) -a avx2 -l cpp -f $(IDISA_AVX2_CPP_LIB).h -g
avx2_test:
	python $(IDISA_TESTER) -a avx2 -l cpp -f $(IDISA_AVX2_CPP_LIB) -t
#avx_strategy_count:
#	python $(IDISA_GENERATOR) -a avx -l cpp -f $(IDISA_AVX_CPP_LIB).h -g --strategy_count = True
#avx_strategy_compare:
#	python $(IDISA_GENERATOR) -a avx -l cpp -f $(IDISA_AVX_CPP_LIB).h -g --strategy_comparison = True
#avx_instruction_count:
#	python $(IDISA_TESTER) -a avx -l cpp -f $(IDISA_AVX_CPP_LIB) -t --instruction_count = True
	
idisa128:
	# produces the idisa128.hpp with only declaration of idisa operations
	# copys the idisa128.hpp from generator's directory to idisa_lib/
	python $(IDISA_GENERATOR) -a sse2 -l cpp -f $(IDISA128).hpp -g --body=$(BODY_DECLARATION)
	mv $(GENERATOR_DIR)/$(IDISA128).hpp $(LIB_DIR)/
	
	# produces the idisa_sse2/sse3/ssse3/sse4_1/sse4_2.cpp containing the implementation of idisa operations
	# copys the idisa_sse2/sse3/ssse3/sse4_1/sse4_2.cpp from generator's directory to idisa_lib/cpp/
	python $(IDISA_GENERATOR) -a sse2 -l cpp -f $(IDISA_SSE2_CPP_LIB).cpp -g --body=$(BODY_IMPLEMENTATION)
	mv $(GENERATOR_DIR)/$(IDISA_SSE2_CPP_LIB).cpp $(LIB_CPP_DIR)/
	
	python $(IDISA_GENERATOR) -a sse3 -l cpp -f $(IDISA_SSE3_CPP_LIB).cpp -g --body=$(BODY_IMPLEMENTATION)
	mv $(GENERATOR_DIR)/$(IDISA_SSE3_CPP_LIB).cpp $(LIB_CPP_DIR)/
	
	python $(IDISA_GENERATOR) -a ssse3 -l cpp -f $(IDISA_SSSE3_CPP_LIB).cpp -g --body=$(BODY_IMPLEMENTATION)
	mv $(GENERATOR_DIR)/$(IDISA_SSSE3_CPP_LIB).cpp $(LIB_CPP_DIR)/
	
	python $(IDISA_GENERATOR) -a sse4_1 -l cpp -f $(IDISA_SSE4_1_CPP_LIB).cpp -g --body=$(BODY_IMPLEMENTATION)
	mv $(GENERATOR_DIR)/$(IDISA_SSE4_1_CPP_LIB).cpp $(LIB_CPP_DIR)/
	
	python $(IDISA_GENERATOR) -a sse4_2 -l cpp -f $(IDISA_SSE4_2_CPP_LIB).cpp -g --body=$(BODY_IMPLEMENTATION)
	mv $(GENERATOR_DIR)/$(IDISA_SSE4_2_CPP_LIB).cpp $(LIB_CPP_DIR)/
	
	python $(IDISA_GENERATOR) -a neon -l cpp -f $(IDISA_NEON_CPP_LIB).cpp -g --body=$(BODY_IMPLEMENTATION)
	mv $(GENERATOR_DIR)/$(IDISA_NEON_CPP_LIB).cpp $(LIB_CPP_DIR)/

idisa256:
	# produces the idisa256.cpp with only declaration of idisa operations
	# copys the idisa256.cpp from generator's directory to idisa_lib/
	python $(IDISA_GENERATOR) -a avx -l cpp -f $(IDISA256).hpp -g --body=$(BODY_DECLARATION)
	mv $(GENERATOR_DIR)/$(IDISA256).hpp $(LIB_DIR)/
	
	# produces the idisa_avx.hpp containing the implementation of idisa operations
	# copys the idisa_avx.hpp from generator's directory to idisa_lib/cpp/
	python $(IDISA_GENERATOR) -a avx -l cpp -f $(IDISA_AVX_CPP_LIB).cpp -g --body=$(BODY_IMPLEMENTATION)
	mv $(GENERATOR_DIR)/$(IDISA_AVX_CPP_LIB).cpp $(LIB_CPP_DIR)/

	python $(IDISA_GENERATOR) -a avx2 -l cpp -f $(IDISA_AVX2_CPP_LIB).cpp -g --body=$(BODY_IMPLEMENTATION)
	mv $(GENERATOR_DIR)/$(IDISA_AVX2_CPP_LIB).cpp $(LIB_CPP_DIR)/

idisa:
	make idisa128
	make idisa256
	python $(IDISA_GENERATOR) -a sse2 -l cpp -f $(IDISA).hpp -g --body=$(BODY_DECLARATION)
	mv $(GENERATOR_DIR)/$(IDISA).hpp $(LIB_DIR)/

idisa128_c:
	make sse2_c
	make sse3_c
	make ssse3_c
	make sse4_1_c
	make sse4_2_c	

	mv $(GENERATOR_DIR)/idisa_sse2_c.h $(LIB_DIR)/idisa_c
	mv $(GENERATOR_DIR)/idisa_sse3_c.h $(LIB_DIR)/idisa_c
	mv $(GENERATOR_DIR)/idisa_ssse3_c.h $(LIB_DIR)/idisa_c
	mv $(GENERATOR_DIR)/idisa_sse4_1_c.h $(LIB_DIR)/idisa_c
	mv $(GENERATOR_DIR)/idisa_sse4_2_c.h $(LIB_DIR)/idisa_c

clean:
	rm -f $(GENERATOR_DIR)/*.pyc
	rm -f $(GENERATOR_DIR)/idisa*.*
	rm -f $(TESTER_DIR)/*.pyc
	rm -f $(TESTER_DIR)/*test.cpp
	rm -f $(TESTER_DIR)/SS*_test
	rm -f $(TESTER_DIR)/AVX*_test
	rm -f $(TESTER_DIR)/idisa*.*
	rm -f $(TESTER_DIR)/CalculatingModules/*.pyc
	rm -f $(TESTER_DIR)/input/*
	rm -f $(TESTER_DIR)/output/*
	rm -f $(TESTER_DIR)/output_temp/*
	rm -f $(CONFIGURE_DIR)/*.pyc
