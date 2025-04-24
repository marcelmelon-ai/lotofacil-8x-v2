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

def gerar_jogos_otimizados(frequencia, num_jogos=10):
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