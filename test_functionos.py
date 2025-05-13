import pandas as pd
import random
from ajustes import carregar_dados_excel, preprocessar_dados
from estatisticas import calcular_frequencia
from models import gerar_jogos_otimizados
from paginas.gerador import pagina_gerador
import streamlit as st

def test_carregar_dados_excel():
    df = carregar_dados_excel("data/resultados.xlsx")
    assert not df.empty, "O DataFrame deve ser carregado corretamente!"

def test_preprocessar_dados():
    """
    Testa o pré-processamento dos dados para garantir que as colunas irrelevantes sejam removidas.
    """
    df = pd.DataFrame({
        "D1": [random.randint(1, 25) for _ in range(10)],
        "D2": [random.randint(1, 25) for _ in range(10)],
        "D3": [random.randint(1, 25) for _ in range(10)],
        "D15": [random.randint(1, 25) for _ in range(10)],  # Valores válidos
        "Soma das dezenas": [random.randint(100, 200) for _ in range(10)]
    })
    X, y = preprocessar_dados(df)
    assert "Soma das dezenas" not in X.columns, "Coluna irrelevante não foi removida!"
    assert X.shape[1] == 4, "Número incorreto de colunas relevantes em X!"
    assert y.name == "D15", "A última coluna não foi definida como alvo corretamente!"
    assert y.between(1, 25).all(), "Valores de y fora do intervalo esperado (1 a 25)!"
    
def test_calcular_frequencia():
    """
    Testa o cálculo da frequência das dezenas.
    """
    df = pd.DataFrame({
        f"D{i}": [random.randint(1, 25) for _ in range(10)] for i in range(1, 15)
    })
    freq = calcular_frequencia(df)
    assert not freq.empty, "Frequência não foi calculada corretamente!"
    assert freq["Dezena"].between(1, 25).all(), "Frequência contém dezenas fora do intervalo esperado!"

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

def test_pagina_estatisticas():
    """
    Testa a página de estatísticas para garantir que os dados são processados corretamente.
    """
    df = pd.DataFrame({
        f"D{i}": [random.randint(1, 25) for _ in range(10)] for i in range(1, 15)
    })
    frequencia = calcular_frequencia(df)
    assert not frequencia.empty, "Frequência não foi calculada corretamente!"
    assert frequencia["Dezena"].between(1, 25).all(), "Frequência contém dezenas fora do intervalo esperado!"

def test_gerar_jogos_otimizados():
    """
    Testa a geração de jogos otimizados para garantir que os jogos gerados estão corretos.
    """
    df = pd.DataFrame({
        f"D{i}": [random.randint(1, 25) for _ in range(25)] for i in range(1, 16)
    })
    jogos = gerar_jogos_otimizados(df, num_jogos=2)
    assert len(jogos) == 2, "Número de jogos gerados está incorreto!"
    assert all(len(jogo) == 15 for jogo in jogos), "Cada jogo deve ter 15 dezenas!"
    for jogo in jogos:
        assert all(1 <= dezena <= 25 for dezena in jogo), "Dezenas fora do intervalo permitido!"

def test_gerar_jogos_otimizados():
    df = pd.DataFrame({
        "D1": [random.randint(1, 25) for _ in range(25)],
        "D2": [random.randint(1, 25) for _ in range(25)],
        "D3": [random.randint(1, 25) for _ in range(25)],
        "D15": [random.randint(1, 25) for _ in range(25)]
    })
    jogos = gerar_jogos_otimizados(df, num_jogos=2)
    assert jogos is not None, "Os jogos devem ser gerados corretamente!"