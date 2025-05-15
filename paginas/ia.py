import streamlit as st
from inteligencia import treinar_modelo_xgb, prever_dezenas

def pagina_ia():
    """
    Página para treinar modelos de IA e prever dezenas.
    """
    st.header("🧠 IA e Previsões")
    st.write("Treine modelos de IA para prever as dezenas mais prováveis.")

    # Carregar dados do estado da sessão
    frequencia = st.session_state.get("frequencia", None)
    resultados = st.session_state.get("resultados", None)

    if frequencia is None or resultados is None:
        st.warning("⚠️ Dados não encontrados. Por favor, carregue os dados na aba 'Dashboard'.")
        return

    # Preparar dados para treinamento
    st.write("🔄 Preparando dados para treinamento...")
    X = [[f] for f in frequencia]
    y = resultados

    # Treinar modelo
    if st.button("Treinar Modelo"):
        modelo = treinar_modelo_xgb(X, y)
        st.success("Modelo treinado com sucesso!")

        # Prever dezenas mais prováveis
        top_n = st.slider("Quantas dezenas mais prováveis deseja prever?", min_value=1, max_value=15, value=10)
        dezenas_previstas = prever_dezenas(modelo, frequencia, top_n=top_n)
        st.write(f"### Dezenas mais prováveis: {', '.join(map(str, dezenas_previstas))}")