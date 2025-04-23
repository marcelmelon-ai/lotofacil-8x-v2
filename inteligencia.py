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

    try:
        df_freq = tabelas["Tabela 1"].copy()
        df_freq.columns = ['Dezena', 'Frequência']
        df_freq['Dezena'] = df_freq['Dezena'].astype(str).str.zfill(2)
        df_freq['Frequência'] = pd.to_numeric(df_freq['Frequência'], errors='coerce')
        dados_ia = df_freq.set_index('Dezena')
    except Exception as e:
        st.error("Erro ao carregar Tabela 1: Frequência")

    try:
        df_atraso = tabelas["Tabela 2"].copy()
        df_atraso.columns = ['Dezena', 'Atraso']
        df_atraso['Dezena'] = df_atraso['Dezena'].astype(str).str.zfill(2)
        df_atraso['Atraso'] = pd.to_numeric(df_atraso['Atraso'], errors='coerce')
        dados_ia['Atraso'] = df_atraso.set_index('Dezena')['Atraso']
    except Exception as e:
        st.error("Erro ao carregar Tabela 2: Atraso")

    try:
        df_maior_atraso = tabelas["Tabela 3"].copy()
        df_maior_atraso.columns = ['Dezena', 'Maior_Atraso']
        df_maior_atraso['Dezena'] = df_maior_atraso['Dezena'].astype(str).str.zfill(2)
        df_maior_atraso['Maior_Atraso'] = pd.to_numeric(df_maior_atraso['Maior_Atraso'], errors='coerce')
        dados_ia['Maior_Atraso'] = df_maior_atraso.set_index('Dezena')['Maior_Atraso']
    except Exception as e:
        st.error("Erro ao carregar Tabela 3: Maior Atraso")

    dados_ia = dados_ia.dropna()
    return dados_ia.reset_index()

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
    try:
        # Tenta carregar as tabelas da Numeromania
        tabelas = carregar_tabelas_numeromania()
        
        # Garante que o conteúdo necessário foi encontrado
        if not tabelas or 'Tabela_01' not in tabelas or 'Tabela_02' not in tabelas or 'Tabela_03' not in tabelas:
            st.warning("As tabelas necessárias da Numeromania não foram carregadas corretamente.")
            return pd.DataFrame()

        # Prepara os dados
        dados_ia = preparar_dados_para_ia(tabelas)

        # Verifica as colunas obrigatórias
        validar_colunas(dados_ia)

        return dados_ia
    
    except Exception as e:
        st.error(f"Erro ao carregar e preparar os dados da IA: {e}")
        return pd.DataFrame()

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
