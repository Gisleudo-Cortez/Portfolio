import requests
import unicodedata

DICT_URL_1 = "https://www.ime.usp.br/~pf/dicios/br-utf8.txt"
DICT_URL = "https://raw.githubusercontent.com/fserb/pt-br/refs/heads/master/palavras"

INVALIDAS = {'aioes'}


def remove_acentos(palavra):
    return ''.join(c for c in unicodedata.normalize('NFD', palavra) if unicodedata.category(c) != 'Mn')


def obter_palavras(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.strip().splitlines()


def filtrar_palavras(palavras):
    return {remove_acentos(p.lower()) for p in palavras if len(p) == 5} - INVALIDAS


def salvar_palavras(arquivo, palavras):
    with open(arquivo, "w") as file:
        file.write("\n".join(sorted(palavras)) + "\n")


pt_br_letras_5 = filtrar_palavras(obter_palavras(DICT_URL))
pt_br_letras_5_1 = filtrar_palavras(obter_palavras(DICT_URL_1))

completo_pt = pt_br_letras_5.union(pt_br_letras_5_1)
salvar_palavras("portugues_completo.txt", completo_pt)
