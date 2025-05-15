@st.cache_data
def calcular_frequencia(resultados):
    """
    Calcula a frequência de cada dezena nos resultados fornecidos.

    Args:
        resultados (list): Lista de listas com os resultados da Lotofácil.

    Returns:
        list: Lista com a frequência de cada dezena.
    """
    frequencia = [0] * 25
    for resultado in resultados:
        for dezena in resultado:
            frequencia[dezena - 1] += 1
    return frequencia