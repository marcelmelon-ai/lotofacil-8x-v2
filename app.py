# === IMPORTS ===
import os
import random
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier


# === FUNÇÕES UTILITÁRIAS ===
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    x = 5 * n * n
    return int(x**0.5 + 0.5)**2 in [x + 4, x - 4]


# === FUNÇÕES DE PROCESSAMENTO ===
def processar_dados(caminho_excel):
    df = pd.read_excel(caminho_excel)
    df = df.dropna()

    dezenas = df.iloc[:, 2:17].astype(int)  # colunas com as dezenas

    # Criação da matriz binária
    jogos_binarios = [
        [1 if i in row.values else 0 for i in range(1, 26)]
        for _, row in dezenas.iterrows()
    ]

    jogos_binarios_df = pd.DataFrame(jogos_binarios, columns=[f'D{i}' for i in range(1, 26)])
    return jogos_binarios_df, df


# === FUNÇÕES DE MACHINE LEARNING ===
def treinar_modelo(X, y):
    modelo_rf = RandomForestClassifier(n_estimators=200, random_state=42)
    modelo = MultiOutputClassifier(modelo_rf)
    modelo.fit(X, y)
    return modelo

def gerar_jogos(modelo, X_referencia, n_jogos=10):
    probabilidades = modelo.predict_proba(X_referencia)

    # Média das probabilidades para cada dezena
    probs_medias = [
        (i + 1, np.mean([p[1] for p in probabilidades[i]]))
        for i in range(25)
    ]

    # Seleciona 15 dezenas entre as 20 mais prováveis
    dezenas_ordenadas = sorted(probs_medias, key=lambda x: x[1], reverse=True)
    jogos = [
        sorted(random.sample([d[0] for d in dezenas_ordenadas[:20]], 15))
        for _ in range(n_jogos)
    ]

    return jogos

def avaliar_acertos(jogos, resultado_real):
    return [len(set(jogo).intersection(set(resultado_real))) for jogo in jogos]


# === FUNÇÕES DE INTERFACE STREAMLIT ===
def main():
    st.set_page_config(page_title="Lotofácil 8X", layout="wide")
    st.sidebar.title("🎯 Lotofácil 8X")

    escolha = st.sidebar.radio(
        "Navegação",
        ["Carregar Arquivos", "Dashboard", "Gerar Sugestões", "Sobre"]
    )

    if escolha == "Carregar Arquivos":
        carregar_arquivos()

    elif escolha == "Dashboard":
        st.title("📊 Dashboard de Estatísticas")
        try:
            mostrar_dashboard()
        except FileNotFoundError:
            st.error("Os arquivos necessários não foram encontrados. Por favor, carregue os arquivos na aba 'Carregar Arquivos'.")

    elif escolha == "Gerar Sugestões":
        st.title("🎲 Geração de Jogos Inteligentes")
        st.info("Em breve...")

    elif escolha == "Sobre":
        st.title("ℹ️ Sobre o Projeto")
        st.markdown("""
        Aplicativo de análise inteligente da Lotofácil.
        Desenvolvido com Streamlit + IA (Random Forest).
        """)


def carregar_arquivos():
    st.title("📂 Carregar Arquivos Excel")
    st.write("Carregue os arquivos necessários para continuar.")

    resultados_file = st.file_uploader("Arquivo de resultados históricos", type=["xlsx"])
    estatisticas_file = st.file_uploader("Arquivo de estatísticas", type=["xlsx"])
    jogos_atuais_file = st.file_uploader("Arquivo de jogos atuais", type=["xlsx"])

    if resultados_file and estatisticas_file and jogos_atuais_file:
        try:
            resultados = pd.read_excel(resultados_file)
            estatisticas = pd.read_excel(estatisticas_file)
            jogos_atuais = pd.read_excel(jogos_atuais_file)

            if "Data Sorteio" in resultados.columns:
                resultados["Data Sorteio"] = resultados["Data Sorteio"].astype(str)

            os.makedirs("dados", exist_ok=True)
            resultados.to_excel("dados/resultados_historicos.xlsx", index=False)
            estatisticas.to_excel("dados/estatisticas.xlsx", index=False)
            jogos_atuais.to_excel("dados/jogos_atuais.xlsx", index=False)

            st.session_state["resultados"] = resultados
            st.session_state["estatisticas"] = estatisticas
            st.session_state["jogos_atuais"] = jogos_atuais

            st.success("Arquivos carregados e salvos com sucesso!")
            st.write("### Pré-visualização dos Resultados:")
            st.dataframe(resultados.head())
            st.write("### Pré-visualização das Estatísticas:")
            st.dataframe(estatisticas.head())
            st.write("### Pré-visualização dos Jogos Atuais:")
            st.dataframe(jogos_atuais.head())

        except Exception as e:
            st.error(f"Erro ao processar os arquivos: {e}")
    else:
        st.info("Por favor, carregue todos os arquivos para continuar.")


def mostrar_dashboard():
    st.warning("⚠️ Função mostrar_dashboard() ainda não implementada.")
    # Aqui você pode incluir gráficos, KPIs, contadores, etc.


# === EXECUÇÃO ===
if __name__ == "__main__":
    main()
