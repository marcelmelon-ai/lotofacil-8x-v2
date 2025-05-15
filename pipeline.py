import pandas as pd
import os

def carregar_dados_historicos():
    """
    Carrega os dados históricos dos resultados da Lotofácil.
    """
    caminho = "dados/resultados_historicos.xlsx"
    if not os.path.exists(caminho):
        raise FileNotFoundError("Arquivo de resultados históricos não encontrado.")
    return pd.read_excel(caminho)

def carregar_dados_estatisticos():
    """
    Carrega os dados estatísticos.
    """
    caminho = "dados/estatisticas.xlsx"
    if not os.path.exists(caminho):
        raise FileNotFoundError("Arquivo de estatísticas não encontrado.")
    return pd.read_excel(caminho)

def processar_dados_diarios():
    """
    Processa novos resultados diários e atualiza os dados históricos.
    """
    historico = carregar_dados_historicos()
    novos_resultados = pd.read_excel("dados/novos_resultados.xlsx")

    # Validar estrutura dos novos resultados
    if not set(historico.columns).issubset(novos_resultados.columns):
        raise ValueError("Estrutura dos novos resultados inválida.")

    # Atualizar histórico
    historico_atualizado = pd.concat([historico, novos_resultados]).drop_duplicates()
    historico_atualizado.to_excel("dados/resultados_historicos.xlsx", index=False)
    print("Dados históricos atualizados com sucesso.")