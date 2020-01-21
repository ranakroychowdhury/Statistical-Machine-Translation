# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 03:15:51 2019

@author: Ranak Roy Chowdhury
"""
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
    with open("t.json") as file:
       t_esp_eng = json.load(file)
    with open("dev.key", "r") as file:
        gold = [[int(x) for x in line.split()] for line in file]
    return eng, esp, eng_dev, esp_dev, t_esp_eng, gold


def appendNull(corpus):
    for sentence in corpus:
        sentence.insert(0, 'NULL')
        
        
def buildList(corpus):
    l = []
    for sentence in corpus:
        for word in sentence:
            if word not in l:
                l.append(word)
    return l


def saveResult(l):
    with open("dev.out", 'w') as file:
        file.writelines(' '.join(str(j) for j in i) + '\n' for i in l)
        

def saveParameters(t_esp_eng, q_jilm):
    js = json.dumps(t_esp_eng)
    f = open("t.json","w")
    f.write(js)
    f.close()
    js = json.dumps(q_jilm)
    f = open("q.json","w")
    f.write(js)
    f.close()


def buildDataStructures(eng, esp, eng_list, esp_list):
    i = 0
    c_ilm = {}
    c_jilm = {}
    q_jilm = {}
    check = []
    for esp_sent in esp:
        eng_sent = eng[i]
        l = len(eng_sent)
        m = len(esp_sent)
        ch = str(l) + ' ' + str(m)
        if ch not in check:
            for esp_idx in range(1, m + 1):
                key_i = str(esp_idx) + ' ' + ch
                c_ilm[key_i] = 0
                for eng_idx in range(l):
                    key = str(eng_idx) + ' ' + key_i
                    c_jilm[key] = 0
                    q_jilm[key] = 0
            check.append(ch)
        i += 1
    count_eng_esp = {}
    count_eng = {}
    for eng_word in eng_list:
        dic_eng_word = {}
        i = 0
        for sentence in eng:
            if eng_word in sentence:
                for esp_word in esp[i]:
                    dic_eng_word[esp_word] = 0
            i += 1
        count_eng_esp[eng_word] = dic_eng_word
        count_eng[eng_word] = 0
        
    return count_eng_esp, count_eng, c_ilm, c_jilm, q_jilm


def initialize(q_jilm):
    for key in q_jilm:
        keys = key.split()
        q_jilm[key] = 1 / (int(keys[2]))
    
 
def Expectation(eng, esp, count_eng_esp, count_eng, t_esp_eng, c_ilm, c_jilm, q_jilm, iteration):
    i = 0
    for esp_sent in esp:
        if i % 400 == 0:
            print('Iteration ' + str(iteration) + ': ' + str(i))
        eng_sent = eng[i]
        ch = str(len(eng_sent)) + ' ' + str(len(esp_sent))
        esp_idx = 1
        for esp_word in esp_sent:
            total = 0
            eng_idx = 0
            for eng_word in eng_sent:
                key = str(eng_idx) + ' ' + str(esp_idx) + ' ' + ch
                total += q_jilm[key] * t_esp_eng[eng_word][esp_word]
                eng_idx += 1
            eng_idx = 0
            key_i = str(esp_idx) + ' ' + ch
            for eng_word in eng_sent:
                key = str(eng_idx) + ' ' + str(esp_idx) + ' ' + ch
                delta = (q_jilm[key] * t_esp_eng[eng_word][esp_word]) / total
                count_eng_esp[eng_word][esp_word] += delta
                count_eng[eng_word] += delta
                c_jilm[key] += delta
                c_ilm[key_i] += delta
                eng_idx += 1
            esp_idx += 1
        i += 1
        
        
def Maximization(count_eng_esp, count_eng, t_esp_eng, c_ilm, c_jilm, q_jilm):
    for eng_word in t_esp_eng:
        for esp_word in t_esp_eng[eng_word]:
            t_esp_eng[eng_word][esp_word] = count_eng_esp[eng_word][esp_word] / count_eng[eng_word]
    for key in q_jilm:
        keys = key.split()
        c_ilm_key = keys[1] + ' ' + keys[2] + ' ' + keys[3]
        q_jilm[key] = c_jilm[key] / c_ilm[c_ilm_key]
        

def EM(eng, esp, eng_list, esp_list, t_esp_eng, iteration):
    count_eng_esp, count_eng, c_ilm, c_jilm, q_jilm = buildDataStructures(eng, esp, eng_list, esp_list)
    initialize(q_jilm)
    for i in range(iteration):
        Expectation(eng, esp, count_eng_esp, count_eng, t_esp_eng, c_ilm, c_jilm, q_jilm, i)
        Maximization(count_eng_esp, count_eng, t_esp_eng, c_ilm, c_jilm, q_jilm)
    return t_esp_eng, q_jilm


def evaluate(eng_dev, esp_dev, t_esp_eng, q_jilm, gold):
    l = []
    i = 0
    for esp_sent in esp_dev:
        eng_sent = eng_dev[i]
        ch = str(len(eng_sent)) + ' ' + str(len(esp_sent))
        esp_idx = 1
        for esp_word in esp_sent:
            l_esp = []
            temp_l = []
            eng_idx = 0
            for eng_word in eng_sent:
                key = str(eng_idx) + ' ' + str(esp_idx) + ' ' + ch
                if eng_word in t_esp_eng and esp_word in t_esp_eng[eng_word] and key in q_jilm:
                    l_esp.append(q_jilm[key] * t_esp_eng[eng_word][esp_word])
                eng_idx += 1
            maximum = max(l_esp)
            idx = l_esp.index(maximum)
            temp_l.append(i + 1)
            temp_l.append(idx)
            temp_l.append(esp_idx)
            l.append(temp_l)
            esp_idx += 1
        i += 1
    return l


if __name__ == "__main__":
    print("Reading Files")
    eng, esp, eng_dev, esp_dev, t_esp_eng, gold = readFiles()
    appendNull(eng)
    appendNull(eng_dev) #if we do't consider NULL while testing, remove this line
    eng_list = buildList(eng)
    esp_list = buildList(esp)
    iteration = 5
    t_esp_eng, q_jilm = EM(eng, esp, eng_list, esp_list, t_esp_eng, iteration)
    saveParameters(t_esp_eng, q_jilm)
    l = evaluate(eng_dev, esp_dev, t_esp_eng, q_jilm, gold)
    saveResult(l)
    