import os
import pandas as pd
import numpy as np
import random
import streamlit as st
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from visualizacao import mostrar_dashboard
from inteligencia import gerar_jogos_inteligentes_v2, treinar_modelo, gerar_jogos_ml_filtrados
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

# --- Exporta jogos para Excel ---
def exportar_jogos_para_excel(jogos, nome_arquivo="dados/jogos_gerados.xlsx"):
    df = pd.DataFrame(jogos, columns=[f'D{i+1}' for i in range(15)])
    df.to_excel(nome_arquivo, index=False)
    return df

# --- Calcula estatísticas do jogo ---
def calcular_estatisticas_jogo(jogo):
    pares = len([d for d in jogo if d % 2 == 0])
    impares = 15 - pares
    primos = len([d for d in jogo if is_prime(d)])
    fibonacci = len([d for d in jogo if is_fibonacci(d)])
    soma = sum(jogo)
    return {
        "jogo": jogo,
        "soma": soma,
        "pares": pares,
        "ímpares": impares,
        "primos": primos,
        "fibonacci": fibonacci
    }

# --- Salva histórico de jogos ---
def salvar_historico(jogos, acertos=None, nome_arquivo="dados/historico_jogos.xlsx"):
    estatisticas = []
    for i, jogo in enumerate(jogos):
        stats = calcular_estatisticas_jogo(jogo)
        stats["acertos"] = acertos[i] if acertos else None
        estatisticas.append(stats)

    df = pd.DataFrame(estatisticas)
    if os.path.exists(nome_arquivo):
        df_antigo = pd.read_excel(nome_arquivo)
        df = pd.concat([df_antigo, df], ignore_index=True)

    df.to_excel(nome_arquivo, index=False)
    return df

# --- Exibe o dashboard interativo ---
def mostrar_dashboard():
    """
    Exibe o dashboard com gráficos e tabelas.
    """
    resultados = st.session_state.get("resultados", None)
    estatisticas_file = "dados/estatisticas.xlsx"
    jogos_atuais = st.session_state.get("jogos_atuais", None)

    # Verificar se os dados necessários existem
    if resultados is None or not os.path.exists(estatisticas_file):
        st.warning("Os dados necessários não foram encontrados. Carregue os arquivos primeiro.")
        return

    # Carregar o arquivo Excel com múltiplas planilhas
    estatisticas = pd.ExcelFile(estatisticas_file)

    # Exibir os resultados históricos
    st.subheader("📅 Resultados Históricos")
    st.dataframe(resultados.tail(15))

    # Selecionar a planilha de estatísticas
    st.subheader("📊 Estatísticas")
    st.write("Selecione uma planilha para visualizar os dados estatísticos:")
    planilhas_disponiveis = estatisticas.sheet_names
    planilha_selecionada = st.selectbox("Selecione a planilha:", planilhas_disponiveis)

    # Carregar a planilha selecionada
    df_estatisticas = estatisticas.parse(planilha_selecionada)
    st.write(f"### Dados da Planilha: {planilha_selecionada}")
    st.dataframe(df_estatisticas)

    # Verificar se há colunas suficientes para gráfico
    if len(df_estatisticas.columns) >= 2:
        coluna_x = st.selectbox("Selecione a coluna para o eixo X:", df_estatisticas.columns)
        coluna_y = st.selectbox("Selecione a coluna para o eixo Y:", df_estatisticas.columns)

        try:
            fig = px.bar(df_estatisticas, x=coluna_x, y=coluna_y, title=f"{coluna_y} por {coluna_x}")
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Erro ao gerar o gráfico: {e}")
    else:
        st.warning("A planilha selecionada não contém colunas suficientes para gerar gráficos.")

    # Exibir os jogos atuais
    if jogos_atuais is not None:
        st.subheader("🎰 Jogos Atuais")
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
        mostrar_dashboard()
    
    opcao = st.sidebar.selectbox(
        "Escolha uma opção:",
        ["Geração de Jogos Inteligentes", "Gerar Sugestões com IA"]
    )
    caminho_estatisticas = "dados/estatisticas.xlsx"
    if not os.path.exists(caminho_estatisticas):
        df_vazio = pd.DataFrame(columns=["Data", "Jogo", "Acertos", "Pares", "Ímpares", "Primos", "Múltiplos de 3", "Fibonacci", "Soma"])
        os.makedirs("dados", exist_ok=True)
        df_vazio.to_excel(caminho_estatisticas, index=False)
        estatisticas_dict = mostrar_dashboard(caminho_estatisticas)

        if st.button("Gerar Jogos Inteligentes"):
            jogos_inteligentes = gerar_jogos_inteligentes_v2(n=10, estatisticas_dict=estatisticas_dict)

        st.subheader("🤖 Jogos Gerados")
        for i, jogo in enumerate(jogos_inteligentes, 1):
            st.write(f"Jogo {i}: {jogo}")

        df_historico = salvar_historico(jogos_inteligentes)
        st.download_button("📥 Baixar Jogos Inteligentes", data=df_historico.to_excel(index=False), file_name="jogos_inteligentes.xlsx")

    elif "Gerar Sugestões com IA":
        st.header("📊 Geração com IA baseada em histórico")
        X, df_original = processar_dados("dados/resultados_historicos.xlsx")
        modelo = treinar_modelo(X, X)
        jogos_gerados = gerar_jogos_ml_filtrados(modelo, X.tail(1), n_jogos=10)

        ultimo_resultado = df_original.iloc[-1, 2:17].tolist()
        acertos = avaliar_acertos(jogos_gerados, ultimo_resultado)

        st.subheader("🔢 Jogos Sugeridos com IA")
        for i, jogo in enumerate(jogos_gerados, 1):
            st.write(f"Jogo {i}: {jogo} - Acertos: {acertos[i-1]}")

        df_historico = salvar_historico(jogos_gerados, acertos)
        st.download_button("📥 Baixar Jogos em Excel", data=df_historico.to_excel(index=False), file_name="jogos_sugeridos.xlsx")

    if escolha == "Sobre":
        st.title("📘 Sobre o Projeto Lotofácil 8X")
        st.write("""
        Este aplicativo foi desenvolvido para analisar os resultados da Lotofácil e gerar sugestões inteligentes de jogos utilizando aprendizado de máquina. 
        Ele também apresenta estatísticas e dashboards interativos a partir de arquivos do Excel enviados pelo usuário.
        """)

if __name__ == "__main__":
    main()
