from configs import *

class Mesa:
    def __init__(self, player1, player2):
        self.fonte = pygame.font.Font(None, 36)  # Fonte padrão com tamanho 36
        self.cartas_na_mesa = [Carta(None) for _ in range(10)]  # Gera 10 cartas aleatórias sem dono inicial
        self.cartas_jogador1 = []
        self.cartas_jogador2 = []
        self.players = [player1, player2]
        self.turno_atual = 0  # Índice para alternar entre os jogadores

    def desenhar_cartas_na_mesa(self, tela, bg):
        tela.blit(bg, (0, 0))
        largura_tela, altura_tela = tela.get_size()

        largura_carta = self.cartas_na_mesa[0].visual.get_width()
        altura_carta = self.cartas_na_mesa[0].visual.get_height()

        posicao_x_inicial = (largura_tela - (4 * largura_carta + 40)) // 2
        posicao_y_inicial = (altura_tela - (1 * altura_carta + 10)) // 2

        for i, carta in enumerate(self.cartas_na_mesa):
            x = posicao_x_inicial + (i % 5) * largura_carta  # Posição x da carta
            y = posicao_y_inicial + (i // 5) * altura_carta  # Posição y da carta
            carta.rect.center = (x, y)
            tela.blit(carta.visual, carta.rect)

    def desenhar_turno(self, tela):
        jogador_atual = self.players[self.turno_atual]

        turno = f'Vez do Jogador {jogador_atual.numPlayer}'
        texto_renderizado = self.fonte.render(turno, True, (255, 255, 255))  # Branco

        largura_tela = tela.get_width()
        altura_tela = tela.get_height()
        tela.blit(texto_renderizado, (largura_tela // 2 - texto_renderizado.get_width() // 2, altura_tela - 150))

    def selecionar_carta(self, mouse_x, mouse_y):
        for i, carta in enumerate(self.cartas_na_mesa):
            if carta.rect.collidepoint(mouse_x, mouse_y):
                return carta
        return None

    def distribuir_cartas(self, tela, bg, sfxCardPick):
        carta_escolhida = None
        while len(self.cartas_na_mesa) > 0:
            self.desenhar_cartas_na_mesa(tela, bg)
            self.desenhar_turno(tela)
            pygame.display.update()

            jogador_atual = self.players[self.turno_atual]

            carta_escolhida = False
            while not carta_escolhida:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        carta_escolhida = self.selecionar_carta(mouse_x, mouse_y)
                        sfxCardPick.play()

            if carta_escolhida:
                self.cartas_na_mesa.remove(carta_escolhida)

                carta_escolhida.switchDono(jogador_atual)
                jogador_atual.cartas_selecionadas.append(carta_escolhida)

                self.turno_atual = (self.turno_atual + 1) % 2

        tela.blit(bg, (0, 0))
        texto = self.fonte.render(f'Distribuição Concluída', True, (255, 255, 255))
        tela.blit(texto, (tela.get_width() // 2 - texto.get_width() // 2, tela.get_height() - 150))
        pygame.display.update()
        while carta_escolhida is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Verifica se o botão esquerdo foi clicado
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    carta_escolhida = self.selecionar_carta(mouse_x, mouse_y)
                    sfxCardPick.play()

        if carta_escolhida in self.cartas_na_mesa:
            self.cartas_na_mesa.remove(carta_escolhida)

            # Define o dono da carta escolhida
            carta_escolhida.switchDono(jogador_atual)
            jogador_atual.cartas_selecionadas.append(carta_escolhida)

            # Alterna para o próximo jogador
            self.turno_atual = (self.turno_atual + 1) % 2
