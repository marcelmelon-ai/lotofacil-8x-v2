from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

def treinar_modelo_xgb(X, y):
    """
    Treina um modelo XGBoost com os dados fornecidos.
    
    Args:
        X (pd.DataFrame): Dados de entrada.
        y (pd.Series): Rótulos de saída.
    
    Returns:
        XGBClassifier: Modelo treinado.
    """
    # Removido o parâmetro `use_label_encoder` para evitar avisos
    model = XGBClassifier(eval_metric="logloss")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {acc:.2f}")
    return model

def prever_dezenas(model, X):
    """
    Faz previsões com base no modelo treinado.
    
    Args:
        model (XGBClassifier): Modelo treinado.
        X (pd.DataFrame): Dados de entrada para previsão.
    
    Returns:
        np.ndarray: Previsões do modelo.
    """
    return model.predict(X)