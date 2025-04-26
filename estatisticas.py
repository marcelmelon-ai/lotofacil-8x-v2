import pandas as pd
import streamlit as st

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

def calcular_estatisticas_avancadas(resultados_df, tabelas):
    """
    Calcula estatísticas avançadas com base nos resultados e nas tabelas de estatísticas.

    Args:
        resultados_df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
        tabelas (dict): Dicionário com DataFrames das tabelas carregadas.

    Returns:
        dict: Dicionário com estatísticas calculadas.
    """
    estatisticas = {}

    # Frequência das dezenas
    estatisticas["Frequencia"] = calcular_frequencia(resultados_df)

    # Estatísticas baseadas nas tabelas
    if "Frequencia" in tabelas:
        tabela_frequencia = tabelas["Frequencia"]
        estatisticas["Mais Sorteadas"] = tabela_frequencia.nlargest(10, "Frequência")
        estatisticas["Menos Sorteadas"] = tabela_frequencia.nsmallest(10, "Frequência")

    if "Pares e Ímpares" in tabelas:
        pares_impares = tabelas["Pares e Ímpares"]
        estatisticas["Pares e Ímpares"] = pares_impares

    if "Dezenas mais atrasadas" in tabelas:
        atrasadas = tabelas["Dezenas mais atrasadas"]
        estatisticas["Mais Atrasadas"] = atrasadas.nlargest(10, "Atraso")

    # Adicione mais cálculos conforme necessário
    # Exemplo: Soma das dezenas, Fibonacci, etc.
    if "Soma das dezenas" in tabelas:
        soma_dezenas = tabelas["Soma das dezenas"]
        estatisticas["Soma das Dezenas"] = soma_dezenas

    return estatisticas

def preparar_dados_para_ia(resultados_df, estatisticas):
    """
    Prepara os dados para treinamento de modelos de IA.

    Args:
        resultados_df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
        estatisticas (dict): Dicionário com estatísticas calculadas.

    Returns:
        tuple: Dados de entrada (X) e saída (y) para treinamento.
    """
    # Exemplo de preparação de dados
    X = resultados_df.filter(like="D").copy()
    y = resultados_df["Resultado"] if "Resultado" in resultados_df.columns else None

    # Adicione colunas de estatísticas ao conjunto de dados
    if "Frequencia" in estatisticas:
        frequencia = estatisticas["Frequencia"]
        X = X.merge(frequencia, left_on="D1", right_on="Dezena", how="left")

    return X, y
