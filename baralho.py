from carta import *

class Baralho:
    deck = []

    def __init__(self,arquivo):
        self.deck = self.lerBaralho(arquivo)

    def lerBaralho(self,arquivo):
        deck = []
        try:
            with open(arquivo, 'r') as file:
                for linha in file:
                    cima,direita,baixo,esquerda = linha.strip().split('|')
                    deck.append(Carta(cima,direita,baixo,esquerda))
        
        except FileNotFoundError:
            print(f'Arquivo {arquivo} não encontrado.')
        except ValueError:
            print('Formato de arquivo inválido. O arquivo deve conter as cartas no formato cima|direita|baixo|esquerda.')
        
        return deck

