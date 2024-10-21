from configs import *

class Player:
    def __init__(self, nump):
        self.deck = []
        self.pontos = 5
        self.numPlayer = nump
        self.cartasSelecionadas = []  # Atributo para armazenar cartas selecionadas
        self.numCartas = 5

    def downPoint(self):
        self.pontos -= 1

    def upPoint(self):
        self.pontos += 1

    def desenharPontuacao(self, tela, posX, posY):
        """Desenha a pontuação do jogador na tela com uma sombra."""
        font = pygame.font.Font(None, 36)  # Define uma fonte de texto
        textoPontos = f"Player {self.numPlayer}: {self.pontos} pontos"

        # Cria a sombra do texto (deslocada e em cor mais escura)
        sombraSurface = font.render(textoPontos, True, (50, 50, 50))  # Cor da sombra em cinza escuro
        sombraOffsetX, sombraOffsetY = 2, 2  # Deslocamento da sombra
        tela.blit(sombraSurface, (posX + sombraOffsetX, posY + sombraOffsetY))

        # Cria o texto principal
        textoSurface = font.render(textoPontos, True, (255, 255, 255))  # Texto em branco
        tela.blit(textoSurface, (posX, posY))  # Desenha o texto na posição especificada
