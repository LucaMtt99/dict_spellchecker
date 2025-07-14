import os
import re 
import time
from multiprocessing import Pool
import multiprocessing as mp
from jiwer import cer, wer 
import nltk
import re

dict_path = "dizionario.txt"
with open(dict_path, "r") as f:
    d = f.read()
d = d.split("\n")

#######################################################
#                        FUNCS                        #
#######################################################

def my_eval(t1,t2,verb=False):
    CER = cer(t1,t2)
    WER = wer(t1,t2)
    if verb: print("CER:", CER,
                   "\nWER:", WER)
    return CER, WER

def levenstein_similarity(text1: str, text2: str) -> float:
    return 1 - nltk.edit_distance(text1, text2) / max(len(text1), len(text2))

#TODO do this more efficiently 
def best_match(w,d=d):
    max_d = 0
    res = w
    for cw in d:
        supp = levenstein_similarity(w,cw)
        if supp>0.5 and supp>max_d:
            max_d = supp
            res = cw
    return res

def spellcheck(text,d=d):
    punctuation = [".", ",", ":", ";", "!", "?"]
    text_splitted = re.split('(\W+?)', text)
    empty = ["", " "]
    text_splitted = [t for t in text_splitted if t not in empty]
    res = list()
    for w in text_splitted:
        capital = False
        if w[0].isupper(): capital = True
        w = w.lower()
        if w in punctuation or w in d:
            if capital: w = w.capitalize()
            res.append(w)
        else:
            m = best_match(w,d)
            if capital: m = m.capitalize()
            res.append(m)
    return re.sub(r'\s([?.,;:!\'\"](?:\s|$))', r'\1', " ".join(res))  
                
def spellchecker(text):
    data = text.split("\n")
    pool = Pool(processes=min(mp.cpu_count(), len(data)))
    return "\n".join(pool.map(spellcheck, data))    


#######################################################
#                        TESTS                        #
#######################################################

text = """Dilecteyy notro havendo nui facto experientia che cussi sei
longio a finire una opera, como sei de persona. Te
recordanmo che il te bisognay a questa volta mutare
nattura: perchè se non haverai fiinto el studdiolo al rtorno
nostro te faremo metter in presonne in lo battiponte
del castiello, et non serra snzah.
"""

text_gt = """Dilecte nostro havendo nui facto experientia che cussi sei 
longo a finire una opera, como sei de persona. Te 
recordamo che il te bisogna a questa volta mutare 
natura: perchè se non haverai finito el studiolo al retorno 
nostro te faremo mettere in presone in lo battiponte 
del castello, et non serra senza.
"""

for _ in range(10):
    text = text + text
    text_gt = text_gt + text_gt
print("NUMBER OF LINES:", len(text.split("\n")))
print("NUMBER OF WORDS:", len([w for w in re.split('(\W+?)', text) if w not in ["", " "]]))

"""
start_t = time.time()
text_checked = spellcheck(text)
print("ELAPSED TIME NO PARALLEL:", time.time()-start_t)
"""

start_t = time.time()
text_checked = spellchecker(text)
print("ELAPSED TIME PARALLEL:", time.time()-start_t)

print("CER WER BEFORE")
my_eval(text_gt,text,True)
print("CER WER AFTER")
my_eval(text_gt,text_checked,True)
