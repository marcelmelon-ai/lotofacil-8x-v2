import random
import streamlit as st

def menu_lateral():
    """
    Cria o menu lateral para navegação no aplicativo.
    
    Returns:
        str: A escolha do usuário no menu.
    """
    st.sidebar.title("🎯 Lotofácil 8X")
    escolha = st.sidebar.radio(
        "Navegação",
        ["Dashboard", "Gerar Jogos", "Simulação de Jogos", "Sobre"]
    )
    return escolha

def gerar_jogos_otimizados(frequencia, num_jogos=15):
    """
    Gera combinações de jogos otimizados com base na frequência das dezenas.
    
    Args:
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.
    
    Returns:
        list: Lista de jogos gerados.
    """
    dezenas = frequencia["Dezena"].tolist()
    jogos = []
    
    for _ in range(num_jogos):
        jogo = sorted(random.sample(dezenas, 15))
        jogos.append(jogo)
    
    return jogos

def gerar_jogos_inteligentes(frequencia, num_jogos=15):
    """
    Gera combinações de jogos inteligentes com base nas estatísticas fornecidas.

    Args:
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    # Ordenar as dezenas pela frequência (mais frequentes primeiro)
    dezenas_ordenadas = frequencia.sort_values(by="Frequência", ascending=False)["Dezena"].tolist()

    jogos = []
    for _ in range(num_jogos):
        # Selecionar as 15 dezenas mais prováveis
        jogo = sorted(random.sample(dezenas_ordenadas[:20], 15))  # Exemplo: usar as 20 mais frequentes
        jogos.append(jogo)

    return jogos