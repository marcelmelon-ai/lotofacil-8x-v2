import streamlit as st
import pandas as pd
import plotly.express as px
import os

def mostrar_dashboard():
    """
    Exibe o dashboard com gráficos e tabelas.
    """
    # Verificar se os arquivos necessários existem
    if not os.path.exists("dados/resultados_historicos.xlsx") or not os.path.exists("dados/estatisticas.xlsx"):
        raise FileNotFoundError("Os arquivos necessários não foram encontrados.")

    # Carregar os dados
    resultados = pd.read_excel("dados/resultados_historicos.xlsx")
    estatisticas = pd.ExcelFile("dados/estatisticas.xlsx")  # Carregar o arquivo Excel com múltiplas planilhas

    # Verificar se o arquivo de jogos atuais existe
    jogos_atuais = None
    if os.path.exists("dados/jogos_atuais.xlsx"):
        jogos_atuais = pd.read_excel("dados/jogos_atuais.xlsx")

    # Exibir os resultados históricos
    st.write("### Resultados Históricos")
    st.dataframe(resultados)

    # Exibir as estatísticas
    st.write("### Estatísticas")
    st.write("Selecione uma planilha para visualizar os dados estatísticos.")

    # Listar as planilhas disponíveis no arquivo de estatísticas
    planilhas_disponiveis = estatisticas.sheet_names
    planilha_selecionada = st.selectbox("Selecione a planilha:", planilhas_disponiveis)

    # Carregar a planilha selecionada
    df_estatisticas = estatisticas.parse(planilha_selecionada)
    st.write(f"### Dados da Planilha: {planilha_selecionada}")
    st.dataframe(df_estatisticas)

    # Verificar se a coluna "Dezena" e pelo menos uma métrica relevante estão presentes
    if "Dezena" in df_estatisticas.columns:
        metricas_disponiveis = [col for col in df_estatisticas.columns if col != "Dezena"]
        if metricas_disponiveis:
            # Permitir que o usuário escolha a métrica para o gráfico
            metrica_selecionada = st.selectbox("Selecione a métrica para o gráfico:", metricas_disponiveis)

            # Gerar o gráfico com a métrica selecionada
            try:
                st.write(f"### Gráfico: {metrica_selecionada} por Dezena")
                fig = px.bar(df_estatisticas, x="Dezena", y=metrica_selecionada, title=f"{metrica_selecionada} por Dezena")
                st.plotly_chart(fig)
            except ValueError as e:
                st.error(f"Erro ao gerar o gráfico: {e}")
        else:
            st.warning("A planilha selecionada não contém métricas para exibir.")
    else:
        st.warning("A planilha selecionada não contém uma coluna chamada 'Dezena'.")

    # Exibir os jogos atuais, se disponíveis
    if jogos_atuais is not None:
        st.write("### Jogos Atuais")
        st.dataframe(jogos_atuais)