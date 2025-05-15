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

    # Caminho para o arquivo Excel (ajuste conforme o local no seu Codespaces)
file_path = "estatisticas.xlsx"

# Carrega todas as planilhas do arquivo
excel_file = pd.ExcelFile(file_path)

# Lista os nomes das planilhas
print("Planilhas disponíveis:", excel_file.sheet_names)

# Cria um dicionário para armazenar os DataFrames de cada planilha
dataframes = {}

# Lê cada planilha com os nomes corretos das colunas
for sheet in excel_file.sheet_names:
    df = excel_file.parse(sheet)
    print(f"\nPlanilha: {sheet}")
    print("Colunas:", df.columns.tolist())
    dataframes[sheet] = df