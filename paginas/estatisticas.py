import streamlit as st
from ajustes import carregar_dados_excel
from estatisticas import calcular_frequencia

def pagina_estatisticas():
    """
    Página para exibir estatísticas dos resultados da Lotofácil.
    """
    st.subheader("📊 Estatísticas dos Resultados")
    st.write("Carregue os dados para visualizar as estatísticas.")

    # Carregar arquivo Excel
    arquivo = st.file_uploader("Envie o arquivo de resultados (Excel)", type=["xlsx"])
    if arquivo is not None:
        df = carregar_dados_excel(arquivo)
        if df.empty:
            st.error("O arquivo enviado está vazio ou inválido.")
            return

        # Calcular frequência
        frequencia = calcular_frequencia(df)
        st.session_state["frequencia"] = frequencia

        # Exibir tabela de frequência
        st.write("### Frequência das Dezenas")
        st.dataframe(frequencia)

        # Exibir gráfico
        st.bar_chart(frequencia.set_index("Dezena")["Frequência"])
