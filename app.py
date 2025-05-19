import os
import pandas as pd
import numpy as np
import random
import streamlit as st
from inteligencia import gerar_jogos_inteligentes_v2, gerar_jogos_ml_filtrados
from visualizacao import mostrar_dashboard
from utils import salvar_historico, is_prime, is_fibonacci

# --- Filtros Estatísticos ---
def atende_filtros(jogo, ultimo_resultado):
    pares = len([d for d in jogo if d % 2 == 0])
    impares = 15 - pares
    primos = len([d for d in jogo if is_prime(d)])
    mult3 = len([d for d in jogo if d % 3 == 0])
    fib = len([d for d in jogo if is_fibonacci(d)])
    soma = sum(jogo)
    repetidas = len(set(jogo).intersection(set(ultimo_resultado)))

    return (
        6 <= pares <= 9 and
        6 <= impares <= 9 and
        4 <= primos <= 7 and
        4 <= mult3 <= 6 and
        3 <= fib <= 5 and
        165 <= soma <= 224 and
        8 <= repetidas <= 11
    )

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

if __name__ == "__main__":
    main()