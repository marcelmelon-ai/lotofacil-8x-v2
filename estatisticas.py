import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados_resultados(resultados_file):
    """
    Carrega os dados do arquivo 'resultados_lotofacil.xlsx' enviado manualmente.

    Args:
        resultados_file: Arquivo Excel enviado pelo usuário.

    Returns:
        pd.DataFrame: DataFrame com os dados dos resultados da Lotofácil.
    """
    try:
        df = pd.read_excel(resultados_file)
        # Ajustar a nomenclatura das colunas
        colunas_esperadas = [
            "Concurso", "Data do sorteio", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8",
            "D9", "D10", "D11", "D12", "D13", "D14", "D15"
        ]
        df.columns = colunas_esperadas
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo de resultados: {e}")
        return pd.DataFrame()

@st.cache_data
def carregar_tabelas_numeromania(tabelas_file):
    """
    Carrega as tabelas do arquivo 'tabelas_numeromania.xlsx' enviado manualmente.

    Args:
        tabelas_file: Arquivo Excel enviado pelo usuário.

    Returns:
        dict: Dicionário com DataFrames das tabelas carregadas.
    """
    try:
        xls = pd.ExcelFile(tabelas_file)
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
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo de tabelas: {e}")
        return {}

@st.cache_data
def calcular_frequencia(resultados_df):
    """
    Calcula a frequência de cada dezena no DataFrame de resultados.

    Args:
        resultados_df (pd.DataFrame): DataFrame com os resultados da Lotofácil.

    Returns:
        pd.DataFrame: DataFrame com a frequência de cada dezena.
    """
    try:
        dezenas = resultados_df.filter(like="D").values.flatten()
        freq = pd.Series(dezenas).value_counts().sort_index().reset_index()
        freq.columns = ["Dezena", "Frequência"]
        freq["Dezena"] = freq["Dezena"].astype(str).str.zfill(2)
        return freq
    except Exception as e:
        st.error(f"Erro ao calcular a frequência das dezenas: {e}")
        return pd.DataFrame()

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

    return X, y
def preparar_dados_para_ia(resultados_df, estatisticas):
    """
    Prepara os dados para treinamento de modelos de IA.

    Args:
        resultados_df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
        estatisticas (dict): Dicionário com estatísticas calculadas.

    Returns:
        tuple: Dados de entrada (X) e saída (y) para treinamento.
    """
    try:
        # Selecionar as colunas de dezenas
        X = resultados_df.filter(like="D").copy()
        y = resultados_df["Concurso"] if "Concurso" in resultados_df.columns else None

        # Adicionar colunas de estatísticas ao conjunto de dados
        if "Frequencia" in estatisticas:
            frequencia = estatisticas["Frequencia"]
            X = X.merge(frequencia, left_on="D1", right_on="Dezena", how="left")

        return X, y
    except Exception as e:
        st.error(f"Erro ao preparar os dados para IA: {e}")
        return pd.DataFrame(), None