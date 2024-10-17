from configs import *

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

class Carta:
    def __init__(self, player, proporcao_posicao=(0.5, 0.5)):
        self.fonte = pygame.font.Font(None, 30)
        self.dono = player
        self.valores = gerarValor()
        self.visual = self.desenhar_carta()

        # Calcula a posição inicial baseada em valores relativos à tela
        x = 1366 * proporcao_posicao[0]
        y = 768 * proporcao_posicao[1]

        self.rect = self.visual.get_rect()  # Define o rect de forma relativa

    def desenhar_carta(self):
        largura, altura = 200, 200
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

        self._renderizar_valores(desenho, largura, altura)
        
        return desenho

    def _renderizar_valores(self, desenho, largura, altura):
        for pos, direcao in zip([(largura // 2, 40), (largura - 55, altura // 2), (largura // 2, altura - 40),
                                 (55, altura // 2)], ['up', 'right', 'down', 'left']):
            texto = self.fonte.render(str(self.valores[direcao]), True, (255, 255, 255))
            desenho.blit(texto, (pos[0] - texto.get_width() // 2, pos[1] - texto.get_height() // 2))

    def desenhar(self, tela):
        # Desenha a carta na tela
        tela.blit(self.visual, self.rect)

        # Desenha o retângulo vermelho sobre a carta
        pygame.draw.rect(tela, (255, 0, 0), self.rect, 2)  # 2 é a largura da borda do retângulo

    def switchDono(self, p):
        self.dono = p
        self.visual = self.desenhar_carta()
        self.rect = self.visual.get_rect(center=self.rect.center)  # Atualiza o rect com a nova imagem
