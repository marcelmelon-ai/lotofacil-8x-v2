# inteligencia.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split

# Funções auxiliares
def vetorizar_jogo(jogo):
    vetor = [1 if i + 1 in jogo else 0 for i in range(25)]
    return vetor

def processar_dados(path_excel='data/lotofacil.xlsx'):
    df = pd.read_excel(path_excel)
    
    # Espera-se que a coluna 'dezenas' contenha lista com os 15 números do concurso
    df['vetor'] = df['dezenas'].apply(vetorizar_jogo)
    
    X = np.array(df['vetor'].tolist()[:-1])  # todos menos o último
    Y = np.array(df['vetor'].tolist()[1:])   # target = próximo concurso
    
    return X, Y, df

def treinar_modelo(X, Y):
    model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
    model.fit(X, Y)
    return model

def gerar_jogos(modelo, ultimo_jogo, n=10):
    jogos = []
    for _ in range(n):
        probs = modelo.predict_proba([ultimo_jogo])
        dezenas_prob = [p[1] for p in probs[0]]  # prob de estar presente (1)
        indices = np.argsort(dezenas_prob)[-15:]  # pega as 15 maiores
        jogo = sorted([i + 1 for i in indices])
        jogos.append(jogo)
    return jogos

def avaliar_acertos(jogos_gerados, ultimo_resultado):
    acertos = []
    for jogo in jogos_gerados:
        acertos.append(len(set(jogo) & set(ultimo_resultado)))
    return acertos
