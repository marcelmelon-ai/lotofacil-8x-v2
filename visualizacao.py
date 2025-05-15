import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar_dashboard():
    """
    Exibe o dashboard com gráficos e tabelas.
    """
    resultados = pd.read_excel("dados/resultados_historicos.xlsx")
    estatisticas = pd.read_excel("dados/estatisticas.xlsx")

    st.write("### Resultados Históricos")
    st.dataframe(resultados)

    st.write("### Estatísticas")
    st.dataframe(estatisticas)

    # Gráfico de frequência
    st.write("### Frequência das Dezenas")
    fig = px.bar(estatisticas, x="Dezena", y="Frequência", title="Frequência das Dezenas")
    st.plotly_chart(fig)