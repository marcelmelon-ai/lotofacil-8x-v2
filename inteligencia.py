from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import pandas as pd

def treinar_modelo_xgb(X, y):
    """
    Treina um modelo XGBoost com os dados fornecidos.

    Args:
        X (pd.DataFrame): Dados de entrada.
        y (pd.Series): Rótulos de saída.

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

def preparar_dados_para_treinamento(resultados_df, estatisticas):
    """
    Prepara os dados para treinamento de modelos de Machine Learning.

    Args:
        resultados_df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
        estatisticas (dict): Dicionário com estatísticas calculadas.

    Returns:
        tuple: Dados de entrada (X) e saída (y) para treinamento.
    """
    # Selecionar as colunas de dezenas
    dezenas_cols = [col for col in resultados_df.columns if col.startswith("D")]

    # Criar o DataFrame de entrada (X)
    X = resultados_df[dezenas_cols].copy()

    # Adicionar estatísticas como features
    if "Frequencia" in estatisticas:
        frequencia = estatisticas["Frequencia"]
        X = X.merge(frequencia, left_on="D1", right_on="Dezena", how="left")

    # Criar a saída (y) com base nos resultados futuros
    y = resultados_df["Resultado"] if "Resultado" in resultados_df.columns else None

    return X, y

def prever_dezenas(model, estatisticas, top_n=15):
    """
    Faz previsões com base no modelo treinado e nas estatísticas fornecidas.

    Args:
        model (XGBClassifier): Modelo treinado.
        estatisticas (dict): Dicionário com estatísticas calculadas.
        top_n (int): Número de dezenas mais prováveis a serem retornadas.

    Returns:
        list: Lista das dezenas mais prováveis.
    """
    if "Frequencia" not in estatisticas:
        raise ValueError("Estatísticas de frequência não encontradas.")

    # Usar a frequência como base para prever as dezenas
    frequencia = estatisticas["Frequencia"]
    frequencia["Probabilidade"] = model.predict_proba(frequencia[["Frequência"]])[:, 1]
    dezenas_ordenadas = frequencia.sort_values(by="Probabilidade", ascending=False)["Dezena"].head(top_n).tolist()

    return dezenas_ordenadas