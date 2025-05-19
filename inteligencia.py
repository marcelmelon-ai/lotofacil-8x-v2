import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
import streamlit as st
import plotly.express as px
import os

# Função para processar os dados
def processar_dados(resultados_path="dados/resultados_historicos.xlsx", 
                    estatisticas_path="dados/estatisticas.xlsx", 
                    jogos_atuais_path="dados/jogos_atuais.xlsx"):
    """
    Processa os dados dos arquivos Excel e extrai métricas.
    """
    # Verifica se os arquivos existem
    if not os.path.exists(resultados_path):
        raise FileNotFoundError("Arquivo de resultados históricos não encontrado.")
    if not os.path.exists(estatisticas_path):
        raise FileNotFoundError("Arquivo de estatísticas não encontrado.")
    if not os.path.exists(jogos_atuais_path):
        raise FileNotFoundError("Arquivo de jogos atuais não encontrado.")

    # Carregar os arquivos Excel
    resultados = pd.read_excel(resultados_path)
    estatisticas = pd.read_excel(estatisticas_path)
    jogos_atuais = pd.read_excel(jogos_atuais_path)

    # Transformar cada concurso em vetor binário (25 colunas: 1 para presente, 0 para ausente)
    jogos_binarios = pd.DataFrame(
        [[1 if i in row[2:].values else 0 for i in range(1, 26)] for _, row in resultados.iterrows()],
        columns=[f"Dezena_{i}" for i in range(1, 26)]
    )

    # Adicionar métricas ao DataFrame original
    resultados["Pares"] = jogos_binarios.apply(lambda row: sum([1 for i in range(1, 26) if i % 2 == 0 and row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Ímpares"] = jogos_binarios.apply(lambda row: sum([1 for i in range(1, 26) if i % 2 != 0 and row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Primos"] = jogos_binarios.apply(lambda row: sum([1 for i in [2, 3, 5, 7, 11, 13, 17, 19, 23] if row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Múltiplos_3"] = jogos_binarios.apply(lambda row: sum([1 for i in range(1, 26) if i % 3 == 0 and row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Fibonacci"] = jogos_binarios.apply(lambda row: sum([1 for i in [1, 2, 3, 5, 8, 13, 21] if row[f"Dezena_{i}"] == 1]), axis=1)
    resultados["Soma"] = jogos_binarios.apply(lambda row: sum([i for i in range(1, 26) if row[f"Dezena_{i}"] == 1]), axis=1)

    return jogos_binarios, resultados, estatisticas, jogos_atuais

# Função para treinar o modelo
def treinar_modelo(X, y):
    modelo = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
    modelo.fit(X, y)
    return modelo

# Função para gerar jogos
def gerar_jogos_ml_filtrados(modelo, X_base, n=10, ultimo_resultado=None):
    candidatos = gerar_jogos_inteligentes_v2(n*5, ultimo_resultado)  # gera 5x mais
    jogos_bin = pd.DataFrame([[1 if i in jogo else 0 for i in range(1, 26)] for jogo in candidatos],
                             columns=[f'Dezena_{i}' for i in range(1, 26)])
    probs = modelo.predict_proba(jogos_bin)
    scores = [np.mean([p[1] for p in jogo_probs]) for jogo_probs in probs]
    melhores_idx = np.argsort(scores)[-n:]
    return [candidatos[i] for i in melhores_idx]

import random

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5)+1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    x1 = 5*n*n + 4
    x2 = 5*n*n - 4
    return int(x1**0.5)**2 == x1 or int(x2**0.5)**2 == x2

def gerar_jogos_inteligentes_v2(n=10, ultimo_resultado=None):
    jogos = []
    tentativas = 0
    fibonacci_set = {1, 2, 3, 5, 8, 13, 21}
    primos_set = {2, 3, 5, 7, 11, 13, 17, 19, 23}

    while len(jogos) < n and tentativas < 10000:
        jogo = sorted(random.sample(range(1, 26), 15))
        pares = sum(1 for d in jogo if d % 2 == 0)
        impares = 15 - pares
        primos = sum(1 for d in jogo if d in primos_set)
        mult3 = sum(1 for d in jogo if d % 3 == 0)
        fibos = sum(1 for d in jogo if d in fibonacci_set)
        soma = sum(jogo)
        repetidas = len(set(jogo) & set(ultimo_resultado)) if ultimo_resultado else 0

        if (
            6 <= pares <= 9 and
            6 <= impares <= 9 and
            4 <= primos <= 7 and
            4 <= mult3 <= 6 and
            3 <= fibos <= 5 and
            165 <= soma <= 224 and
            8 <= repetidas <= 11
        ):
            jogos.append(jogo)
        tentativas += 1

    return jogos

# Função para avaliar os acertos
def avaliar_acertos(jogos_gerados, ultimo_resultado):
    return [len(set(jogo) & set(ultimo_resultado)) for jogo in jogos_gerados]

# Função para atualizar o dashboard
def atualizar_dashboard(jogos_gerados, acertos, resultados):
    st.title("Lotofácil - Dashboard de Resultados")
    
    st.write("### Jogos Gerados")
    for i, jogo in enumerate(jogos_gerados, 1):
        st.write(f"Jogo {i}: {jogo}")

    st.write("### Acertos por Jogo")
    st.bar_chart(acertos)

    st.write("### Estatísticas dos Concursos")
    fig = px.histogram(resultados, x="Pares", title="Distribuição de Pares")
    st.plotly_chart(fig)
    fig = px.histogram(resultados, x="Primos", title="Distribuição de Primos")
    st.plotly_chart(fig)

