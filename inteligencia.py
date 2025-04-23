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

    # Tabelas 1 a 8
    col_base = ['dezenas', 'numero de vez', 'atual', 'último', 'maior já registrado', 'média']
    for i in range(1, 9):
        if f'Tabela {i}' in tabelas:
            df = tabelas[f'Tabela {i}'].copy()
            df = padronizar(df)
            df = df.rename(columns={
                'dezenas': 'Dezena',
                'numero de vez': 'Frequência',
                'atual': 'Atraso',
                'maior já registrado': 'Maior_Atraso'
            })
            df['Dezena'] = df['Dezena'].astype(str).str.zfill(2)
            if dados_ia.empty:
                dados_ia = df[['Dezena', 'Frequência', 'Atraso', 'Maior_Atraso']].copy()
                dados_ia.set_index('Dezena', inplace=True)
            else:
                dados_ia.update(df.set_index('Dezena')[['Frequência', 'Atraso', 'Maior_Atraso']])

    # Tabela 9 – Quantidades por dezena
    if 'Tabela 9' in tabelas:
        df = padronizar(tabelas['Tabela 9'].copy())
        df = df.rename(columns={'dezenas': 'Dezena', 'quantidades': 'Qtd_Sorteios'})
        df['Dezena'] = df['Dezena'].astype(str).str.zfill(2)
        dados_ia['Qtd_Sorteios'] = df.set_index('Dezena')['Qtd_Sorteios']

    # Tabela 10 – Diferença
    if 'Tabela 10' in tabelas:
        df = padronizar(tabelas['Tabela 10'].copy())
        df = df.rename(columns={'dezenas': 'Dezena', 'diferença': 'Diferenca'})
        df['Dezena'] = df['Dezena'].astype(str).str.zfill(2)
        dados_ia['Diferenca'] = df.set_index('Dezena')['Diferenca']

    # Tabela 11 – Atraso total
    if 'Tabela 11' in tabelas:
        df = padronizar(tabelas['Tabela 11'].copy())
        df = df.rename(columns={'dezenas': 'Dezena', 'atraso': 'Atraso_Total'})
        df['Dezena'] = df['Dezena'].astype(str).str.zfill(2)
        dados_ia['Atraso_Total'] = df.set_index('Dezena')['Atraso_Total']

    # Tabela 12 – Pares/Ímpares
    if 'Tabela 12' in tabelas:
        df = padronizar(tabelas['Tabela 12'].copy())
        df = df.rename(columns={
            'quantidade pares': 'Qtd_Pares',
            'quantidade ímpares': 'Qtd_Impares',
            'quantidade de ocorrências': 'Ocorrencias_P_I'
        })
        dados_ia['Qtd_Pares'] = df['Qtd_Pares']
        dados_ia['Qtd_Impares'] = df['Qtd_Impares']
        dados_ia['Ocorrencias_P_I'] = df['Ocorrencias_P_I']

    # Tabela 13 – Primos
    if 'Tabela 13' in tabelas:
        df = padronizar(tabelas['Tabela 13'].copy())
        df = df.rename(columns={'quantidade de primos': 'Qtd_Primos'})
        dados_ia['Qtd_Primos'] = df['Qtd_Primos']

    # Tabela 14 – Múltiplos de 3
    if 'Tabela 14' in tabelas:
        df = padronizar(tabelas['Tabela 14'].copy())
        df = df.rename(columns={'quantidade de múltiplos de 3': 'Qtd_Multiplos3'})
        dados_ia['Qtd_Multiplos3'] = df['Qtd_Multiplos3']

    # Tabela 15 – Fibonacci
    if 'Tabela 15' in tabelas:
        df = padronizar(tabelas['Tabela 15'].copy())
        df = df.rename(columns={'quantidade n. de fibonacci': 'Qtd_Fibonacci'})
        dados_ia['Qtd_Fibonacci'] = df['Qtd_Fibonacci']

    # Tabela 16 – Intervalos
    if 'Tabela 16' in tabelas:
        df = padronizar(tabelas['Tabela 16'].copy())
        df = df.rename(columns={'intervalo': 'Intervalo'})
        dados_ia['Intervalo'] = df['Intervalo']

    # Tabela 17 – Repetidas do concurso anterior
    if 'Tabela 17' in tabelas:
        df = padronizar(tabelas['Tabela 17'].copy())
        df = df.rename(columns={'dezenas repetidas': 'Repetidas'})
        dados_ia['Repetidas'] = df['Repetidas']

    dados_ia = dados_ia.dropna().reset_index()

    st.write("✅ Dados IA completos:", dados_ia)
    return dados_ia

# Função para validar se todas as colunas obrigatórias estão presentes e sem dados inválidos
def validar_colunas(dados_ia):
    colunas_esperadas = {'Frequência', 'Atraso', 'Maior_Atraso'}
    if not colunas_esperadas.issubset(set(dados_ia.columns)):
        st.error("❌ Dados incompletos para treinar o modelo. As colunas obrigatórias são: Frequência, Atraso e Maior_Atraso.")
        st.stop()

    # Verificando se há valores negativos ou nulos nas colunas
    if (dados_ia[['Frequência', 'Atraso', 'Maior_Atraso']] < 0).any().any():
        st.error("❌ Dados inválidos: as colunas 'Frequência', 'Atraso' e 'Maior_Atraso' não podem conter valores negativos.")
        st.stop()
    
    if dados_ia[['Frequência', 'Atraso', 'Maior_Atraso']].isnull().any().any():
        st.error("❌ Dados inválidos: as colunas 'Frequência', 'Atraso' e 'Maior_Atraso' não podem conter valores nulos.")
        st.stop()

# Função aplicar ia para jogos 
def aplicar_ia_para_jogos(X, y):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    # Confirma que colunas certas estão presentes
    colunas_esperadas = ['Media_Frequência', 'Media_Atraso', 'Media_MaiorAtraso']
    if not all(col in X.columns for col in colunas_esperadas):
        raise ValueError(f"❌ Dados incompletos para treinar o modelo. As colunas obrigatórias são: {', '.join(colunas_esperadas)}")

    # Divide os dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X[colunas_esperadas], y, test_size=0.2, random_state=42)

    # Treina modelo de floresta aleatória
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Avaliação
    y_pred = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)

    return modelo, acuracia
    
# Função para treinar o modelo XGBoost
def treinar_modelo_xgb(dados):
    X = dados[['Frequência', 'Atraso', 'Maior_Atraso']]
    y = [1 if freq > dados['Frequência'].median() else 0 for freq in dados['Frequência']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"Acurácia do modelo XGBoost: {accuracy:.2f}")

    return modelo, accuracy, y_test, y_pred

# Função para treinar o modelo Random Forest
def treinar_modelo_rf(dados):
    X = dados[['Frequência', 'Atraso', 'Maior_Atraso']]
    y = [1 if freq > dados['Frequência'].median() else 0 for freq in dados['Frequência']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    y_pred = modelo_rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"Acurácia do modelo Random Forest: {accuracy:.2f}")

    return modelo_rf, accuracy, y_test, y_pred

# Função para treinar o modelo MLP (Multi-Layer Perceptron)
def treinar_modelo_mlp(dados):
    X = dados[['Frequência', 'Atraso', 'Maior_Atraso']]
    y = [1 if freq > dados['Frequência'].median() else 0 for freq in dados['Frequência']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlp = MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=1000, random_state=42)
    mlp.fit(X_train, y_train)

    y_pred = mlp.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"Acurácia do modelo MLP: {accuracy:.2f}")

    return mlp, accuracy, y_test, y_pred

# Função para prever as dezenas mais prováveis com base no modelo
def prever_dezenas(modelo, dados, top_n=15):
    X = dados[['Frequência', 'Atraso', 'Maior_Atraso']]
    probabilidades = modelo.predict_proba(X)[:, 1]
    dados['Probabilidade'] = probabilidades
    dezenas_recomendadas = dados.sort_values(by='Probabilidade', ascending=False).head(top_n)
    return dezenas_recomendadas

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

# Carregar os dados antes de treinar
dados_ia = carregar_e_preparar_dados()

# Selecionar o modelo
modelo_selecionado = st.selectbox("Selecione o modelo:", ['XGBoost', 'Random Forest', 'MLP'])

# Treinar e avaliar o modelo escolhido
if modelo_selecionado == 'XGBoost':
    modelo, accuracy, y_test, y_pred = treinar_modelo_xgb(dados_ia)
elif modelo_selecionado == 'Random Forest':
    modelo, accuracy, y_test, y_pred = treinar_modelo_rf(dados_ia)
else:
    modelo, accuracy, y_test, y_pred = treinar_modelo_mlp(dados_ia)

# Exibir resultados do modelo
st.write(f"Acurácia do modelo {modelo_selecionado}: {accuracy:.2f}")
exibir_graficos_desempenho(y_test, y_pred, modelo_selecionado)

# Prever as dezenas mais prováveis
top_dezenas = prever_dezenas(modelo, dados_ia)

# Exibindo resultados no Streamlit
st.subheader(f"🎯 Dezenas mais prováveis segundo IA ({modelo_selecionado})")
st.dataframe(top_dezenas[['Dezena', 'Probabilidade']])

# Gerar um jogo com base nas top 15
jogo_gerado = sorted(top_dezenas['Dezena'].sample(15).tolist())
st.success(f"Jogo gerado com IA: {', '.join(jogo_gerado)}")

# Exemplo de gráfico de calor com seaborn
fig, ax = plt.subplots()
sns.heatmap(dados_ia.set_index('Dezena'), annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
st.pyplot(fig)
