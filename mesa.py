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

    def desenhar_cartas_na_mesa(self, tela,bg):
        tela.blit(bg,(0,0))
        # Desenha as cartas restantes na mesa
        for i, carta in enumerate(self.cartas_na_mesa):
            x = 50 + (i % 5) * 210  # Calcula a posição x
            y = 50 + (i // 5) * 250  # Calcula a posição y
            tela.blit(carta.visual, (x, y))

    def selecionar_carta(self, mouse_x, mouse_y):
        for carta in self.cartas_na_mesa:
            # Verifica se a carta foi clicada
            carta_rect = carta.visual.get_rect(topleft=(50 + self.cartas_na_mesa.index(carta) % 5 * 210, 
                                                          50 + self.cartas_na_mesa.index(carta) // 5 * 250))
            if carta_rect.collidepoint(mouse_x, mouse_y):
                return carta
        return None

    def distribuir_cartas(self, tela,bg):
        while len(self.cartas_na_mesa) > 0:
            jogador_atual = self.players[self.turno_atual]
            print(f"Vez do jogador {jogador_atual.numPlayer} escolher uma carta.")
            
            self.desenhar_cartas_na_mesa(tela,bg)
            pygame.display.update()

            carta_escolhida = None
            while carta_escolhida is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        carta_escolhida = self.selecionar_carta(mouse_x, mouse_y)

            # Define o dono da carta escolhida
            carta_escolhida.switchDono(jogador_atual)
            jogador_atual.cartas_selecionadas.append(carta_escolhida)

            # Adiciona a carta à lista de cartas do jogador
            if jogador_atual.numPlayer == 1:
                self.cartas_jogador1.append(carta_escolhida)
            else:
                self.cartas_jogador2.append(carta_escolhida)

            # Remove a carta escolhida da mesa
            self.cartas_na_mesa.remove(carta_escolhida)

            # Alterna para o próximo jogador
            self.turno_atual = (self.turno_atual + 1) % 2

        print("Distribuição de cartas concluída!")
