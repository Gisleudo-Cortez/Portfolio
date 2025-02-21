import requests
import unicodedata

# DICT_URL = "https://www.ime.usp.br/~pf/dicios/br-utf8.txt"
DICT_URL = "https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/palavras"

def remove_acentos(palavra):
    return ''.join(
        c for c in unicodedata.normalize('NFD', palavra) if unicodedata.category(c) != 'Mn'
    )

pt_br_full = requests.get(DICT_URL).text.strip().splitlines()
pt_br_letras_5 = {remove_acentos(p.lower()) for p in pt_br_full if len(p) == 5}

with open("portugues_5_letras_gh.txt", "w") as file:
    for p in pt_br_letras_5:
        palavras_invalidas_no_termoo = ['aioes']
        if p in palavras_invalidas_no_termoo:
            continue
        else:
            file.write(f"{p}\n")
