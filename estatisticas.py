import pandas as pd
import streamlit as st
from estatisticas import calcular_frequencia

@st.cache_data
def calcular_frequencia(df):
    """
    Calcula a frequência de cada dezena em um DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
    
    Returns:
        pd.DataFrame: DataFrame com a frequência de cada dezena.
    """
    dezenas = df.filter(like="D").values.flatten()
    freq = pd.Series(dezenas).value_counts().sort_index().reset_index()
    freq.columns = ["Dezena", "Frequência"]
    freq["Dezena"] = freq["Dezena"].astype(str).str.zfill(2)
    return freq

def mostrar_dashboard_estatistico(df):
    """
    Exibe o dashboard estatístico com gráficos.
    
    Args:
        df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
    """
    st.title("📊 Dashboard de Estatísticas")
    st.write("Análise completa dos concursos anteriores.")
    
    col1, col2 = st.columns(2)

    with col1:
        freq = calcular_frequencia(df)
        st.subheader("Frequência das Dezenas")
        st.bar_chart(freq.set_index("Dezena")["Frequência"])

    with col2:
        st.subheader("Ocorrência por posição (em construção)")
        st.info("🔧 Essa funcionalidade está em desenvolvimento.")