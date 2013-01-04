
# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

class ValidOperation:
	def __init__(self, fullName, fw, cost=-1):
		self.fullName = fullName
		self.fw = fw
		self.cost = cost

def Parse(dbName):
	validOperations = {}
	fileIn = open(dbName, "r")
	inText = fileIn.readline()
	
	while inText != "":
		colonPos = inText.find(":")
		opFullName = inText[0:colonPos]
		
		#store all valid operations along with their valid fws
		validOperations[opFullName] = []
		
		dbInfo = {}
		
		while inText != "":
			inText = fileIn.readline()
			
			if ":" in inText:
				break
			
			eqPos = inText.find("=")
			infoName = inText[0:eqPos]
			inText = inText[eqPos+1:]
			
			dbInfo[infoName] = []
			
			while inText.find(" ") != -1:
				spacePos = inText.find(" ")
				try:
					info = eval(inText[0:spacePos])
				except:
					info = inText[0:spacePos]
				
				dbInfo[infoName].append(info)
				
				inText = inText[spacePos+1:]
			#print validOperations[opFullName]
		
		for i in range(len(dbInfo["fw"])):
			validOperations[opFullName].append(ValidOperation(opFullName, dbInfo["fw"][i], dbInfo["cost"][i]))
		
	fileIn.close()
	
	return validOperations
