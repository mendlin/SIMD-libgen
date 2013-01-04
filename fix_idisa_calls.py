#
# fix_idisa_calls.py - Convert from old IDISA calling syntax
# such as simd_mergel_8 to new syntax such as esimd<8>::mergel.
#
# (c) Robert D. Cameron,  Dec. 20, 2011
# Licensed under Academic Free License, 3.0.
#
import sys, re, os, shutil, optparse

SIMD_type_RE = re.compile("SIMD_type")
ScanBlock_RE = re.compile("ScanBlock")
sisd_to_int_RE = re.compile("sisd_to_int")
sisd_from_int_RE = re.compile("sisd_from_int")

shift_immed_RE = re.compile("::(s[rl][la]i)\(([^(),]*),\s*([^()]*)\)")
shift_immed_RE2 = re.compile("::(s[rl][la]i)\(([^(),]*\([^(]*\)),\s*([^()]*)\)")
shift_immed_RE3 = re.compile("::(s[rl][la]i)\(([^(),]*),\s*([^()]*\([^()]*\))\)")
shift_immed_RE4 = re.compile("::(s[rl][la]i)\(([^(),]*\([^(]*\)),\s*([^()]*\([^()]*\))\)")

has_bit_RE = re.compile("bitblock_has_bit")
const_RE = re.compile("simd_const_([0-9]+)")
movemask_RE = re.compile("simd_movemask_([0-9]+)")
add_hl_RE = re.compile("simd_add_([0-9]+)_hl")

hsimd_RE = re.compile("simd_(packh|packl|packus)_([0-9]+)")
esimd_RE = re.compile("simd_(mergel|mergeh)_([0-9]+)")

default_simd_RE = re.compile("simd_([a-z]+)_([0-9]+)")

default_sisd_RE = re.compile("sisd_(store_aligned|store_unaligned|load_aligned|load_unaligned|srl|sll|srli|slli)")

simd_lib_RE = re.compile("lib_simd.h")
carryQ_RE = re.compile("carryQ.h")

def simd_fixer(s):
        s = simd_lib_RE.sub("lib/bitblock.hpp", s)
        s = carryQ_RE.sub("lib/carryQ.hpp", s)
        s = SIMD_type_RE.sub("BitBlock", s)
        s = ScanBlock_RE.sub("long", s)
	s = sisd_from_int_RE.sub("convert", s)
	s = sisd_to_int_RE.sub("mvmd<32>::extract<0>", s)
	s = has_bit_RE.sub("bitblock::any", s)
	s = movemask_RE.sub(r"hsimd<\1>::signmask", s)
	s = const_RE.sub(r"mvmd<\1>::fill", s)
	s = add_hl_RE.sub(r"simd<\1>::add_hl", s)
	s = esimd_RE.sub(r"esimd<\2>::\1", s)
	s = hsimd_RE.sub(r"hsimd<\2>::\1", s)
	s = default_simd_RE.sub(r"simd<\2>::\1", s)
	s = default_sisd_RE.sub(r"bitblock::\1", s)
	s = shift_immed_RE.sub(r"::\1<\3>(\2)", s)
	s = shift_immed_RE2.sub(r"::\1<\3>(\2)", s)
	s = shift_immed_RE3.sub(r"::\1<\3>(\2)", s)
	s = shift_immed_RE4.sub(r"::\1<\3>(\2)", s)
        return s


fixable = re.compile("\.(h|c|hpp|cpp|hxx|cxx)$")

def fix_file(path):
	if fixable.search(path):
		infile = open(path)
		indata = infile.read()
		infile.close()
		outdata = simd_fixer(indata)
		if outdata != indata:
			print("Modifying %s\n" % (path))
			shutil.move(path, path + '.bak')
			outfile = open(path, 'w')
			outfile.write(outdata)
			outfile.close()

def fix_directory(path, do_recursive = False):
	for f in os.listdir(path):
                subpath = os.path.join(path, f)
		if os.path.isdir(subpath):
			if do_recursive: fix_directory(subpath, do_recursive)
		else:
			fix_file(subpath)


if __name__ == '__main__':

	option_parser = optparse.OptionParser(usage='python %prog [options] <input file>', version='1.0')
	option_parser.add_option('-r', '--recursive', 
                          dest = 'do_recursive', action='store_true', default=False,
                          help = 'Process subdirectories recursively.')
	options, args = option_parser.parse_args(sys.argv[1:])
	if len(args) != 1:
		option_parser.print_usage()
		sys.exit()
	path = args[0]
        if path[0] != '/': path = os.getcwd() + '/' + path
	print "Fixing path = %s\n" % path
	if os.path.isdir(path):
		fix_directory(path, options.do_recursive)
	else:
		fix_file(path)


