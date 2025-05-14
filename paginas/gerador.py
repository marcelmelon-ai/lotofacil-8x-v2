import pandas as pd
import streamlit as st
import random
import logging
import numpy as np
from models import gerar_jogos_otimizados, gerar_jogos_simples, gerar_jogos_ia, gerar_jogos_com_fechamento
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

def gerar_jogo(modelo, frequencia, num_jogos=10):
    """
    Gera jogos inteligentes com base no modelo treinado e na frequência das dezenas.

    Args:
        modelo: Modelo treinado de IA.
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    probabilidades = modelo.predict_proba(frequencia[["Frequência"]])[:, 1]
    frequencia["Probabilidade"] = probabilidades
    dezenas_ordenadas = frequencia.sort_values(by="Probabilidade", ascending=False)["Dezena"].tolist()

    jogos = []
    for _ in range(num_jogos):
        jogo = sorted(random.sample(dezenas_ordenadas[:20], 15))  # Seleciona as 20 mais prováveis
        jogos.append(jogo)

    return jogos

def gerar_jogos_simples(frequencia, num_jogos=10):
    """
    Gera jogos simples com base na frequência das dezenas.

    Args:
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    dezenas_ordenadas = frequencia.sort_values(by="Frequência", ascending=False)["Dezena"].tolist()
    jogos = [sorted(random.sample(dezenas_ordenadas[:20], 15)) for _ in range(num_jogos)]
    return jogos

def gerar_jogos_ia(modelo, frequencia, num_jogos=10):
    """
    Gera jogos inteligentes com base no modelo treinado.

    Args:
        modelo: Modelo treinado de IA.
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    probabilidades = modelo.predict_proba(frequencia[["Frequência"]])[:, 1]
    frequencia["Probabilidade"] = probabilidades
    dezenas_ordenadas = frequencia.sort_values(by="Probabilidade", ascending=False)["Dezena"].tolist()
    jogos = [sorted(random.sample(dezenas_ordenadas[:20], 15)) for _ in range(num_jogos)]
    return jogos

def gerar_jogos_com_fechamento(frequencia, num_jogos=10):
    """
    Gera jogos com fechamento baseado nas dezenas mais frequentes.

    Args:
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados com fechamento.
    """
    dezenas_ordenadas = frequencia.sort_values(by="Frequência", ascending=False)["Dezena"].tolist()

    jogos = []
    for _ in range(num_jogos):
        jogo = sorted(random.sample(dezenas_ordenadas[:20], 15))  # Seleciona as 20 mais frequentes
        jogos.append(jogo)

    return jogos

def pagina_gerador():
    """
    Página para gerar jogos otimizados.
    """
    st.header("🎲 Gerador de Jogos Inteligentes")
    st.write("Crie combinações de jogos otimizados com base em estatísticas e modelos de IA.")

    # Simular dados de frequência
    frequencia = pd.DataFrame({
        "Dezena": [i for i in range(1, 25)],
        "Frequência": [100 - i for i in range(1, 25)]  # Exemplo de frequência decrescente
    })

    # Exibir tabela de frequência
    st.write("Frequência das dezenas:")
    st.dataframe(frequencia)

    # Gerar jogos
    num_jogos = st.slider("Número de jogos a gerar:", min_value=1, max_value=20, value=10)
    if st.button("Gerar Jogos"):
        jogos = gerar_jogos_otimizados(frequencia, num_jogos=num_jogos)
        st.write("Jogos Gerados:")
        for i, jogo in enumerate(jogos, 1):
            st.write(f"Jogo {i}: {jogo}")

def pagina_gerador():
    st.header("🎲 Gerador de Jogos Inteligentes")
    st.write("Crie combinações de jogos otimizados com base em estatísticas e modelos de IA.")
    
    frequencia = pd.DataFrame({
        "Dezena": [i for i in range(1, 25)],
        "Frequência": [100 - i for i in range(1, 25)]
    })