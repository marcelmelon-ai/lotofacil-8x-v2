import os
import pandas as pd
import streamlit as st
from datetime import datetime
from inteligencia import gerar_jogos_inteligentes_v2, gerar_jogos_ml_filtrados
from visualizacao import is_prime,is_fibonacci,atende_filtros,gerar_jogos_filtrados,calcular_estatisticas_jogo,mostrar_dashboard


# --- Geração de Jogos com Filtros ---
def gerar_jogos_filtrados(ultimo_resultado, n_jogos=10):
    jogos = []
    tentativas = 0
    while len(jogos) < n_jogos and tentativas < 10000:
        jogo = sorted(random.sample(range(1, 26), 15))
        if atende_filtros(jogo, ultimo_resultado):
            jogos.append(jogo)
        tentativas += 1
    return jogos

# --- Função Principal Streamlit ---
def main():
    st.set_page_config(page_title="Lotofácil 8X", layout="wide")
    st.title("🎯 Lotofácil 8X - Geração Inteligente de Jogos")

    arquivo_excel = st.file_uploader("Carregar Planilha Unificada", type=["xlsx"])

    if arquivo_excel:
        df = pd.read_excel(arquivo_excel)

        # Espera que as últimas 15 colunas sejam as dezenas
        col_dezenas = df.columns[-15:]
        ultimo_jogo = df.iloc[-1][col_dezenas].values.tolist()

        st.success("Arquivo carregado com sucesso!")
        st.write("Último Jogo:", sorted(ultimo_jogo))

        if st.button("Gerar Jogos Inteligentes com Filtros"):
            jogos = gerar_jogos_filtrados(ultimo_jogo, n_jogos=10)
            for i, jogo in enumerate(jogos, 1):
                st.write(f"Jogo {i}: {jogo}")

            df_resultado = salvar_historico(jogos)
            st.download_button("📥 Baixar Jogos", data=df_resultado.to_excel(index=False), file_name="jogos_filtrados.xlsx")

# --- Caminhos dos arquivos ---
CAMINHO_HISTORICO = "dados/resultados_historicos.xlsx"
CAMINHO_ESTATISTICAS = "dados/estatisticas.xlsx"

# --- Inicialização de diretórios e arquivos ---
def inicializar_arquivos():
    os.makedirs("dados", exist_ok=True)

    if not os.path.exists(CAMINHO_ESTATISTICAS):
        df_vazio = pd.DataFrame(columns=[
            "Data", "Jogo", "Acertos", "Pares", "Ímpares", "Primos",
            "Múltiplos de 3", "Fibonacci", "Soma", "Repetidas com último"
        ])
        df_vazio.to_excel(CAMINHO_ESTATISTICAS, index=False)

    if not os.path.exists(CAMINHO_HISTORICO):
        st.error("❌ Arquivo de resultados históricos não encontrado.")
        st.stop()

# --- Carregar último resultado do concurso ---
def carregar_ultimo_resultado():
    historico = pd.read_excel(CAMINHO_HISTORICO)
    ultimo = historico.sort_values(by='Concurso', ascending=False).iloc[0, 2:]
    return [int(d) for d in ultimo if not pd.isna(d)]

# --- Interface principal ---
def main():
    st.set_page_config(page_title="Gerador Inteligente Lotofácil", layout="centered")
    st.title("🎯 Gerador Inteligente de Jogos da Lotofácil")
    st.markdown("Crie jogos usando **filtros estatísticos e inteligência matemática**.")

    inicializar_arquivos()
    ultimo_resultado = carregar_ultimo_resultado()

    # --- Seção: Geração de jogos ---
    qtd_jogos = st.number_input("🎮 Quantidade de jogos a gerar:", min_value=1, max_value=20, value=5)
    if st.button("🚀 Gerar Jogos Inteligentes"):
        jogos = gerar_jogos_filtrados(ultimo_resultado, qtd_jogos)
        hoje = datetime.now().date()

        # Calcular estatísticas de cada jogo
        dados_jogos = []
        for jogo in jogos:
            estatisticas = calcular_estatisticas_jogo(jogo, ultimo_resultado)
            dados_jogos.append({
                "Data": hoje,
                "Jogo": ", ".join(f"{d:02d}" for d in jogo),
                "Acertos": "",  # A ser preenchido posteriormente
                "Pares": estatisticas[0],
                "Ímpares": estatisticas[1],
                "Primos": estatisticas[2],
                "Múltiplos de 3": estatisticas[3],
                "Fibonacci": estatisticas[4],
                "Soma": estatisticas[5],
                "Repetidas com último": estatisticas[6]
            })

        df_jogos = pd.DataFrame(dados_jogos)
        st.success("✅ Jogos gerados com sucesso!")
        st.dataframe(df_jogos)

        # Salvar no Excel
        df_antigo = pd.read_excel(CAMINHO_ESTATISTICAS)
        df_total = pd.concat([df_antigo, df_jogos], ignore_index=True)
        df_total.to_excel(CAMINHO_ESTATISTICAS, index=False)

    # --- Seção: Visualização dos jogos salvos ---
    st.markdown("---")
    mostrar_dashboard(CAMINHO_ESTATISTICAS)

# --- Execução principal ---
if __name__ == "__main__":
    main()