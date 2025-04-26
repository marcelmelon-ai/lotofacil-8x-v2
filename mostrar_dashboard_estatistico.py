import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def mostrar_dashboard_estatistico(df):
    """
    Exibe o dashboard estatístico com gráficos interativos baseados nos dados fornecidos.

    Args:
        df (pd.DataFrame): DataFrame com os resultados da Lotofácil.
    """
    st.title("📊 Dashboard de Estatísticas Interativo")
    st.write("Análise completa e interativa dos concursos anteriores da Lotofácil.")

    # Verificar se o DataFrame está vazio
    if df.empty:
        st.warning("⚠️ O DataFrame está vazio. Por favor, carregue os dados corretamente.")
        return

    # Calcular a frequência das dezenas
    try:
        freq = df.filter(like="D").apply(pd.Series.value_counts).sum(axis=1).sort_values(ascending=False)
        freq_df = freq.reset_index()
        freq_df.columns = ["Dezena", "Frequência"]
        freq_df["Dezena"] = freq_df["Dezena"].astype(int).astype(str).str.zfill(2)
    except Exception as e:
        st.error(f"Erro ao calcular a frequência das dezenas: {e}")
        return

    # Dividir a página em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de barras interativo da frequência das dezenas
        st.subheader("Frequência das Dezenas")
        fig_bar = px.bar(
            freq_df,
            x="Dezena",
            y="Frequência",
            title="Frequência das Dezenas",
            labels={"Dezena": "Dezena", "Frequência": "Frequência"},
            text="Frequência",
        )
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Gráfico de pizza para proporção de dezenas pares e ímpares
        st.subheader("Proporção de Pares e Ímpares")
        pares = freq_df[freq_df["Dezena"].astype(int) % 2 == 0]["Frequência"].sum()
        impares = freq_df[freq_df["Dezena"].astype(int) % 2 != 0]["Frequência"].sum()
        fig_pie = px.pie(
            names=["Pares", "Ímpares"],
            values=[pares, impares],
            title="Proporção de Pares e Ímpares",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Gráfico de linha para exibir a soma das dezenas por concurso
    try:
        st.subheader("Soma das Dezenas por Concurso")
        df["Soma"] = df.filter(like="D").sum(axis=1)
        fig_line = px.line(
            df,
            y="Soma",
            title="Soma das Dezenas por Concurso",
            labels={"index": "Concurso", "Soma": "Soma das Dezenas"},
        )
        st.plotly_chart(fig_line, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao calcular a soma das dezenas: {e}")

    # Tabela interativa com os dados
    st.subheader("Tabela de Frequência das Dezenas")
    st.dataframe(freq_df)

    # Adicionar filtros interativos
    st.subheader("Filtrar Dezenas")
    dezenas_selecionadas = st.multiselect(
        "Selecione as dezenas para visualizar:",
        options=freq_df["Dezena"],
        default=freq_df["Dezena"].head(10),
    )
    if dezenas_selecionadas:
        filtro_df = freq_df[freq_df["Dezena"].isin(dezenas_selecionadas)]
        st.write(f"Frequência das dezenas selecionadas:")
        st.dataframe(filtro_df)
        fig_filtered = px.bar(
            filtro_df,
            x="Dezena",
            y="Frequência",
            title="Frequência das Dezenas Selecionadas",
            labels={"Dezena": "Dezena", "Frequência": "Frequência"},
            text="Frequência",
        )
        fig_filtered.update_traces(textposition="outside")
        st.plotly_chart(fig_filtered, use_container_width=True)