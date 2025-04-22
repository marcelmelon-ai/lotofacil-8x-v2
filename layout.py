import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from ajustes import carregar_dados_excel as carregar_dados
from estatisticas import mostrar_estatisticas


def carregar_dados_e_treinar_modelos(arquivo):
    df = carregar_dados(arquivo)
    if df is not None:
        st.success("Arquivo carregado com sucesso!")
        st.write("Prévia do DataFrame:")
        st.dataframe(df.head())

        X = df[['Frequência', 'Atraso', 'Maior_Atraso']]
        y = [1 if freq > df['Frequência'].median() else 0 for freq in df['Frequência']]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelo_xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        modelo_xgb.fit(X_train, y_train)
        y_pred_xgb = modelo_xgb.predict(X_test)
        accuracy_xgb = accuracy_score(y_test, y_pred_xgb)

        modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
        modelo_rf.fit(X_train, y_train)
        y_pred_rf = modelo_rf.predict(X_test)
        accuracy_rf = accuracy_score(y_test, y_pred_rf)

        mlp = MLPClassifier(hidden_layer_sizes=(50, 25), max_iter=1000, random_state=42)
        mlp.fit(X_train, y_train)
        y_pred_mlp = mlp.predict(X_test)
        accuracy_mlp = accuracy_score(y_test, y_pred_mlp)

        return {
            'xgb': (modelo_xgb, accuracy_xgb, y_test, y_pred_xgb),
            'rf': (modelo_rf, accuracy_rf, y_test, y_pred_rf),
            'mlp': (mlp, accuracy_mlp, y_test, y_pred_mlp),
            'dados': df
        }
    else:
        st.warning("Nenhuma tabela foi carregada.")
        return None


def mostrar_graficos_desempenho(y_test, y_pred, modelo_nome):
    st.subheader(f"📊 Desempenho do Modelo {modelo_nome}")

    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=['Classe 0', 'Classe 1'], yticklabels=['Classe 0', 'Classe 1'])
    ax.set_xlabel('Predição')
    ax.set_ylabel('Real')
    st.pyplot(fig)

    cr = classification_report(y_test, y_pred)
    st.text(cr)


def gerar_jogo(modelo, dados):
    X = dados[['Frequência', 'Atraso', 'Maior_Atraso']]
    probabilidades = modelo.predict_proba(X)[:, 1]
    dados = dados.copy()
    dados['Probabilidade'] = probabilidades
    dezenas_recomendadas = dados.sort_values(by='Probabilidade', ascending=False).head(15)
    return dezenas_recomendadas


def menu_lateral():
    st.sidebar.title("Menu")
    opcoes = ["Início", "Estatísticas", "Gerar Jogos", "Simulação de Jogos", "Sobre"]
    escolha = st.sidebar.radio("Ir para:", opcoes)

    arquivo = st.sidebar.file_uploader("Enviar arquivo Excel", type=["xlsx"])
    if arquivo:
        modelos = carregar_dados_e_treinar_modelos(arquivo)

        if modelos:
            if escolha == "Início":
                st.title("🎯 Bem-vindo ao Lotofácil 8X")
                st.write("Escolha uma opção no menu lateral para começar.")

            elif escolha == "Estatísticas":
                mostrar_estatisticas(arquivo)

            elif escolha == "Gerar Jogos":
                st.subheader("🔮 Gerador de Jogos com IA")
                modelo_selecionado = st.selectbox("Escolha o Modelo", ["XGBoost", "Random Forest", "MLP"])
                if modelo_selecionado == "XGBoost":
                    modelo, accuracy, y_test, y_pred = modelos['xgb']
                elif modelo_selecionado == "Random Forest":
                    modelo, accuracy, y_test, y_pred = modelos['rf']
                else:
                    modelo, accuracy, y_test, y_pred = modelos['mlp']

                st.write(f"Acurácia do Modelo {modelo_selecionado}: **{accuracy:.2%}**")
                mostrar_graficos_desempenho(y_test, y_pred, modelo_selecionado)

                df_dados = modelos['dados']
                top_dezenas = gerar_jogo(modelo, df_dados)
                st.write("Top 15 dezenas mais prováveis:")
                st.dataframe(top_dezenas[['Dezena', 'Probabilidade']])

                jogo_gerado = sorted(top_dezenas['Dezena'].sample(15).tolist())
                st.success(f"Jogo gerado com IA: {', '.join(map(str, jogo_gerado))}")

            elif escolha == "Simulação de Jogos":
                st.subheader("🎲 Simulação de Jogos")
                st.info("Em breve...")

            elif escolha == "Sobre":
                st.subheader("📜 Sobre o Lotofácil 8X")
                st.markdown("""
                Este app utiliza **Inteligência Artificial** e **estatísticas** para analisar e gerar combinações prováveis para a Lotofácil.  
                Desenvolvido por **Marcel Melon** com ❤ e tecnologia.
                """)
        else:
            st.warning("Erro ao carregar ou treinar modelos. Verifique o arquivo.")
    else:
        st.info("Envie um arquivo Excel válido para começar.")
