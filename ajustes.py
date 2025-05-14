import pandas as pd
import streamlit as st
import logging
from paginas.dados import dados
from paginas.dados import carregar_dados_excel

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

caminho_arquivo = 'data/resultados.xlsx'
arquivo_enviado = None

@st.cache_data
def carregar_dados_excel(caminho_arquivo):
    try:
        logging.info(f"Carregando dados do arquivo: {caminho_arquivo}")
        return pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {caminho_arquivo}")
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

def preprocessar_dados(df):
    """
    Pré-processa os dados carregados do Excel.

    Args:
        df (pd.DataFrame): DataFrame com os dados brutos.

    Returns:
        tuple: (X, y) onde X são as colunas relevantes e y é a coluna alvo.
    """
    try:
        logging.info("Iniciando o pré-processamento dos dados...")

        # Verificar se o DataFrame está vazio
        if df.empty:
            raise ValueError("O DataFrame fornecido está vazio.")

        # Verificar se existem colunas que começam com "D" (dezenas)
        colunas_relevantes = [col for col in df.columns if col.startswith("D")]
        if not colunas_relevantes:
            raise ValueError("Nenhuma coluna de dezenas encontrada no DataFrame.")

        # Selecionar as colunas relevantes (X)
        X = df[colunas_relevantes]

        # Supondo que a última coluna contenha as dezenas sorteadas (y)
        y = df.iloc[:, -1]  # Última coluna como alvo

        # Tratar valores inválidos em y
        if y.dtype == 'object':
            y = pd.to_numeric(y, errors='coerce')  # Converter para numérico, substituindo inválidos por NaN
        y = y.dropna().astype(int)

        # Validar se os valores de y estão no intervalo esperado (1 a 25)
        if not y.between(1, 25).all():
            raise ValueError(f"Valores inválidos encontrados em y. Esperado: números entre 1 e 25, obtido: {y.unique()}")

        logging.info("Pré-processamento concluído com sucesso.")
        return X, y
    except Exception as e:
        logging.error(f"Erro durante o pré-processamento dos dados: {e}")
        raise
        
        # Verificar se existem colunas que começam com "D" (dezenas)
        colunas_relevantes = [col for col in df.columns if col.startswith("D")]
        if not colunas_relevantes:
            raise ValueError("Nenhuma coluna de dezenas encontrada no DataFrame.")
        
        # Selecionar as colunas relevantes (X)
        X = df[colunas_relevantes]
        
        # Supondo que a última coluna contenha as dezenas sorteadas (y)
        y = df.iloc[:, -1]  # Última coluna como alvo
        
        # Tratar valores inválidos em y
        if y.dtype == 'object':
            y = pd.to_numeric(y, errors='coerce')  # Converter para numérico, substituindo inválidos por NaN
        y = y[(y >= 1) & (y <= 25)]
        
        # Validar se os valores de y estão no intervalo esperado (1 a 25)
        if not y.between(1, 25).all():
            raise ValueError(f"Valores inválidos encontrados em y. Esperado: números entre 1 e 25, obtido: {y.unique()}")
        
        logging.info("Pré-processamento concluído com sucesso.")
        return X, y
    except Exception as e:
        logging.error(f"Erro durante o pré-processamento dos dados: {e}")
        raise

    def preprocessar_dados(output_file):
         # Carrega os dados do Excel (somente no ambiente online)
        df = carregar_dados_excel(output_file)
        if df.empty:
            return "Nenhum dado carregado no ambiente local."
        # Processa os dados (exemplo)
        return df.describe() 