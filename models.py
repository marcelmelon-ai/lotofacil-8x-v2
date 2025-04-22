import numpy as np
import pandas as pd
from xgboost import XGBClassifier
import streamlit as st
from helpers import carregar_tabelas_numeromania, preparar_dados_para_ia  # Certifique-se de que essas funções estão no helpers.py

# ⚙️ Função para treinar o modelo XGBoost com estatísticas simples
def treinar_modelo_xgb(df_stats):
    X = df_stats[["Frequência", "Atraso", "Maior_Atraso"]]
    y = np.arange(len(X)) % 2  # Simulação temporária de rótulos
    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X, y)
    return model

# ⚙️ Função para prever dezenas com base no modelo treinado
def prever_dezenas(model, df_stats):
    X = df_stats[["Frequência", "Atraso", "Maior_Atraso"]]
    df_stats["Score"] = model.predict_proba(X)[:, 1]
    return df_stats.sort_values("Score", ascending=False).head(25)

# ⚙️ Função para extrair features a partir de um DataFrame contendo colunas com dezenas
def extrair_features(df):
    moldura = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}
    primos = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    multiplos3 = {i for i in range(1, 26) if i % 3 == 0}
    fibonacci = {1, 2, 3, 5, 8, 13, 21}
    linhas = {i: set(range(5*(i-1)+1, 5*i+1)) for i in range(1, 6)}
    colunas = {i: set(range(i, 26, 5)) for i in range(1, 6)}

    features = []
    for _, row in df.iterrows():
        dezenas = set(row["Dezenas"])
        feat = {
            "pares": sum(1 for d in dezenas if d % 2 == 0),
            "ímpares": sum(1 for d in dezenas if d % 2 != 0),
            "soma": sum(dezenas),
            "moldura": len(dezenas & moldura),
            "primos": len(dezenas & primos),
            "multiplos3": len(dezenas & multiplos3),
            "fibonacci": len(dezenas & fibonacci),
        }

        for i in range(1, 6):
            feat[f"linha_{i}"] = len(dezenas & linhas[i])
            feat[f"coluna_{i}"] = len(dezenas & colunas[i])

        features.append(feat)

    return pd.DataFrame(features)

# ⚙️ Pré-processador de DataFrame: extrai jogos válidos com 15 dezenas
def preprocessar_dados(df):
    colunas_dezenas = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and df[col].dropna().between(1, 25).all()]
    for i in range(len(colunas_dezenas) - 14):
        sub = colunas_dezenas[i:i+15]
        if df[sub].notna().all(axis=1).sum() > 5:
            jogos = df[sub].dropna().astype(int).values.tolist()
            return jogos
    return []

# ⚙️ Carregamento e preparação de dados para IA com cache
@st.cache_data(ttl=3600)
def carregar_e_preparar_dados():
    tabelas = carregar_tabelas_numeromania()
    dados_ia = preparar_dados_para_ia(tabelas)
    return dados_ia

# 📊 Interface Streamlit (essa parte normalmente fica em outro arquivo como main.py)
def exibir_estatisticas_streamlit():
    st.title("📊 Estatísticas da Lotofácil - Numeromania")

    tabelas = carregar_tabelas_numeromania()

    if tabelas:
        st.success(f"{len(tabelas)} tabelas carregadas com sucesso!")
        for nome, df in tabelas.items():
            st.subheader(f"{nome}")
            st.dataframe(df)
    else:
        st.warning("Nenhuma tabela foi carregada.")
