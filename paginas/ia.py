import streamlit as st
import logging
from inteligencia import treinar_modelo_xgb, preparar_dados_para_treinamento, prever_dezenas
from estatisticas import calcular_estatisticas_avancadas

def pagina_ia():
    """
    Página para treinar modelos de IA e prever dezenas.
    """
    st.header("🧠 IA e Previsões")
    st.write("Treine modelos de IA para prever as dezenas mais prováveis.")

    # Carregar dados do estado da sessão
    resultados_df = st.session_state.get("resultados_df", None)
    tabelas = st.session_state.get("tabelas", None)

    if resultados_df is None or tabelas is None:
        st.warning("⚠️ Dados não encontrados. Por favor, carregue os dados na aba 'Dashboard'.")
        return

    # Calcular estatísticas avançadas
    estatisticas = calcular_estatisticas_avancadas(resultados_df, tabelas)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Antes de treinar o modelo, verifique os valores de y
    logging.info(f"Valores únicos em y antes do treinamento: {y.unique()}")

    # Verifique se os valores estão no formato esperado
    classes_esperadas = [0, 1, 2, 3, 4]
    if not set(y.unique()).issubset(classes_esperadas):
        raise ValueError(f"Invalid classes inferred from unique values of y. Expected: {classes_esperadas}, got {y.unique()}")
    
    # Mapeamento dinâmico de classes
    mapeamento_classes = {21: 0, 22: 1, 23: 2, 24: 3, 25: 4}  # Ajuste conforme necessário
    y = y.map(mapeamento_classes)

    # Verifique se o mapeamento foi bem-sucedido
    if y.isnull().any():
        raise ValueError("Erro no mapeamento de classes. Verifique os valores de entrada.")

    # Preparar dados para treinamento
    st.write("🔄 Preparando dados para treinamento...")
    X, y = preparar_dados_para_treinamento(resultados_df, estatisticas)

    if y is None:
        st.error("⚠️ Dados de saída (y) não encontrados. Verifique os dados carregados.")
        return

    # Treinar modelo
    if st.button("Treinar Modelo"):
        modelo = treinar_modelo_xgb(X, y)
        st.success("Modelo treinado com sucesso!")

        # Prever dezenas mais prováveis
        top_n = st.slider("Quantas dezenas mais prováveis deseja prever?", min_value=1, max_value=15, value=10)
        dezenas_previstas = prever_dezenas(modelo, estatisticas, top_n=top_n)
        st.write(f"### Dezenas mais prováveis: {', '.join(dezenas_previstas)}")