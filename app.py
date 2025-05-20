import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load
from io import BytesIO


# ------------------------------------------
# --- Utilitários Matemáticos ---
# ------------------------------------------
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    x1 = 5 * n * n + 4
    x2 = 5 * n * n - 4
    return int(x1**0.5)**2 == x1 or int(x2**0.5)**2 == x2

# ------------------------------------------
# --- Filtros Estatísticos para os Jogos ---
# ------------------------------------------
def atende_filtros(jogo, ultimo_resultado):
    pares = len([d for d in jogo if d % 2 == 0])
    primos = len([d for d in jogo if is_prime(d)])
    mult3 = len([d for d in jogo if d % 3 == 0])
    fib = len([d for d in jogo if is_fibonacci(d)])
    soma = sum(jogo)
    repetidas = len(set(jogo).intersection(set(ultimo_resultado)))

    return (
        6 <= pares <= 8 and
        4 <= primos <= 7 and
        4 <= mult3 <= 6 and
        3 <= fib <= 5 and
        8 <= repetidas <= 10 and
        160 <= soma <= 225
    )

# ------------------------------------------
# --- Gerar Jogos com Base nos Filtros ---
# ------------------------------------------
def gerar_jogos_filtrados(ultimo_resultado, n_jogos=10):
    jogos = []
    tentativas = 0
    while len(jogos) < n_jogos and tentativas < 10000:
        jogo = sorted(random.sample(range(1, 26), 15))
        if atende_filtros(jogo, ultimo_resultado):
            jogos.append(jogo)
        tentativas += 1
    return jogos

# ------------------------------------------
# --- Calcular Estatísticas por Jogo ---
# ------------------------------------------
def calcular_estatisticas_jogo(jogo, ultimo_resultado):
    pares = len([d for d in jogo if d % 2 == 0])
    impares = 15 - pares
    primos = len([d for d in jogo if is_prime(d)])
    mult3 = len([d for d in jogo if d % 3 == 0])
    fib = len([d for d in jogo if is_fibonacci(d)])
    soma = sum(jogo)
    repetidas = len(set(jogo).intersection(set(ultimo_resultado)))
    return [pares, impares, primos, mult3, fib, soma, repetidas]

# ------------------------------------------
# --- Dashboard com Estatísticas ---
# ------------------------------------------
def mostrar_dashboard(df_jogos):
    st.subheader("📊 Estatísticas dos Jogos Gerados")
    st.dataframe(df_jogos)

    st.bar_chart(df_jogos[["Pares", "Ímpares", "Primos", "Múltiplos de 3", "Fibonacci"]])
    st.line_chart(df_jogos[["Soma"]])

# ------------------------------------------
# --- Aprendizado de Máquina com Feedback ---
# ------------------------------------------
def treinar_modelo(df_feedback):
    if "Acertos" not in df_feedback.columns:
        return None

    X = df_feedback[["Pares", "Ímpares", "Primos", "Múltiplos de 3", "Fibonacci", "Soma", "Repetidas"]]
    y = df_feedback["Acertos"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    dump(model, "modelo_lotofacil.joblib")
    return model

def carregar_modelo():
    if os.path.exists("modelo_lotofacil.joblib"):
        return load("modelo_lotofacil.joblib")
    return None

# ------------------------------------------
# --- Interface Principal com Streamlit ---
# ------------------------------------------
def main():
    st.set_page_config(page_title="Lotofácil Inteligente", layout="wide")
    st.title("🎯 Gerador Inteligente de Jogos da Lotofácil")

    # Upload dos arquivos Excel
    st.header("📤 Upload dos Arquivos")
    col1, col2 = st.columns(2)
    with col1:
        arquivo_resultados = st.file_uploader("✅ Suba o arquivo de resultados oficiais", type=["xlsx"])
    with col2:
        arquivo_feedback = st.file_uploader("📊 Suba os jogos anteriores com desempenho", type=["xlsx"])

    if arquivo_resultados:
        df_resultados = pd.read_excel(arquivo_resultados)
        col_dezenas = df_resultados.columns[-15:]
        ultimo_jogo = df_resultados.iloc[-1][col_dezenas].tolist()
        st.success("✔️ Resultados carregados com sucesso!")

        # Gerar jogos
        st.subheader("🎮 Geração de Jogos Inteligentes")
        qtd_jogos = st.slider("Quantidade de jogos", 1, 20, 10)
        if st.button("🚀 Gerar Jogos"):
            jogos = gerar_jogos_filtrados(ultimo_jogo, qtd_jogos)
            hoje = datetime.now().date()

            dados = []
            for jogo in jogos:
                stats = calcular_estatisticas_jogo(jogo, ultimo_jogo)
                dados.append({
                    "Data": hoje,
                    "Jogo": ", ".join(f"{d:02d}" for d in jogo),
                    "Pares": stats[0],
                    "Ímpares": stats[1],
                    "Primos": stats[2],
                    "Múltiplos de 3": stats[3],
                    "Fibonacci": stats[4],
                    "Soma": stats[5],
                    "Repetidas": stats[6],
                    "Acertos": ""  # A ser preenchido manualmente depois
                })

            df_jogos = pd.DataFrame(dados)
            st.success("✅ Jogos gerados com sucesso!")
            mostrar_dashboard(df_jogos)

    def to_excel_bytes(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        processed_data = output.getvalue()
    return processed_data

    # Download dos jogos gerados
excel_bytes = to_excel_bytes(df_jogos)
st.download_button(
    label="📥 Baixar Jogos",
    data=excel_bytes,
    file_name="jogos_inteligentes.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)  

    # Treinamento com feedback
if arquivo_feedback:
    st.subheader("🤖 Aprendizado de Máquina")
    df_feedback = pd.read_excel(arquivo_feedback)
    if "Acertos" in df_feedback.columns:
        modelo = treinar_modelo(df_feedback)
        st.success("🧠 Modelo treinado com base nos acertos passados.")
    else:
        st.warning("⚠️ A planilha deve conter a coluna 'Acertos'.")

if __name__ == "__main__":
    main()
