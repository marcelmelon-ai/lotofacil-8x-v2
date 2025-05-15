import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import random

def treinar_modelo():
    """
    Treina um modelo de IA com base nos dados históricos.
    """
    dados = pd.read_excel("dados/resultados_historicos.xlsx")
    X = dados.iloc[:, 2:17]  # Colunas das dezenas
    y = dados["Soma das dezenas"]  # Exemplo de rótulo

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    return modelo

def gerar_sugestoes(num_jogos=10):
    """
    Gera sugestões de apostas com base no modelo treinado.
    """
    modelo = treinar_modelo()
    frequencias = pd.read_excel("dados/estatisticas.xlsx")["Frequência"]
    dezenas = list(range(1, 26))
    probabilidades = modelo.predict_proba([[f] for f in frequencias])[:, 1]
    dezenas_prob = sorted(zip(dezenas, probabilidades), key=lambda x: x[1], reverse=True)

    jogos = []
    for _ in range(num_jogos):
        jogo = sorted(random.sample([d[0] for d in dezenas_prob[:20]], 15))
        jogos.append(jogo)
    return jogos