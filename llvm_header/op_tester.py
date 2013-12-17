#!/usr/bin/python
# This file is used to test vertical operations
# e.g.
# llvm_add_2 is an invalid operation since llc/lli raise exceptions on SelectionDAG
import config
import os

failed = []

def change_makefile_source(sfrom, sto):
	comm = "sed -i 's/SOURCE = {sfrom}/SOURCE = {sto}/' Makefile".format(
		sfrom=sfrom, sto=sto)	
	return os.system(comm)


def claim_make_fail(fw, ir_func):
	print "Make failed for {ir_func}::{fw}".format(fw=fw, ir_func=ir_func)


def claim_lli_fail(fw, ir_func):
	print "lli failed for {ir_func}::{fw}".format(fw=fw, ir_func=ir_func)
	failed.append((fw, ir_func))


def generate_teseter_cpp(fw, ir_func):
	with open('tester.cpp', 'w') as tester:	
		code = config.minimal_test_cpp.format(
			llvm_func=config.get_llvm_func(fw, ir_func))
		tester.write(code)


# Prepare Makefile
change_makefile_source('playground', 'tester')

for ir_func in config.vertical_ir_set:
	for fw in config.fw_set:
		generate_teseter_cpp(fw, ir_func)				

		if os.system("make with_ir_header") != 0:
			claim_make_fail(fw, ir_func)
			continue

		if os.system("lli optimized.bc") != 0:
			claim_lli_fail(fw, ir_func)			

# Get back Makefile
change_makefile_source('tester', 'playground')

print "----------------------------All that failed---------------------------------"
print failed

# [(2, 'add'), (4, 'add'), (2, 'sub'), (4, 'sub'), (2, 'mul'), (4, 'mul'), 
#  (2, 'and'), (4, 'and'), (2, 'or'), (4, 'or'), (2, 'xor'), (4, 'xor'), 
#  (2, 'icmp eq'), (4, 'icmp eq'), (2, 'icmp sgt'), (4, 'icmp sgt'), 
#  (2, 'icmp ugt'), (4, 'icmp ugt'), (2, 'icmp slt'), (4, 'icmp slt'), 
#  (2, 'icmp ult'), (4, 'icmp ult'), (2, 'shl'), (4, 'shl'), (128, 'shl'), 
#  (2, 'lshr'), (4, 'lshr'), (128, 'lshr'), (2, 'ashr'), (4, 'ashr'), (128, 'ashr')]
