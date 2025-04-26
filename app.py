import streamlit as st
from estatisticas import carregar_tabelas_numeromania, carregar_dados_excel, calcular_frequencia
from inteligencia import treinar_modelo_xgb, prever_dezenas
from ajustes import preprocessar_dados
from models import gerar_jogo
from paginas.gerador import gerar_jogo, gerar_jogos_com_fechamento
from paginas.ia import pagina_ia
from paginas.sobre import pagina_sobre
from paginas.dados_online import pagina_dados_online
from mostrar_dashboard_estatistico import mostrar_dashboard_estatistico

def main():
    """
    Função principal para executar o aplicativo Streamlit.
    """
    st.set_page_config(page_title="Lotofácil 8X", layout="wide")
    st.sidebar.title("🎯 Lotofácil 8X")
    
    # Menu lateral
    escolha = st.sidebar.radio(
        "Navegação",
        ["Dashboard", "Gerar Jogos", "Simulação de Jogos", "Sobre"]
    )

    # Carregar os dados dos arquivos Excel
    st.sidebar.write("🔄 Carregando dados...")
    resultados_path = "data/resultados_lotofacil.xlsx"
    tabelas_path = "data/tabelas_numeromania.xlsx"

    resultados_df = carregar_dados_excel(resultados_path)
    tabelas = carregar_tabelas_numeromania(tabelas_path)

    if resultados_df.empty or not tabelas:
        st.error("Erro ao carregar os dados. Verifique os arquivos Excel.")
        return

    # Calcular frequência das dezenas
    frequencia = calcular_frequencia(resultados_df)

    if escolha == "Dashboard":
        st.title("📊 Dashboard de Estatísticas")
        st.write("Análise completa dos concursos anteriores.")

         # Exibir o dashboard
        mostrar_dashboard_estatistico(resultados_df)

        # Exibir frequência das dezenas
        st.subheader("Frequência das Dezenas")
        st.bar_chart(frequencia.set_index("Dezena")["Frequência"])

        # Exibir tabelas do arquivo 'Tabelas_numeromania.xlsx'
        st.subheader("Estatísticas Avançadas")
        for nome, tabela in tabelas.items():
            st.write(f"### {nome}")
            st.dataframe(tabela)

    elif escolha == "Gerar Jogos":
        st.title("🎲 Gerar Jogos Inteligentes")
        st.write("Crie combinações de jogos otimizados com base em estatísticas e modelos de IA.")

        # Treinar modelo de IA
        st.write("🔄 Treinando modelo de IA...")
        X, y = preprocessar_dados(resultados_df)  # Prepara os dados para IA
        modelo = treinar_modelo_xgb(X, y)

        # Gerar jogos inteligentes
        num_jogos = st.number_input("Quantos jogos deseja gerar?", min_value=1, max_value=100, value=10)
        if st.button("Gerar Jogos"):
            jogos = gerar_jogo(frequencia, num_jogos)
            st.success(f"{num_jogos} jogos gerados com sucesso!")
            for i, jogo in enumerate(jogos, 1):
                st.write(f"Jogo {i}: {', '.join(jogo)}")

          # Gerar jogos
    num_jogos = st.number_input("Quantos jogos deseja gerar?", min_value=1, max_value=100, value=10)
    if st.button("Gerar Jogos"):
        if escolha == "Jogos Inteligentes":
            jogos = gerar_jogo(modelo, frequencia, num_jogos)
        else:  # Caso "Jogos com Fechamento"
            jogos = gerar_jogos_com_fechamento(frequencia, num_jogos)

        st.success(f"{num_jogos} jogos gerados com sucesso!")
        for i, jogo in enumerate(jogos, 1):
            st.write(f"Jogo {i}: {', '.join(jogo)}")

        # Prever dezenas mais prováveis
        st.write("🔮 Prevendo dezenas mais prováveis...")
        top_n = st.slider("Quantas dezenas mais prováveis deseja prever?", min_value=1, max_value=15, value=10)
        dezenas_previstas = prever_dezenas(modelo, frequencia, top_n=top_n)

        st.write(f"### Dezenas mais prováveis: {', '.join(dezenas_previstas)}")        

        # Prever dezenas mais prováveis
        st.write("🔮 Prevendo dezenas mais prováveis...")
        top_n = st.slider("Quantas dezenas mais prováveis deseja prever?", min_value=1, max_value=15, value=10)
        dezenas_previstas = prever_dezenas(modelo, frequencia, top_n=top_n)

        st.write(f"### Dezenas mais prováveis: {', '.join(dezenas_previstas)}")        

    elif escolha == "Simulação de Jogos":
        st.title("🎲 Simulação de Jogos")
        st.write("Simule os jogos gerados com base nos resultados históricos.")
        pagina_ia()  # Página de IA para simulação

    elif escolha == "Sobre":
        st.title("ℹ️ Sobre")
        pagina_sobre()  # Página com informações sobre o projeto

    else:
        st.error("Seleção inválida. Por favor, escolha uma opção válida no menu.")

if __name__ == "__main__":
    main()