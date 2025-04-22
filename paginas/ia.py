import streamlit as st
from inteligencia import (
    carregar_e_preparar_dados,
    treinar_modelo_xgb,
    treinar_modelo_rf,
    treinar_modelo_mlp,
    prever_dezenas,
    exibir_graficos_desempenho
)
import seaborn as sns
import matplotlib.pyplot as plt

def pagina_ia():
    st.header("🧠 IA e Previsões")

    # Só carrega os dados depois que o usuário estiver nessa página
    dados_ia = carregar_e_preparar_dados()

    modelo_selecionado = st.selectbox("Selecione o modelo:", ['XGBoost', 'Random Forest', 'MLP'])

    if modelo_selecionado == 'XGBoost':
        modelo, accuracy, y_test, y_pred = treinar_modelo_xgb(dados_ia)
    elif modelo_selecionado == 'Random Forest':
        modelo, accuracy, y_test, y_pred = treinar_modelo_rf(dados_ia)
    else:
        modelo, accuracy, y_test, y_pred = treinar_modelo_mlp(dados_ia)

    st.write(f"Acurácia do modelo {modelo_selecionado}: {accuracy:.2%}")
    exibir_graficos_desempenho(y_test, y_pred, modelo_selecionado)

    top_dezenas = prever_dezenas(modelo, dados_ia)
    st.subheader(f"🎯 Dezenas mais prováveis segundo IA ({modelo_selecionado})")
    st.dataframe(top_dezenas[['Dezena', 'Probabilidade']])

    jogo_gerado = sorted(top_dezenas['Dezena'].sample(15).tolist())
    st.success(f"Jogo gerado com IA: {', '.join(jogo_gerado)}")

    fig, ax = plt.subplots()
    sns.heatmap(dados_ia.set_index('Dezena'), annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    st.pyplot(fig)
