from configs import *
from carta import *


class Mesa:
    def __init__(self, player1, player2):
        """
        Inicializa a classe Mesa.

        :param player1: O primeiro jogador (instância de Player).
        :param player2: O segundo jogador (instância de Player).
        """
        self.fonte = pygame.font.Font(None, 36)  # Fonte padrão com tamanho 36
        self.cartasMesa = []
        self.quantCartas = 10
        self.cartasP1 = []
        self.cartasP2 = []
        self.players = [player1, player2]
        self.turnoAtual = 0  # Índice para alternar entre os jogadores

    def desenharMesa(self, tela, bg, bgX, bgY):
        """
        Desenha a mesa e as cartas na tela.

        :param tela: A superfície onde a mesa será desenhada (instância de pygame.Surface).
        :param bg: A imagem de fundo da mesa (instância de pygame.Surface).
        :param bgX: A coordenada X para desenhar o fundo.
        :param bgY: A coordenada Y para desenhar o fundo.
        :return: None
        """
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

    @staticmethod
    def desenharTurno(tela, p1, p2, turnoAtual, verificador, bgLetras):
        """
        Desenha o turno atual na tela.

        :param tela: A superfície onde o turno será desenhado (instância de pygame.Surface).
        :param p1: O primeiro jogador (instância de Player).
        :param p2: O segundo jogador (instância de Player).
        :param turnoAtual: O índice do jogador atual (0 ou 1).
        :param verificador: Booleano para verificar se o turno deve ser destacado.
        :param bgLetras: A imagem de fundo para o texto (instância de pygame.Surface).
        :return: None
        """
        players = [p1, p2]
        fonte = pygame.font.Font(None, 36)

        jogadorAtual = players[turnoAtual]

        turno = f'Vez do Jogador {jogadorAtual.numPlayer}'
        textRenderizado = fonte.render(turno, True, (255, 255, 255))

        larguraTela = tela.get_width()
        alturaTela = tela.get_height()

        if verificador:
            tela.blit(textRenderizado, (larguraTela // 2 - textRenderizado.get_width() // 2 - 10, alturaTela - 150))
        else:
            tela.blit(bgLetras, ((larguraTela // 2 - textRenderizado.get_width() // 2 - 40, alturaTela - 65)))
            tela.blit(textRenderizado, (larguraTela // 2 - textRenderizado.get_width() // 2 - 10, alturaTela - 50))

    def selecionarCarta(self, mouseX, mouseY):
        """
        Seleciona uma carta na mesa com base na posição do mouse.

        :param mouseX: A coordenada X do mouse.
        :param mouseY: A coordenada Y do mouse.
        :return: A carta selecionada (instância de Carta) ou None se nenhuma carta for selecionada.
        """
        for i, carta in enumerate(self.cartasMesa):
            if carta.rect.collidepoint(mouseX, mouseY):
                return carta
        return None
    @staticmethod
    def confirmPlayer(tela,turno,bg,bgX,bgY):
        font = pygame.font.Font(None, 36)
        txt = f'Player {turno + 1}, clique na tela para continuar!'
        txt = font.render(txt, True, (255, 255, 255))
        tela.blit(bg, (bgX, bgY))
        dark = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        dark.fill(pygame.Color(0, 0, 0))
        dark.set_alpha(int(255 / 100 * 70))  # Para editar em porcentagem
        tela.blit(dark, (0, 0))
        tela.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, ALTURA_TELA // 2 - txt.get_height() // 2))
        return tela
        
    def distribuirCartas(self, tela, bg, bgX, bgY, sfxCardPick, p1, p2, bgLetras):
        """
        Distribui cartas entre os jogadores.

        :param tela: A superfície onde a distribuição será realizada (instância de pygame.Surface).
        :param bg: A imagem de fundo da mesa (instância de pygame.Surface).
        :param bgX: A coordenada X para desenhar o fundo.
        :param bgY: A coordenada Y para desenhar o fundo.
        :param sfxCardPick: O efeito sonoro para a seleção de cartas (instância de pygame.mixer.Sound).
        :param p1: O primeiro jogador (instância de Player).
        :param p2: O segundo jogador (instância de Player).
        :param bgLetras: A imagem de fundo para o texto (instância de pygame.Surface).
        :return: None
        """
        cartaEscolhida = None
        key = True
        font = pygame.font.Font(None, 36)
        while self.quantCartas > 0:
            while key == False:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        key = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                self.confirmPlayer(tela,self.turnoAtual,bg,bgX,bgY)
                pygame.display.update()
            key = False
            self.cartasMesa = [Carta(None) for _ in range(self.quantCartas)]
            self.desenharMesa(tela, bg, bgX, bgY)
            self.desenharTurno(tela, p1, p2, self.turnoAtual, True, bgLetras)
            pygame.display.update()

            jogadorAtual = self.players[self.turnoAtual]

            cartaEscolhida = False
            while not cartaEscolhida:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print('Pygame recebeu o esc')
                            pygame.quit()
                            exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouseX, mouseY = pygame.mouse.get_pos()
                        cartaEscolhida = self.selecionarCarta(mouseX, mouseY)
                        

            if cartaEscolhida:
                self.quantCartas -= 1
                sfxCardPick.play()
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
                if event.type == pygame.K_ESCAPE:
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
