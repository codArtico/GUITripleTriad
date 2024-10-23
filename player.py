from configs import *

class Player:
    """
    Classe que representa um jogador no jogo Triple Triad.
    Cada jogador possui uma pontuação, um número de jogador, cartas selecionadas e um limite de cartas.
    """

    def __init__(self, nump):
        """
        Inicializa um jogador com pontuação inicial de 5 pontos, um número identificador de jogador
        e uma lista vazia de cartas selecionadas. Também define o número máximo de cartas como 5.

        :param nump: O número identificador do jogador (Player 1, Player 2, etc.).
        :type nump: int
        """
        self.pontos = 5  # Pontos iniciais do jogador
        self.numPlayer = nump  # Número identificador do jogador
        self.cartasSelecionadas = []  # Lista para armazenar as cartas selecionadas pelo jogador
        self.numCartas = 5  # Número máximo de cartas que o jogador pode ter

    def downPoint(self):
        """
        Diminui um ponto da pontuação do jogador.
        :param None:
        :return: None:
        """
        self.pontos -= 1

    def upPoint(self):
        """
        Adiciona um ponto à pontuação do jogador.
        :param None:
        :return: None:
        """
        self.pontos += 1

    def desenharPontuacao(self, tela, posX, posY):
        """
        Desenha a pontuação do jogador na tela, exibindo-a com um efeito de sombra.

        :param tela: A superfície na qual o texto será desenhado.
        :type tela: pygame.Surface
        :param posX: A posição X na tela onde o texto será exibido.
        :type posX: int
        :param posY: A posição Y na tela onde o texto será exibido.
        :type posY: int
        :return: None
        """
        font = pygame.font.Font(None, 36)  # Define a fonte e o tamanho do texto
        textoPontos = f"Player {self.numPlayer}: {self.pontos} pontos"  # Texto a ser exibido

        # Cria a sombra do texto (deslocada e com uma cor cinza escuro)
        sombraSurface = font.render(textoPontos, True, (50, 50, 50))  # Sombra em cinza escuro
        sombraOffsetX, sombraOffsetY = 2, 2  # Define o deslocamento da sombra
        tela.blit(sombraSurface, (posX + sombraOffsetX, posY + sombraOffsetY))

        # Cria o texto principal
        textoSurface = font.render(textoPontos, True, (255, 255, 255))  # Texto em branco
        tela.blit(textoSurface, (posX, posY))  # Desenha o texto na posição especificada
