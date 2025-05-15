import streamlit as st
import random

def gerar_jogos_simples(frequencia, num_jogos=10):
    """
    Gera jogos simples com base na frequência das dezenas.

    Args:
        frequencia (list): Lista de frequências das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    dezenas_ordenadas = sorted(range(1, len(frequencia) + 1), key=lambda x: frequencia[x - 1], reverse=True)
    jogos = [sorted(random.sample(dezenas_ordenadas[:20], 15)) for _ in range(num_jogos)]
    return jogos

def pagina_gerador():
    """
    Página para gerar jogos otimizados.
    """
    st.header("🎲 Gerador de Jogos Inteligentes")
    st.write("Crie combinações de jogos otimizados com base em estatísticas e modelos de IA.")

    # Carregar dados do estado da sessão
    frequencia = st.session_state.get("frequencia", None)

    if frequencia is None:
        st.warning("⚠️ Dados não encontrados. Por favor, carregue os dados na aba 'Dashboard'.")
        return

    # Gerar jogos
    num_jogos = st.slider("Número de jogos a gerar:", min_value=1, max_value=20, value=10)
    if st.button("Gerar Jogos"):
        jogos = gerar_jogos_simples(frequencia, num_jogos=num_jogos)
        st.write("Jogos Gerados:")
        for i, jogo in enumerate(jogos, 1):
            st.write(f"Jogo {i}: {jogo}")