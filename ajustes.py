import pandas as pd
import streamlit as st
import logging
import os
from paginas.dados import dados
from paginas.dados import carregar_dados_excel

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@st.cache_data
def carregar_dados_excel(caminho_arquivo):
    try:
        if os.getenv("STREAMLIT_CLOUD") == "true":
            logging.info(f"Carregando dados do arquivo: {caminho_arquivo}")
            return pd.read_excel(caminho_arquivo)
        else:
            logging.warning("Ambiente local detectado. Retornando DataFrame vazio.")
            return pd.DataFrame()
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {caminho_arquivo}")
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")


def preprocessar_dados(df):
    try:
        logging.info("Iniciando o pré-processamento dos dados...")

        # Verificar se o DataFrame está vazio
        if df.empty:
            raise ValueError("O DataFrame fornecido está vazio.")

        # Selecionar as colunas relevantes (dezenas)
        colunas_relevantes = [col for col in df.columns if col.startswith("D")]
        if not colunas_relevantes:
            raise ValueError("Nenhuma coluna de dezenas encontrada no DataFrame.")

        X = df[colunas_relevantes]
        y = df["Soma das dezenas"]

        # Validar os valores de y
        y = pd.to_numeric(y, errors="coerce").dropna().astype(int)

        logging.info("Pré-processamento concluído com sucesso.")
        return X, y
    except Exception as e:
        logging.error(f"Erro durante o pré-processamento dos dados: {e}")
        raise