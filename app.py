import streamlit as st
from maquininha import carregar_resultados_excel
from layout import menu_lateral
from ajustes import preprocessar_dados
from estatisticas import calcular_frequencia
from models import gerar_jogos_inteligentes

def main():
    """
    Função principal para executar o aplicativo Streamlit.
    """
    st.set_page_config(page_title="Lotofácil 8X", layout="wide")
    st.sidebar.title("🎯 Lotofácil 8X")
    
    # Menu lateral
    escolha = menu_lateral()
    
    if escolha == "Dashboard":
        from mostrar_dashboard_estatistico import mostrar_dashboard_estatistico
        df = carregar_resultados_excel("data/resultados.xlsx")
        mostrar_dashboard_estatistico(df)
    
    elif escolha == "Gerar Jogos":
        st.title("🎲 Gerar Jogos Inteligentes")
        st.write("Crie combinações de jogos otimizados com base em estatísticas.")

        # Carregar dados de frequência
        df = carregar_resultados_excel("data/resultados.xlsx")
        if df.empty:
            st.warning("⚠️ Os dados não foram carregados. Por favor, carregue os dados no menu 'Dashboard'.")
            return
        
        # Calcular frequência
        frequencia = calcular_frequencia(df)

        # Gerar jogos inteligentes
        num_jogos = st.number_input("Quantos jogos deseja gerar?", min_value=1, max_value=100, value=10)
        if st.button("Gerar Jogos"):
            jogos = gerar_jogos_inteligentes(frequencia, num_jogos)
            st.success(f"{num_jogos} jogos gerados com sucesso!")
            for i, jogo in enumerate(jogos, 1):
                st.write(f"Jogo {i}: {', '.join(jogo)}")
    
    elif escolha == "Simulação de Jogos":
        st.title("🎲 Simulação de Jogos")
        st.write("Em breve...")

    elif escolha == "Sobre":
        from paginas.sobre import pagina_sobre
        pagina_sobre()
    
    else:
        st.error("Seleção inválida. Por favor, escolha uma opção válida no menu.")

if __name__ == "__main__":
    main()