import streamlit as st
import pandas as pd

def mostrar_dashboard_estatistico(df):
    """
    Exibe o dashboard estatístico com gráficos baseados nos dados fornecidos.

    Args:
        df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
    """
    st.title("📊 Dashboard de Estatísticas")
    st.write("Análise completa dos concursos anteriores.")

    # Verificar se o DataFrame está vazio
    if df.empty:
        st.warning("⚠️ O DataFrame está vazio. Por favor, carregue os dados corretamente.")
        return

    # Dividir a página em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        # Calcular a frequência das dezenas
        try:
            freq = df.filter(like="D").apply(pd.Series.value_counts).sum(axis=1).sort_values(ascending=False)
            st.subheader("Frequência das Dezenas")
            st.bar_chart(freq)
        except Exception as e:
            st.error(f"Erro ao calcular a frequência das dezenas: {e}")

    with col2:
        # Placeholder para futuras funcionalidades
        st.subheader("Ocorrência por posição (em construção)")
        st.info("🔧 Essa funcionalidade está em desenvolvimento.")