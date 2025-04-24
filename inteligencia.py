from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

def treinar_modelo_xgb(df):
    """
    Treina um modelo XGBoost com base nos dados fornecidos.
    
    Args:
        df (pd.DataFrame): DataFrame com as estatísticas das dezenas.
    
    Returns:
        XGBClassifier: Modelo treinado.
    """
    X = df[["Frequência", "Atraso"]]
    y = (df["Dezena"].astype(int) <= 15).astype(int)  # Exemplo: Classificar dezenas <= 15 como 1
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {acc:.2f}")
    
    return model