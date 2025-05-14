import random
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
from mostrar_dashboard_estatistico import mostrar_dashboard_estatistico


def carregar_dados_e_treinar_modelos(arquivo):
    """
    Carrega os dados do arquivo Excel e treina modelos de IA.
    """
    df = carregar_dados(arquivo)
    if df is not None:
        st.success("Arquivo carregado com sucesso!")
        st.write("Prévia do DataFrame:")
        st.dataframe(df.head())

        # Identifica colunas das dezenas
        colunas_dezenas = [col for col in df.columns if col.startswith('D')]

        if not colunas_dezenas:
            st.error("❌ Nenhuma coluna de dezenas (D1 a D15) foi encontrada no arquivo.")
            return None

        # Empilha todas as dezenas sorteadas para gerar frequência
        todas_dezenas = pd.concat([df[col] for col in colunas_dezenas])
        todas_dezenas = todas_dezenas.dropna()
        todas_dezenas = todas_dezenas.astype(str).str.strip().str.zfill(2)
        frequencia = todas_dezenas.value_counts().sort_index()

        # Prepara os dados de entrada X e saída y
        dados_ia = pd.DataFrame({
            'dezena': frequencia.index.astype(str).str.zfill(2),
            'frequencia': frequencia.values
        })
        dados_ia['label'] = [1 if f > dados_ia['frequencia'].median() else 0 for f in dados_ia['frequencia']]

        X = dados_ia[['frequencia']]
        y = dados_ia['label']

        # Divisão em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Modelos
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
            'dados': dados_ia
        }
    else:
        st.warning("Nenhuma tabela foi carregada.")


def mostrar_graficos_desempenho(y_test, y_pred, modelo_nome):
    """
    Exibe gráficos de desempenho do modelo.
    """
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
    """
    Gera um jogo com base no modelo treinado.
    """
    colunas_numericas = [col for col in dados.columns if col not in ['dezena', 'label'] and dados[col].dtype in ['int64', 'float64']]

    X = dados[colunas_numericas].copy()

    # Calcula as probabilidades de acerto
    probabilidades = modelo.predict_proba(X)[:, 1]

    dados = dados.copy()
    dados['Probabilidade'] = probabilidades

    # Garante que existe uma coluna 'dezena' para exibição
    if 'dezena' not in dados.columns:
        dados['dezena'] = dados.index.astype(str).str.zfill(2)

    # Seleciona as 15 dezenas mais prováveis
    dezenas_recomendadas = dados.sort_values(by='Probabilidade', ascending=False).head(15)

    return dezenas_recomendadas[['dezena', 'Probabilidade']]

def gerar_jogos_otimizados(resultados, num_jogos=10):
    """
    Gera jogos otimizados com base em estatísticas e fechamento das 20 dezenas mais prováveis.

    Args:
        resultados (pd.DataFrame): DataFrame com os últimos 25 resultados da Lotofácil.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    # Verificar se há pelo menos 25 resultados
    if len(resultados) < 25:
        raise ValueError("É necessário pelo menos 25 resultados para gerar estatísticas.")

    # Estatísticas básicas
    def calcular_estatisticas(dezenas):
        pares = sum(1 for d in dezenas if d % 2 == 0)
        impares = sum(1 for d in dezenas if d % 2 != 0)
        primos = sum(1 for d in dezenas if d in {2, 3, 5, 7, 11, 13, 17, 19, 23})
        fibonacci = sum(1 for d in dezenas if d in {1, 2, 3, 5, 8, 13, 21})
        soma = sum(dezenas)
        return pares, impares, primos, fibonacci, soma

    # Calcular frequência das dezenas nos últimos 25 resultados
    dezenas = [f"D{i}" for i in range(1, 16)]
    frequencia = pd.DataFrame(resultados[dezenas].stack().value_counts(), columns=["Frequência"])
    frequencia.index.name = "Dezena"
    frequencia.reset_index(inplace=True)
    frequencia["Dezena"] = frequencia["Dezena"].astype(int)

    # Ordenar as dezenas pela frequência
    dezenas_ordenadas = frequencia.sort_values(by="Frequência", ascending=False)["Dezena"].tolist()

    # Selecionar as 20 dezenas mais prováveis
    dezenas_mais_provaveis = dezenas_ordenadas[:20]

    # Gerar jogos otimizados
    jogos = []
    for _ in range(num_jogos):
        # Selecionar 15 dezenas aleatórias das 20 mais prováveis
        jogo = sorted(random.sample(dezenas_mais_provaveis, 15))
        
        # Calcular estatísticas do jogo
        pares, impares, primos, fibonacci, soma = calcular_estatisticas(jogo)
        
        # Garantir que o jogo atende critérios estatísticos
        if 6 <= pares <= 9 and 6 <= impares <= 9 and 3 <= primos <= 6 and 2 <= fibonacci <= 5 and 180 <= soma <= 225:
            jogos.append(jogo)

    # Garantir que o número de jogos gerados seja igual ao solicitado
    while len(jogos) < num_jogos:
        jogo = sorted(random.sample(dezenas_mais_provaveis, 15))
        pares, impares, primos, fibonacci, soma = calcular_estatisticas(jogo)
        if 6 <= pares <= 9 and 6 <= impares <= 9 and 3 <= primos <= 6 and 2 <= fibonacci <= 5 and 180 <= soma <= 225:
            jogos.append(jogo)

    return jogos

def gerar_jogos_simples(frequencia, num_jogos=10):
    """
    Gera jogos simples com base na frequência das dezenas.

    Args:
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    dezenas_ordenadas = frequencia.sort_values(by="Frequência", ascending=False)["Dezena"].tolist()
    jogos = [sorted(random.sample(dezenas_ordenadas[:20], 15)) for _ in range(num_jogos)]
    return jogos

def gerar_jogos_ia(modelo, frequencia, num_jogos=10):
    """
    Gera jogos inteligentes com base no modelo treinado.

    Args:
        modelo: Modelo treinado de IA.
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados.
    """
    probabilidades = modelo.predict_proba(frequencia[["Frequência"]])[:, 1]
    frequencia["Probabilidade"] = probabilidades
    dezenas_ordenadas = frequencia.sort_values(by="Probabilidade", ascending=False)["Dezena"].tolist()
    jogos = [sorted(random.sample(dezenas_ordenadas[:20], 15)) for _ in range(num_jogos)]
    return jogos

def gerar_jogos_com_fechamento(frequencia, num_jogos=10):
    """
    Gera jogos com fechamento baseado nas dezenas mais frequentes.

    Args:
        frequencia (pd.DataFrame): DataFrame com a frequência das dezenas.
        num_jogos (int): Número de jogos a serem gerados.

    Returns:
        list: Lista de jogos gerados com fechamento.
    """
    dezenas_ordenadas = frequencia.sort_values(by="Frequência", ascending=False)["Dezena"].tolist()

    jogos = []
    for _ in range(num_jogos):
        jogo = sorted(random.sample(dezenas_ordenadas[:20], 15))  # Seleciona as 20 mais frequentes
        jogos.append(jogo)

    return jogos

def menu_lateral():
    """
    Cria o menu lateral do aplicativo.
    """
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
                mostrar_dashboard_estatistico(modelos['dados'])

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

                if 'dezena' not in top_dezenas.columns:
                    top_dezenas = top_dezenas.reset_index()

                st.subheader(f"🎯 Dezenas mais prováveis segundo IA ({modelo_selecionado})")
                st.dataframe(top_dezenas[['dezena', 'Probabilidade']])

                jogo_gerado = sorted(top_dezenas['dezena'].sample(15).tolist())
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
        st.sidebar.info("📤 Por favor, envie um arquivo Excel para começar.")