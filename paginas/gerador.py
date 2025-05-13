import random

def gerar_jogo(modelo, frequencia, num_jogos=10):
    """
    Gera jogos inteligentes com base no modelo treinado e na frequência das dezenas.

    Args:
        modelo: Modelo treinado de IA.
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    probabilidades = modelo.predict_proba(frequencia[["Frequência"]])[:, 1]
    frequencia["Probabilidade"] = probabilidades
    dezenas_ordenadas = frequencia.sort_values(by="Probabilidade", ascending=False)["Dezena"].tolist()

    jogos = []
    for _ in range(num_jogos):
        jogo = sorted(random.sample(dezenas_ordenadas[:15], 25))  # Seleciona as 15 mais prováveis
        jogos.append(jogo)

    return jogos

def gerar_jogos_com_fechamento(frequencia, num_jogos=10):
    """
    Gera jogos com fechamento baseado nas dezenas mais frequentes.

    Args:
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados com fechamento.
    """
    dezenas_ordenadas = frequencia.sort_values(by="Frequência", ascending=False)["Dezena"].tolist()

    jogos = []
    for _ in range(num_jogos):
        jogo = sorted(random.sample(dezenas_ordenadas[:15], 25))  # Seleciona as 15 mais frequentes
        jogos.append(jogo)

    return jogos