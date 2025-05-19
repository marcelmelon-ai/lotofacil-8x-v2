import pandas as pd
import os

# Caminhos dos arquivos
ARQUIVO_HISTORICO = "dados/resultados_historicos.xlsx"
ARQUIVO_NOVOS = "dados/novos_resultados.xlsx"
ARQUIVO_ESTATS = "dados/estatisticas.xlsx"

def carregar_planilha(caminho):
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    return pd.read_excel(caminho)

def salvar_planilha(df, caminho):
    df.to_excel(caminho, index=False)

def atualizar_historico():
    """
    Atualiza os dados históricos com novos resultados (sem duplicatas).
    """
    historico = carregar_planilha(ARQUIVO_HISTORICO)
    novos = carregar_planilha(ARQUIVO_NOVOS)

    # Verifica se os novos resultados têm as mesmas colunas
    if not set(historico.columns).issubset(novos.columns):
        raise ValueError("Estrutura dos novos resultados não compatível com o histórico.")

    # Atualiza histórico
    atualizado = pd.concat([historico, novos], ignore_index=True)
    atualizado = atualizado.drop_duplicates().sort_values(by='Concurso')

    salvar_planilha(atualizado, ARQUIVO_HISTORICO)
    print("✅ Histórico atualizado com sucesso.")

    return atualizado

def gerar_estatisticas(historico):
    """
    Gera estatísticas com base no histórico atualizado.
    """
    dezenas = [col for col in historico.columns if col not in ['Concurso', 'Data']]

    estatisticas = pd.DataFrame(columns=['Dezena', 'Frequência'])

    # Conta a frequência de cada dezena
    todas = historico[dezenas].values.flatten()
    contagem = pd.Series(todas).value_counts().sort_index()
    estatisticas['Dezena'] = contagem.index
    estatisticas['Frequência'] = contagem.values

    salvar_planilha(estatisticas, ARQUIVO_ESTATS)
    print("📊 Estatísticas geradas com sucesso.")

    return estatisticas

def main():
    historico_atualizado = atualizar_historico()
    gerar_estatisticas(historico_atualizado)

if __name__ == "__main__":
    main()