from configs import *
from os.path import join
from random import randint
from tabuleiro import *

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
            vetor = ["A" if v == 10 else v for v in valores]
            valores = {
                'up': vetor[0],
                'right': vetor[1],
                'down': vetor[2],
                'left': vetor[3]
            }
            return valores

# def cartaForcada():
#         valores = {}
#         valores['up'] = 4
#         valores['right'] = 4
#         valores['down'] = 4
#         valores['left'] = 4
#         return valores

class Carta:
    def __init__(self, player, posicaoProp=(0.5, 0.5)):
        """
        Inicializa uma instância da classe Carta.

        :param player: O jogador que possui a carta.
        :param posicaoProp: A posição relativa da carta na tela (x, y), padrão é (0.5, 0.5).
        """
        self.fonte = pygame.font.Font(None, 30)
        self.dono = player
        self.valores = gerarValor()
        self.visual = self.desenharCarta(200,200)
        self.selected = False
        self.pos = None
        self.hovered = False

        # Calcula a posição inicial baseada em valores relativos à tela
        x = 1366 * posicaoProp[0]
        y = 768 * posicaoProp[1]

        self.rect = self.visual.get_rect()  # Define o rect de forma relativa

    def desenharCarta(self, largura, altura):
        """
        Desenha a carta com a imagem de fundo correspondente ao dono.

        :param largura: A largura da carta.
        :param altura: A altura da carta.
        :return: A superfície da carta desenhada.
        """
        desenho = None
        try:
            if self.dono is None:
                desenho = pygame.image.load(join('imagens', 'fundoCartaGreen.png')).convert_alpha()
            elif self.dono.numPlayer == 1:
                desenho = pygame.image.load(join('imagens', 'fundoCartaBlue.png')).convert_alpha()
            elif self.dono.numPlayer == 2:
                desenho = pygame.image.load(join('imagens', 'fundoCartaRed.png')).convert_alpha()
            desenho = pygame.transform.smoothscale(desenho, (largura, altura))
        except pygame.error as e:
            desenho = pygame.Surface((largura, altura))
            desenho.fill((0, 0, 0))  # Preenche com preto para indicar erro
        self.renderValores(desenho, largura, altura)
        
        return desenho

    def renderValores(self, desenho, largura, altura):
        """
        Renderiza os valores na carta.

        :param desenho: A superfície da carta onde os valores serão desenhados.
        :param largura: A largura da carta.
        :param altura: A altura da carta.
        """
        for pos, direcao in zip([(largura // 2, 40), (largura - 55, altura // 2), (largura // 2, altura - 40),
                                 (55, altura // 2)], ['up', 'right', 'down', 'left']):
            texto = self.fonte.render(str(self.valores[direcao]), True, (255, 255, 255))
            desenho.blit(texto, (pos[0] - texto.get_width() // 2, pos[1] - texto.get_height() // 2))

    def animaCaptura(self, tela, novoDono, bg, turno, bgX, bgY, tabuleiro):
        """
        Anima a captura de uma carta, mudando sua propriedade.

        :param tela: A tela onde a animação ocorrerá.
        :param novoDono: O novo jogador que irá possuir a carta.
        :param bg: O fundo a ser utilizado durante a animação.
        :param turno: O turno atual do jogo.
        :param bgX: A posição X do fundo.
        :param bgY: A posição Y do fundo.
        :param tabuleiro: O objeto do tabuleiro onde a carta está.
        :return: A instância da carta após a animação.
        """
        r, g, b = 100, 100, 100  # Cores iniciais

        # Animação
        for i in range(10):  # 10 frames para a animação
            if i == 5:
                self.switchDono(novoDono)  # Troca de dono quando i atinge 5
                r, g, b = 255, 255, 255
            if i <= 5:
                r = min(r + 30, 255)  # Garante que não passe de 255
                g = min(g + 30, 255) 
                b = min(b + 30, 255)
            else:
                r = max(r - 30, 0)  # Garante que não fique abaixo de 0
                g = max(g - 30, 0)
                b = max(b - 30, 0)

            # Desenha a carta com novo tamanho
            self.visual = self.desenharCarta(175, 175)
            self.visual.fill((r, g, b), special_flags=pygame.BLEND_RGB_ADD)

            # Atualiza o rect da carta
            self.rect = self.visual.get_rect(center=self.rect.center)  # Atualiza o rect
            
            # Limpa a tela e desenha
            self.limparTela(tabuleiro, bg, turno, bgX, bgY)
            self.desenhar(tela)  # Desenha a carta
            pygame.display.flip()
            pygame.time.delay(1)  # Atraso para suavizar a animação

        # Retorna ao tamanho original
        self.visual = self.desenharCarta(200, 200)
        return self

    def desenhar(self, tela):
        """
        Desenha a carta na tela.

        :param tela: A tela onde a carta será desenhada.
        """
        tela.blit(self.visual, self.rect)

    def switchDono(self, p):
        """
        Troca o dono da carta e atualiza sua visualização.

        :param p: O novo jogador que irá possuir a carta.
        """
        self.dono = p
        self.visual = self.desenharCarta(200,200)
        self.rect = self.visual.get_rect(center=self.rect.center)  # Atualiza o rect com a nova imagem

    def animarMovimento(self, tela, posIni, posFim, bg, turno, bgX, bgY, tabuleiro, duracao=10, fps=120):
        """
        Anima o movimento da carta de uma posição inicial para uma posição final.

        :param tela: A tela onde a animação ocorrerá.
        :param posIni: A posição inicial da carta como (x, y).
        :param posFim: A posição final da carta como (x, y).
        :param bg: O fundo a ser utilizado durante a animação.
        :param turno: O turno atual do jogo.
        :param bgX: A posição X do fundo.
        :param bgY: A posição Y do fundo.
        :param tabuleiro: O objeto do tabuleiro onde a carta está.
        :param duracao: A duração da animação em quadros (padrão é 10).
        :param fps: Frames por segundo para controlar a fluidez da animação (padrão é 120).
        """
        xIni, yIni = posIni
        xFim, yFim = posFim

        clock = pygame.time.Clock()  # Inicializa o controle de tempo do Pygame

        # Multiplicador de velocidade para mover a carta mais rápido, mantendo a suavidade
        velocidade = 1  # Você pode ajustar esse valor para controlar a rapidez do movimento

        for i in range(duracao + 1):
            self.limparTela(tabuleiro, bg, turno, bgX, bgY)
            
            # Calcula a posição atual da carta usando interpolação linear, ajustando a velocidade
            progresso = min(1, i * velocidade / duracao)  # Mantém o progresso entre 0 e 1
            xAtual = xIni + (xFim - xIni) * progresso
            yAtual = yIni + (yFim - yIni) * progresso
            if xAtual == xFim and yAtual == yFim:
                break  # Sai do loop se a posição atual for igual à final

            # Atualiza a posição do rect da carta para a nova posição
            self.rect.topleft = (xAtual, yAtual)

            # Desenha a carta na nova posição
            self.desenhar(tela)
            pygame.display.flip()

            clock.tick(fps)  # Controla a taxa de quadros por segundo para manter a fluidez

    def limparTela(self, tabuleiro, bg, turno, bgX, bgY):
        """
        Limpa a tela desenhando o tabuleiro e o fundo.

        :param tabuleiro: O objeto do tabuleiro que deve ser desenhado.
        :param bg: O fundo a ser utilizado.
        :param turno: O turno atual do jogo.
        :param bgX: A posição X do fundo.
        :param bgY: A posição Y do fundo.
        """
        tabuleiro.desenharTabuleiro(bg, turno, bgX, bgY)