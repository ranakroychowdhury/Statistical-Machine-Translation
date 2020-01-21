# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:48:42 2019

@author: Ranak Roy Chowdhury
"""    
def readFiles():
    with open("dev.en", "r") as file:
        eng_dev = [[x for x in line.split()] for line in file]
    with open("dev.es", "r") as file:
        esp_dev = [[x for x in line.split()] for line in file]
    with open("dev1.out", "r") as file:
        gold_eng = [[int(x) for x in line.split()] for line in file]
    with open("dev2.out", "r") as file:
        gold_esp = [[int(x) for x in line.split()] for line in file]
    return eng_dev, esp_dev, gold_eng, gold_esp


def prepare(gold_eng, gold_esp, i):
    A = []
    B = []
    for element in gold_eng:
        l = []
        if element[0] == i + 1:
            l.append(element[1])
            l.append(element[2])
            A.append(l)
    for element in gold_esp:
        l = []
        if element[0] == i + 1:
            l.append(element[2])
            l.append(element[1])
            B.append(l)
    return A, B
    

def intersection(setA, setB):
    inter = []
    for element in setA:
        if element in setB:
            inter.append(element)
    return inter


def union(setA, setB):
    un = []
    for element in setA:
        un.append(element)
    for element in setB:
        if element not in un:
            un.append(element)
    return un


def findBest(intersect, uni, len_eng, len_esp):
    best = []
    eng = []
    esp = []
    for element in intersect:
        best.append(element)
        eng.append(element[0])
        esp.append(element[1])
    for i in range(1, len_esp + 1):
        if i not in esp:
            l = []
            sublist = []
            for element in uni:
                if element[1] == i:
                    sublist.append(element)
            result = -1
            for element in sublist:
                if element[1] + 1 in esp:
                    idx = esp.index(element[1] + 1)
                    res = eng[idx] - 1
                    subl = [res, i]
                    if subl in uni:
                        result = res
                        break
                elif element[1] - 1 in esp:
                    idx = esp.index(element[1] - 1)
                    res = eng[idx] + 1
                    subl = [res, i]
                    if subl in uni:
                        result = res
                        break
            if result == -1:
                result = sublist[0][0]
            l.append(result)
            l.append(i)
            best.append(l)
            esp.append(i)
            eng.append(result)
    for i in range(1, len_eng + 1):
        if i not in eng:
            l = []
            sublist = []
            for element in uni:
                if element[0] == i:
                    sublist.append(element)
            result = -1
            for element in sublist:
                if element[0] + 1 in eng:
                    idx = eng.index(element[0] + 1)
                    res = esp[idx] - 1
                    subl = [i, res]
                    if subl in uni:
                        result = res
                        break
                elif element[0] - 1 in eng:
                    idx = eng.index(element[0] - 1)
                    res = esp[idx] + 1
                    subl = [i, res]
                    if subl in uni:
                        result = res
                        break
            if result == -1:
                result = sublist[0][1]
            l.append(i)
            l.append(result)
            best.append(l)
            esp.append(result)
            eng.append(i)
    return best
    

def sort(best):  
    return(sorted(best, key = lambda x: x[1]))
    
    
def growingAlignment(eng_dev, esp_dev, gold_eng, gold_esp, length):
    l = []
    for i in range(length):
        print(i)
        len_eng = len(eng_dev[i])
        len_esp = len(esp_dev[i])
        setA, setB = prepare(gold_eng, gold_esp, i)
        intersect = intersection(setA, setB)
        uni = union(setA, setB)
        best = findBest(intersect, uni, len_eng, len_esp)
        best = sort(best) 
        for j in range(len(best)):
            best[j].insert(0, i + 1)
        for element in best:
            l.append(element)
    return l


def saveResult(l):
    with open("devres.out", 'w') as file:
        file.writelines(' '.join(str(j) for j in i) + '\n' for i in l)
        
        
if __name__ == "__main__":
    print("Reading Files")
    eng_dev, esp_dev, gold_eng, gold_esp = readFiles()
    l = growingAlignment(eng_dev, esp_dev, gold_eng, gold_esp, len(eng_dev))
    saveResult(l)
    