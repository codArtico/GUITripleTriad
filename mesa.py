from configs import *
from carta import *

class Mesa:
    def __init__(self, player1, player2):
        self.fonte = pygame.font.Font(None, 36)  # Fonte padrão com tamanho 36
        self.cartasMesa = [Carta(None) for _ in range(10)]  # Gera 10 cartas aleatórias sem dono inicial
        self.cartasP1 = []
        self.cartasP2 = []
        self.players = [player1, player2]
        self.turnoAtual = 0  # Índice para alternar entre os jogadores

    def desenharMesa(self, tela, bg, bgX,bgY):
        tela.blit(bg, (bgX, bgY))
        larguraTela, alturaTela = tela.get_size()

        larguraCarta = self.cartasMesa[0].visual.get_width()
        alturaCarta = self.cartasMesa[0].visual.get_height()

        posicaoXInicial = (larguraTela - (4 * larguraCarta + 40)) // 2
        posicaoYInicial = (alturaTela - (1 * alturaCarta + 10)) // 2

        for i, carta in enumerate(self.cartasMesa):
            x = posicaoXInicial + (i % 5) * larguraCarta  # Posição x da carta
            y = posicaoYInicial + (i // 5) * alturaCarta  # Posição y da carta
            carta.rect.center = (x, y)
            tela.blit(carta.visual, carta.rect)

    def desenharTurno(self, tela):
        jogadorAtual = self.players[self.turnoAtual]

        turno = f'Vez do Jogador {jogadorAtual.numPlayer}'
        textRenderizado = self.fonte.render(turno, True, (255, 255, 255))  # Branco

        larguraTela = tela.get_width()
        alturaTela = tela.get_height()
        tela.blit(textRenderizado, (larguraTela // 2 - textRenderizado.get_width() // 2, alturaTela - 150))

    def selecionarCarta(self, mouseX, mouseY):
        for i, carta in enumerate(self.cartasMesa):
            if carta.rect.collidepoint(mouseX, mouseY):
                return carta
        return None

    def distribuirCartas(self, tela, bg, bgX, bgY, sfxCardPick):
        cartaEscolhida = None
        while len(self.cartasMesa) > 0:
            self.desenharMesa(tela, bg, bgX,bgY)
            self.desenharTurno(tela)
            pygame.display.update()

            jogadorAtual = self.players[self.turnoAtual]

            cartaEscolhida = False
            while not cartaEscolhida:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouseX, mouseY = pygame.mouse.get_pos()
                        cartaEscolhida = self.selecionarCarta(mouseX, mouseY)
                        sfxCardPick.play()

            if cartaEscolhida:
                self.cartasMesa.remove(cartaEscolhida)

                cartaEscolhida.switchDono(jogadorAtual)
                jogadorAtual.cartasSelecionadas.append(cartaEscolhida)

                self.turnoAtual = (self.turnoAtual + 1) % 2

        tela.blit(bg, (0, 0))
        texto = self.fonte.render(f'Distribuição Concluída', True, (255, 255, 255))
        tela.blit(texto, (tela.get_width() // 2 - texto.get_width() // 2, tela.get_height() - 150))
        pygame.display.update()
        while cartaEscolhida is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Verifica se o botão esquerdo foi clicado
                    mouseX, mouseY = pygame.mouse.get_pos()
                    cartaEscolhida = self.selecionarCarta(mouseX, mouseY)
                    sfxCardPick.play()

        if cartaEscolhida in self.cartasMesa:
            self.cartasMesa.remove(cartaEscolhida)

            # Define o dono da carta escolhida
            cartaEscolhida.switchDono(jogadorAtual)
            jogadorAtual.cartasSelecionadas.append(cartaEscolhida)

            # Alterna para o próximo jogador
            self.turnoAtual = (self.turnoAtual + 1) % 2
