import pandas as pd
import streamlit as st
from estatisticas import carregar_dados_excel

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

@st.cache_data
def carregar_dados_excel(caminho_arquivo_excel):
    """
    Carrega os dados de um arquivo Excel.

    Args:
        caminho_arquivo_excel (str): Caminho para o arquivo Excel.

    Returns:
        pd.DataFrame: DataFrame com os dados carregados.
    """
    try:
        return pd.read_excel(caminho_arquivo_excel)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho_arquivo_excel}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo Excel: {e}")
        return pd.DataFrame()

@st.cache_data
def carregar_tabelas_numeromania(caminho_arquivo_excel):
    """
    Carrega as tabelas do arquivo 'Tabelas_numeromania.xlsx'.

    Args:
        caminho_arquivo_excel (str): Caminho para o arquivo Excel.

    Returns:
        dict: Dicionário com DataFrames das tabelas carregadas.
    """
    try:
        xls = pd.ExcelFile(caminho_arquivo_excel)
        tabelas = {
            "Tabela 1": "Frequencia",
            "Tabela 2": "Duplas maiores frequencias",
            "Tabela 3": "Duplas menores frequencias",
            "Tabela 4": "Trios maiores frequencias",
            "Tabela 5": "Quadras maiores frequencias",
            "Tabela 6": "Dezenas repetição consecutiva",
            "Tabela 7": "Dezenas ausência consecutiva",
            "Tabela 8": "Controle de ciclos normais",
            "Tabela 9": "Mais sorteadas",
            "Tabela 10": "Média das dezenas",
            "Tabela 11": "Dezenas mais atrasadas",
            "Tabela 12": "Pares e Ímpares",
            "Tabela 13": "Números primos",
            "Tabela 14": "Múltiplos de 3",
            "Tabela 15": "Fibonacci",
            "Tabela 16": "Soma das dezenas",
            "Tabela 17": "Dezenas repetidas do jogo anterior",
        }

        dados_tabelas = {}
        for aba, nome in tabelas.items():
            try:
                dados_tabelas[nome] = xls.parse(aba)
            except Exception as e:
                st.warning(f"Erro ao carregar a aba {aba}: {e}")

        return dados_tabelas
    except FileNotFoundError:
        st.error(f"Arquivo '{caminho_arquivo_excel}' não encontrado.")
        return {}
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo Excel: {e}")
        return {}
