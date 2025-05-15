from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

def treinar_modelo_xgb(X, y):
    """
    Treina um modelo XGBoost com os dados fornecidos.

    Args:
        X (list): Dados de entrada.
        y (list): Rótulos de saída.

    Returns:
        XGBClassifier: Modelo treinado.
    """
    model = XGBClassifier(eval_metric="logloss")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {acc:.2f}")
    return model

def prever_dezenas(model, frequencia, top_n=15):
    """
    Faz previsões com base no modelo treinado e na frequência fornecida.

    Args:
        model (XGBClassifier): Modelo treinado.
        frequencia (list): Lista de frequências das dezenas.
        top_n (int): Número de dezenas mais prováveis a serem retornadas.

    Returns:
        list: Lista das dezenas mais prováveis.
    """
    probabilidades = model.predict_proba([[f] for f in frequencia])[:, 1]
    dezenas_probabilidades = list(zip(range(1, len(frequencia) + 1), probabilidades))
    dezenas_ordenadas = sorted(dezenas_probabilidades, key=lambda x: x[1], reverse=True)[:top_n]
    return [dezena for dezena, _ in dezenas_ordenadas]