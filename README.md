# 🎯 Lotofácil 8X

**Geração Inteligente de Jogos com Estatísticas e Inteligência Artificial**

## 📋 Descrição do Projeto

O **Lotofácil 8X** é um aplicativo desenvolvido em Python que utiliza estatísticas e inteligência artificial para gerar jogos otimizados da Lotofácil. O projeto analisa dados históricos de resultados e estatísticas para criar combinações inteligentes, aumentando as chances de acerto.

## 🚀 Funcionalidades

- **Dashboard Estatístico**: Visualize a frequência das dezenas, atrasos e outras análises.
- **Gerador de Jogos**: Crie combinações otimizadas com base em dados estatísticos.
- **Simulação de Jogos**: Teste combinações geradas contra resultados históricos.
- **IA e Previsões**: Treine modelos de inteligência artificial para prever dezenas mais prováveis.
- **Importação de Dados Online**: (Em breve) Carregue dados diretamente da internet.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Bibliotecas**:
  - [Streamlit](https://streamlit.io/) - Interface interativa
  - [Pandas](https://pandas.pydata.org/) - Manipulação de dados
  - [Scikit-learn](https://scikit-learn.org/) - Modelos de aprendizado de máquina
  - [XGBoost](https://xgboost.readthedocs.io/) - Algoritmos de boosting
  - [Matplotlib](https://matplotlib.org/) e [Seaborn](https://seaborn.pydata.org/) - Visualização de dados
  - [OpenPyXL](https://openpyxl.readthedocs.io/) - Manipulação de arquivos Excel

## 📂 Estrutura do Projeto
### Revisão do README.md

Aqui está uma versão revisada e mais detalhada do README.md para o projeto:

```markdown
# 🎯 Lotofácil 8X

**Geração Inteligente de Jogos com Estatísticas e Inteligência Artificial**

## 📋 Descrição do Projeto

O **Lotofácil 8X** é um aplicativo desenvolvido em Python que utiliza estatísticas e inteligência artificial para gerar jogos otimizados da Lotofácil. O projeto analisa dados históricos de resultados e estatísticas para criar combinações inteligentes, aumentando as chances de acerto.

## 🚀 Funcionalidades

- **Dashboard Estatístico**: Visualize a frequência das dezenas, atrasos e outras análises.
- **Gerador de Jogos**: Crie combinações otimizadas com base em dados estatísticos.
- **Simulação de Jogos**: Teste combinações geradas contra resultados históricos.
- **IA e Previsões**: Treine modelos de inteligência artificial para prever dezenas mais prováveis.
- **Importação de Dados Online**: (Em breve) Carregue dados diretamente da internet.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3
- **Bibliotecas**:
  - [Streamlit](https://streamlit.io/) - Interface interativa
  - [Pandas](https://pandas.pydata.org/) - Manipulação de dados
  - [Scikit-learn](https://scikit-learn.org/) - Modelos de aprendizado de máquina
  - [XGBoost](https://xgboost.readthedocs.io/) - Algoritmos de boosting
  - [Matplotlib](https://matplotlib.org/) e [Seaborn](https://seaborn.pydata.org/) - Visualização de dados
  - [OpenPyXL](https://openpyxl.readthedocs.io/) - Manipulação de arquivos Excel

## 📂 Estrutura do Projeto

```
lotofacil-8x/
│
├── app.py                     # Arquivo principal do Streamlit
├── ajustes.py                 # Funções auxiliares (carregamento e pré-processamento de dados)
├── estatisticas.py            # Processamento e análise estatística
├── inteligencia.py            # Algoritmos de IA e validação
├── models.py                  # Modelos de IA e geração de jogos
├── paginas/                   # Páginas do Streamlit
│   ├── __init__.py
│   ├── gerador.py
│   ├── estatisticas.py
│   ├── ia.py
│   ├── dados_online.py
│   └── sobre.py
├── data/                      # Dados de entrada
│   ├── resultados.xlsx
│   ├── estatisticas.xlsx
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação
```

## ⚙️ Como Executar o Projeto

### Pré-requisitos

- Python 3 instalado
- Dependências listadas no `requirements.txt`

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/lotofacil-8x.git
   cd lotofacil-8x
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

4. Acesse o aplicativo no navegador em: [http://localhost:8501](http://localhost:8501)

## 🧪 Testes

Para executar os testes unitários, use o comando:

```bash
pytest test_functionos.py
```

## 📈 Exemplos de Uso

- **Dashboard Estatístico**: Carregue os dados históricos e visualize gráficos de frequência e atraso.
- **Gerador de Jogos**: Gere combinações otimizadas com base em análises estatísticas.
- **IA e Previsões**: Treine modelos de IA para prever as dezenas mais prováveis.

## 📝 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.

## 👨‍💻 Autor

- **Seu Nome** - [GitHub](https://github.com/seu-usuario)
```

---

### Revisão do requirements.txt

Aqui está uma versão revisada e organizada do requirements.txt:

```plaintext
# Bibliotecas para interface
streamlit

# Manipulação de dados
pandas
numpy

# Visualização de dados
matplotlib
seaborn

# Manipulação de arquivos Excel
openpyxl

# Aprendizado de máquina
scikit-learn
xgboost

# Web scraping (opcional, para dados online)
beautifulsoup4
requests
lxml
```

---

### **Próximos Passos**
1. **Atualizar o README.md com links e informações específicas do projeto.**
2. **Testar o requirements.txt para garantir que todas as dependências estão corretas.**
3. **Executar o aplicativo e validar a funcionalidade completa.**