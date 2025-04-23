import streamlit as st


def mostrar_dashboard_estatistico(df):
    st.title("📊 Dashboard de Estatísticas")
    st.write("Análise completa dos concursos anteriores.")

    col1, col2 = st.columns(2)

    with col1:
        freq = df.drop(columns=["Concurso", "Data", "Dezenas"], errors='ignore').sum().sort_values(ascending=False)
        st.subheader("Frequência das Dezenas")
        st.bar_chart(freq)

    with col2:
        st.subheader("Ocorrência por posição (em construção)")
        st.info("🔧 Essa funcionalidade está em desenvolvimento.")