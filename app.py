mport streamlit as st
from pipeline import processar_dados_diarios
from inteligencia import treinar_modelo, gerar_sugestoes
from visualizacao import mostrar_dashboard

def main():
    st.set_page_config(page_title="Lotofácil 8X", layout="wide")
    st.sidebar.title("🎯 Lotofácil 8X")

    # Menu lateral
    escolha = st.sidebar.radio(
        "Navegação",
        ["Dashboard", "Gerar Sugestões", "Sobre"]
    )

    if escolha == "Dashboard":
        st.title("📊 Dashboard de Estatísticas")
        mostrar_dashboard()

    elif escolha == "Gerar Sugestões":
        st.title("🔮 Sugestões de Apostas")
        processar_dados_diarios()
        sugestoes = gerar_sugestoes()
        st.write("Sugestões de Apostas:")
        for i, sugestao in enumerate(sugestoes, 1):
            st.write(f"Jogo {i}: {sugestao}")

    elif escolha == "Sobre":
        st.title("ℹ️ Sobre o Lotofácil 8X")
        st.markdown("""
        Este aplicativo utiliza **Inteligência Artificial** e **estatísticas** para analisar e gerar combinações prováveis para a Lotofácil.
        Desenvolvido para uso pessoal.
        """)

if __name__ == "__main__":
    main()