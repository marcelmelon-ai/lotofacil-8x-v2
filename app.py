import streamlit as st
from maquininha import carregar_resultados_excel
from layout import menu_lateral
from ajustes import preprocessar_dados
from inteligencia import treinar_modelo_xgb, prever_dezenas
from models import gerar_jogos_otimizados

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
        from paginas.gerador import pagina_gerador
        pagina_gerador()
    
    elif escolha == "Simulação de Jogos":
        from paginas.ia import pagina_ia
        pagina_ia()
    
    elif escolha == "Sobre":
        from paginas.sobre import pagina_sobre
        pagina_sobre()
    
    else:
        st.error("Seleção inválida. Por favor, escolha uma opção válida no menu.")

if __name__ == "__main__":
    main()