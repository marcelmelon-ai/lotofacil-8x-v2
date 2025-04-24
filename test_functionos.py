import pandas as pd
from ajustes import carregar_dados_excel, preprocessar_dados
from estatisticas import calcular_frequencia
from models import gerar_jogos_otimizados
from paginas.gerador import pagina_gerador
from paginas.estatisticas import pagina_estatisticas

def test_carregar_dados_excel():
    df = carregar_dados_excel("data/resultados.xlsx")
    assert not df.empty, "O DataFrame está vazio!"

def test_preprocessar_dados():
    df = pd.DataFrame({"D1": [1, 2], "D2": [3, 4], "Outros": [5, 6]})
    df_pre = preprocessar_dados(df)
    assert "Outros" not in df_pre.columns, "Coluna irrelevante não foi removida!"

def test_calcular_frequencia():
    df = pd.DataFrame({"D1": [1, 2], "D2": [2, 3]})
    freq = calcular_frequencia(df)
    assert freq["Dezena"].tolist() == ["01", "02", "03"], "Frequência calculada incorretamente!"

def test_pagina_gerador():
    # Simular dados de frequência
    frequencia = pd.DataFrame({"Dezena": ["01", "02", "03"], "Frequência": [10, 20, 30]})
    # Simular sessão do Streamlit
    st.session_state["frequencia"] = frequencia
    pagina_gerador()  # Verificar se a página carrega sem erros

def test_pagina_estatisticas():
    # Simular carregamento de dados
    df = pd.DataFrame({"D1": [1, 2], "D2": [3, 4]})
    frequencia = calcular_frequencia(df)
    assert not frequencia.empty, "Frequência não foi calculada corretamente!"    

def test_gerar_jogos_otimizados():
    df = pd.DataFrame({"Dezena": ["01", "02", "03"], "Frequência": [10, 20, 30]})
    jogos = gerar_jogos_otimizados(df, num_jogos=2)
    assert len(jogos) == 2, "Número de jogos gerados está incorreto!"
    assert all(len(jogo) == 15 for jogo in jogos), "Cada jogo deve ter 15 dezenas!"