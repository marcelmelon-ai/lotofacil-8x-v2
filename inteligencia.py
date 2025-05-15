import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
import streamlit as st
import plotly.express as px

# Função para processar os dados
def processar_dados(resultados_path, estatisticas_path, jogos_atuais_path):
    """
    Processa os dados dos arquivos Excel e extrai métricas.
    """
    # Carregar os arquivos Excel
    resultados = pd.read_excel(resultados_path)
    estatisticas = pd.read_excel(estatisticas_path)
    jogos_atuais = pd.read_excel(jogos_atuais_path)

    # Transformar cada concurso em vetor binário (25 colunas: 1 para presente, 0 para ausente)
    jogos_binarios = pd.DataFrame(
        [[1 if i in row[2:].values else 0 for i in range(1, 26)] for _, row in resultados.iterrows()],
        columns=[f"Dezena_{i}" for i in range(1, 26)]
    )

    # Adicionar métricas (pares/ímpares, primos, múltiplos de 3, Fibonacci, soma das dezenas)
    resultados["Pares"] = jogos_binarios.apply(lambda row: sum([1 for i in range(1, 26) if i % 2 == 0 and row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Ímpares"] = jogos_binarios.apply(lambda row: sum([1 for i in range(1, 26) if i % 2 != 0 and row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Primos"] = jogos_binarios.apply(lambda row: sum([1 for i in [2, 3, 5, 7, 11, 13, 17, 19, 23] if row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Múltiplos_3"] = jogos_binarios.apply(lambda row: sum([1 for i in range(1, 26) if i % 3 == 0 and row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Fibonacci"] = jogos_binarios.apply(lambda row: sum([1 for i in [1, 2, 3, 5, 8, 13, 21] if row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Soma"] = jogos_binarios.apply(lambda row: sum([i for i in range(1, 26) if row[f"Dezena_{i}"] == 1]), axis=1)

    return jogos_binarios, resultados, estatisticas, jogos_atuais

# Função para treinar o modelo
def treinar_modelo(X, y):
    """
    Treina um modelo RandomForestClassifier para prever os 15 números de um jogo.
    """
    modelo = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
    modelo.fit(X, y)
    return modelo

# Função para gerar jogos
def gerar_jogos(modelo, X, num_jogos=10):
    """
    Gera novos jogos com base nas probabilidades previstas pelo modelo.
    """
    probabilidades = modelo.predict_proba(X)
    jogos = []

    for _ in range(num_jogos):
        jogo = []
        for i, prob in enumerate(probabilidades):
            if prob[1] > 0.5:  # Ajuste o limiar conforme necessário
                jogo.append(i + 1)
        if len(jogo) >= 15:
            jogo = sorted(jogo[:15])
        else:
            restantes = [i for i in range(1, 26) if i not in jogo]
            jogo.extend(sorted(np.random.choice(restantes, 15 - len(jogo), replace=False)))
        jogos.append(jogo)

    return jogos

# Função para avaliar os acertos
def avaliar_acertos(jogos_gerados, ultimo_resultado):
    """
    Avalia os acertos dos jogos gerados em relação ao último resultado real.
    """
    acertos = [len(set(jogo) & set(ultimo_resultado)) for jogo in jogos_gerados]
    return acertos

# Função para atualizar o dashboard
def atualizar_dashboard(jogos_gerados, acertos, resultados):
    """
    Atualiza o dashboard interativo com os jogos gerados e estatísticas.
    """
    st.title("Lotofácil - Dashboard de Resultados")
    
    # Exibir os jogos gerados
    st.write("### Jogos Gerados")
    for i, jogo in enumerate(jogos_gerados, 1):
        st.write(f"Jogo {i}: {jogo}")

    # Exibir os acertos
    st.write("### Acertos por Jogo")
    st.bar_chart(acertos)

    # Exibir gráficos de métricas
    st.write("### Estatísticas dos Concursos")
    fig = px.histogram(resultados, x="Pares", title="Distribuição de Pares")
    st.plotly_chart(fig)
    fig = px.histogram(resultados, x="Primos", title="Distribuição de Primos")
    st.plotly_chart(fig)