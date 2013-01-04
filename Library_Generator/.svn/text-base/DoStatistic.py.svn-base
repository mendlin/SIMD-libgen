
import StrategyPool
from Utility import configure
import SSE2Instructions
import AVXInstructions
import NEONInstructions

def IntrinsicCount(arch):
    dict = None
    if arch == configure.SSE2:
        dict = SSE2Instructions.SSE2BuiltIns
    elif arch == configure.AVX:
        dict = AVXInstructions.AVXBuiltIns
    elif arch == configure.NEON:
        dict = NEONInstructions.NEONBuiltIns
    ct = 0
    for x in dict:
        y = dict[x]
        ct += len(y["fws"])
    
    return ct

def StrategyCount(arch):
    regSize = configure.RegisterSize[arch]
    stDict = StrategyPool.StrategyPool(regSize)
    ct = 0
    tct = 0
    for st in stDict:
        dt = stDict[st]
        #tct += 1
        if configure.ALL in dt["Platforms"]:
            ct += 1
        elif arch in dt["Platforms"]:
            ct += 1
        #else:
         #   tct += 1
    return ct

badFunc = ["bitblock_popcount", "bitblock_sll", "bitblock_slli", "bitblock_srl", "bitblock_srli", "simd_umult", "simd_sub_hl"]

def IDISAOperationCount(arch):
    content = None
    if arch == configure.SSE2:
        fileIn = open("idisa_sse2.db", "r")
        content = fileIn.readlines()
        fileIn.close()
    elif arch == configure.AVX:
        fileIn = open("idisa_avx.db", "r")
        content = fileIn.readlines()
        fileIn.close()
    elif arch == configure.NEON:
        fileIn = open("idisa_neon.db", "r")
        content = fileIn.readlines()
        fileIn.close()
    ct = 0
    i, sz = 0, len(content)
    while i<sz:
        op = content[i].replace(":", "").replace("\n", "")
        if op not in badFunc:
            ct += 1
        i += 3

    return ct

def IDISAFunctionCount(arch):
    content = None
    if arch == configure.SSE2:
        fileIn = open("idisa_sse2.db", "r")
        content = fileIn.readlines()
        fileIn.close()
    elif arch == configure.AVX:
        fileIn = open("idisa_avx.db", "r")
        content = fileIn.readlines()
        fileIn.close()
    elif arch == configure.NEON:
        fileIn = open("idisa_neon.db", "r")
        content = fileIn.readlines()
        fileIn.close()
    ct = 0
    i, sz = 0, len(content)
    while i<sz:
        op = content[i].replace(":", "").replace("\n", "")
        if op not in badFunc:
            fws = content[i+1].replace("\n", "").strip().split(" ")
            ct += len(fws)
        i += 3

    return ct

def GetAvgEstInstructionCount(arch, opt):
    fileIn = open(arch.upper()+"_strategy_cost.ods", "r")
    content = fileIn.readlines()
    fileIn.close()
    
    regSize = configure.RegisterSize[arch]
    fw = 1
    index = 1
    
    avg = []
    while fw <= regSize:
        sz = len(content)
        sum0, num0 = 0, 0
        for i in range(1, sz):
            arr0 = content[i].split("\t")
            arr = []
            for x in arr0:
                arr.append(x.replace('''"''', ""))
            
            if arr[0] in badFunc:
                continue
            
            cost = arr[index][:arr[index].find(",")].strip()
            cost1 = arr[index][arr[index].find(",")+1:].strip()
            if cost == "1000000":
                continue
            
            
            if (opt==1 or opt == 2) and cost1 == "SAME":
                continue
            
            if opt == 2:
                cost = cost1
            
            sum0 += int(cost)
            num0 += 1
        avg.append(sum0*1.0/num0)
        index = index + 1
        fw = 2*fw
    return avg

def GetAvgRealInstructionCount(arch, opt):
    fileIn = open("../Library_Tester/"+arch.upper()+"_instruction_count.ods", "r")
    content = fileIn.readlines()
    fileIn.close()
    
    regSize = configure.RegisterSize[arch]
    fw = 1
    index = 1
    
    avg0 = []
    avg1 = []
    while fw <= regSize:
        sz = len(content)
        sum0, sum1, num0, num1 = 0, 0, 0, 0
        for i in range(1, sz):
            arr0 = content[i].split("\t")
            arr = []
            for x in arr0:
                arr.append(x.replace('''"''', ""))
            
            if arr[0] in badFunc:
                continue
            
            if "N/A" in arr[index]:
                continue
            
            cost = arr[index][:arr[index].find("/")]
            cost = cost.replace("(", "").replace(")", "")
            cost0 = cost[:cost.find(",")]
            cost1 = cost[cost.find(",")+1:]
            
            cost = arr[index][arr[index].find("/")+1:].strip()
            cost = cost.replace("(", "").replace(")", "")
            cost2 = cost[:cost.find(",")]
            cost3 = cost[cost.find(",")+1:]
            
            if "IF" in cost0 or "IF" in cost1:
                continue
            
            if opt == 1 and cost2 == "-1":
                continue
            
            if opt == 1:
                cost0 = cost1
                cost1 = cost3 if cost3 != "IF" else cost1
            
            sum0 += int(cost0)
            num0 += 1
            sum1 += int(cost1)
            num1 += 1
        avg0.append(sum0*1.0/num0)
        avg1.append(sum1*1.0/num1)
        index = index + 1
        fw = 2*fw
    
    return [avg0, avg1]

def GetAvgInstructionCount(arch, opt):
    if opt == 0:
        #just get the estimated instruction count for the best imp.
        return GetAvgEstInstructionCount(arch, 0)
    elif opt == 1:
        #just get the real instruction count for the best imp.
        return GetAvgRealInstructionCount(arch, 0)
    elif opt == 2:
        #just get the estimated instruction count for the best imp. if its has a second best imp.
        return GetAvgEstInstructionCount(arch, 1)
    elif opt == 3:
        #just get the estimated instruction count for the second best imp.
        return GetAvgEstInstructionCount(arch, 2)
    elif opt == 4:
        #just get the real instruction count for the best imp. and second best imp.
        return GetAvgRealInstructionCount(arch, 1)

if __name__ == "__main__":
    
    #print StrategyCount(configure.SSE2)
    #print StrategyCount(configure.AVX)
    #print StrategyCount(configure.NEON)
    
    #print IntrinsicCount(configure.SSE2)
    #print IntrinsicCount(configure.AVX)
    #print IntrinsicCount(configure.NEON)
    
    #print IDISAOperationCount(configure.SSE2)
    #print IDISAOperationCount(configure.AVX)
    #print IDISAOperationCount(configure.NEON)
    
    #print IDISAFunctionCount(configure.SSE2)
    #print IDISAFunctionCount(configure.AVX)
    #print IDISAFunctionCount(configure.NEON)
    
    #print GetAvgInstructionCount(configure.SSE2, 0)
    #print GetAvgInstructionCount(configure.SSE2, 1)

    #print GetAvgInstructionCount(configure.AVX, 0)
    #print GetAvgInstructionCount(configure.AVX, 1)
    
    #print GetAvgInstructionCount(configure.SSE2, 2)
    #print GetAvgInstructionCount(configure.SSE2, 3)
    #print GetAvgInstructionCount(configure.SSE2, 4)