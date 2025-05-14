import pandas as pd
import random
import pytest
from ajustes import carregar_dados_excel, preprocessar_dados
from estatisticas import calcular_frequencia
from models import gerar_jogos_otimizados
from paginas.gerador import pagina_gerador
import streamlit as st

def test_carregar_dados_excel():
    df = carregar_dados_excel("data/resultados.xlsx")
    assert not df.empty, "O DataFrame deve ser carregado corretamente!"

def test_carregar_dados_excel_com_dados_corrompidos():
    """
    Testa o comportamento da função carregar_dados_excel quando o arquivo contém dados corrompidos.
    """
    try:
        df = carregar_dados_excel("data/dados_corrompidos.xlsx")
        print(df)  # Accessing df to avoid "not accessed" error
        assert False, "Deveria ter ocorrido um erro ao carregar dados corrompidos!"
    except ValueError as e:
        assert "Erro ao processar o arquivo Excel" in str(e), "Mensagem de erro incorreta para dados corrompidos!"

def test_preprocessar_dados_com_todas_colunas_irrelevantes():
    """
    Testa o pré-processamento de dados quando todas as colunas do DataFrame são irrelevantes.
    """
    df = pd.DataFrame({
        "Irrelevante1": [random.randint(1, 100) for _ in range(10)],
        "Irrelevante2": [random.randint(1, 100) for _ in range(10)]
    })
    try:
        preprocessar_dados(df)
        assert False, "Deveria ter ocorrido um erro ao processar um DataFrame sem colunas relevantes!"
    except ValueError as e:
        assert "Nenhuma coluna relevante encontrada" in str(e), "Mensagem de erro incorreta para colunas irrelevantes!"

def test_calcular_frequencia_com_dados_negativos():
    """
    Testa o cálculo da frequência quando o DataFrame contém valores negativos.
    """
    df = pd.DataFrame({
        f"D{i}": [random.choice([-5, random.randint(1, 25)]) for _ in range(10)] for i in range(1, 15)
    })
    try:
        calcular_frequencia(df)
        assert False, "Deveria ter ocorrido um erro ao calcular frequência com valores negativos!"
    except ValueError as e:
        assert "Valores negativos encontrados" in str(e), "Mensagem de erro incorreta para valores negativos!"

def test_gerar_jogos_otimizados_com_frequencia_incompleta():
    """
    Testa a geração de jogos otimizados quando a frequência está incompleta.
    """
    df = pd.DataFrame({
        f"D{i}": [random.randint(1, 25) for _ in range(25)] for i in range(1, 16)
    })
    frequencia = pd.DataFrame({
        "Dezena": [1, 2, 3],  # Frequência incompleta
        "Frequência": [10, 20, 30]
    })
    try:
        gerar_jogos_otimizados(df, frequencia=frequencia, num_jogos=3)
        assert False, "Deveria ter ocorrido um erro ao gerar jogos com frequência incompleta!"
    except ValueError as e:
        assert "Frequência incompleta!" in str(e), "Mensagem de erro incorreta para frequência incompleta!"

def test_pagina_gerador_com_frequencia_duplicada():
    """
    Testa a página do gerador de jogos quando há duplicatas nos dados de frequência.
    """
    frequencia = pd.DataFrame({
        "Dezena": [1, 1, 2, 3],
        "Frequência": [10, 15, 20, 30]
    })
    st.session_state["frequencia"] = frequencia
    try:
        pagina_gerador()
        assert False, "Deveria ter ocorrido um erro ao carregar a página com frequência duplicada!"
    except ValueError as e:
        assert "Dados de frequência duplicados!" in str(e), "Mensagem de erro incorreta para frequência duplicada!"
    
def test_carregar_dados_excel_com_arquivo_vazio():
    """
    Testa o comportamento da função carregar_dados_excel quando o arquivo está vazio.
    """
    try:
        df = carregar_dados_excel("data/arquivo_vazio.xlsx")
        assert df.empty, "O DataFrame deveria estar vazio para um arquivo vazio!"
    except Exception as e:
        assert False, f"Erro inesperado ao carregar arquivo vazio: {e}"

def test_preprocessar_dados_com_colunas_extras():
    """
    Testa o pré-processamento de dados quando há colunas extras no DataFrame.
    """
    df = pd.DataFrame({
        "D1": [random.randint(1, 25) for _ in range(10)],
        "D2": [random.randint(1, 25) for _ in range(10)],
        "D3": [random.randint(1, 25) for _ in range(10)],
        "D15": [random.randint(1, 25) for _ in range(10)],
        "Extra": [random.randint(1, 100) for _ in range(10)]  # Coluna extra
    })
    print(df)  # Accessing df to avoid "not accessed" error
    X, y = preprocessar_dados(df)
    assert "Extra" not in X.columns, "Coluna extra não foi removida!"
    assert X.shape[1] == 4, "Número incorreto de colunas relevantes em X!"

def test_calcular_frequencia_com_dados_nulos():
    """
    Testa o cálculo da frequência quando o DataFrame contém valores nulos.
    """
    df = pd.DataFrame({
        f"D{i}": [random.choice([None, random.randint(1, 25)]) for _ in range(10)] for i in range(1, 15)
    })
    try:
        freq = calcular_frequencia(df)
        assert not freq.empty, "Frequência não foi calculada corretamente!"
        assert freq["Dezena"].between(1, 25).all(), "Frequência contém dezenas fora do intervalo esperado!"
    except ValueError as e:
        assert "Dados nulos encontrados" in str(e), "Mensagem de erro incorreta para dados nulos!"

def test_gerar_jogos_otimizados_com_num_jogos_zero():
    """
    Testa a geração de jogos otimizados quando o número de jogos solicitado é zero.
    """
    df = pd.DataFrame({
        f"D{i}": [random.randint(1, 25) for _ in range(25)] for i in range(1, 16)
    })
    frequencia = calcular_frequencia(df)
    jogos = gerar_jogos_otimizados(df, frequencia=frequencia, num_jogos=0)
    assert len(jogos) == 0, "Nenhum jogo deveria ser gerado quando num_jogos é zero!"

def test_pagina_gerador_com_frequencia_parcial():
    """
    Testa a página do gerador de jogos quando os dados de frequência estão parcialmente preenchidos.
    """
    frequencia = pd.DataFrame({
        "Dezena": [i for i in range(1, 25)],
        "Frequência": [random.choice([None, random.randint(1, 100)]) for _ in range(1, 25)]
    })
    st.session_state["frequencia"] = frequencia
    try:
        pagina_gerador()
        assert True, "A página deveria carregar mesmo com frequência parcial!"
    except Exception as e:
        assert False, f"Erro inesperado ao carregar a página com frequência parcial: {e}"

def test_pagina_gerador():
    """
    Testa a página do gerador de jogos para garantir que ela carrega sem erros.
    """
    # Simular dados de frequência
    frequencia = pd.DataFrame({
        "Dezena": [i for i in range(1, 25)],
        "Frequência": [random.randint(1, 100) for _ in range(1, 25)]
    })
    # Simular sessão do Streamlit
    st.session_state["frequencia"] = frequencia
    pagina_gerador()  # Verificar se a página carrega sem erros

def test_carregar_dados_excel_arquivo_inexistente():
    """
    Testa o comportamento da função carregar_dados_excel quando o arquivo não existe.
    """
    try:
        carregar_dados_excel("data/arquivo_inexistente.xlsx")
        assert False, "Deveria ter ocorrido um erro ao tentar carregar um arquivo inexistente!"
    except FileNotFoundError as e:
        assert "No such file or directory" in str(e), "Mensagem de erro incorreta para arquivo inexistente!"

def test_preprocessar_dados_com_dados_invalidos():
    """
    Testa o pré-processamento de dados quando há valores inválidos no DataFrame.
    """
    df = pd.DataFrame({
        "D1": [random.randint(1, 25) for _ in range(10)],
        "D2": [random.randint(1, 25) for _ in range(10)],
        "D3": [random.randint(1, 25) for _ in range(10)],
        "D15": [random.choice([None, "invalid", 30]) for _ in range(10)],  # Valores inválidos
        "Soma das dezenas": [random.randint(100, 200) for _ in range(10)]
    })
    try:
        preprocessar_dados(df)
        assert False, "Deveria ter ocorrido um erro ao processar dados inválidos!"
    except ValueError as e:
        assert "Dados inválidos encontrados" in str(e), "Mensagem de erro incorreta para dados inválidos!"

def test_calcular_frequencia_com_valores_repetidos():
    """
    Testa o cálculo da frequência quando há valores repetidos no DataFrame.
    """
    df = pd.DataFrame({
        f"D{i}": [5 for _ in range(10)] for i in range(1, 15)
    })
    frequencia = calcular_frequencia(df)
    assert not frequencia.empty, "Frequência não foi calculada corretamente!"
    assert (frequencia["Frequência"] == 140).all(), "Frequência calculada incorretamente para valores repetidos!"

def test_gerar_jogos_otimizados_com_frequencia_vazia():
    """
    Testa a geração de jogos otimizados quando a frequência está vazia.
    """
    df = pd.DataFrame({
        f"D{i}": [random.randint(1, 25) for _ in range(25)] for i in range(1, 16)
    })
    frequencia = pd.DataFrame(columns=["Dezena", "Frequência"])
    try:
        gerar_jogos_otimizados(df, frequencia=frequencia, num_jogos=3)
        assert False, "Deveria ter ocorrido um erro ao gerar jogos com frequência vazia!"
    except ValueError as e:
        assert "Frequência está vazia!" in str(e), "Mensagem de erro incorreta para frequência vazia!"

def test_pagina_gerador_com_frequencia_invalida():
    """
    Testa a página do gerador de jogos quando os dados de frequência são inválidos.
    """
    frequencia = pd.DataFrame({
        "Dezena": [i for i in range(1, 25)],
        "Frequência": [random.choice([-1, "invalid"]) for _ in range(1, 25)]  # Valores inválidos
    })
    st.session_state["frequencia"] = frequencia
    try:
        pagina_gerador()
        assert False, "Deveria ter ocorrido um erro ao carregar a página com frequência inválida!"
    except ValueError as e:
        assert "Dados de frequência inválidos!" in str(e), "Mensagem de erro incorreta para frequência inválida!"

def test_gerar_jogos_otimizados_com_frequencia():
    """
    Testa a geração de jogos otimizados utilizando dados de frequência para garantir que os jogos gerados estão corretos.
    """
    df = pd.DataFrame({
        f"D{i}": [random.randint(1, 25) for _ in range(25)] for i in range(1, 16)
    })
    frequencia = calcular_frequencia(df)
    jogos = gerar_jogos_otimizados(df, frequencia=frequencia, num_jogos=3)
    assert len(jogos) == 3, "Número de jogos gerados está incorreto!"
    assert all(len(jogo) == 15 for jogo in jogos), "Cada jogo deve ter 15 dezenas!"
    for jogo in jogos:
        assert all(1 <= dezena <= 25 for dezena in jogo), "Dezenas fora do intervalo permitido!"

def test_gerar_jogos_otimizados_sem_dados():
    """
    Testa a geração de jogos otimizados quando o DataFrame de entrada está vazio.
    """
    df = pd.DataFrame()  # Define an empty DataFrame
    try:
        jogos = gerar_jogos_otimizados(df, num_jogos=2)
        print(jogos)  # Accessing jogos to avoid "not accessed" error
        assert False, "Deveria ter ocorrido um erro ao gerar jogos com DataFrame vazio!"
    except ValueError as e:
        assert str(e) == "O DataFrame de entrada está vazio!", "Mensagem de erro incorreta!"

def test_calcular_frequencia_com_dados_vazios():
    """
    Testa o cálculo da frequência quando o DataFrame de entrada está vazio.
    """
    df = pd.DataFrame()
    frequencia = calcular_frequencia(df)
    assert frequencia.empty, "A frequência deve ser vazia para um DataFrame vazio!"

def test_preprocessar_dados_sem_colunas_irrelevantes():
    """
    Testa o pré-processamento de dados quando não há colunas irrelevantes no DataFrame.
    """
    df = pd.DataFrame({
        "D1": [random.randint(1, 25) for _ in range(10)],
        "D2": [random.randint(1, 25) for _ in range(10)],
        "D3": [random.randint(1, 25) for _ in range(10)],
        "D15": [random.randint(1, 25) for _ in range(10)]
    })
    X, y = preprocessar_dados(df)
    assert X.shape[1] == 4, "Número incorreto de colunas relevantes em X!"
    assert y.name == "D15", "A última coluna não foi definida como alvo corretamente!"

def test_dataframe_creation():
    # Placeholder for the actual implementation of test_dataframe_creation
    pass

def setup_test_environment(tmp_path):
    # Placeholder for the actual implementation of setup_test_environment
    return tmp_path

def test_excel_file_creation(test_dir):
    # Placeholder for the actual implementation of test_excel_file_creation
    pass

def test_dataframe_creation_validity():
    # Test the DataFrame creation function
    try:
        test_dataframe_creation()
    except AssertionError as e:
        pytest.fail(f"DataFrame creation test failed: {e}")

def test_excel_file_creation_validity(tmp_path):
    # Test the Excel file creation function
    try:
        test_dir = setup_test_environment(tmp_path)
        test_excel_file_creation(test_dir)
    except AssertionError as e:
        pytest.fail(f"Excel file creation test failed: {e}")

def test_pagina_gerador_sem_frequencia():
    """
    Testa a página do gerador de jogos quando não há dados de frequência disponíveis.
    """
    if "frequencia" in st.session_state:
        del st.session_state["frequencia"]
    try:
        pagina_gerador()
        assert False, "Deveria ter ocorrido um erro ao carregar a página sem dados de frequência!"
    except KeyError as e:
        assert str(e) == "'frequencia'", "Mensagem de erro incorreta ao acessar dados de frequência!"