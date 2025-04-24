import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Função para carregar os resultados da planilha Excel
def carregar_resultados_excel(caminho_arquivo):
    return pd.read_excel(caminho_arquivo)

# Função para carregar e nomear todas as 12 tabelas do site Numeromania
def carregar_estatisticas_numeromania():
    try:
        xls = pd.ExcelFile("tabelas_numeromania.xlsx")  # O arquivo deve estar na mesma pasta do app

        nomes_abas = {
            "Tabela 1": "Frequencia",
            "Tabela 2": "Duplas_Mais_Frequentes",
            "Tabela 3": "Duplas_Menos_Frequentes",
            "Tabela 4": "Trincas_Mais_Frequentes",
            "Tabela 5": "Quadras_Mais_Frequentes",
            "Tabela 6": "Repeticoes_Consecutivas",
            "Tabela 7": "Ausencias_Consecutivas",
            "Tabela 8": "Controle_de_Ciclos",
            "Tabela 9": "Dezenas_Mais_Sorteadas",
            "Tabela 10": "Media_das_Dezenas",
            "Tabela 11": "Dezenas_Mais_Atrasadas",
            "Tabela 12": "Pares_Impares",
            "Tabela 13": "Numeros_Primos",
            "Tabela 14": "Multiplos_de_3",
            "Tabela 15": "Fibonacci",
            "Tabela 16": "Soma_das_Dezenas",
            "Tabela 17": "Repetidas_do_Concurso"
        }

        estatisticas = {}
        for aba_original, nome_padronizado in nomes_abas.items():
            try:
                df = xls.parse(aba_original)
                estatisticas[nome_padronizado] = df
            except Exception as e:
                print(f"Erro ao carregar a aba {aba_original}: {e}")

        return estatisticas

    except FileNotFoundError:
        print("❌ Arquivo 'tabelas_numeromania.xlsx' não encontrado.")
        return {}

    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {e}")
        return {}

# Função auxiliar para reconstruir estatísticas básicas (caso faltem)
def reconstruir_estatisticas_basicas(planilha):
    col_dezenas = [f'D{i}' for i in range(1, 16)]
    dezenas_str = planilha[col_dezenas].astype(str).apply(lambda x: x.str.zfill(2))
    todas = [f"{i:02}" for i in range(1, 26)]

    estat = []
    for dez in todas:
        freq = (dezenas_str == dez).sum().sum()
        atraso = next((i for i, row in enumerate(dezenas_str[::-1].values) if dez in row), len(planilha))
        estat.append({"Dezena": dez, "Frequência": freq, "Atraso": atraso})

    df = pd.DataFrame(estat)
    return df.set_index("Dezena")

# Função para combinar dados da planilha com as 3 estatísticas principais
def combinar_dados(planilha_excel, estatisticas):
    df = planilha_excel.copy()
    dezenas = [f'D{i}' for i in range(1, 16)]

    # Tenta carregar estatísticas do site; se falhar, usa fallback local
    try:
        freq = estatisticas['Frequencia'].set_index('Dezena')['Frequência']
        atraso = estatisticas['Atraso'].set_index('Dezena')['Atraso']
        maior_atraso = estatisticas['Maior_Atraso'].set_index('Dezena')['Maior Atraso']
    except:
        print("⚠️ Problema ao carregar estatísticas do site. Reconstruindo localmente...")
        reconstruido = reconstruir_estatisticas_basicas(df)
        freq = reconstruido['Frequência']
        atraso = reconstruido['Atraso']
        maior_atraso = pd.Series(0, index=reconstruido.index)  # Não temos como saber o maior atraso localmente

    for dez in dezenas:
        df[f'{dez}_Frequência'] = df[dez].astype(str).str.zfill(2).map(freq)
        df[f'{dez}_Atraso'] = df[dez].astype(str).str.zfill(2).map(atraso)
        df[f'{dez}_MaiorAtraso'] = df[dez].astype(str).str.zfill(2).map(maior_atraso)

    df.dropna(inplace=True)
    return df

# Preparação dos dados para IA (média das 15 dezenas por jogo)
def preparar_dados_ia(df_combined):
    dezenas = [f'D{i}' for i in range(1, 16)]
    col_freq = [f'{d}_Frequência' for d in dezenas]
    col_atraso = [f'{d}_Atraso' for d in dezenas]
    col_ma = [f'{d}_MaiorAtraso' for d in dezenas]

    df_combined['Media_Frequência'] = df_combined[col_freq].mean(axis=1)
    df_combined['Media_Atraso'] = df_combined[col_atraso].mean(axis=1)
    df_combined['Media_MaiorAtraso'] = df_combined[col_ma].mean(axis=1)

    X = df_combined[['Media_Frequência', 'Media_Atraso', 'Media_MaiorAtraso']]
    y = [1 if val > X['Media_Frequência'].median() else 0 for val in X['Media_Frequência']]

    return X, y

# Função principal
def maquininha(caminho_arquivo_excel):
    resultados_excel = carregar_resultados_excel(caminho_arquivo_excel)
    estatisticas = carregar_estatisticas_numeromania()
    dados_combinados = combinar_dados(resultados_excel, estatisticas)
    X, y = preparar_dados_ia(dados_combinados)
    return X, y, estatisticas
