import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from ajustes import carregar_tabelas_excel_local


# -----------------------------
# 🔢 Página Estatísticas (Dashboard)
# -----------------------------
@st.cache_data
def carregar_resultados_lotofacil():
    try:
        tabelas = pd.read_excel("tabelas_numeromania.xlsx", sheet_name=None)

        # Supondo que Tabela 1 contém a frequência das dezenas
        df_base = tabelas['Tabela 1'].copy()
        df_base.columns = [col.strip().lower() for col in df_base.columns]
        df_base = df_base.rename(columns={
            'dezenas': 'Dezena',
            'numero de vez': 'Frequência'
        })
        df_base['Dezena'] = df_base['Dezena'].astype(str).str.zfill(2)
        df_base.set_index('Dezena', inplace=True)

        return df_base

    except Exception as e:
        st.error(f"Erro ao carregar dados da Tabela 1: {e}")
        return pd.DataFrame()
    
def mostrar_dashboard_estatistico(df):
    st.title("📊 Dashboard de Estatísticas")
    st.write("Análise completa dos concursos anteriores.")
    
    col1, col2 = st.columns(2)

    with col1:
        freq = df.drop(columns=["Concurso", "Data sorteio", "D1 a D15"], errors='ignore').sum().sort_values(ascending=False)
        st.subheader("Frequência das Dezenas")
        st.bar_chart(freq)

    with col2:
        st.subheader("Ocorrência por posição (em construção)")
        st.info("🔧 Essa funcionalidade está em desenvolvimento.")
        
# -----------------------------
# 📈 Estatísticas por frequência geral
# -----------------------------
import pandas as pd
import streamlit as st

def mostrar_estatisticas(arquivo):
    # Carregar o DataFrame (exemplo, ajuste conforme necessário)
    df = pd.read_csv(arquivo)  # Certifique-se de que o arquivo existe e está correto

    # Verificar se o DataFrame está vazio
    if df.empty:
        raise ValueError("O DataFrame está vazio. Verifique os dados de entrada.")

    # Verificar as colunas do DataFrame
    print("Colunas do DataFrame:", df.columns)

    # Processar o DataFrame
    try:
        freq = df.iloc[:, 1:].apply(pd.Series.value_counts).sum(axis=1).sort_values(ascending=False)
        print(freq)  # Exibir o resultado para depuração
    except Exception as e:
        print(f"Erro ao processar o DataFrame: {e}")
        raise
        
# -----------------------------
# ⏱ Cálculo de atraso
# -----------------------------
def calcular_atraso(dezena, df, col_dezenas):
    for i, row in df[::-1].iterrows():
        if dezena in row[col_dezenas].astype(str).str.zfill(2).values:
            return len(df) - i - 1
    return len(df)


def calcular_maior_atraso(dezena, df, col_dezenas):
    atraso = 0
    max_atraso = 0
    for _, row in df.iterrows():
        if dezena in row[col_dezenas].astype(str).str.zfill(2).values:
            max_atraso = max(max_atraso, atraso)
            atraso = 0
        else:
            atraso += 1
    return max(max_atraso, atraso)


# -----------------------------
# 📊 Processamento do Excel com estatísticas
# -----------------------------
@st.cache_data
def processar_excel_resultados(df_excel):
    col_dezenas = [col for col in df_excel.columns if col.upper().startswith('D')]
    dezenas_flat = df_excel[col_dezenas].values.flatten()
    df_freq = pd.Series(dezenas_flat).value_counts().sort_index().reset_index()
    df_freq.columns = ['Dezena', 'Frequência']

    df_freq['Dezena'] = df_freq['Dezena'].astype(str).str.zfill(2)
    df_freq['Atraso'] = df_freq['Dezena'].apply(lambda d: calcular_atraso(d, df_excel, col_dezenas))
    df_freq['Maior_Atraso'] = df_freq['Dezena'].apply(lambda d: calcular_maior_atraso(d, df_excel, col_dezenas))

    return df_freq.sort_values(by='Dezena')


# -----------------------------
# 🤖 Modelo de previsão com IA (XGBoost)
# -----------------------------
def treinar_modelo_xgb(df_stats):
    X = df_stats[['Frequência', 'Atraso', 'Maior_Atraso']]
    y = [1 if int(d) <= 15 else 0 for d in df_stats['Dezena']]
    model = GradientBoostingClassifier()
    model.fit(X, y)
    return model


def prever_dezenas(model, df_stats):
    X = df_stats[['Frequência', 'Atraso', 'Maior_Atraso']]
    probs = model.predict_proba(X)[:, 1]
    df_stats['Probabilidade'] = probs
    return df_stats.sort_values(by='Probabilidade', ascending=False).head(25)


# -----------------------------
# 📤 Interface da aba de Estatísticas
# -----------------------------
def interface_estatisticas(tab):
    with tab:
        if 'df_excel' in st.session_state:
            df_excel = st.session_state['df_excel']
            df_stats = processar_excel_resultados(df_excel)

            st.success("✅ Estatísticas calculadas com base no histórico.")
            st.dataframe(df_stats)

            st.download_button(
                "📥 Baixar estatísticas em CSV",
                df_stats.to_csv(index=False),
                file_name="estatisticas_lotofacil.csv"
            )

            st.session_state['df_stats'] = df_stats
        else:
            st.warning("⚠️ Por favor, envie um Excel válido na aba '📥 Histórico'.")
