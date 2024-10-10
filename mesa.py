import pygame
from carta import *
from random import choice

class Mesa:
    def __init__(self, player1, player2):
        self.cartas_na_mesa = [Carta(None) for _ in range(10)]  # Gera 10 cartas aleatórias sem dono inicial
        self.cartas_jogador1 = []
        self.cartas_jogador2 = []
        self.players = [player1, player2]
        self.turno_atual = 0  # Índice para alternar entre os jogadores
        pygame.font.init()  # Inicializa o módulo de fonte

    def desenhar_cartas_na_mesa(self, tela, bg):
        tela.blit(bg, (0, 0))
        # Define as dimensões da tela
        largura_tela = tela.get_width()
        
        # Define a largura e altura de uma carta
        largura_carta = self.cartas_na_mesa[0].visual.get_width()  # Supondo que todas as cartas tenham a mesma largura
        altura_carta = self.cartas_na_mesa[0].visual.get_height()  # Supondo que todas as cartas tenham a mesma altura

        # Calcula a posição inicial para centralizar as cartas
        posicao_x_inicial = (largura_tela - 5 * largura_carta) // 2  # 5 cartas em linha
        posicao_y_inicial = (tela.get_height() - 2 * altura_carta) // 2  # Centraliza verticalmente em duas linhas

        # Desenha as cartas restantes na mesa
        for i, carta in enumerate(self.cartas_na_mesa):
            x = posicao_x_inicial + (i % 5) * largura_carta  # Posição x da carta
            y = posicao_y_inicial + (i // 5) * altura_carta  # Posição y da carta
            tela.blit(carta.visual, (x, y))

    def desenhar_turno(self, tela):
        # Seleciona a fonte e tamanho
        font = pygame.font.Font(None, 48)  # Fonte padrão com tamanho 36
        jogador_atual = self.players[self.turno_atual]
        
        # Cria o texto do turno
        texto_turno = f"Vez do Jogador {jogador_atual.numPlayer}"  # Altere conforme necessário
        texto_renderizado = font.render(texto_turno, True, (255, 255, 255))  # Branco

        # Desenha o texto na tela
        largura_tela = tela.get_width()
        altura_tela = tela.get_height()
        posicao_texto = (largura_tela // 2 - texto_renderizado.get_width() // 2, altura_tela - 150)  # Centraliza horizontalmente na parte inferior
        tela.blit(texto_renderizado, posicao_texto)

    def selecionar_carta(self, mouse_x, mouse_y):
        # Obtem a largura e altura da carta
        largura_carta = self.cartas_na_mesa[0].visual.get_width()
        altura_carta = self.cartas_na_mesa[0].visual.get_height()
        
        # Calcula a posição inicial para centralizar as cartas
        largura_tela = pygame.display.get_surface().get_width()
        posicao_x_inicial = (largura_tela - 5 * largura_carta) // 2
        
        for i, carta in enumerate(self.cartas_na_mesa):
            carta_rect = carta.visual.get_rect(topleft=(posicao_x_inicial + (i % 5) * largura_carta,
                                                          (i // 5) * altura_carta + (pygame.display.get_surface().get_height() - 2 * altura_carta) // 2))  # Ajuste para a posição y
            if carta_rect.collidepoint(mouse_x, mouse_y):
                return carta
        return None

    def distribuir_cartas(self, tela, bg, sfxCardPick):
        while len(self.cartas_na_mesa) > 0:
            # Desenha as cartas e o turno atual
            self.desenhar_cartas_na_mesa(tela, bg)
            self.desenhar_turno(tela)
            pygame.display.update()

            jogador_atual = self.players[self.turno_atual]
            print(f"Vez do jogador {jogador_atual.numPlayer} escolher uma carta.")

            carta_escolhida = None
            while carta_escolhida is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Verifica se o botão esquerdo foi clicado
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        carta_escolhida = self.selecionar_carta(mouse_x, mouse_y)
                        sfxCardPick.play()

            if carta_escolhida:  # Apenas prossegue se uma carta foi escolhida
                # Esconde a carta escolhida
                self.cartas_na_mesa.remove(carta_escolhida)

                # Define o dono da carta escolhida
                carta_escolhida.switchDono(jogador_atual)
                jogador_atual.cartas_selecionadas.append(carta_escolhida)

                # Alterna para o próximo jogador
                self.turno_atual = (self.turno_atual + 1) % 2

        print("Distribuição de cartas concluída!")
