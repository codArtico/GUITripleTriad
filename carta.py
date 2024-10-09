import pygame
import os
from random import randint

class Carta:

    @staticmethod
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

    # @staticmethod
    # def lerValores(arquivo):
    #     valores = {}
    #     try:
    #         with open(arquivo, 'r') as dados:
    #             linha = dados.readline().strip()
    #             cima, direita, baixo, esquerda = linha.split('|')
    #             valores['cima'] = int(cima)
    #             valores['direita'] = int(direita)
    #             valores['baixo'] = int(baixo)
    #             valores['esquerda'] = int(esquerda)
    #     except FileNotFoundError:
    #         print(f'Erro: O arquivo {arquivo} não foi encontrado')
    #     except ValueError:
    #         print("Erro: Problema ao processar os dados do arquivo.")
    #     return valores

    def __init__(self):
        self.cor = None
        self.valores = self.gerarValor()
        self.dono = None
        pygame.font.init()
        self.fonte = pygame.font.Font(None, 30)
        self.visual = self.criarCarta()

    def criarCarta(self):
        largura = 200
        altura = 200
        
        # Carrega a imagem do verso da carta
        try:
            desenho = pygame.image.load(os.path.join('imagens', 'versoCartaBlue.png')).convert_alpha()
            # Redimensiona a imagem para o tamanho da carta
            desenho = pygame.transform.smoothscale(desenho, (largura, altura))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem do verso da carta: {e}")
            desenho = pygame.Surface((largura, altura))  # Superfície de fallback
            desenho.fill((0, 0, 0))  # Preenche com preto para indicar erro

        # Cria a superfície da carta
        self.visual = pygame.Surface((largura, altura), pygame.SRCALPHA)

        # Blita a imagem do verso na superfície da carta
        self.visual.blit(desenho, (0, 0))

        # Renderiza os valores na carta usando índices
        cima = self.fonte.render(str(self.valores[0]), True, (255, 255, 255))  # Acesso correto
        direita = self.fonte.render(str(self.valores[1]), True, (255, 255, 255))
        baixo = self.fonte.render(str(self.valores[2]), True, (255, 255, 255))
        esquerda = self.fonte.render(str(self.valores[3]), True, (255, 255, 255))

        # Calcula as posições para desenhar os textos
        posicao_cima = (largura // 2 - cima.get_width() // 2, 40)
        posicao_direita = (largura - direita.get_width() - 55, altura // 2 - direita.get_height() // 2)
        posicao_baixo = (largura // 2 - baixo.get_width() // 2, altura - baixo.get_height() - 40)
        posicao_esquerda = (55, altura // 2 - esquerda.get_height() // 2)

        # Blita os textos na superfície da carta
        self.visual.blit(cima, posicao_cima)
        self.visual.blit(direita, posicao_direita)
        self.visual.blit(baixo, posicao_baixo)
        self.visual.blit(esquerda, posicao_esquerda)

        return self.visual
