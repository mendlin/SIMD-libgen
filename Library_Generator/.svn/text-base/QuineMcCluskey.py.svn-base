
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import copy
import sys

import Operation
from Utility import configure

sys.path.append("../Library_Tester")

import CalculateResult

varNum = 4
tableSize = 2**varNum

def BinaryRepr(var):
	ret = bin(var)[2:]
	retLen = len(ret)
	ret = "0"*(varNum-retLen) + ret if retLen<varNum else ret
	return ret

def CoveredNums(nums, term, dep, var):
	if dep < varNum:
		if term[dep] == '-':
			CoveredNums(nums, term, dep+1, var*2+1)
			CoveredNums(nums, term, dep+1, var*2)
		else:
			CoveredNums(nums, term, dep+1, var*2+int(term[dep]))
	else:
		nums.append(var)

def CombineTwoTerms(term0, term1):
	newTerm = ""
	for i in range(varNum):
		if i == 0 and term0[i+1:] == term1[i+1:]:
			newTerm = "-" + term0[i+1:]
			break
		elif i == varNum-1 and term0[0:i] == term1[0:i]:
			newTerm = term0[0:i] + "-"
			break
		elif i > 0 and i < varNum-1 and term0[0:i] == term1[0:i] and term0[i+1:] == term1[i+1:]:
			newTerm = term0[0:i] + "-" + term0[i+1:]
			break
	return newTerm

def IsCovered(term0, term1):
	#print term0, term1
	for i in range(varNum):
		if term0[i] == '0' and term1[i] == '1':
			return False
		elif term0[i] == '1' and term1[i] == '0':
			return False
		elif term0[i] == '-' and term1[i] != '-':
			return False
	return True

def CleanUp(newTerms):
	sz = len(newTerms)
	tmpSz = len(newTerms)
	for i in range(sz):
		j = 0
		while j<tmpSz:
			k = 0
			cov = False
			while k<tmpSz:
				if j != k and IsCovered(newTerms[j], newTerms[k]) == True:
					cov = True
					break
				k += 1
			if cov == True:
				del newTerms[j]
				tmpSz -= 1
			j += 1

def Combine(minTerms):
	newTerms = []
	sz = len(minTerms)
	
	for i in range(sz):
		newTerms.append(minTerms[i])
	
	for i in range(sz):
		for j in range(i+1, sz):
			term = CombineTwoTerms(minTerms[i], minTerms[j])
			if term != "":
				#print "t0=", minTerms[i], " t1=", minTerms[j]
				#print "new term=", term
				newTerms.append(term)
	
	CleanUp(newTerms)
	return newTerms

def FindBestImplicants(dep, termNum, chosenImplicants, implicantsChart, allSolutions):
	if dep < termNum:
		FindBestImplicants(dep+1, termNum, chosenImplicants, implicantsChart, allSolutions)
		
		chosenImplicants[dep] = 1
		FindBestImplicants(dep+1, termNum, chosenImplicants, implicantsChart, allSolutions)
		del chosenImplicants[dep]
	else:
		for num in implicantsChart:
			cov = False
			for impId in implicantsChart[num]:
				if impId in chosenImplicants:
					cov = True
					break
			if cov == False:
				return {}
		
		if len(allSolutions) <= 0:
			allSolutions.append(copy.deepcopy(chosenImplicants))
		elif len(chosenImplicants) < len(allSolutions[0]):
			del allSolutions[:]
			allSolutions.append(copy.deepcopy(chosenImplicants))
		elif len(chosenImplicants) == len(allSolutions[0]):
			allSolutions.append(copy.deepcopy(chosenImplicants))

def Not(term):
	if "'" in term:
		return term[:-1]
	else:
		return term + "'"

def XorCombineTwoTerms(term1, term2):
	term3 = []
	sz = len(term1)
	for i in range(sz):
		if "^" in term1[i] or len(term1[i])>3:
			continue
		for j in range(i+1, sz):
			if "^" in term1[j] or len(term1[j])>3:
				continue
			if ("'" in term1[i] and "'" in term1[j]) or ("'" not in term1[i] and "'" not in term1[j]):
				continue
			notTermi = Not(term1[i])
			notTermj = Not(term1[j])
			flag = True
			for term in term1:
				if term!=term1[i] and term!=term1[j] and term not in term2:
					flag = False
					break
			if flag == True and notTermi in term2 and notTermj in term2:
				for term in term1:
					if term!=term1[i] and term!=term1[j]:
						term3.append(term)
				xorStr = (term1[i][:-1] if "'" in term1[i] else term1[i]) + "^" + (term1[j][:-1] if "'" in term1[j] else term1[j])
				term3.append(xorStr)
				return term3
	return term3

def XorCombine(listOfMinterms):
	while True:
		sz = len(listOfMinterms)
		isCombined = False
		for i in range(sz):
			for j in range(i+1, sz):
				minterm1 = listOfMinterms[i]
				minterm2 = listOfMinterms[j]
				newMinterm = XorCombineTwoTerms(minterm1, minterm2)
				if len(newMinterm) > 0:
					isCombined = True
					listOfMinterms.remove(minterm1)
					listOfMinterms.remove(minterm2)
					listOfMinterms.append(newMinterm)
					break
			if isCombined == True:
				break
		if isCombined == False:
			break

	return listOfMinterms

def NotXorCombineTwoTerms(term1, term2):
	term3 = []
	sz = len(term1)
	for i in range(sz):
		if "^" in term1[i] or len(term1[i])>3:
			continue
		for j in range(i+1, sz):
			if "^" in term1[j] or len(term1[j])>3:
				continue
			if ("'" in term1[i] and "'" not in term1[j]) or ("'" not in term1[i] and "'" in term1[j]):
				continue
			notTermi = Not(term1[i])
			notTermj = Not(term1[j])
			flag = True
			for term in term1:
				if term!=term1[i] and term!=term1[j] and term not in term2:
					flag = False
					break
			if flag == True and notTermi in term2 and notTermj in term2:
				for term in term1:
					if term!=term1[i] and term!=term1[j]:
						term3.append(term)
				notXorStr = "(" + (term1[i][:-1] if "'" in term1[i] else term1[i]) + "^" + (term1[j][:-1] if "'" in term1[j] else term1[j]) + ")" + "'"
				term3.append(notXorStr)
				return term3
	return term3

def NotXorCombine(listOfMinterms):
	while True:
		sz = len(listOfMinterms)
		isCombined = False
		for i in range(sz):
			for j in range(i+1, sz):
				minterm1 = listOfMinterms[i]
				minterm2 = listOfMinterms[j]
				newMinterm = NotXorCombineTwoTerms(minterm1, minterm2)
				if len(newMinterm) > 0:
					isCombined = True
					listOfMinterms.remove(minterm1)
					listOfMinterms.remove(minterm2)
					listOfMinterms.append(newMinterm)
					break
			if isCombined == True:
				break
		if isCombined == False:
			break
	
	return listOfMinterms

def MinCombineTwoTerms(term1, term2):
	term3 = []
	for term in term1:
		if term in term2:
			term3.append(term)
	
	if len(term3) <= 0:
		return term3
	
	newterm1 = ""
	for term in term1:
		if term not in term3:
			newterm1 += term
	newterm2 = ""
	for term in term2:
		if term not in term3:
			newterm2 += term
	
	term3.append("(" + newterm1 + "+" + newterm2 + ")")
	
	return term3
	
def MinCombine(listOfMinterms):
	while True:
		sz = len(listOfMinterms)
		isCombined = False
		for i in range(sz):
			for j in range(i+1, sz):
				minterm1 = listOfMinterms[i]
				minterm2 = listOfMinterms[j]
				newMinterm = MinCombineTwoTerms(minterm1, minterm2)
				if len(newMinterm) > 0:
					isCombined = True
					listOfMinterms.remove(minterm1)
					listOfMinterms.remove(minterm2)
					listOfMinterms.append(newMinterm)
					break
			if isCombined == True:
				break
		if isCombined == False:
			break
	
	return listOfMinterms

def OutputRes(listOfMinterms):
	res = ""
	for term in listOfMinterms:
		minterm = ""
		for ele in term:
			minterm += ele 
		res += minterm + "+"
	print res[:-1]

def QuineMcCluskey(fTable):
	minTerms = []
	for i in range(tableSize):
		if fTable[i] == "1":
			minTerms.append(BinaryRepr(i))

	preMinTerms = copy.deepcopy(minTerms)
	while True:
		minTerms = Combine(minTerms)
		if preMinTerms == minTerms:
			break
		preMinTerms = copy.deepcopy(minTerms)

	#print "prime implicants are: "
	#for term in minTerms:
	#	print term

	termNum = len(minTerms)
	implicantsChart = {}
	
	for i in range(termNum):
		nums = []
		CoveredNums(nums, minTerms[i], 0, 0)
		for num in nums:
			if num not in implicantsChart:
				implicantsChart[num] = [i]
			else:
				implicantsChart[num].append(i)
	
	allSolutions = []
	FindBestImplicants(0, termNum, {}, implicantsChart, allSolutions)
	
	'''
	for sol in allSolutions:
		#print "solution:"
		res = ""
		for impId in sol:
			for i in range(varNum):
				if minTerms[impId][i] == "-":
					continue
				res += "a" if i<2 else "b"
				res += str(i) if i<2 else str(i-2)
				res += "" if minTerms[impId][i] == "1" else "'"
			res += "+"
		print res[:-1]
	'''
	
	listOfMinterms = []
	for impId in allSolutions[0]:
		minterms = []
		for i in range(varNum):
			if minTerms[impId][i] == "-":
				continue
			minterm = "a" if i<2 else "b"
			minterm += str(i) if i<2 else str(i-2)
			minterm += "" if minTerms[impId][i] == "1" else "'"
			minterms.append(minterm)
		listOfMinterms.append(minterms)

	#print listOfMinterms
	
	XorCombine(listOfMinterms)
	NotXorCombine(listOfMinterms)
	MinCombine(listOfMinterms)
	
	return listOfMinterms
	
def MinLogic(f0Table, f1Table):
	
	print "f0 =",
	OutputRes(QuineMcCluskey(f0Table))
	print "f1 =",
	OutputRes(QuineMcCluskey(f1Table))
	

#algorithm to combine two implicants by xor
# use a list to hold an implicant, a0b0a1' => [a0, b0, a1'], a0^b0a1' => [a0^b0, a1']
# when combining, we only combine implicants which are not yet combined, [a0^b0, a1, b1'] and [a0^b0, a1', b1], we combine a1b1' and a1'b1 and keep a0^b0 unchanged.
# there might be a case that [a0^b0, a1'+b1'] and [a0^b0, a1, b1], we don't process it further in this version
if __name__ == "__main__":
	
	arch = configure.SSE2
	
	definedOperations = Operation.LoadDefinedOperations(configure.AllOperations, arch)
	
	testdata = []
	for i in range(tableSize):
		binRepr = BinaryRepr(i)
		testdata.append((binRepr[0:2], binRepr[2:]))
	
	fTable = CalculateResult.GetResult(definedOperations["simd_add"][2], testdata, configure.RegisterSize[arch])
	
	print fTable
	
	f0Table = []
	f1Table = []
	for val in fTable:
		f0Table.append(val[0])
		f1Table.append(val[1])
	
	#print f0Table
	#print f1Table
	
	MinLogic(f0Table, f1Table)
	
