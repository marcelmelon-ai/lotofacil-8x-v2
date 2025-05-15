import streamlit as st
from inteligencia import processar_dados, treinar_modelo, gerar_jogos, avaliar_acertos, atualizar_dashboard
import pandas as pd
import os
from sklearn.model_selection import train_test_split

def main():
    st.set_page_config(page_title="Lotofácil 8X", layout="wide")
    st.sidebar.title("🎯 Lotofácil 8X")

    # Menu de navegação
    escolha = st.sidebar.radio(
        "Navegação",
        ["Carregar Arquivos", "Gerar Sugestões", "Sobre"]
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
                # Criar o diretório 'dados' se não existir
                os.makedirs("dados", exist_ok=True)

                # Salvar os arquivos carregados no diretório 'dados'
                pd.read_excel(resultados_file).to_excel("dados/resultados_historicos.xlsx", index=False)
                pd.read_excel(estatisticas_file).to_excel("dados/estatisticas.xlsx", index=False)
                pd.read_excel(jogos_atuais_file).to_excel("dados/jogos_atuais.xlsx", index=False)

                st.success("Arquivos carregados com sucesso!")
                st.write("### Pré-visualização dos Resultados Históricos:")
                st.dataframe(pd.read_excel("dados/resultados_historicos.xlsx").head())
                st.write("### Pré-visualização das Estatísticas:")
                st.dataframe(pd.read_excel("dados/estatisticas.xlsx").head())
                st.write("### Pré-visualização dos Jogos Atuais:")
                st.dataframe(pd.read_excel("dados/jogos_atuais.xlsx").head())
            except Exception as e:
                st.error(f"Erro ao carregar os arquivos: {e}")

    elif escolha == "Gerar Sugestões":
        st.title("🔮 Sugestões de Apostas")
        try:
            # Caminhos dos arquivos
            resultados_path = "dados/resultados_historicos.xlsx"
            estatisticas_path = "dados/estatisticas.xlsx"
            jogos_atuais_path = "dados/jogos_atuais.xlsx"

            # Processar os dados
            jogos_binarios, resultados, estatisticas, jogos_atuais = processar_dados(
                resultados_path, estatisticas_path, jogos_atuais_path
            )

            # Dividir os dados em treino e teste
            X = jogos_binarios
            y = jogos_binarios.iloc[:, :15]  # As primeiras 15 colunas são o target
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Treinar o modelo
            modelo = treinar_modelo(X_train, y_train)

            # Gerar novos jogos
            jogos_gerados = gerar_jogos(modelo, X_test)

            # Avaliar os acertos
            ultimo_resultado = resultados.iloc[-1, 2:17].values.tolist()  # Último resultado real
            acertos = avaliar_acertos(jogos_gerados, ultimo_resultado)

            # Atualizar o dashboard
            atualizar_dashboard(jogos_gerados, acertos, resultados)
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