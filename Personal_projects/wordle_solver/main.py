import math

def carregar_palavras(arquivo="portugues_5_letras.txt"):
    """
    Lê todas as palavras de 5 letras de um arquivo texto.
    Retorna a lista de palavras em maiúsculas.
    """
    with open(arquivo, "r", encoding="utf-8") as file:
        palavras = file.read().splitlines()
    # Converte tudo para minúsculo (opcional)
    palavras = [p.lower() for p in palavras]
    return palavras

def calcular_distribuicao_letras(palavras):
    """
    Calcula a frequência absoluta de cada letra e o total de letras.
    """
    letra_dict = {}
    total_letras = 0
    for palavra in palavras:
        for letra in palavra:
            letra_dict[letra] = letra_dict.get(letra, 0) + 1
            total_letras += 1
    # Ordena da mais frequente para a menos frequente
    letra_dict = dict(sorted(letra_dict.items(), key=lambda x: x[1], reverse=True))
    return letra_dict, total_letras

def calcular_probabilidades(letra_dict, total_letras):
    return {l: c / total_letras for l, c in letra_dict.items()}

def calcular_entropia_palavra(palavra, prob_letras):
    """
    Calcula a entropia da palavra com base nas probabilidades de cada letra.
    Fórmula: -∑ p * log2(p)
    """
    return -sum(prob_letras[l] * math.log2(prob_letras[l]) 
                for l in set(palavra) if l in prob_letras)

def calcular_entropias(palavras, prob_letras):
    return {p: calcular_entropia_palavra(p, prob_letras) for p in palavras}

def sugerir_melhor_palavra(entropias):
    return max(entropias, key=entropias.get)

def filtrar_palavras(palavras, feedbacks):
    """
    Filtra as palavras a partir de uma lista de tuplas (letra, indice, status),
    onde status pode ser:
      - 'V' (Verde): a letra está correta naquela posição
      - 'A' (Amarelo): a letra existe, mas em outra posição
      - 'P' (Preto): a letra não existe na palavra
    """
    
    def checa_palavra(word, feedbacks):
        """
        Verifica se a 'word' se encaixa em todos os feedbacks dados.
        """
        for (letra, pos, status) in feedbacks:
            if status == 'V':
                if word[pos] != letra:
                    return False
            elif status == 'A':
                if letra not in word:
                    return False
                if word[pos] == letra:
                    return False
            elif status == 'P':
                if letra in word:
                    return False
        return True
    
    return [w for w in palavras if checa_palavra(w, feedbacks)]

def main():

    palavras = carregar_palavras("portugues_5_letras_gh.txt")
    
    letra_dict, total_letras = calcular_distribuicao_letras(palavras)
    prob_letras = calcular_probabilidades(letra_dict, total_letras)
    ent_dict = calcular_entropias(palavras, prob_letras)
    
    melhor_inicial = sugerir_melhor_palavra(ent_dict)
    print(f"\nSugestão de palavra inicial: {melhor_inicial.upper()} (ou escolha outra)")

    tentativas = 20
    feedbacks_acumulados = []
    
    for tentativa in range(1, tentativas + 1):
        print(f"\n--- Tentativa {tentativa} ---")
        
        if len(palavras) == 0:
            print("Não há mais palavras candidatas! (Verifique a lógica ou dicas incorretas.)")
            return
        
        ent_atual = {p: ent_dict[p] for p in palavras if p in ent_dict}
        if len(ent_atual) == 0:

            chute_sugerido = palavras[0]
        else:
            chute_sugerido = max(ent_atual, key=ent_atual.get)
        
        print(f"Sugestão do sistema: {chute_sugerido.upper()}")
        
        chute_usuario = input("Digite a palavra que você usou (ou ENTER para usar a sugestão): ").strip().lower()
        if chute_usuario == "":
            chute_usuario = chute_sugerido
        
        if len(chute_usuario) != 5:
            print("Palavra inválida (não tem 5 letras). Encerrando...")
            return
        
        print("Digite o feedback para cada letra: ")
        print("  V = Green  (Verde)  -> letra correta na posição exata")
        print("  A = Yellow (Amarelo)-> letra existe na palavra, mas outra posição")
        print("  P = Black  (Preto)  -> letra não existe na palavra")
        print(f"Palavra jogada: {chute_usuario.upper()}")
        
        while True:
            fb = input("Feedback (exemplo 'VPPAV'): ").strip().upper()
            if len(fb) == 5 and all(c in "VAP" for c in fb):
                break
            print("Feedback inválido. Tente novamente, usando somente V, A ou P.")
        
        novo_feedback = [(chute_usuario[i], i, fb[i]) for i in range(5)]
        
        feedbacks_acumulados.extend(novo_feedback)
        
        palavras = filtrar_palavras(palavras, feedbacks_acumulados)
        
        if len(palavras) == 1:
            print(f"\nPossível resposta: {palavras[0].upper()}")
            acerto = input("Você acertou a palavra? (S/N) ").strip().upper()
            if acerto == "S":
                print("Parabéns! Encerrando.")
                return
            else:
                continue
    
    print("\nFim das tentativas. Palavras candidatas restantes:")
    print([p.upper() for p in palavras])

if __name__ == "__main__":
    main()
