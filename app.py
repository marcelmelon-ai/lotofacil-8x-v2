import os
import pandas as pd
import numpy as np
import random
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from visualizacao import mostrar_dashboard, ler_estatisticas_personalizadas
from inteligencia import gerar_jogos_inteligentes, treinar_modelo, gerar_jogos

# --- Utilitários ---
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

# --- Processa dados do Excel ---
def processar_dados(caminho_excel):
    df = pd.read_excel(caminho_excel).dropna()
    dezenas = df.iloc[:, 2:17].astype(int)

    jogos_binarios = []
    for _, row in dezenas.iterrows():
        binario = [1 if i in row.values else 0 for i in range(1, 26)]
        jogos_binarios.append(binario)

    jogos_binarios_df = pd.DataFrame(jogos_binarios, columns=[f'D{i}' for i in range(1, 26)])
    return jogos_binarios_df, df

# --- Treina modelo IA ---
def treinar_modelo(X, y):
    modelo_rf = RandomForestClassifier(n_estimators=200, random_state=42)
    modelo = MultiOutputClassifier(modelo_rf)
    modelo.fit(X, y)
    return modelo

# --- Gera jogos usando o modelo treinado ---
def gerar_jogos(modelo, X_referencia, n_jogos=10):
    probabilidades = modelo.predict_proba(X_referencia)
    probs_medias = []

    for i in range(25):
        classe_1_probs = [p[1] for p in probabilidades[i]]
        media = np.mean(classe_1_probs)
        probs_medias.append((i + 1, media))

    dezenas_ordenadas = sorted(probs_medias, key=lambda x: x[1], reverse=True)

    jogos = []
    for _ in range(n_jogos):
        jogo = sorted(random.sample([d[0] for d in dezenas_ordenadas[:20]], 15))
        jogos.append(jogo)
    return jogos

# --- Avalia acertos comparando com o último sorteio real ---
def avaliar_acertos(jogos, resultado_real):
    acertos = []
    for jogo in jogos:
        acerto = len(set(jogo).intersection(set(resultado_real)))
        acertos.append(acerto)
    return acertos

# --- Exibe o dashboard interativo ---
def mostrar_dashboard():
    resultados = st.session_state["resultados"]
    estatisticas = st.session_state["estatisticas"]
    jogos_atuais = st.session_state["jogos_atuais"]

    st.subheader("Últimos Resultados")
    st.dataframe(resultados.tail(10))

    st.subheader("Estatísticas")
    st.dataframe(estatisticas)

    st.subheader("Jogos Atuais")
    st.dataframe(jogos_atuais)

# --- Função Principal ---
def main():
    st.set_page_config(page_title="Lotofácil 8X", layout="wide")
    st.sidebar.title("🎯 Lotofácil 8X")

    escolha = st.sidebar.radio("Navegação", ["Carregar Arquivos", "Dashboard de Estatísticas", "Gerar Sugestões", "Sobre"])

    if escolha == "Carregar Arquivos":
        st.title("📂 Carregar Arquivos Excel")
        resultados_file = st.file_uploader("Resultados Históricos", type=["xlsx"])
        estatisticas_file = st.file_uploader("Estatísticas", type=["xlsx"])
        jogos_atuais_file = st.file_uploader("Jogos Atuais", type=["xlsx"])

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

                st.success("Arquivos carregados com sucesso!")
                st.dataframe(resultados.head())
            except Exception as e:
                st.error(f"Erro ao carregar os arquivos: {e}")
        else:
            st.info("Por favor, carregue todos os arquivos.")

    elif escolha == "Dashboard de Estatísticas":
        st.title("📊 Painel Estatístico Inteligente")

    try:
        estatisticas_dict = ler_estatisticas_personalizadas("dados/estatisticas.xlsx")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🔢 % Pares mais comuns", f"{estatisticas_dict['pares'].iloc[0]['%']}%")
            st.metric("🔢 % Primos mais comuns", f"{estatisticas_dict['primos'].iloc[0]['%']}%")
            st.metric("🔢 % Múltiplos de 3", f"{estatisticas_dict['multiplos3'].iloc[0]['%']}%")

        with col2:
            st.metric("🔢 % Fibonacci", f"{estatisticas_dict['fibonacci'].iloc[0]['%']}%")
            st.metric("➕ Soma mais comum", f"{estatisticas_dict['soma'].iloc[0]['Soma']}")
            st.metric("♻️ % Repetidas do último sorteio", f"{estatisticas_dict['repetidas'].iloc[0]['%']}%")

        st.bar_chart({
            "Pares": [estatisticas_dict["pares"].iloc[0]["%"]],
            "Primos": [estatisticas_dict["primos"].iloc[0]["%"]],
            "Múltiplos de 3": [estatisticas_dict["multiplos3"].iloc[0]["%"]],
            "Fibonacci": [estatisticas_dict["fibonacci"].iloc[0]["%"]],
            "Repetidas": [estatisticas_dict["repetidas"].iloc[0]["%"]],
        })

    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {e}")

    elif escolha == "Gerar Sugestões":
        st.title("🎰 Sugestões de Jogos com IA")
        if "resultados" not in st.session_state:
            st.error("Carregue os arquivos primeiro na aba 'Carregar Arquivos'.")
            return

        st.info("Gerando sugestões com base nos resultados históricos...")

        X, df_original = processar_dados("dados/resultados_historicos.xlsx")
        modelo = treinar_modelo(X, X)

        st.success("Modelo treinado com sucesso!")
        jogos_gerados = gerar_jogos(modelo, X.tail(1), n_jogos=10)

        st.subheader("🔢 Jogos Sugeridos")
        for i, jogo in enumerate(jogos_gerados, 1):
            st.write(f"Jogo {i}: {jogo}")

        ultimo_resultado = df_original.iloc[-1, 2:17].tolist()
        acertos = avaliar_acertos(jogos_gerados, ultimo_resultado)

        st.subheader("🎯 Avaliação de Acertos (com base no último resultado)")
        for i, acerto in enumerate(acertos, 1):
            st.write(f"Jogo {i}: {acerto} acertos")

    elif escolha == "Gerar Sugestões":
    st.title("🎯 Geração de Jogos Inteligentes com IA")

    try:
        estatisticas_dict = ler_estatisticas_personalizadas("dados/estatisticas.xlsx")
        jogos_gerados = gerar_jogos_inteligentes(n=10, estatisticas_dict=estatisticas_dict)

        st.success("✅ Jogos gerados com base nas estatísticas mais relevantes!")
        for i, jogo in enumerate(jogos_gerados):
            st.write(f"Jogo {i+1}: {jogo}")

    except Exception as e:
        st.error(f"Erro ao gerar jogos inteligentes: {e}")

    elif escolha == "Sobre":
        st.title("📘 Sobre o Projeto Lotofácil 8X")
        st.write("""
        Este aplicativo foi desenvolvido para analisar os resultados da Lotofácil e gerar sugestões inteligentes de jogos utilizando aprendizado de máquina. 
        Ele também apresenta estatísticas e dashboards interativos a partir de arquivos do Excel enviados pelo usuário.
        """)

if __name__ == "__main__":
    main()
