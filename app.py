import streamlit as st
from estatisticas import calcular_frequencia
from paginas.ia import pagina_ia
from paginas.gerador import pagina_gerador

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

    # Upload manual dos arquivos
    resultados_file = st.sidebar.file_uploader("Envie o arquivo de resultados", type=["txt", "csv"])

    if not resultados_file:
        st.sidebar.warning("Por favor, envie o arquivo de resultados para continuar.")
        return

    # Carregar resultados
    resultados = []
    for linha in resultados_file:
        resultados.append(list(map(int, linha.strip().split(","))))

    # Calcular frequência
    frequencia = calcular_frequencia(resultados)
    st.session_state["frequencia"] = frequencia
    st.session_state["resultados"] = resultados

    if escolha == "Dashboard":
        st.title("📊 Dashboard de Estatísticas")
        st.write("Frequência das dezenas:")
        st.bar_chart(frequencia)

    elif escolha == "Gerar Jogos":
        pagina_gerador()

    elif escolha == "Simulação de Jogos":
        pagina_ia()

    elif escolha == "Sobre":
        st.title("ℹ️ Sobre")
        st.write("Informações sobre o projeto.")

if __name__ == "__main__":
    main()