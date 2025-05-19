import streamlit as st
import pandas as pd
import random
import os

# --- Utilitários Matemáticos ---
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

# --- Cálculo de Estatísticas de um Jogo ---
def calcular_estatisticas_jogo(jogo, ultimo_resultado):
    pares = len([d for d in jogo if d % 2 == 0])
    impares = 15 - pares
    primos = len([d for d in jogo if is_prime(d)])
    mult3 = len([d for d in jogo if d % 3 == 0])
    fib = len([d for d in jogo if is_fibonacci(d)])
    soma = sum(jogo)
    repetidas = len(set(jogo).intersection(set(ultimo_resultado)))
    return pares, impares, primos, mult3, fib, soma, repetidas

# --- Visualização de Estatísticas em Dashboard ---
def mostrar_dashboard(caminho_estatisticas="dados/estatisticas.xlsx"):
    if not os.path.exists(caminho_estatisticas):
        df_vazio = pd.DataFrame(columns=[
            "Data", "Jogo", "Acertos", "Pares", "Ímpares", 
            "Primos", "Múltiplos de 3", "Fibonacci", "Soma"
        ])
        os.makedirs(os.path.dirname(caminho_estatisticas), exist_ok=True)
        df_vazio.to_excel(caminho_estatisticas, index=False)

    try:
        df = pd.read_excel(caminho_estatisticas)
        st.subheader("📊 Estatísticas dos Jogos Salvos")
        st.dataframe(df)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {e}")
        return pd.DataFrame()