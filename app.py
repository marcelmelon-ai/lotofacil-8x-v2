import streamlit as st
from pipeline import processar_dados_diarios
from inteligencia import treinar_modelo, gerar_sugestoes
from visualizacao import mostrar_dashboard
import pandas as pd
import os

def main():
    st.set_page_config(page_title="Lotofácil 8X", layout="wide")
    st.sidebar.title("🎯 Lotofácil 8X")

    # Menu lateral
    escolha = st.sidebar.radio(
        "Navegação",
        ["Carregar Arquivos", "Dashboard", "Gerar Sugestões", "Sobre"]
    )

    if escolha == "Carregar Arquivos":
        st.title("📂 Carregar Arquivos Excel")
        st.write("Carregue os arquivos de resultados, estatísticas e jogos atuais para continuar.")

        # Upload de arquivos
        resultados_file = st.file_uploader("Envie o arquivo de resultados históricos (Excel)", type=["xlsx"])
        estatisticas_file = st.file_uploader("Envie o arquivo de estatísticas (Excel)", type=["xlsx"])
        jogos_atuais_file = st.file_uploader("Envie o arquivo de jogos atuais (Excel)", type=["xlsx"])

        if resultados_file and estatisticas_file and jogos_atuais_file:
            try:
                # Ler os arquivos carregados
                resultados = pd.read_excel(resultados_file)
                estatisticas = pd.read_excel(estatisticas_file)
                jogos_atuais = pd.read_excel(jogos_atuais_file)

                # Salvar os arquivos carregados no diretório 'dados'
                os.makedirs("dados", exist_ok=True)
                resultados.to_excel("dados/resultados_historicos.xlsx", index=False)
                estatisticas.to_excel("dados/estatisticas.xlsx", index=False)
                jogos_atuais.to_excel("dados/jogos_atuais.xlsx", index=False)

                # Salvar no estado da sessão
                st.session_state["resultados"] = resultados
                st.session_state["estatisticas"] = estatisticas
                st.session_state["jogos_atuais"] = jogos_atuais

                st.success("Arquivos carregados e salvos com sucesso!")
                st.write("### Pré-visualização dos Resultados:")
                st.dataframe(resultados.head())
                st.write("### Pré-visualização das Estatísticas:")
                st.dataframe(estatisticas.head())
                st.write("### Pré-visualização dos Jogos Atuais:")
                st.dataframe(jogos_atuais.head())
            except Exception as e:
                st.error(f"Erro ao processar os arquivos: {e}")
        else:
            st.info("Por favor, carregue todos os arquivos para continuar.")

    elif escolha == "Dashboard":
        st.title("📊 Dashboard de Estatísticas")
        try:
            mostrar_dashboard()
        except FileNotFoundError:
            st.error("Os arquivos necessários não foram encontrados. Por favor, carregue os arquivos na aba 'Carregar Arquivos'.")

    elif escolha == "Gerar Sugestões":
        st.title("🔮 Sugestões de Apostas")
        try:
            processar_dados_diarios()
            sugestoes = gerar_sugestoes()
            st.write("Sugestões de Apostas:")
            for i, sugestao in enumerate(sugestoes, 1):
                st.write(f"Jogo {i}: {sugestao}")
        except FileNotFoundError:
            st.error("Os arquivos necessários não foram encontrados. Por favor, carregue os arquivos na aba 'Carregar Arquivos'.")

    elif escolha == "Sobre":
        st.title("ℹ️ Sobre o Lotofácil 8X")
        st.markdown("""
        Este aplicativo utiliza **Inteligência Artificial** e **estatísticas** para analisar e gerar combinações prováveis para a Lotofácil.
        Desenvolvido para uso pessoal.
        """)

if __name__ == "__main__":
    main()