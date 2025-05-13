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
        jogo = sorted(random.sample(dezenas_ordenadas[:20], 15))  # Seleciona as 20 mais prováveis
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
        jogo = sorted(random.sample(dezenas_ordenadas[:20], 15))  # Seleciona as 20 mais frequentes
        jogos.append(jogo)

    return jogos

def pagina_gerador():
    """
    Página para gerar jogos otimizados.
    """
    st.header("🎲 Gerador de Jogos Inteligentes")
    st.write("Crie combinações de jogos otimizados com base em estatísticas e modelos de IA.")

    # Simular dados de frequência
    frequencia = pd.DataFrame({
        "Dezena": [i for i in range(1, 25)],
        "Frequência": [100 - i for i in range(1, 25)]  # Exemplo de frequência decrescente
    })

    # Exibir tabela de frequência
    st.write("Frequência das dezenas:")
    st.dataframe(frequencia)

    # Gerar jogos
    num_jogos = st.slider("Número de jogos a gerar:", min_value=1, max_value=20, value=10)
    if st.button("Gerar Jogos"):
        jogos = gerar_jogos_otimizados(frequencia, num_jogos=num_jogos)
        st.write("Jogos Gerados:")
        for i, jogo in enumerate(jogos, 1):
            st.write(f"Jogo {i}: {jogo}")