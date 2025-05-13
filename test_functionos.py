import pandas as pd
from ajustes import carregar_dados_excel, preprocessar_dados
from estatisticas import calcular_frequencia
from models import gerar_jogos_otimizados
from paginas.gerador import pagina_gerador
import streamlit as st

def test_carregar_dados_excel():
    """
    Testa se o arquivo Excel é carregado corretamente.
    """
    df = carregar_dados_excel("data/resultados.xlsx")
    assert not df.empty, "O DataFrame está vazio!"
    assert set(df.columns).issuperset([f"D{i}" for i in range(1, 15)]), "Colunas de dezenas não estão presentes!"

def test_preprocessar_dados():
    """
    Testa o pré-processamento dos dados para garantir que as colunas irrelevantes sejam removidas.
    """
    df = pd.DataFrame({
        "D1": [1, 2], "D2": [3, 4], "D3": [5, 6], "Outros": [7, 8]
    })
    X, y = preprocessar_dados(df)
    assert "Outros" not in X.columns, "Coluna irrelevante não foi removida!"
    assert X.shape[1] == 3, "Número incorreto de colunas relevantes em X!"
    assert y.name == "D15", "A última coluna não foi definida como alvo corretamente!"

def test_calcular_frequencia():
    """
    Testa o cálculo da frequência das dezenas.
    """
    df = pd.DataFrame({
        "D1": [1, 2], "D2": [2, 3], "D3": [3, 4], "D4": [4, 5], "D5": [5, 6]
    })
    freq = calcular_frequencia(df)
    assert not freq.empty, "Frequência não foi calculada corretamente!"
    assert set(freq["Dezena"].tolist()) == {"01", "02", "03", "04", "05", "06"}, "Frequência calculada incorretamente!"

def test_pagina_gerador():
    """
    Testa a página do gerador de jogos para garantir que ela carrega sem erros.
    """
    # Simular dados de frequência
    frequencia = pd.DataFrame({
        "Dezena": [f"{i:02}" for i in range(1, 25)],
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
        "D1": [1, 2], "D2": [3, 4], "D3": [5, 6], "D4": [7, 8], "D5": [9, 10]
    })
    frequencia = calcular_frequencia(df)
    assert not frequencia.empty, "Frequência não foi calculada corretamente!"
    assert set(frequencia["Dezena"].tolist()) == {"01", "02", "03", "04", "05", "06", "07", "08", "09", "10"}, \
        "Frequência calculada incorretamente!"

def test_gerar_jogos_otimizados():
    """
    Testa a geração de jogos otimizados para garantir que os jogos gerados estão corretos.
    """
    df = pd.DataFrame({
        "Dezena": [f"{i:02}" for i in range(1, 25)],
        "Frequência": [random.randint(1, 100) for _ in range(1, 25)]
    })
    jogos = gerar_jogos_otimizados(df, num_jogos=2)
    assert len(jogos) == 2, "Número de jogos gerados está incorreto!"
    assert all(len(jogo) == 15 for jogo in jogos), "Cada jogo deve ter 15 dezenas!"
    for jogo in jogos:
        assert all(1 <= int(dezena) <= 25 for dezena in jogo), "Dezenas fora do intervalo permitido!"