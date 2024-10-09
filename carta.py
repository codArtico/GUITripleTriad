import pygame
import os

class Carta:

    @staticmethod
    def lerValores(arquivo):
        valores = {}

        try:
            with open(arquivo, 'r') as dados:
                # Lê a linha e separa pelos '|'
                linha = dados.readline().strip()  # Lê a primeira linha
                cima, direita, baixo, esquerda = linha.split('|')  # Divide os valores
                valores['cima'] = int(cima)  # Converte para inteiro
                valores['direita'] = int(direita)
                valores['baixo'] = int(baixo)
                valores['esquerda'] = int(esquerda)

        except FileNotFoundError:
            print(f'Erro: O arquivo {arquivo} não foi encontrado')
        except ValueError:
            print("Erro: Problema ao processar os dados do arquivo.")

        return valores

    def __init__(self):
        self.cor = None
        self.valores = self.lerValores(os.path.join('cartas', 'valoresTeste.txt'))
        self.dono = None
        pygame.font.init()
        self.fonte = pygame.font.Font(None, 36)
        self.visual = self.criarCarta()

    def criarCarta(self):
        largura = 100
        altura = 100
        desenho = pygame.image.load(os.path.join('imagens', 'versoCartaBlue.png'))
        self.visual = pygame.surface.Surface((largura, altura))
        self.visual.blit(desenho, (0, 0))

        cima = self.fonte.render(str(self.valores['cima']), True, (255, 255, 255))
        direita = self.fonte.render(str(self.valores['direita']), True, (255, 255, 255))
        baixo = self.fonte.render(str(self.valores['baixo']), True, (255, 255, 255))
        esquerda = self.fonte.render(str(self.valores['esquerda']), True, (255, 255, 255))

        posicao_cima = (largura // 2 - cima.get_width() // 2, 10)
        posicao_direita = (largura - direita.get_width() - 10, altura // 2 - direita.get_height() // 2)
        posicao_baixo = (largura // 2 - baixo.get_width() // 2, altura - baixo.get_height() - 10)
        posicao_esquerda = (10, altura // 2 - esquerda.get_height() // 2)

        self.visual.blit(cima, posicao_cima)
        self.visual.blit(direita, posicao_direita)
        self.visual.blit(baixo, posicao_baixo)
        self.visual.blit(esquerda, posicao_esquerda)

        return self.visual