import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
from io import BytesIO
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split, cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------- UTILITÁRIOS --------------------
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    x1 = 5 * n * n + 4
    x2 = 5 * n * n - 4
    return int(x1 ** 0.5) ** 2 == x1 or int(x2 ** 0.5) ** 2 == x2

# -------------------- FILTROS --------------------
def atende_filtros(jogo, ultimo_resultado):
    pares = len([d for d in jogo if d % 2 == 0])
    primos = len([d for d in jogo if is_prime(d)])
    mult3 = len([d for d in jogo if d % 3 == 0])
    fib = len([d for d in jogo if is_fibonacci(d)])
    soma = sum(jogo)
    repetidas = len(set(jogo).intersection(set(ultimo_resultado)))

    return (
        5 <= pares <= 10 and
        3 <= primos <= 6 and
        3 <= mult3 <= 5 and
        2 <= fib <= 4 and
        7 <= repetidas <= 11 and
        140 <= soma <= 245
    )

# -------------------- GERAÇÃO E ESTATÍSTICAS --------------------
def gerar_jogos_filtrados(ultimo_resultado, n_jogos=2000):
    jogos = []
    tentativas = 0
    while len(jogos) < n_jogos and tentativas < 20000:
        jogo = sorted(random.sample(range(1, 26), 15))
        if atende_filtros(jogo, ultimo_resultado):
            jogos.append(jogo)
        tentativas += 1
    return jogos

def calcular_estatisticas(jogo, ultimo_resultado):
    pares = len([d for d in jogo if d % 2 == 0])
    impares = 15 - pares
    primos = len([d for d in jogo if is_prime(d)])
    mult3 = len([d for d in jogo if d % 3 == 0])
    fib = len([d for d in jogo if is_fibonacci(d)])
    soma = sum(jogo)
    repetidas = len(set(jogo).intersection(set(ultimo_resultado)))
    return [pares, impares, primos, mult3, fib, soma, repetidas]

# -------------------- MODELO --------------------
def treinar_modelo(df, modelo_tipo):
    X = df[["Pares", "Ímpares", "Primos", "Múltiplos de 3", "Fibonacci", "Soma", "Repetidas"]]
    y = df["Acertos"]

    if modelo_tipo == "RandomForest":
        modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    elif modelo_tipo == "XGBoost":
        modelo = XGBRegressor(n_estimators=100, random_state=42)
    elif modelo_tipo == "LightGBM":
        modelo = LGBMRegressor(n_estimators=100, random_state=42)
    elif modelo_tipo == "NeuralNet":
        modelo = MLPClassifier(hidden_layer_sizes=(50,50), max_iter=500, random_state=42)
    else:
        modelo = RandomForestClassifier(n_estimators=100, random_state=42)

    modelo.fit(X, y)
    dump(modelo, "modelo_lotofacil.joblib")
    return modelo

def carregar_modelo():
    if os.path.exists("modelo_lotofacil.joblib"):
        return load("modelo_lotofacil.joblib")
    return None

# -------------------- SELEÇÃO DOS MELHORES --------------------
def selecionar_melhores(jogos, modelo, ultimo_resultado, top_n):
    stats = [calcular_estatisticas(jogo, ultimo_resultado) for jogo in jogos]
    colunas = ["Pares", "Ímpares", "Primos", "Múltiplos de 3", "Fibonacci", "Soma", "Repetidas"]
    df_stats = pd.DataFrame(stats, columns=colunas)

    if modelo:
        df_stats["Predito"] = modelo.predict(df_stats)
    else:
        df_stats["Predito"] = 0

    melhores = df_stats.sort_values(by="Predito", ascending=False).head(top_n)
    jogos_selecionados = [jogos[i] for i in melhores.index]
    return jogos_selecionados, melhores

# -------------------- VISUALIZAÇÃO --------------------
def mostrar_dashboard(df):
    st.dataframe(df)
    st.bar_chart(df[["Pares", "Ímpares", "Primos", "Múltiplos de 3", "Fibonacci"]])
    st.line_chart(df[["Soma"]])

# -------------------- EXPORTAÇÃO --------------------
def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# -------------------- APP --------------------
def main():
    st.set_page_config(page_title="Lotofácil IA Turbo", layout="wide")
    st.title("🤖 Lotofácil Inteligente com IA")

    col1, col2 = st.columns(2)
    with col1:
        arquivo_resultados = st.file_uploader("Resultados oficiais (.xlsx)", type=["xlsx"])
    with col2:
        arquivo_feedback = st.file_uploader("Jogos com desempenho (.xlsx)", type=["xlsx"])

    modelo = None
    modelo_tipo = st.selectbox("Modelo de IA", ["RandomForest", "XGBoost", "LightGBM", "NeuralNet"])

    if arquivo_feedback:
        df_feedback = pd.read_excel(arquivo_feedback)
        if set(["Pares", "Ímpares", "Primos", "Múltiplos de 3", "Fibonacci", "Soma", "Repetidas", "Acertos"]).issubset(df_feedback.columns):
            modelo = treinar_modelo(df_feedback, modelo_tipo)
            st.success("Modelo treinado com sucesso!")
        else:
            st.warning("Planilha de feedback incompleta.")

    if arquivo_resultados:
        df_resultados = pd.read_excel(arquivo_resultados)
        ultimo_jogo = df_resultados.iloc[-1, -15:].tolist()
        qtd_jogos = st.slider("Quantos jogos gerar?", 5, 50, 10)

        if st.button("🚀 Gerar e Avaliar Jogos"):
            brutos = gerar_jogos_filtrados(ultimo_jogo, 2000)
            selecionados, stats_df = selecionar_melhores(brutos, modelo, ultimo_jogo, qtd_jogos)

            hoje = datetime.now().date()
            df_final = pd.DataFrame()
            df_final["Data"] = [hoje] * qtd_jogos
            df_final["Jogo"] = [", ".join(f"{d:02d}" for d in jogo) for jogo in selecionados]
            df_final = pd.concat([df_final, stats_df.reset_index(drop=True)], axis=1)
            df_final["Acertos"] = ""

            mostrar_dashboard(df_final)

            excel_bytes = to_excel_bytes(df_final)
            st.download_button("📥 Baixar jogos gerados", excel_bytes, "jogos_com_predicao.xlsx")

if __name__ == "__main__":
    main()
