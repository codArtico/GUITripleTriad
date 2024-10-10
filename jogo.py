import pygame
from pygame.locals import *
from sys import exit
import os
from tabuleiro import Tabuleiro
from menu import Menu
from carta import Carta
from player import Player
from mesa import Mesa

pygame.init()
pygame.mixer.init()

# Classe Game para gerenciar o fluxo do jogo
class Jogo:
    def __init__(self):
        self.largura = 1550
        self.altura = 800
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        self.fps = pygame.time.Clock()
        self.running = True
        self.jogo_iniciado = False
        pygame.display.set_caption("Triple Triad")

        self.bg, self.imagemSlot, self.imagemBorda, self.logo, self.botao, self.bIni, self.bSair = self.carregarImagens()
        self.sfxCaptura, self.sfxColocarCarta, self.sfxPlus, self.sfxVitoria, self.sfxBotao, self.sfxEmpate, self.sfxWinP1, self.sfxWinP2 = self.carregarSfxs()

        self.player1 = Player(1)
        self.player2 = Player(2)

        self.board = Tabuleiro(self.tela, self.imagemSlot, self.imagemBorda, self.largura, self.altura, self.player1, self.player2)
        self.menu_inicial = Menu(self.tela, self.bg, self.logo, self.botao, self.bIni, self.bSair)
        self.distribuindo = False

        pygame.mixer.music.load(os.path.join('audios', 'theme.mp3'))
        pygame.mixer.music.play(-1)


    def carregarImagens(self):
        icon = pygame.image.load(os.path.join('imagens', 'icon.ico'))
        pygame.display.set_icon(icon)

        bg = pygame.image.load(os.path.join('imagens', 'fundo.png'))
        imagemSlot = pygame.image.load(os.path.join('imagens', 'slot.png'))
        imagemBorda = pygame.image.load(os.path.join('imagens', 'borda.png'))
        logo = pygame.image.load(os.path.join('imagens', 'logo.png'))
        logo = pygame.transform.smoothscale(logo, (400, 400))

        botao = pygame.image.load(os.path.join('imagens', 'botao.png'))
        botao = pygame.transform.smoothscale(botao, (600, 600))
        bIni = pygame.image.load(os.path.join('imagens', 'iniciar.png'))
        bIni = pygame.transform.smoothscale(bIni, (350, 85))
        bSair = pygame.image.load(os.path.join('imagens', 'sair.png'))
        bSair = pygame.transform.smoothscale(bSair, (350, 85))

        return bg, imagemSlot, imagemBorda, logo, botao, bIni, bSair

    def carregarSfxs(self):
        sfxCaptura = pygame.mixer.Sound(os.path.join('audios','capture.mp3'))
        sfxColocarCarta = pygame.mixer.Sound(os.path.join('audios','placeCard.mp3'))
        sfxPlus = pygame.mixer.Sound(os.path.join('audios','plus.mp3'))
        sfxVitoria = pygame.mixer.Sound(os.path.join('audios','victory.mp3'))
        sfxBotao = pygame.mixer.Sound(os.path.join('audios','button.wav'))
        sfxEmpate = pygame.mixer.Sound(os.path.join('audios','tie.ogg'))
        sfxWinP1 = pygame.mixer.Sound(os.path.join('audios','WinP1.mp3'))
        sfxWinP2 = pygame.mixer.Sound(os.path.join('audios','WinP2.mp3'))

        return sfxCaptura, sfxColocarCarta, sfxPlus, sfxVitoria, sfxBotao, sfxEmpate, sfxWinP1, sfxWinP2

    def selecionar_cartas(self):
        # Seleciona cartas para cada jogador
        for player in [self.player1, self.player2]:
            print(f"Jogador {player.numPlayer}, selecione suas cartas:")
            for i in range(5):  # Cada jogador escolhe 5 cartas
                carta = None
                while carta is None:
                    # Exibir as cartas disponíveis no baralho do jogador
                    for index, c in enumerate(player.deck):
                        print(f"{index + 1}: {c}")  # Aqui você precisa implementar a representação de string da carta

                    # Solicitar que o jogador escolha uma carta
                    escolha = input(f"Escolha a carta {i + 1}: ")
                    if escolha.isdigit() and 1 <= int(escolha) <= len(player.deck):
                        carta = player.deck[int(escolha) - 1]
                        player.cartas_selecionadas.append(carta)  # Adiciona a carta selecionada
                        player.deck.remove(carta)  # Remove a carta do baralho
                    else:
                        print("Escolha inválida, tente novamente.")

        # Depois que ambos os jogadores escolherem suas cartas, distribui as cartas na mesa
        self.mesa = Mesa(self.player1, self.player2)  # Cria uma nova mesa
        self.mesa.distribuir_cartas(self.tela)  # Distribui as cartas

    def limparTela(self):
        self.tela.blit(self.bg,(0,0))

    @staticmethod
    def checarVitoria(p1, p2):
        if p1.pontos > p2.pontos:
            return 1
        elif p2.pontos > p1.pontos:
            return 2
        else:
            return None

    def run(self):
        vez = 1
        while self.running:
            self.fps.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if not self.jogo_iniciado and not self.distribuindo:
                        botao_iniciar, botao_sair_menu = self.menu_inicial.desenharMenu()
                        if self.menu_inicial.click_botao(botao_iniciar, mouse_x, mouse_y):
                            self.sfxBotao.play()
                            self.mesa = Mesa(self.player1, self.player2)
                            self.mesa.distribuir_cartas(self.tela,self.bg)
                            self.limparTela()
                            self.jogo_iniciado = True
                            
                        elif self.menu_inicial.click_botao(botao_sair_menu, mouse_x, mouse_y):
                            pygame.quit()
                            exit()
                        
                        

                    else:
                        for linha in range(self.board.linhas):
                            for coluna in range(self.board.colunas):
                                slot_rect = pygame.Rect(
                                    self.board.offset_x + coluna * self.board.tamanhoSlotLargura,
                                    self.board.offset_y + linha * self.board.tamanhoSlotAltura,
                                    self.board.tamanhoSlotLargura,
                                    self.board.tamanhoSlotAltura
                                )
                                if slot_rect.collidepoint(mouse_x, mouse_y):
                                    if self.board.slots[linha][coluna] is None:
                                        if vez == 1:
                                            carta = self.player1.cartas_selecionadas.pop(0)  # Retira a carta do jogador
                                            self.board.colocarCarta(carta, linha, coluna)
                                            vez = 2
                                        else:
                                            carta = self.player2.cartas_selecionadas.pop(0)  # Retira a carta do jogador
                                            self.board.colocarCarta(carta, linha, coluna)
                                            vez = 1

                                        if self.board.verificarVizinhas(linha, coluna, carta):
                                            self.sfxCaptura.play()
                                        self.sfxColocarCarta.play()

                                    print(f'Pontuação p1: {self.player1.pontos}')
                                    print(f'Pontuação p2: {self.player2.pontos}')

            if not self.jogo_iniciado:
                self.menu_inicial.desenharMenu()
            else:
                self.board.desenharTabuleiro()

            # Condição de parada do jogo
            if self.board.cartasColocadas == 9:
                # Verificação de vitória
                if self.checarVitoria(self.player1, self.player2) == 1:
                    self.sfxWinP1.play()
                elif self.checarVitoria(self.player1, self.player2) == 2:
                    self.sfxWinP2.play()
                else:
                    self.sfxEmpate.play()

                # Reinicia o jogo
                self.jogo_iniciado = False
                self.player1 = Player(1)
                self.player2 = Player(2)
                self.board = Tabuleiro(self.tela, self.imagemSlot, self.imagemBorda, self.largura, self.altura, self.player1, self.player2)

            pygame.display.update()

if __name__ == "__main__":
    game = Jogo()
    game.run()
