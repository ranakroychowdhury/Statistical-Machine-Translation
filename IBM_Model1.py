# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 21:52:37 2019

@author: Ranak Roy Chowdhury
"""
import operator
import json

    
def readFiles():
    with open("corpus.en", "r") as file:
        eng = [[x for x in line.split()] for line in file]
    with open("corpus.es", "r") as file:
        esp = [[x for x in line.split()] for line in file]
    with open("dev.en", "r") as file:
        eng_dev = [[x for x in line.split()] for line in file]
    with open("dev.es", "r") as file:
        esp_dev = [[x for x in line.split()] for line in file]
    with open("dev.key", "r") as file:
        gold = [[int(x) for x in line.split()] for line in file]
    return eng, esp, eng_dev, esp_dev, gold
    

def printDictionary(dic):
    sorted(dic.items(), key=operator.itemgetter(1))
    for k,v in sorted(dic.items(), key=operator.itemgetter(1))[:]:
        if v == 2:
            print (k,v)
        

def buildList(corpus):
    l = []
    for sentence in corpus:
        for word in sentence:
            if word not in l:
                l.append(word)
    return l


def buildDataStructures(eng, esp, eng_list, esp_list):
    count_eng_esp = {}
    count_eng = {}
    t_esp_eng = {}
    for eng_word in eng_list:
        dic_eng_word = {}
        i = 0
        for sentence in eng:
            if eng_word in sentence:
                for esp_word in esp[i]:
                    if esp_word not in dic_eng_word:
                        dic_eng_word[esp_word] = 0
            i += 1
        count_eng_esp[eng_word] = dic_eng_word
        count_eng[eng_word] = 0
        t_esp_eng[eng_word] = dic_eng_word.copy()
    return count_eng_esp, count_eng, t_esp_eng
    

def initialize(t_esp_eng):
    for eng_word in t_esp_eng:
        for esp_word in t_esp_eng[eng_word]:
            t_esp_eng[eng_word][esp_word] = 1 / len(t_esp_eng[eng_word])


def Expectation(eng, esp, count_eng_esp, count_eng, t_esp_eng, iteration):
    i = 0
    for esp_sent in esp:
        if i % 400 == 0:
            print('Iteration ' + str(iteration) + ': ' + str(i))
        eng_sent = eng[i]
        for esp_word in esp_sent:
            total = 0
            for eng_word in eng_sent:
                total += t_esp_eng[eng_word][esp_word]
            for eng_word in eng_sent:
                delta = t_esp_eng[eng_word][esp_word] / total
                count_eng_esp[eng_word][esp_word] += delta
                count_eng[eng_word] += delta
        i += 1
    

def Maximization(count_eng_esp, count_eng, t_esp_eng):
    for eng_word in t_esp_eng:
        for esp_word in t_esp_eng[eng_word]:
            t_esp_eng[eng_word][esp_word] = count_eng_esp[eng_word][esp_word] / count_eng[eng_word]
    
    
def EM(eng, esp, eng_list, esp_list, iteration):
    count_eng_esp, count_eng, t_esp_eng = buildDataStructures(eng, esp, eng_list, esp_list)
    initialize(t_esp_eng)
    for i in range(iteration):
        Expectation(eng, esp, count_eng_esp, count_eng, t_esp_eng, i)
        Maximization(count_eng_esp, count_eng, t_esp_eng)
    return t_esp_eng

     
def appendNull(corpus):
    for sentence in corpus:
        sentence.insert(0, 'NULL')


def saveParameters(t_esp_eng):
    js = json.dumps(t_esp_eng)
    f = open("t.json","w")
    f.write(js)
    f.close()
    

def evaluate(eng_dev, esp_dev, t_esp_eng, gold):
    l = []
    i = 0
    for esp_sent in esp_dev:
        eng_sent = eng_dev[i]
        j = 0
        for esp_word in esp_sent:
            l_esp = []
            temp_l = []
            for eng_word in eng_sent:
                l_esp.append(t_esp_eng[eng_word][esp_word])
            maximum = max(l_esp)
            idx = l_esp.index(maximum)
            temp_l.append(i + 1)
            temp_l.append(idx)
            temp_l.append(j + 1)
            l.append(temp_l)
            j += 1
        i += 1
    return l


def saveResult(l):
    with open("dev.out", 'w') as file:
        file.writelines(' '.join(str(j) for j in i) + '\n' for i in l)
    
    
if __name__ == "__main__":
    print("Reading Files")
    eng, esp, eng_dev, esp_dev, gold = readFiles()
    appendNull(eng)
    appendNull(eng_dev)
    eng_list = buildList(eng)
    esp_list = buildList(esp)
    iteration = 5
    t_esp_eng = EM(eng, esp, eng_list, esp_list, iteration)
    saveParameters(t_esp_eng)
    l = evaluate(eng_dev, esp_dev, t_esp_eng, gold)
    saveResult(l)
    