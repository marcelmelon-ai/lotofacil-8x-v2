import pytest
import pandas as pd

from app import (
    is_prime,
    is_fibonacci,
    atende_filtros,
    gerar_jogos_filtrados,
    calcular_estatisticas_jogo,
    treinar_modelo,
)

def test_is_prime():
    assert not is_prime(1)
    assert is_prime(2)
    assert is_prime(3)
    assert not is_prime(4)
    assert is_prime(13)
    assert not is_prime(15)

def test_is_fibonacci():
    assert is_fibonacci(1)
    assert is_fibonacci(2)
    assert is_fibonacci(3)
    assert is_fibonacci(5)
    assert not is_fibonacci(4)
    assert not is_fibonacci(6)
    assert is_fibonacci(21)

def test_atende_filtros_true():
    # jogo: 7 pares, 5 primos, 5 múltiplos de 3, 4 fibonacci, soma 180, 9 repetidas
    jogo = [2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 17, 18, 20, 21, 22]
    ultimo_resultado = [2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 17, 18, 20, 21, 25]
    assert atende_filtros(jogo, ultimo_resultado)

def test_atende_filtros_false():
    # jogo: soma too low, not enough pares
    jogo = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 4, 6]
    ultimo_resultado = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 1, 3, 5]
    assert not atende_filtros(jogo, ultimo_resultado)

def test_gerar_jogos_filtrados():
    ultimo_resultado = list(range(1, 16))
    jogos = gerar_jogos_filtrados(ultimo_resultado, n_jogos=2)
    assert len(jogos) == 2
    for jogo in jogos:
        assert len(jogo) == 15
        assert all(1 <= d <= 25 for d in jogo)

def test_calcular_estatisticas_jogo():
    jogo = [2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 17, 18, 20, 21, 22]
    ultimo_resultado = [2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 17, 18, 20, 21, 25]
    stats = calcular_estatisticas_jogo(jogo, ultimo_resultado)
    assert len(stats) == 7
    assert stats[0] == len([d for d in jogo if d % 2 == 0])  # pares
    assert stats[1] == 15 - stats[0]  # impares
    assert stats[2] == len([d for d in jogo if is_prime(d)])  # primos
    assert stats[3] == len([d for d in jogo if d % 3 == 0])  # mult3
    assert stats[4] == len([d for d in jogo if is_fibonacci(d)])  # fib
    assert stats[5] == sum(jogo)  # soma
    assert stats[6] == len(set(jogo).intersection(set(ultimo_resultado)))  # repetidas

def test_treinar_modelo(tmp_path):
    # Create a simple feedback DataFrame
    data = {
        "Pares": [7, 8, 6],
        "Ímpares": [8, 7, 9],
        "Primos": [5, 6, 4],
        "Múltiplos de 3": [5, 4, 6],
        "Fibonacci": [4, 3, 5],
        "Soma": [180, 200, 210],
        "Repetidas": [9, 8, 10],
        "Acertos": [10, 11, 9]
    }
    df_feedback = pd.DataFrame(data)
    model = treinar_modelo(df_feedback)
    assert model is not None
    # Test prediction shape
    X = df_feedback[["Pares", "Ímpares", "Primos", "Múltiplos de 3", "Fibonacci", "Soma", "Repetidas"]]
    preds = model.predict(X)
    assert len(preds) == len(df_feedback)
    