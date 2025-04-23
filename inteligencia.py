import pandas as pd 
import numpy as np
import streamlit as st
from ajustes import carregar_tabelas_excel_local
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import seaborn as sns
import matplotlib.pyplot as plt
from xgboost import XGBClassifier

# Função para preparar os dados para IA
@st.cache_resource
def preparar_dados_para_ia(tabelas):
    dados_ia = pd.DataFrame()

    def padronizar(df):
        df.columns = [col.strip().lower() for col in df.columns]
        return df

    for i in range(1, 9):
        if f'Tabela {i}' in tabelas:
            df = padronizar(tabelas[f'Tabela {i}'].copy())
            df = df.rename(columns={
                'dezenas': 'dezena',
                'numero de vez': 'frequencia',
                'atual': 'atraso',
                'maior já registrado': 'maior_atraso'
            })
            df['dezena'] = df['dezena'].astype(str).str.zfill(2)
            df.set_index('dezena', inplace=True)
            dados_ia = pd.concat([dados_ia, df[['frequencia', 'atraso', 'maior_atraso']]], axis=1)

    if 'Tabela 9' in tabelas:
        df = padronizar(tabelas['Tabela 9'].copy())
        df = df.rename(columns={'dezenas': 'dezena', 'quantidades': 'qtd_sorteios'})
        df['dezena'] = df['dezena'].astype(str).str.zfill(2)
        dados_ia['qtd_sorteios'] = df.set_index('dezena')['qtd_sorteios']

    if 'Tabela 10' in tabelas:
        df = padronizar(tabelas['Tabela 10'].copy())
        df = df.rename(columns={'dezenas': 'dezena', 'diferença': 'diferenca'})
        df['dezena'] = df['dezena'].astype(str).str.zfill(2)
        dados_ia['diferenca'] = df.set_index('dezena')['diferenca']

    if 'Tabela 11' in tabelas:
        df = padronizar(tabelas['Tabela 11'].copy())
        df = df.rename(columns={'dezenas': 'dezena', 'atraso': 'atraso_total'})
        df['dezena'] = df['dezena'].astype(str).str.zfill(2)
        dados_ia['atraso_total'] = df.set_index('dezena')['atraso_total']

    if 'Tabela 12' in tabelas:
        df = padronizar(tabelas['Tabela 12'].copy())
        df = df.rename(columns={
            'quantidade pares': 'qtd_pares',
            'quantidade ímpares': 'qtd_impares',
            'quantidade de ocorrências': 'ocorrencias_p_i'
        })
        dados_ia['qtd_pares'] = df['qtd_pares']
        dados_ia['qtd_impares'] = df['qtd_impares']
        dados_ia['ocorrencias_p_i'] = df['ocorrencias_p_i']

    if 'Tabela 13' in tabelas:
        df = padronizar(tabelas['Tabela 13'].copy())
        df = df.rename(columns={'quantidade de primos': 'qtd_primos'})
        dados_ia['qtd_primos'] = df['qtd_primos']

    if 'Tabela 14' in tabelas:
        df = padronizar(tabelas['Tabela 14'].copy())
        df = df.rename(columns={'quantidade de múltiplos de 3': 'qtd_multiplos3'})
        dados_ia['qtd_multiplos3'] = df['qtd_multiplos3']

    if 'Tabela 15' in tabelas:
        df = padronizar(tabelas['Tabela 15'].copy())
        df = df.rename(columns={'quantidade n. de fibonacci': 'qtd_fibonacci'})
        dados_ia['qtd_fibonacci'] = df['qtd_fibonacci']

    if 'Tabela 16' in tabelas:
        df = padronizar(tabelas['Tabela 16'].copy())
        df = df.rename(columns={'intervalo': 'intervalo'})
        dados_ia['intervalo'] = df['intervalo']

    if 'Tabela 17' in tabelas:
        df = padronizar(tabelas['Tabela 17'].copy())
        df = df.rename(columns={'dezenas repetidas': 'repetidas'})
        dados_ia['repetidas'] = df['repetidas']

    dados_ia = dados_ia.dropna().reset_index()
    st.write("✅ Dados IA completos:", dados_ia)
    return dados_ia

# Validação adaptada

def validar_colunas(dados_ia):
    if dados_ia.isnull().any().any():
        st.error("❌ Existem valores nulos nas colunas das tabelas!")
        st.stop()
    if (dados_ia.select_dtypes(include=['number']) < 0).any().any():
        st.error("❌ Existem valores negativos inválidos nas tabelas!")
        st.stop()

@st.cache_data(ttl=3600)
def carregar_e_preparar_dados():
    tabelas = pd.read_excel("tabelas_numeromania.xlsx", sheet_name=None)
    dados_ia = preparar_dados_para_ia(tabelas)
    validar_colunas(dados_ia)
    return dados_ia

# Função aplicar ia para jogos 
def aplicar_ia_para_jogos(X, y):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    # Divide os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X[colunas_esperadas], y, test_size=0.2, random_state=42) # type: ignore

    # Treina modelo de floresta aleatória
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Avaliação
    y_pred = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)

    return modelo, acuracia

# Função para exibir gráficos de desempenho do modelo
def exibir_graficos_desempenho(y_test, y_pred, modelo_nome):
    st.subheader(f"📊 Desempenho do Modelo {modelo_nome}")

    # Matriz de Confusão
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=['Classe 0', 'Classe 1'], yticklabels=['Classe 0', 'Classe 1'])
    ax.set_xlabel('Predição')
    ax.set_ylabel('Real')
    st.pyplot(fig)

    # Relatório de Classificação
    cr = classification_report(y_test, y_pred)
    st.text(cr)

# Função para carregar e preparar os dados somente após o app estar rodando
@st.cache_data(ttl=3600)
def carregar_e_preparar_dados():
    tabelas = pd.read_excel("tabelas_numeromania.xlsx", sheet_name=None)  # ← lê todas as abas
    dados_ia = preparar_dados_para_ia(tabelas)
    validar_colunas(dados_ia)
    return dados_ia

# Funções de treino com todas as colunas disponíveis

def _preparar_X_y(dados):
    X = dados.drop(columns=['dezena'])
    y = [1 if freq > dados['frequencia'].median() else 0 for freq in dados['frequencia']]
    return X, y

def treinar_modelo_xgb(dados):
    X, y = _preparar_X_y(dados)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return modelo, accuracy, y_test, y_pred

def treinar_modelo_rf(dados):
    X, y = _preparar_X_y(dados)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return modelo, accuracy, y_test, y_pred

def treinar_modelo_mlp(dados):
    X, y = _preparar_X_y(dados)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=1000, random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return modelo, accuracy, y_test, y_pred

def prever_dezenas(modelo, dados, top_n=15):
    X = dados.drop(columns=['dezena'])
    probabilidades = modelo.predict_proba(X)[:, 1]
    dados['probabilidade'] = probabilidades
    return dados.sort_values(by='probabilidade', ascending=False).head(top_n)

def exibir_graficos_desempenho(y_test, y_pred, modelo_nome):
    st.subheader(f"📊 Desempenho do Modelo {modelo_nome}")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=['Classe 0', 'Classe 1'], yticklabels=['Classe 0', 'Classe 1'])
    ax.set_xlabel('Predição')
    ax.set_ylabel('Real')
    st.pyplot(fig)
    st.text(classification_report(y_test, y_pred))

def carregar_e_preparar_dados():
    tabelas = pd.read_excel("tabelas_numeromania.xlsx", sheet_name=None)
    dados_ia = preparar_dados_para_ia(tabelas)
    validar_colunas(dados_ia)
    return dados_ia

# Exibir resultados do modelo
st.write(f"Acurácia do modelo {modelo_selecionado}: {accuracy:.2f}") # type: ignore
exibir_graficos_desempenho(y_test, y_pred, modelo_selecionado) # type: ignore

# Prever as dezenas mais prováveis
top_dezenas = prever_dezenas(modelo, dados_ia) # type: ignore

# Exibindo resultados no Streamlit
st.subheader(f"🎯 Dezenas mais prováveis segundo IA ({modelo_selecionado})") # type: ignore
st.dataframe(top_dezenas[['Dezena', 'Probabilidade']])

# Gerar um jogo com base nas top 15
jogo_gerado = sorted(top_dezenas['Dezena'].sample(15).tolist())
st.success(f"Jogo gerado com IA: {', '.join(jogo_gerado)}")

# Exemplo de gráfico de calor com seaborn
fig, ax = plt.subplots()
sns.heatmap(dados_ia.set_index('Dezena'), annot=True, fmt=".0f", cmap="YlGnBu", ax=ax) # type: ignore
st.pyplot(fig)
