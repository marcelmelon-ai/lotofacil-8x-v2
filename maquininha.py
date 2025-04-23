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
        xls = pd.ExcelFile("tabelas_numeromania.xlsx")  # Certifique-se que o Excel esteja no mesmo diretório do app

        nomes_abas = {
            "tabela1 - atraso": "Frequencia",
            "tabela 2 - duplas mais sairam": "Duplas_Mais_Frequentes",
            "tabela 3 - duplas que - sairam": "Duplas_Menos_Frequentes",
            "tabela 4 - tricas mais sairam": "Trincas_Mais_Frequentes",
            "tabela 5 quadras que + sairam": "Quadras_Mais_Frequentes",
            "tabela 6 -repetição consecutiva": "Repeticoes_Consecutivas",
            "tabela 7 - AUSÊNCIA CONSECUTIVA": "Ausencias_Consecutivas",
            "tabela 8 - CONTROLE DE CICLOS": "Controle_de_Ciclos",
            "tabela 9 Dezenas mais sorteadas": "Dezenas_Mais_Sorteadas",
            "tabela 10 - Média das dezenas": "Media_das_Dezenas",
            "tabela 11 - Dezenas + atrasadas": "Dezenas_Mais_Atrasadas",
            "tabela 12 - Pares e ímpares": "Pares_Impares",
            "tabela 13 - Números primos": "Numeros_Primos",
            "tabela 14 - multiplos de 3": "Multiplos_de_3",
            "tabela 15 -Números de Fibonacci": "Fibonacci",
            "tabela 16 Soma das dezenas": "Soma_das_Dezenas",
            "tabela 17 repetidas do concurso": "Repetidas_do_Concurso"
        }

        estatisticas = {}

        for aba_excel, nome_tabela in nomes_abas.items():
            if aba_excel in xls.sheet_names:
                df = xls.parse(aba_excel)
                df.columns = [str(c).strip() for c in df.columns]
                estatisticas[nome_tabela] = df
            else:
                st.warning(f"Aba '{aba_excel}' não foi encontrada no Excel!")

        return estatisticas

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
