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
def carregar_tabelas_numeromania():
    url = "https://www.numeromania.com.br/fa9912.html"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        tabelas_html = soup.find_all("table")
        nomes = [
    "Tabela_01",  # Ordem crescente das Dezenas
    "Tabela_02",  # Ordem decrescente de ATRASO
    "Tabela_03",  # Ordem decrescente de OCORRÊNCIA
    "Tabela_04",  # As DUPLAS
    "Tabela_04a", # As DUPLAS em ordem decrescente de atraso
    "Tabela_04a", # AS DUPLAS de Dezenas queMENOS SAÍRAM
    "Tabela_05",  # As TRINCAS
    "Tabela_05a", # As TRINCAS em ordem decrescente de atraso
    "Tabela_06",  # As QUADRAS
    "Tabela_06a", # As QUADRAS em ordem decrescente de atraso
    "Tabela_07",  # As QUINAS de Dezenas que MAIS SAÍRAM
    "Tabela_08",  # As SENAS de Dezenas que MAIS SAÍRAM
    "Tabela_09",  # Os GRUPOS DE 7 DEZENAS
    "Tabela_10"   # REPETIÇÃO CONSECUTIVA
    "Tabela_11",  # AUSÊNCIA CONSECUTIVA
    "Tabela_12",  # CONTROLE DE CICLOS NORMAIS
    "Tabela_13",  # ESTATÍSTICAS DIVERSAS - LOTOFÁCIL - (Todos os resultados)
]

        tabelas = {}

        for i, nome in enumerate(nomes):
            if i >= len(tabelas_html):
                st.warning(f"Tabela '{nome}' não encontrada.")
                continue

            tabela = tabelas_html[i]
            linhas = tabela.find_all("tr")
            dados = [[col.get_text(strip=True) for col in linha.find_all(["td", "th"])] for linha in linhas]

            if len(dados) > 1 and len(dados[1]) == len(dados[0]):
                df = pd.DataFrame(dados[1:], columns=dados[0])
            else:
                df = pd.DataFrame(dados)

            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col].str.extract(r'(\d+)')[0])
                except Exception as e:
                    st.warning(f"Erro ao converter coluna '{col}' para numérico: {e}")

            tabelas[nome] = df
            
            if st.sidebar.checkbox("🔍 Ver tabelas brutas da Numeromania"):
                for nome, tabela in tabelas.items():
                    st.subheader(f"Tabela: {nome}")
                    st.dataframe(tabela)

        return tabelas

    except Exception as e:
        st.error(f"Erro ao carregar tabelas estatísticas: {e}")
        return {}

    except Exception as e:
        st.error(f"Erro ao carregar tabelas estatísticas: {e}")
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