import streamlit as st
from inteligencia import processar_dados, treinar_modelo, gerar_jogos, avaliar_acertos
from visualizacao import mostrar_dashboard
import pandas as pd
import os
from sklearn.model_selection import train_test_split

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
        st.write("Carregue os arquivos necessários para continuar.")

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

                # Corrigir tipos incompatíveis para Streamlit
                if "Data Sorteio" in resultados.columns:
                    resultados["Data Sorteio"] = resultados["Data Sorteio"].astype(str)

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
            # Processar os dados
            filepath = "dados/resultados_historicos.xlsx"
            jogos_binarios, df = processar_dados(filepath)

            # Dividir os dados em treino e teste
            X = jogos_binarios
            y = jogos_binarios.iloc[:, :15]  # As primeiras 15 colunas são o target
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Treinar o modelo
            modelo = treinar_modelo(X_train, y_train)

            # Gerar novos jogos
            jogos_gerados = gerar_jogos(modelo, X_test)

            # Avaliar os acertos
            ultimo_resultado = df.iloc[-1, 2:17].values.tolist()  # Último resultado real
            acertos = avaliar_acertos(jogos_gerados, ultimo_resultado)

            # Exibir os jogos gerados
            st.write("### Jogos Gerados")
            for i, jogo in enumerate(jogos_gerados, 1):
                st.write(f"Jogo {i}: {jogo}")

            # Exibir os acertos
            st.write("### Acertos por Jogo")
            st.bar_chart(acertos)
        except FileNotFoundError:
            st.error("Os arquivos necessários não foram encontrados. Por favor, carregue os arquivos na aba 'Carregar Arquivos'.")
        except Exception as e:
            st.error(f"Erro ao gerar sugestões: {e}")

    elif escolha == "Sobre":
        st.title("ℹ️ Sobre o Lotofácil 8X")
        st.markdown("""
        Este aplicativo utiliza **Inteligência Artificial** e **estatísticas** para analisar e gerar combinações prováveis para a Lotofácil.
        Desenvolvido para uso pessoal.
        """)

if __name__ == "__main__":
    main()