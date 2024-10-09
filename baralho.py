from carta import *
from random import randint
class Baralho:
    deck = []

    def __init__(self):
        self.deck = self.gerarValor()

    def gerarValor():
        while True:
            valores = [randint(1, 10) for _ in range(4)]

            contagem = {}
            for valor in valores:
                if valor in contagem:
                    contagem[valor] += 1
                else:
                    contagem[valor] = 1

            if any(contagem[v] > 2 for v in contagem):
                continue

            if 14 <= sum(v for v in valores) <= 30:
                return ["A" if v == 10 else v for v in valores]

