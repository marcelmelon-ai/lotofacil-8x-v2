import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
import random

# --- Função para verificar propriedades de um número ---
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

# --- Função para processar os dados ---
def processar_dados(caminho_excel):
    df = pd.read_excel(caminho_excel)
    df = df.dropna()

    # Seleciona as colunas com as dezenas (assumimos da coluna 2 até 16)
    dezenas = df.iloc[:, 2:17].astype(int)

    # Cria uma matriz binária com 25 colunas
    jogos_binarios = []
    for _, row in dezenas.iterrows():
        binario = [1 if i in row.values else 0 for i in range(1, 26)]
        jogos_binarios.append(binario)

    jogos_binarios_df = pd.DataFrame(jogos_binarios, columns=[f'D{i}' for i in range(1, 26)])
    return jogos_binarios_df, df

# --- Função para treinar o modelo ---
def treinar_modelo(X, y):
    modelo_rf = RandomForestClassifier(n_estimators=200, random_state=42)
    modelo = MultiOutputClassifier(modelo_rf)
    modelo.fit(X, y)
    return modelo

# --- Função para gerar jogos ---
def gerar_jogos(modelo, X_referencia, n_jogos=10):
    probabilidades = modelo.predict_proba(X_referencia)

    # Calcula a média das probabilidades previstas para cada dezena (coluna)
    probs_medias = []
    for i in range(25):
        classe_1_probs = [p[1] for p in probabilidades[i]]  # probabilidade de "1"
        media = np.mean(classe_1_probs)
        probs_medias.append((i + 1, media))

    # Ordena pela maior probabilidade e seleciona os 15 mais prováveis
    dezenas_ordenadas = sorted(probs_medias, key=lambda x: x[1], reverse=True)

    jogos = []
    for _ in range(n_jogos):
        jogo = sorted(random.sample([d[0] for d in dezenas_ordenadas[:20]], 15))  # sorteia 15 entre os 20 mais prováveis
        jogos.append(jogo)

    return jogos

# --- Função para avaliar acertos ---
def avaliar_acertos(jogos, resultado_real):
    acertos = []
    for jogo in jogos:
        acerto = len(set(jogo).intersection(set(resultado_real)))
        acertos.append(acerto)
    return acertos
