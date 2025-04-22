import pandas as pd
import requests
from bs4 import BeautifulSoup

# Função para carregar os resultados da planilha Excel
def carregar_resultados_excel(caminho_arquivo):
    return pd.read_excel(caminho_arquivo)

# Função para carregar e nomear todas as 12 tabelas do site Numeromania
def carregar_estatisticas_numeromania():
    url = "https://www.numeromania.com.br/fa9912.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Captura todas as tabelas com a classe esperada
    tabelas_html = soup.find_all('table', {'class': 'tabelaResultado'})
    tabelas = pd.read_html(str(soup))[:12]  # Limita às 12 primeiras

    nomes_tabelas = [
        'Frequencia',
        'Atraso',
        'Maior_Atraso',
        'Duplas_Mais_Frequentes',
        'Trincas_Mais_Frequentes',
        'Quadras_Mais_Frequentes',
        'Quinas_Mais_Frequentes',
        'Senas_Mais_Frequentes',
        'Setes_Mais_Frequentes',
        'Dezenas_Repetidas',
        'Dezenas_Ausentes',
        'Final_Impar_Par'
    ]

    estatisticas = {nome: tabela for nome, tabela in zip(nomes_tabelas, tabelas)}
    return estatisticas

# Função auxiliar para reconstruir estatísticas básicas (caso faltem)
def reconstruir_estatisticas_basicas(planilha):
    col_dezenas = [f'D{i}' for i in range(1, 16)]
    dezenas_str = planilha[col_dezenas].astype(str).apply(lambda x: x.str.zfill(2))
    todas = [f"{i:02}" for i in range(1, 26)]

    estat = []
    for dez in todas:
        freq = (dezenas_str == dez).sum().sum()
        atraso = next((i for i, row in enumerate(dezenas_str[::-1].values) if dez in row), len(planilha))
        estat.append({"Dezena": dez, "Frequência": freq, "Atraso": atraso})

    df = pd.DataFrame(estat)
    return df.set_index("Dezena")

# Função para combinar dados da planilha com as 3 estatísticas principais
def combinar_dados(planilha_excel, estatisticas):
    df = planilha_excel.copy()
    dezenas = [f'D{i}' for i in range(1, 16)]

    # Tenta carregar estatísticas do site; se falhar, usa fallback local
    try:
        freq = estatisticas['Frequencia'].set_index('Dezena')['Frequência']
        atraso = estatisticas['Atraso'].set_index('Dezena')['Atraso']
        maior_atraso = estatisticas['Maior_Atraso'].set_index('Dezena')['Maior Atraso']
    except:
        print("⚠️ Problema ao carregar estatísticas do site. Reconstruindo localmente...")
        reconstruido = reconstruir_estatisticas_basicas(df)
        freq = reconstruido['Frequência']
        atraso = reconstruido['Atraso']
        maior_atraso = pd.Series(0, index=reconstruido.index)  # Não temos como saber o maior atraso localmente

    for dez in dezenas:
        df[f'{dez}_Frequência'] = df[dez].astype(str).str.zfill(2).map(freq)
        df[f'{dez}_Atraso'] = df[dez].astype(str).str.zfill(2).map(atraso)
        df[f'{dez}_MaiorAtraso'] = df[dez].astype(str).str.zfill(2).map(maior_atraso)

    df.dropna(inplace=True)
    return df

# Preparação dos dados para IA (média das 15 dezenas por jogo)
def preparar_dados_ia(df_combined):
    dezenas = [f'D{i}' for i in range(1, 16)]
    col_freq = [f'{d}_Frequência' for d in dezenas]
    col_atraso = [f'{d}_Atraso' for d in dezenas]
    col_ma = [f'{d}_MaiorAtraso' for d in dezenas]

    df_combined['Media_Frequência'] = df_combined[col_freq].mean(axis=1)
    df_combined['Media_Atraso'] = df_combined[col_atraso].mean(axis=1)
    df_combined['Media_MaiorAtraso'] = df_combined[col_ma].mean(axis=1)

    X = df_combined[['Media_Frequência', 'Media_Atraso', 'Media_MaiorAtraso']]
    y = [1 if val > X['Media_Frequência'].median() else 0 for val in X['Media_Frequência']]

    return X, y

# Função principal
def maquininha(caminho_arquivo_excel):
    resultados_excel = carregar_resultados_excel(caminho_arquivo_excel)
    estatisticas = carregar_estatisticas_numeromania()
    dados_combinados = combinar_dados(resultados_excel, estatisticas)
    X, y = preparar_dados_ia(dados_combinados)
    return X, y, estatisticas
