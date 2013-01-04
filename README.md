Copyright (c) 2011, Hua Huang and Robert D. Cameron.

Licensed under the Academic Free License 3.0. 

# Overview:
This is a toolkit called IDISA+ which could automatically generate SIMD libraries
for SSE2/SSE3/SSSE3/SSE4.1/SSE4.2/AVX/NEON platforms. The supported operations can be found in the IDISA+.pdf.
This toolkit has two components, the library generator and the library tester.

## The Generator:
BuiltIns.py - it packs all built-in intrinsics of a specified instruction set;
CppTranslator.py - it parses the strategies and intrinsics to omit the C++ candidate implementations for analyzer to use;
OperationSetAnalyzer.py - it analyzes the C++ candidate implementations to find the best implementations for each operation on certain fields;      

I have created two algorithms for evaluating the cost of if-else branches, they are "CheckIfElseBranch" and "CheckIfElseBranchAvg";
The current version uses the "CheckIfElseBranchAvg", i.e., use the average cost of all branches as the final cost;
StrategyPool.py - it's the file in which you can create your own strategies;

## The Tester:
CalculatingModules - this folder has the simulation programs for all defined operations;
GenerateCppTests.py - creates the C++ file for doing unit-test on each function in a generated library;
utility.h - it contains some I/O routines and other auxiliary programs for unit-testing;
			Changes will be made to this file (such as define a different macro or include a correct SIMD library) by the tester when it is doing unit-test;

## Configuration:
All configuration files are placed at the Configure/ directory.
* configure.py - it defines many information for both generator and tester to use;
* IDISAOperations.py - this is the file where users can define their own operations;

*Remember to add intrinsics (if the newly defined operations have built-in intrinsics) or create strategies to implement the operations;*


## For NEON testing:
Please work on a machine where the ARM NEON environment is set up correcly (e.g., the "cs-osl-04" in our lab).

1. copy the libgen/ to the location "/opt/android-ndk-r5b/samples/hello-neon/jni" (there is a makefile located at "/opt/android-ndk-r5b/samples/hello-neon/");

2. go to "/opt/android-ndk-r5b/samples/hello-neon", issue the following commands:

   "make neon" - it generates neon library, i.e., the idisa_neon.h;
   "make binary" - it generates a testing cpp file called "NEON_test.cpp" and compiles it with idisa_neon.h and "utility.h" into binary and
   				   pushes the binary as well as the test data to the tablet;

3. switch to the tablet terminal and go the /data/neon-test directory of the tablet, run "./NEON_test" (type "su" to make sure you are in the superuser mode);

4. switch back to the computer terminal(at "/opt/android-ndk-r5b/samples/hello-neon"), run
   "make check" - it pulls the output of NEON_test out from the tablet and compares this output with the standard output to check the correctness of NEON library;

