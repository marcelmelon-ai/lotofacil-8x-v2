import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# === CARREGAMENTO EXCEL ===


@st.cache_data
def carregar_dados_excel(arquivo):
    if not arquivo.name.endswith(('.xlsx', '.xls')):
        st.warning("Por favor, envie um arquivo Excel válido.")
        return pd.DataFrame()
    try:
        df = pd.read_excel(arquivo)
        df.columns = [col.strip() for col in df.columns]
        return df
    except Exception as e:
        st.warning(f"Erro ao carregar Excel: {e}")
        return pd.DataFrame()
        

# === CARREGAMENTO DAS ESTATÍSTICAS (SITE NUMEROMANIA) ===

@st.cache_data
def carregar_tabelas_excel_local(caminho_excel: str) -> dict:
    try:
        xls = pd.ExcelFile(caminho_excel)

        nomes_abas = {
            "tabela1 - atraso": "Tabela_01",
            "tabela 2 - duplas mais sairam": "Tabela_02",
            "tabela 3 - duplas que - sairam": "Tabela_03",
            "tabela 4 - tricas mais sairam": "Tabela_04",
            "tabela 5 quadras que + sairam": "Tabela_05",
            "tabela 6 -repetição consecutiva": "Tabela_06",
            "tabela 7 - AUSÊNCIA CONSECUTIVA": "Tabela_07",
            "tabela 8 - CONTROLE DE CICLOS": "Tabela_08",
            "tabela 9 Dezenas mais sorteadas": "Tabela_09",
            "tabela 10 - Média das dezenas": "Tabela_10",
            "tabela 11 - Dezenas + atrasadas": "Tabela_11",
            "tabela 12 - Pares e ímpares": "Tabela_12",
            "tabela 13 - Números primos": "Tabela_13",
            "tabela 14 - multiplos de 3": "Tabela_14",
            "tabela 15 -Números de Fibonacci": "Tabela_15",
            "tabela 16 Soma das dezenas": "Tabela_16",
            "tabela 17 repetidas do concurso": "Tabela_17"
        }

        tabelas = {}

        for aba_original, nome_padrao in nomes_abas.items():
            if aba_original in xls.sheet_names:
                df = xls.parse(aba_original)
                df.columns = [str(c).strip() for c in df.columns]
                tabelas[nome_padrao] = df
            else:
                st.warning(f"Aba '{aba_original}' não encontrada no Excel.")

        return tabelas

    except Exception as e:
        st.error(f"Erro ao carregar tabelas do Excel: {e}")
        return {}


# === PRÉ-PROCESSAMENTO DE RESULTADOS EXCEL ===

def preprocessar_dados(df):
    col_dezenas = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and df[col].dropna().between(1, 25).all()]
    for i in range(len(col_dezenas) - 14):
        sub = col_dezenas[i:i+15]
        if df[sub].notna().all(axis=1).sum() > 5:
            return df[sub].dropna().astype(int).values.tolist()
    return []

# === EXTRAÇÃO DE FEATURES PARA IA ===

def preprocessar_dados(df):
    fibo_set = {1, 2, 3, 5, 8, 13, 21}
    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    multiplos_3 = set(range(3, 26, 3))

    features = []
    
    # Supondo que o DataFrame tenha colunas D1 a D15 com os números sorteados
    col_dezenas = [col for col in df.columns if col.startswith("D")]
    
    for _, row in df.iterrows():
        dezenas = row[col_dezenas].astype(int).tolist()

        pares = sum(1 for d in dezenas if d % 2 == 0)
        impares = 15 - pares
        primos_count = sum(1 for d in dezenas if d in primos)
        fibo_count = sum(1 for d in dezenas if d in fibo_set)
        moldura_count = sum(1 for d in dezenas if d in moldura)
        multiplos_3_count = sum(1 for d in dezenas if d in multiplos_3)
        soma = sum(dezenas)

        features.append({
            "pares": pares,
            "impares": impares,
            "primos": primos_count,
            "fibonacci": fibo_count,
            "moldura": moldura_count,
            "multiplos_3": multiplos_3_count,
            "soma": soma
        })

    return pd.DataFrame(features)

# === ESTATÍSTICAS DE FREQUÊNCIA E ATRASO ===

@st.cache_data
def processar_excel_resultados(df_excel):
    col_dezenas = [col for col in df_excel.columns if col.startswith('D')]
    dezenas_flat = df_excel[col_dezenas].values.flatten()

    df_freq = pd.Series(dezenas_flat).value_counts().sort_index().reset_index()
    df_freq.columns = ['Dezena', 'Frequência']
    df_freq['Dezena'] = df_freq['Dezena'].astype(str).str.zfill(2)

    df_freq['Atraso'] = df_freq['Dezena'].apply(lambda d: calcular_atraso(d, df_excel, col_dezenas))
    df_freq['Maior_Atraso'] = df_freq['Dezena'].apply(lambda d: calcular_maior_atraso(d, df_excel, col_dezenas))

    return df_freq.sort_values(by='Dezena')

def calcular_atraso(dezena, df, col_dezenas):
    for i, row in df[::-1].iterrows():
        if dezena in row[col_dezenas].astype(str).str.zfill(2).values:
            return len(df) - i - 1
    return len(df)

def calcular_maior_atraso(dezena, df, col_dezenas):
    atraso = 0
    max_atraso = 0
    for _, row in df.iterrows():
        if dezena in row[col_dezenas].astype(str).str.zfill(2).values:
            max_atraso = max(max_atraso, atraso)
            atraso = 0
        else:
            atraso += 1
    return max(max_atraso, atraso)