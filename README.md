# 🎯 Lotofácil 8X

**Geração Inteligente de Jogos com Estatísticas e Inteligência Artificial**

![banner](https://img.shields.io/badge/Projeto-Streamlit-brightgreen) ![GitHub](https://img.shields.io/badge/IA-Ativada-blue) ![Status](https://img.shields.io/badge/status-Em%20Desenvolvimento-yellow)

## 🔍 Descrição

Lotofácil 8X é um aplicativo interativo desenvolvido com **Streamlit** que combina estatísticas históricas e **modelos de IA** para gerar jogos inteligentes da Lotofácil. A plataforma permite ao usuário:

- Enviar arquivos Excel com resultados.
- Visualizar análises e tabelas estatísticas.
- Aplicar inteligência artificial para prever dezenas com base em dados históricos.
- Gerar jogos otimizados.

## 📁 Estrutura do Projeto

```
lotofacil-8x/
│
├── App.py                         # Arquivo principal do Streamlit
├── ajustes.py                     # Funções auxiliares e carregamento de dados
├── estatisticas.py                # Dashboard estatístico com tabelas e gráficos
├── inteligencia.py                # Algoritmos de IA e validação
├── layout.py                      # Layout e menu lateral
├── maquininha.py                  # Geração de features e processamento
├── modelos.py                     # Modelos de ML como XGBoost, RandomForest, MLP
│
├── paginas/
│   ├── __init__.py
│   ├── gerador.py                 # Página para gerar jogos
│   ├── estatisticas.py           # Página de estatísticas
│   ├── ia.py                      # Página de previsões com IA
│   ├── dados_online.py            # Página para leitura de dados externos
│   └── sobre.py                   # Informações sobre o app
│
└── README.md                      # Este arquivo
```

## 🚀 Como Rodar o Projeto

1. Clone o repositório:

```bash
git clone https://github.com/marcelmelon-ai/lotofacil-8x.git
cd lotofacil-8x
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Rode a aplicação:

```bash
streamlit run App.py
```

4. Acesse o navegador:

```
http://localhost:8501
```

## 📦 Requisitos

- Python 3.8+
- Pandas, Scikit-learn, Streamlit, XGBoost, entre outros

> Você pode gerar automaticamente os requisitos com:
```bash
pip freeze > requirements.txt
```

## 📊 Fontes de Dados

- Planilhas da Lotofácil em `.xlsx`
- Dados estatísticos do site [Numeromania](https://www.numeromania.com.br/fa9912.html)

## 🤖 Modelos Utilizados

- XGBoost
- RandomForest
- Multi-Layer Perceptron (MLP)

## ✨ Funcionalidades Futuras

- Integração com banco de dados
- Exportação de jogos para PDF ou TXT
- Otimizações de IA com ensemble learning
- Deploy na Web com GitHub Pages ou alternativa

## 👨‍💻 Desenvolvedor

**Marcel Ribeiro Ártico Melon**  
8X Agro | Inteligência para o Agro e além  
📧 marcelribeiroarticomelon@gmail.com
