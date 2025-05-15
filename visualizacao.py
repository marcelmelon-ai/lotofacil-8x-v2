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

    # Verificar se o arquivo de jogos atuais existe
    jogos_atuais = None
    if os.path.exists("dados/jogos_atuais.xlsx"):
        jogos_atuais = pd.read_excel("dados/jogos_atuais.xlsx")

    st.write("### Resultados Históricos")
    st.dataframe(resultados)

    st.write("### Estatísticas")
    st.dataframe(estatisticas)

    if jogos_atuais is not None:
        st.write("### Jogos Atuais")
        st.dataframe(jogos_atuais)

    # Gráfico de frequência
    st.write("### Frequência das Dezenas")
    fig = px.bar(estatisticas, x="Dezena", y="Frequência", title="Frequência das Dezenas")
    st.plotly_chart(fig)