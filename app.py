import os
import pandas as pd
import numpy as np
import random
import streamlit as st
from inteligencia import gerar_jogos_inteligentes_v2, gerar_jogos_ml_filtrados
from visualizacao import is_prime, is_fibonacci, atende_filtros, gerar_jogos_filtrados, calcular_estatisticas_jogo
from pipeline import atualizar_historico, gerar_estatisticas, carregar_planilha

# --- Funções auxiliares ---
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def is_fibonacci(n):
    x1 = 5 * n * n + 4
    x2 = 5 * n * n - 4
    return int(x1**0.5)**2 == x1 or int(x2**0.5)**2 == x2

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

# --- Dashboard Streamlit ---
def mostrar_dashboard(caminho_estatisticas):
    try:
        df = pd.read_excel(caminho_estatisticas)
        st.subheader("📊 Estatísticas dos Jogos Salvos")
        st.dataframe(df)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {e}")
        return pd.DataFrame()

# --- Função para calcular estatísticas de um jogo ---
def calcular_estatisticas_jogo(jogo, ultimo_resultado):
    pares = len([d for d in jogo if d % 2 == 0])
    impares = 15 - pares
    primos = len([d for d in jogo if is_prime(d)])
    mult3 = len([d for d in jogo if d % 3 == 0])
    fib = len([d for d in jogo if is_fibonacci(d)])
    soma = sum(jogo)
    repetidas = len(set(jogo).intersection(set(ultimo_resultado)))
    return pares, impares, primos, mult3, fib, soma, repetidas

# --- Função principal do app ---
def main():
    st.set_page_config(page_title="Gerador Inteligente Lotofácil", layout="centered")
    st.title("🎯 Gerador Inteligente de Jogos da Lotofácil")
    st.markdown("Use filtros matemáticos e estatísticos para criar jogos inteligentes.")

    caminho_historico = "dados/resultados_historicos.xlsx"
    caminho_estatisticas = "dados/estatisticas.xlsx"
    os.makedirs("dados", exist_ok=True)

    if not os.path.exists(caminho_estatisticas):
        df_vazio = pd.DataFrame(columns=[
            "Data", "Jogo", "Acertos", "Pares", "Ímpares", "Primos",
            "Múltiplos de 3", "Fibonacci", "Soma", "Repetidas com último"
        ])
        df_vazio.to_excel(caminho_estatisticas, index=False)

    # Carregar último resultado
    if not os.path.exists(caminho_historico):
        st.error("Arquivo de resultados históricos não encontrado.")
        return
    historico = pd.read_excel(caminho_historico)
    ultimo_resultado = historico.sort_values(by='Concurso', ascending=False).iloc[0, 2:].tolist()
    ultimo_resultado = [int(d) for d in ultimo_resultado if not pd.isna(d)]

    # Interface para gerar jogos
    qtd_jogos = st.number_input("Quantidade de jogos a gerar:", min_value=1, max_value=20, value=5)
    if st.button("🎲 Gerar Jogos"):
        jogos = gerar_jogos_filtrados(ultimo_resultado, qtd_jogos)

        # Calcular estatísticas
        hoje = pd.Timestamp.now().date()
        df_resultado = []
        for jogo in jogos:
            pares, impares, primos, mult3, fib, soma, repetidas = calcular_estatisticas_jogo(jogo, ultimo_resultado)
            df_resultado.append({
                "Data": hoje,
                "Jogo": ", ".join([f"{d:02d}" for d in jogo]),
                "Acertos": "",  # Pode ser preenchido após o sorteio
                "Pares": pares,
                "Ímpares": impares,
                "Primos": primos,
                "Múltiplos de 3": mult3,
                "Fibonacci": fib,
                "Soma": soma,
                "Repetidas com último": repetidas
            })

        df_jogos = pd.DataFrame(df_resultado)
        st.success("Jogos gerados com sucesso!")
        st.dataframe(df_jogos)

        # Salvar no Excel
        df_antigo = pd.read_excel(caminho_estatisticas)
        df_total = pd.concat([df_antigo, df_jogos], ignore_index=True)
        df_total.to_excel(caminho_estatisticas, index=False)

    # Exibir dashboard
    st.markdown("---")
    mostrar_dashboard(caminho_estatisticas)

if __name__ == "__main__":
    main()