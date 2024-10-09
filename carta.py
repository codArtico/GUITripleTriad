import pygame
import os

class Carta:

    @staticmethod
    def lerValores(arquivo):
        valores = {}
        try:
            with open(arquivo, 'r') as dados:
                linha = dados.readline().strip()
                cima, direita, baixo, esquerda = linha.split('|')
                valores['cima'] = int(cima)
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
        self.fonte = pygame.font.Font(None, 30)
        self.visual = self.criarCarta()

    def criarCarta(self):
        largura = 200
        altura = 200
        
        # Carrega a imagem do verso da carta
        try:
            desenho = pygame.image.load(os.path.join('imagens', 'versoCartaBlue.png')).convert_alpha()
            # Redimensiona a imagem para o tamanho da carta
            desenho = pygame.transform.scale(desenho, (largura, altura))
        except pygame.error as e:
            print(f"Erro ao carregar a imagem do verso da carta: {e}")
            desenho = pygame.Surface((largura, altura))  # Superfície de fallback
            desenho.fill((0, 0, 0))  # Preenche com preto para indicar erro

        # Cria a superfície da carta
        self.visual = pygame.Surface((largura, altura), pygame.SRCALPHA)

        # Blita a imagem do verso na superfície da carta
        self.visual.blit(desenho, (0, 0))

        # Renderiza os valores na carta
        cima = self.fonte.render(str(self.valores['cima']), True, (255, 255, 255))
        direita = self.fonte.render(str(self.valores['direita']), True, (255, 255, 255))
        baixo = self.fonte.render(str(self.valores['baixo']), True, (255, 255, 255))
        esquerda = self.fonte.render(str(self.valores['esquerda']), True, (255, 255, 255))

        # Calcula as posições para desenhar os textos
        posicao_cima = (largura // 2 - cima.get_width() // 2, 40)
        posicao_direita = (largura - direita.get_width() - 60, altura // 2 - direita.get_height() // 2)
        posicao_baixo = (largura // 2 - baixo.get_width() // 2, altura - baixo.get_height() - 40)
        posicao_esquerda = (60, altura // 2 - esquerda.get_height() // 2)

        # Blita os textos na superfície da carta
        self.visual.blit(cima, posicao_cima)
        self.visual.blit(direita, posicao_direita)
        self.visual.blit(baixo, posicao_baixo)
        self.visual.blit(esquerda, posicao_esquerda)

        return self.visual