import streamlit as st
import pandas as pd
import plotly.express as px
import os

def mostrar_dashboard():
    """
    Exibe o dashboard com gráficos e tabelas.
    """
    # Verificar se os arquivos necessários existem
    if not os.path.exists("dados/resultados_historicos.xlsx") or not os.path.exists("dados/estatisticas.xlsx"):
        raise FileNotFoundError("Os arquivos necessários não foram encontrados.")

    # Carregar os dados
    resultados = pd.read_excel("dados/resultados_historicos.xlsx")
    estatisticas = pd.ExcelFile("dados/estatisticas.xlsx")  # Carregar o arquivo Excel com múltiplas planilhas

    # Verificar se o arquivo de jogos atuais existe
    jogos_atuais = None
    if os.path.exists("dados/jogos_atuais.xlsx"):
        jogos_atuais = pd.read_excel("dados/jogos_atuais.xlsx")

    # Exibir os resultados históricos
    st.write("### Resultados Históricos")
    st.dataframe(resultados)

    # Exibir as estatísticas
    st.write("### Estatísticas")
    st.write("Selecione uma planilha para visualizar os dados estatísticos.")

    # Listar as planilhas disponíveis no arquivo de estatísticas
    planilhas_disponiveis = estatisticas.sheet_names
    planilha_selecionada = st.selectbox("Selecione a planilha:", planilhas_disponiveis)

    # Carregar a planilha selecionada
    df_estatisticas = estatisticas.parse(planilha_selecionada)
    st.write(f"### Dados da Planilha: {planilha_selecionada}")
    st.dataframe(df_estatisticas)

    # Verificar se há colunas suficientes para gerar gráficos
    if len(df_estatisticas.columns) < 2:
        st.warning("A planilha selecionada não contém colunas suficientes para gerar gráficos.")
        return

    # Permitir que o usuário escolha as colunas para o gráfico
    coluna_x = st.selectbox("Selecione a coluna para o eixo X:", df_estatisticas.columns)
    coluna_y = st.selectbox("Selecione a coluna para o eixo Y:", df_estatisticas.columns)

    # Gerar o gráfico com as colunas selecionadas
    try:
        st.write(f"### Gráfico: {coluna_y} por {coluna_x}")
        fig = px.bar(df_estatisticas, x=coluna_x, y=coluna_y, title=f"{coluna_y} por {coluna_x}")
        st.plotly_chart(fig)
    except ValueError as e:
        st.error(f"Erro ao gerar o gráfico: {e}")

    # Exibir os jogos atuais, se disponíveis
    if jogos_atuais is not None:
        st.write("### Jogos Atuais")
        st.dataframe(jogos_atuais)