import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

def carregar_resultados_excel(caminho_arquivo):
    """
    Carrega os resultados da planilha Excel.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo Excel.
    
    Returns:
        pd.DataFrame: DataFrame com os resultados carregados.
    """
    try:
        return pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {caminho_arquivo}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo Excel: {e}")
        return pd.DataFrame()

def carregar_estatisticas_numeromania():
    """
    Carrega estatísticas do arquivo Excel 'tabelas_numeromania.xlsx'.
    
    Returns:
        dict: Dicionário com DataFrames das estatísticas.
    """
    try:
        xls = pd.ExcelFile("tabelas_numeromania.xlsx")
        nomes_abas = {
            "Tabela 1": "Frequencia",
            "Tabela 2": "Duplas moiores frequencias",
            "Tabela 3": "Duplas menos frequencias",
            "Tabela 4": "Trios moiores frequencias",
            "Tabela 5": "Quadras moiores frequencias",
            "Tabela 6": "Dezenas repetição consecutiva",
            "Tabela 7": "Dezenas ausencia consecutiva",
            "Tabela 8": "Dezenas_controle de ciclos normais",
            "Tabela 9": "Mais sorteadas",
            "Tabela 10": "Media das dezenas",
            "Tabela 11": "Dezenas_Mais_Atrasadas",
            "Tabela 12": "Pares_Impares",
            "Tabela 13": "Numeros primos",
            "Tabela 14": "multiplos de 3",
            "Tabela 15": "Fibonacci",
            "Tabela 16": "Soma das dezenas",
            "Tabela 17": "Dezenas repetidas do jogo anterior",
        }

        estatisticas = {}
        for aba_original, nome_padronizado in nomes_abas.items():
            try:
                estatisticas[nome_padronizado] = xls.parse(aba_original)
            except Exception as e:
                st.warning(f"Erro ao carregar a aba {aba_original}: {e}")

        return estatisticas
    except FileNotFoundError:
        st.error("Arquivo 'tabelas_numeromania.xlsx' não encontrado.")
        return {}
    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {e}")
        return {}

def reconstruir_estatisticas_basicas(planilha):
    """
    Reconstrói estatísticas básicas (frequência e atraso) a partir de uma planilha.
    
    Args:
        planilha (pd.DataFrame): DataFrame com os resultados da Lotofácil.
    
    Returns:
        pd.DataFrame: DataFrame com estatísticas básicas.
    """
    col_dezenas = [f'D{i}' for i in range(1, 16)]
    dezenas_str = planilha[col_dezenas].astype(str).apply(lambda x: x.str.zfill(2))
    todas = [f"{i:02}" for i in range(1, 26)]

    estat = []
    for dez in todas:
        freq = (dezenas_str == dez).sum().sum()
        atraso = next((i for i, row in enumerate(dezenas_str[::-1].values) if dez in row), len(planilha))
        estat.append({"Dezena": dez, "Frequência": freq, "Atraso": atraso})

    return pd.DataFrame(estat).set_index("Dezena")

def combinar_dados(planilha_excel, estatisticas):
    """
    Combina dados da planilha com estatísticas principais.
    
    Args:
        planilha_excel (pd.DataFrame): DataFrame com os resultados da Lotofácil.
        estatisticas (dict): Dicionário com estatísticas carregadas.
    
    Returns:
        pd.DataFrame: DataFrame combinado com estatísticas.
    """
    df = planilha_excel.copy()
    dezenas = [f'D{i}' for i in range(1, 16)]

    try:
        freq = estatisticas['Frequencia'].set_index('Dezena')['Frequência']
        atraso = estatisticas['Dezenas_Mais_Atrasadas'].set_index('Dezena')['Atraso']
    except KeyError:
        st.warning("Estatísticas ausentes. Reconstruindo localmente...")
        reconstruido = reconstruir_estatisticas_basicas(df)
        freq = reconstruido['Frequência']
        atraso = reconstruido['Atraso']

    for dez in dezenas:
        df[f'{dez}_Frequência'] = df[dez].astype(str).str.zfill(2).map(freq)
        df[f'{dez}_Atraso'] = df[dez].astype(str).str.zfill(2).map(atraso)

    df.dropna(inplace=True)
    return df

def preparar_dados_ia(df_combined):
    """
    Prepara os dados combinados para treinamento de IA.
    
    Args:
        df_combined (pd.DataFrame): DataFrame combinado com estatísticas.
    
    Returns:
        tuple: Dados de entrada (X) e saída (y).
    """
    dezenas = [f'D{i}' for i in range(1, 16)]
    col_freq = [f'{d}_Frequência' for d in dezenas]
    col_atraso = [f'{d}_Atraso' for d in dezenas]

    df_combined['Media_Frequência'] = df_combined[col_freq].mean(axis=1)
    df_combined['Media_Atraso'] = df_combined[col_atraso].mean(axis=1)

    X = df_combined[['Media_Frequência', 'Media_Atraso']]
    y = (X['Media_Frequência'] > X['Media_Frequência'].median()).astype(int)

    return X, y

def maquininha(caminho_arquivo_excel):
    """
    Função principal para carregar dados, combinar estatísticas e preparar dados para IA.
    
    Args:
        caminho_arquivo_excel (str): Caminho para o arquivo Excel.
    
    Returns:
        tuple: Dados de entrada (X), saída (y) e estatísticas carregadas.
    """
    resultados_excel = carregar_resultados_excel(caminho_arquivo_excel)
    estatisticas = carregar_estatisticas_numeromania()
    dados_combinados = combinar_dados(resultados_excel, estatisticas)
    X, y = preparar_dados_ia(dados_combinados)
    return X, y, estatisticas