import pandas as pd
import streamlit as st
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@st.cache_data
def carregar_dados_excel(caminho_arquivo):
    """
    Carrega os dados de um arquivo Excel.

    Args:
        caminho_arquivo (str): Caminho para o arquivo Excel.

    Returns:
        pd.DataFrame: DataFrame com os dados carregados.
    """
    try:
        logging.info(f"Carregando dados do arquivo: {caminho_arquivo}")
        return pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {caminho_arquivo}")
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo Excel: {e}")
        raise

def preprocessar_dados(resultados):
    # ... código existente ...
    
    # Remover linhas com valores ausentes ou inválidos
    resultados = resultados.dropna()
    
    # Separar X e y
    X = resultados[["D1", "D2", "D3", "D4", "D5"]]  # Exemplo de colunas de entrada
    y = resultados["Soma das dezenas"]  # Exemplo de coluna de saída
    
    return X, y

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
        y = y[(y >= 1) & (y <= 25)]
        
        # Validar se os valores de y estão no intervalo esperado (1 a 25)
        if not y.between(1, 25).all():
            raise ValueError(f"Valores inválidos encontrados em y. Esperado: números entre 1 e 25, obtido: {y.unique()}")
        
        logging.info("Pré-processamento concluído com sucesso.")
        return X, y
    except Exception as e:
        logging.error(f"Erro durante o pré-processamento dos dados: {e}")
        raise