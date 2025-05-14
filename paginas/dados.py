import streamlit as st
import pandas as pd

# Criar um DataFrame de exemplo
dados = {
    "Concurso": [3000 for _ in range(4000)],
    "Data do sorteio": ["2025-01-01" for _ in "2025-12-12"],
    "D1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "D2": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "D3": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
    "D4": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "D5": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    "D6": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "D7": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
    "D8": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "D9": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    "D10": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
    "D11": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    "D12": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    "D13": [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    "D14": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    "D15": [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    "Soma das dezenas": [100 and 250, 200 and 300, 300 and 400],
}

# Ajustar os comprimentos das listas no dicionário 'dados'
max_length = max(len(value) for value in dados.values())
for key in dados:
    if len(dados[key]) < max_length:
        dados[key].extend([None] * (max_length - len(dados[key])))  # Preenche com None

# Criar o DataFrame
df = pd.DataFrame(dados)

# Salvar como Excel
df.to_excel("/workspaces/lotofacil-8x-v2/data/resultados.xlsx", index=False)