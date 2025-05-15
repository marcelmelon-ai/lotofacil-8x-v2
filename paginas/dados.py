import streamlit as st
import pandas as pd
import os

def carregar_dados_excel(output_file):
    """
    Carrega dados de um arquivo Excel.
    Retorna um DataFrame vazio se estiver em ambiente local.
    """
    if os.getenv("STREAMLIT_CLOUD") == "true":
        # Carregamento do arquivo Excel no ambiente online
        return pd.read_excel(output_file)
    else:
        # Retorna um DataFrame vazio no ambiente local
        return pd.DataFrame()

def test_dataframe_creation():
    """
    Testa a criação de um DataFrame com dados simulados.
    """
    # Dados simulados
    dados = {
        "Concurso": [3000 for _ in range(400)],
        "Data do sorteio": pd.date_range(start="2025-01-01", periods=400).strftime("%Y-%m-%d").tolist(),
        "D1": [1 for _ in range(400)],
        "D2": [2 for _ in range(400)],
        "D3": [3 for _ in range(400)],
        "D4": [4 for _ in range(400)],
        "D5": [5 for _ in range(400)],
        "D6": [6 for _ in range(400)],
        "D7": [7 for _ in range(400)],
        "D8": [8 for _ in range(400)],
        "D9": [9 for _ in range(400)],
        "D10": [10 for _ in range(400)],
        "D11": [11 for _ in range(400)],
        "D12": [12 for _ in range(400)],
        "D13": [13 for _ in range(400)],
        "D14": [14 for _ in range(400)],
        "D15": [15 for _ in range(400)],
        "Soma das dezenas": [120 for _ in range(400)]
    }

    # Criação do DataFrame
    df = pd.DataFrame(dados)

    # Verificações
    assert not df.empty, "O DataFrame não deveria estar vazio."
    assert list(df.columns) == list(dados.keys()), "As colunas do DataFrame não correspondem aos dados simulados."
    assert len(df) == 400, "O número de linhas do DataFrame está incorreto."

def test_excel_file_creation(setup_test_environment):
    """
    Testa a criação de um arquivo Excel com dados simulados.
    """
    # Dados simulados
    dados = {
        "Concurso": [3000 for _ in range(400)],
        "Data do sorteio": pd.date_range(start="2025-01-01", periods=400).strftime("%Y-%m-%d").tolist(),
        "D1": [1 for _ in range(400)],
        "D2": [2 for _ in range(400)],
        "D3": [3 for _ in range(400)],
        "D4": [4 for _ in range(400)],
        "D5": [5 for _ in range(400)],
        "D6": [6 for _ in range(400)],
        "D7": [7 for _ in range(400)],
        "D8": [8 for _ in range(400)],
        "D9": [9 for _ in range(400)],
        "D10": [10 for _ in range(400)],
        "D11": [11 for _ in range(400)],
        "D12": [12 for _ in range(400)],
        "D13": [13 for _ in range(400)],
        "D14": [14 for _ in range(400)],
        "D15": [15 for _ in range(400)],
        "Soma das dezenas": [120 for _ in range(400)]
    }

    # Diretório e arquivo de saída
    output_dir = setup_test_environment
    output_file = os.path.join(output_dir, "resultados.xlsx")

    # Criação do DataFrame e salvamento no Excel
    df = pd.DataFrame(dados)
    df.to_excel(output_file, index=False)

    # Verificação se o arquivo foi criado
    assert os.path.exists(output_file), "O arquivo Excel não foi criado."

    # Carregamento do arquivo Excel e verificação do conteúdo
    loaded_df = carregar_dados_excel(output_file)
    if not loaded_df.empty:
        pd.testing.assert_frame_equal(df, loaded_df, check_dtype=False)