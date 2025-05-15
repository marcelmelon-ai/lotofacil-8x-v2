import streamlit as st
import pandas as pd
import plotly.express as px
import os

def mostrar_dashboard():
    """
    Exibe o dashboard com gráficos e tabelas.
    """
    # Verificar se os arquivos existem
    if not os.path.exists("dados/resultados_historicos.xlsx") or not os.path.exists("dados/estatisticas.xlsx"):
        raise FileNotFoundError("Os arquivos necessários não foram encontrados.")

    # Carregar os dados
    resultados = pd.read_excel("dados/resultados_historicos.xlsx")
    estatisticas = pd.read_excel("dados/estatisticas.xlsx")

    st.write("### Resultados Históricos")
    st.dataframe(resultados)

    st.write("### Estatísticas")
    st.dataframe(estatisticas)

    # Gráfico de frequência
    st.write("### Frequência das Dezenas")
    fig = px.bar(estatisticas, x="Dezena", y="Frequência", title="Frequência das Dezenas")
    st.plotly_chart(fig)