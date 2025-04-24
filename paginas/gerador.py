import streamlit as st
from models import gerar_jogos_otimizados

def pagina_gerador():
    """
    Página para gerar jogos inteligentes com base em estatísticas.
    """
    st.subheader("🎰 Gerador de Jogos Inteligentes")
    st.write("Nesta página você poderá gerar jogos da Lotofácil com base em estatísticas e IA.")

    # Entrada do número de jogos
    num_jogos = st.number_input("Quantos jogos deseja gerar?", min_value=1, max_value=100, value=10)

    # Simulação de dados de frequência (substituir com dados reais)
    frequencia = st.session_state.get("frequencia", None)
    if frequencia is None:
        st.warning("⚠️ Dados de frequência não encontrados. Por favor, carregue os dados na aba 'Dashboard'.")
        return

    # Gerar jogos
    if st.button("Gerar Jogos"):
        jogos = gerar_jogos_otimizados(frequencia, num_jogos=num_jogos)
        st.success(f"{num_jogos} jogos gerados com sucesso!")
        for i, jogo in enumerate(jogos, 1):
            st.write(f"Jogo {i}: {', '.join(jogo)}")