import pandas as pd
import random
import pytest
from ajustes import carregar_dados_excel, preprocessar_dados
from estatisticas import calcular_frequencia
from models import gerar_jogos_otimizados
from paginas.gerador import pagina_gerador
import streamlit as st


def test_carregar_dados_excel():
    """
    Testa o carregamento de um arquivo Excel válido.
    """
    df = carregar_dados_excel("data/resultados.xlsx")
    assert not df.empty, "O DataFrame deve ser carregado corretamente!"


def test_carregar_dados_excel_com_arquivo_inexistente():
    """
    Testa o comportamento da função carregar_dados_excel quando o arquivo não existe.
    """
    with pytest.raises(FileNotFoundError, match="No such file or directory"):
        carregar_dados_excel("data/arquivo_inexistente.xlsx")


def test_carregar_dados_excel_com_arquivo_vazio():
    """
    Testa o comportamento da função carregar_dados_excel quando o arquivo está vazio.
    """
    df = carregar_dados_excel("data/arquivo_vazio.xlsx")
    assert df.empty, "O DataFrame deveria estar vazio para um arquivo vazio!"


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
    X, y = preprocessar_dados(df)
    assert "Extra" not in X.columns, "Coluna extra não foi removida!"
    assert X.shape[1] == 4, "Número incorreto de colunas relevantes em X!"


def test_calcular_frequencia_com_dados_vazios():
    """
    Testa o cálculo da frequência quando o DataFrame de entrada está vazio.
    """
    df = pd.DataFrame()
    frequencia = calcular_frequencia(df)
    assert frequencia.empty, "A frequência deve ser vazia para um DataFrame vazio!"


def test_calcular_frequencia_com_dados_nulos():
    """
    Testa o cálculo da frequência quando o DataFrame contém valores nulos.
    """
    df = pd.DataFrame({
        f"D{i}": [random.choice([None, random.randint(1, 25)]) for _ in range(10)] for i in range(1, 15)
    })
    frequencia = calcular_frequencia(df)
    assert not frequencia.empty, "Frequência não foi calculada corretamente!"
    assert frequencia["Dezena"].between(1, 25).all(), "Frequência contém dezenas fora do intervalo esperado!"


def test_gerar_jogos_otimizados_com_frequencia():
    """
    Testa a geração de jogos otimizados utilizando dados de frequência.
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


def test_pagina_gerador_com_frequencia_invalida():
    """
    Testa a página do gerador de jogos quando os dados de frequência são inválidos.
    """
    frequencia = pd.DataFrame({
        "Dezena": [i for i in range(1, 25)],
        "Frequência": [random.choice([-1, "invalid"]) for _ in range(1, 25)]  # Valores inválidos
    })
    st.session_state["frequencia"] = frequencia
    with pytest.raises(ValueError, match="Dados de frequência inválidos!"):
        pagina_gerador()


def test_preprocessar_dados_empty_dataframe():
    """
    Testa o pré-processamento de dados quando o DataFrame está vazio.
    """
    df = pd.DataFrame()
    with pytest.raises(ValueError, match="O DataFrame fornecido está vazio."):
        preprocessar_dados(df)


def test_preprocessar_dados_no_relevant_columns():
    """
    Testa o pré-processamento de dados quando não há colunas relevantes no DataFrame.
    """
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    with pytest.raises(ValueError, match="Nenhuma coluna de dezenas encontrada no DataFrame."):
        preprocessar_dados(df)