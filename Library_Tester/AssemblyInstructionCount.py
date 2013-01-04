# Copyright (c) 2011, Hua Huang and Robert D. Cameron.
# Licensed under the Academic Free License 3.0. 

import os
import random

import ParseIdisaDB
import TesterUtility
from TesterUtility import configure

cppTemplate = r'''
#include "$header_file$"
#include "utility.h"

int main()
{
    $variables$
    asm volatile("nop");
    $call_function$
    asm volatile("nop");
    $output$
    return 0;
}
'''

headerFileDir = os.getcwd().replace("Library_Tester", "Library_Generator") + "/tmp/"

def GetCppText4TemplatedFunc(headerFile, operation):
    oprdNum = len(operation.arguments)
    SIMD_type = configure.Bitblock_type[operation.arch]
    
    variables = ""
    args = []
    for i in range(oprdNum):
        variables += "\t" + SIMD_type + " arg" + str(i) + " = LoadfromInt(" + str(random.randint(0, 1<<10)) + ", "  + str(TesterUtility.GetOptId(operation.arch)) + ");\n"
        args.append("arg" + str(i))
    
    immVal = 0
    for key in operation.valueRange:
        lowBound = operation.valueRange[key]["min"]
        upBound = operation.valueRange[key]["max"]
        immVal = random.randint(lowBound, upBound)

    call_function = ""
    output = ""
    if operation.returnType == SIMD_type:
        call_function = "\t" + SIMD_type + " ans = " + operation.CallingStatementToCppText(operation.fieldWidth, args, immVal, True) + ";"
        output = "cout << Store2String(ans, " + str(TesterUtility.GetOptId(operation.arch)) + ") << endl;"
    elif operation.returnType == "uint64_t":
        call_function = "\t" + "uint64_t" + " ans = " + operation.CallingStatementToCppText(operation.fieldWidth, args, immVal, True) + ";"
        output = "cout << ans << endl;"
    else:
        assert False, "can't process this data type " + operation.returnType
    
    cppText = cppTemplate.replace("$header_file$", headerFile)
    cppText = cppText.replace("$variables$", variables)
    cppText = cppText.replace("$call_function$", call_function)
    cppText = cppText.replace("$output$", output)
    
    return cppText

def GetCppText4NormalFunc(headerFile, operation):
    oprdNum = len(operation.arguments)
    SIMD_type = configure.Bitblock_type[operation.arch]
    
    args = []
    variables = ""
    for i in range(oprdNum):
        if operation.arguments[i].type == SIMD_type:
            variables += "\t" + SIMD_type + " arg" + str(i) + " = LoadfromInt(" + str(random.randint(0, 1<<10)) + ", "  + str(TesterUtility.GetOptId(operation.arch)) + ");\n"
        elif operation.arguments[i].type == "uint64_t":
            variables += "\t" + "uint64_t arg" + str(i) + " = " + str(random.randint(0, 1<<10)) + ";\n"
        else:
            assert False, "can't process this data type" + str(operation.arguments[i].type)
        args.append("arg"+str(i))
    
    call_function = ""
    output = ""
    if operation.returnType == SIMD_type:
        call_function = "\t" + SIMD_type + " ans = " + operation.CallingStatementToCppText(operation.fieldWidth, args) + ";"
        output = "cout << Store2String(ans, " + str(TesterUtility.GetOptId(operation.arch)) + ") << endl;"
    elif operation.returnType == "uint64_t":
        call_function = "\t" + "uint64_t" + " ans = " + operation.CallingStatementToCppText(operation.fieldWidth, args) + ";"
        output = "cout << ans << endl;"
    elif operation.returnType == "bool":
        call_function = "\t" + "bool" + " ans = " + operation.CallingStatementToCppText(operation.fieldWidth, args) + ";"
        output = "cout << ans << endl;"
    else:
        #print operation.returnType
        assert False, "can't process this data type " + operation.returnType

    cppText = cppTemplate.replace("$header_file$", headerFile)
    cppText = cppText.replace("$variables$", variables)
    cppText = cppText.replace("$call_function$", call_function)
    cppText = cppText.replace("$output$", output)

    return cppText

def ModifyUtilityH(arch, headerFile):
    fileIn = open("utility.h", "r")
    utilityCodes = fileIn.readlines()
    utilityCodes[0] = '''#include "''' + headerFile + '''"\n'''
    utilityCodes[1] = '''#define USE_SSE\n''' if arch in configure.SSE_SERIES else ('''#define USE_AVX\n''' if arch == configure.AVX else '''''') 
    utilityCodes[2] = '''typedef ''' + configure.SIMD_type[arch] + " SIMD_type;\n"
    fileIn.close()
    fileIn = open("utility.h", "w")
    for code in utilityCodes:
        fileIn.write(code)
    fileIn.close()

def RunIt(arch, headerFile, objFile, srcFile):
    ModifyUtilityH(arch, headerFile)
    os.system("g++ -m" + arch.lower() + " -O3 -S " + " " + srcFile + " --param inline-unit-growth=100000 --param large-function-growth=5000")
    os.system("mv " + srcFile + " perf_out/" + arch)
    os.system("mv " + objFile + ".s" + " perf_out/" + arch)

def MakeCpps(arch, definedOperations, validOperations):
    
    for opFullName in validOperations:
        for validOp in validOperations[opFullName]:
            operation = definedOperations[opFullName][int(validOp.fw)]
            cppText = ""
            
            #write the best implementation
            headerFile = "idisa_" + arch.lower() + ".h"
            if operation.opPattern == 1 or operation.opPattern == 4:
                cppText = GetCppText4TemplatedFunc(headerFile, operation)
            elif operation.opPattern == 0 or operation.opPattern == 2 or operation.opPattern == 3:
                cppText = GetCppText4NormalFunc(headerFile, operation)
            WriteCodes(opFullName + "_" + str(validOp.fw) + "_best.cpp", cppText)
            RunIt(arch, headerFile, opFullName + "_" + str(validOp.fw) + "_best", opFullName + "_" + str(validOp.fw) + "_best.cpp")
            #os.system("mv " + opFullName + "_" + str(validOp.fw) + "_best.cpp" + " perf_out/")
            
            #write the second best implementation
            headerFile = headerFileDir + arch + "/" + opFullName + "_" + str(validOp.fw) + ".h"
            secValidOperations = ParseIdisaDB.Parse(headerFile.replace(".h", ".db"))
            if opFullName not in secValidOperations:
                continue
            flag = False
            for secValidOp in secValidOperations[opFullName]:
                if validOp.fw == secValidOp.fw:
                    flag = True
            if flag:
                if operation.opPattern == 1 or operation.opPattern == 4:
                    cppText = GetCppText4TemplatedFunc(headerFile, operation)
                elif operation.opPattern == 0 or operation.opPattern == 2 or operation.opPattern == 3:
                    cppText = GetCppText4NormalFunc(headerFile, operation)
                WriteCodes(opFullName + "_" + str(validOp.fw) + "_sec.cpp", cppText)
            
                RunIt(arch, headerFile, opFullName + "_" + str(validOp.fw) + "_sec", opFullName + "_" + str(validOp.fw) + "_sec.cpp")
            
def WriteCodes(outFile, cppText):
    fileOut = open(outFile, "w")
    fileOut.write(cppText)
    fileOut.close()

assembyFileDir = os.getcwd() + "/perf_out/"

def CountIt(arch, file):
    file = assembyFileDir + arch.upper() + "/" + file
    fileIn = open(file, "r")
    content = fileIn.readlines()
    fileIn.close()
    
    cLen = len(content)
    nopSt = -1
    nopEd = -1
    for i in range(cLen):
        s = content[i].strip()
        if s == "nop":
            nopSt = i
            break
    
    if nopSt == -1:
        return (-1, -1)   
    else:
        for i in range(nopSt+1, cLen):
            s = content[i].strip()
            if s == "nop":
                nopEd = i
                break
        if nopEd == -1:
            return (-1, -1)
        else:
            pureCt = 0
            totCt = 0
            for i in range(nopSt+1, nopEd):
                if "#" in content[i]:
                    continue
                totCt += 1
                s = content[i].strip()
                if "mov" == s[0:3] or "vmov" == s[0:4]:
                    continue
                if "call" in s and "call" == s[0:4]:
                    return ("IF", "IF")
                pureCt += 1
            return (pureCt, totCt)
    
def GetInstructionCount(arch, definedOperations, validOperations):
    resultTable = {}
    
    for opFullName in validOperations:
        resultTable[opFullName] = {}
        for validOp in validOperations[opFullName]:
            
            operation = definedOperations[opFullName][int(validOp.fw)]
            
            #check the best implementation
            best = CountIt(arch, opFullName + "_" + str(validOp.fw) + "_best.s")
            sec = (-1, -1)
            
            #write the second best implementation
            headerFile = headerFileDir + arch + "/" + opFullName + "_" + str(validOp.fw) + ".h"
            secValidOperations = ParseIdisaDB.Parse(headerFile.replace(".h", ".db"))
            if opFullName not in secValidOperations:
                print opFullName, "=>", best[0], best[1], sec[0], sec[1]
                resultTable[opFullName][int(validOp.fw)] = (best, sec)
                continue
            flag = False
            for secValidOp in secValidOperations[opFullName]:
                if validOp.fw == secValidOp.fw:
                    flag = True
            if flag:
                sec = CountIt(arch, opFullName + "_" + str(validOp.fw) + "_sec.s")
            
            print opFullName, "=>", best[0], best[1], sec[0], sec[1]
            resultTable[opFullName][int(validOp.fw)] = (best, sec)
    
    WriteCountInfo(arch, resultTable)

def WriteCountInfo(arch, table):
    fileOut = open(arch+"_instruction_count.ods", "w")
    fileOut.write("name")
    
    validFws = []
    fw = 1
    while fw <= configure.RegisterSize[arch]:
        validFws.append(fw)
        fw = 2*fw
    
    for fw in validFws:
        fileOut.write("\t" + str(fw))
    fileOut.write("\n")
    
    for opFullName in table:
        fileOut.write(opFullName)
        for fw in validFws:
            if fw in table[opFullName]:
                fileOut.write("\t(" + str(table[opFullName][fw][0][0]) + "," + str(table[opFullName][fw][0][1]) + ")/(" + str(table[opFullName][fw][1][0]) + "," + str(table[opFullName][fw][1][1]) + ")")
            else:
                fileOut.write("\t" + "N/A")
        fileOut.write("\n")
    
    fileOut.close()