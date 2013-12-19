# How to setup LLVM header playground

When we are writing LLVM header files, we want to have a quick check of whether it works. So we have `playground.cpp`. It has access to 
IDISA SSE2 library and LLVM headers(`header.h` and `header.ll`).

## Setup

Clone this repo's master branch:

```shell
git clone https://github.com/Logicalmars/SIMD-libgen.git libgen
```

Or get the code from SVN:

```shell
svn co http://parabix.costar.sfu.ca/svn/trunk/libgen
```

Then, prepare header files:

```shell
/libgen$ make sse2
/libgen$ make sse2_test  #generate necessary headers
/libgen$ cd llvm_header
/libgen/llvm_header$ make native
```

The last `make` should success and you will have the executable `./optimized`.

## Folder layout

### Generator

```
├── config.py
├── func_gener
│   ├── AbstractFuncGener.py
│   ├── Constant.py
│   ├── IFH.py
│   ├── __init__.py
├── header_gen.py
├── op_tester.py
```

Those python files are all for auto-generating `header.h` and `header.ll`. Run `./header_gen.py` to generate. 

### Playground

```
├── header.h
├── header.ll
├── playground.cpp
├── Makefile
```

Those are for quick play. Some explanation on [Makefile](https://github.com/Logicalmars/SIMD-libgen/blob/master/llvm_header/Makefile) are:

* `ir` compiles statically `playground.cpp` to `playground.ll`
* `with_ir_header` links `header.ll` and `playgound.ll`, does standard optimization, get `optimized.bc`
* `native` further compiles bitcode file into machine native code `optimized`.
* You can also run `lli optimized.bc` instead of native.