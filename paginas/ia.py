import streamlit as st
from inteligencia import treinar_modelo_xgb

def pagina_ia():
    """
    Página para treinar modelos de IA e prever dezenas.
    """
    st.header("🧠 IA e Previsões")
    st.write("Treine modelos de IA para prever as dezenas mais prováveis.")

    # Simulação de dados (substituir com dados reais)
    df_stats = st.session_state.get("frequencia", None)
    if df_stats is None:
        st.warning("⚠️ Dados estatísticos não encontrados. Por favor, carregue os dados na aba 'Dashboard'.")
        return

    # Treinar modelo
    if st.button("Treinar Modelo"):
        modelo = treinar_modelo_xgb(df_stats)
        st.success("Modelo treinado com sucesso!")
        st.write("Use o modelo para prever as dezenas mais prováveis (em breve).")