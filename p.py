from multiprocessing import Pool
import os
import re 
import time
from jiwer import cer, wer 
import nltk
import string
translator = str.maketrans('', '', string.punctuation)

dict_path = "dizionario.txt"
with open(dict_path, "r") as f:
    d = f.read()
d = d.split("\n")




def levenstein_similarity(text1: str, text2: str) -> float:
    return 1 - nltk.edit_distance(text1, text2) / max(len(text1), len(text2))

#TODO keep the punctuation and the capital letters
def spellchecker(text,d=d):
    text_nopunc = text.translate(translator).lower()
    t = text_nopunc.split()
    res = list()
    for w in t:
        if w not in d:
            max_d = 0
            res_supp = w
            for cw in d:
                supp = levenstein_similarity(w,cw)
                if supp>0.8 and supp>max_d:
                    max_d = supp
                    res_supp = cw
            res.append(res_supp)
        else:
            res.append(w)
    return " ".join(res)

def run_parallel(data):
    pool = Pool(processes=len(data))
    return pool.map(spellchecker, data)


text = """
Dilecteyy notro havendo nui facto experientia che cussi sei
longio a finire una opera, como sei de persona. Te
recordanmo che il te bisognay a questa volta mutare
nattura: perchè se non haverai fiinto el studdiolo al rtorno
nostro te faremo metter in presonne in lo battiponte
del castiello, et non serra snzah.
Dilecteyy notro havendo nui facto experientia che cussi sei
longio a finire una opera, como sei de persona. Te
recordanmo che il te bisognay a questa volta mutare
nattura: perchè se non haverai fiinto el studdiolo al rtorno
nostro te faremo metter in presonne in lo battiponte
del castiello, et non serra snzah.
Dilecteyy notro havendo nui facto experientia che cussi sei
longio a finire una opera, como sei de persona. Te
recordanmo che il te bisognay a questa volta mutare
nattura: perchè se non haverai fiinto el studdiolo al rtorno
nostro te faremo metter in presonne in lo battiponte
del castiello, et non serra snzah.
"""

start_t = time.time()
res = run_parallel(text.split("\n"))
print("ELAPSED TIME:", time.time()-start_t)
print(res)