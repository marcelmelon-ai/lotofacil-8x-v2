import streamlit as st
import pandas as pd
import os

def carregar_dados_excel(output_file):
    # Verifica se está no ambiente online
    if os.getenv("STREAMLIT_CLOUD") == "true":
        # Carregamento do arquivo Excel
        return pd.read_excel(output_file)
    else:
        # Retorna um DataFrame vazio no ambiente local
        return pd.DataFrame()

def test_dataframe_creation():
    # Sample data to mimic the 'dados' dictionary
    dados = {
    "Concurso": [3000 for _ in range(4000)],
    "Data do sorteio": pd.date_range(start="2025-01-01", end="2025-12-31").strftime("%Y-%m-%d").tolist(),
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
    "Soma das dezenas": [100 for _ in range(400)]
    }

# Create the DataFrame
    df = pd.DataFrame(dados)

    # Assert the DataFrame is created correctly
    assert not df.empty
    assert list(df.columns) == list(dados.keys())
    assert len(df) == 400

def test_excel_file_creation(setup_test_environment):
    # Sample data to mimic the 'dados' dictionary
    dados = {
    "Concurso": [3000 for _ in range(4000)],
    "Data do sorteio": pd.date_range(start="2025-01-01", end="2025-12-31").strftime("%Y-%m-%d").tolist(),
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
    "Soma das dezenas": [100 for _ in range(400)]
    }

# Diretório e arquivo de saída
    output_dir = setup_test_environment
    output_file = os.path.join(output_dir, "resultados.xlsx")

    # Criação do DataFrame e salvamento no Excel
    df = pd.DataFrame(dados)
    df.to_excel(output_file, index=False)

    # Verificação se o arquivo foi criado
    assert os.path.exists(output_file)

    # Carregamento do arquivo Excel e verificação do conteúdo
    loaded_df = carregar_dados_excel(output_file)
    if not loaded_df.empty:
        pd.testing.assert_frame_equal(df, loaded_df)