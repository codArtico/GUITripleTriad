import pygame
from pygame.locals import *
from sys import exit
import os
from tabuleiro import Tabuleiro
from menu import Menu
from carta import Carta
from player import Player

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
        self.sfxCaptura,self.sfxColocarCarta,self.sfxPlus,self.sfxVitoria,self.sfxBotao,self.sfxEmpate = self.carregarSfxs()

        self.board = Tabuleiro(self.tela, self.imagemSlot, self.imagemBorda, self.largura, self.altura)
        self.menu_inicial = Menu(self.tela, self.bg, self.logo, self.botao, self.bIni, self.bSair)

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

        return sfxCaptura,sfxColocarCarta,sfxPlus,sfxVitoria,sfxBotao,sfxEmpate
    
    @staticmethod
    def checarVitoria(p1, p2):
        if p1.pontos > p2.pontos:
            return 1
        elif p2.pontos > p1.pontos:
            return 2
        else:
            return None

    def run(self):
        player1 = Player(1)
        player2 = Player(2)
        vez = 1
        while self.running:
            self.fps.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if not self.jogo_iniciado:
                        botao_iniciar, botao_sair_menu = self.menu_inicial.desenharMenu()
                        if self.menu_inicial.click_botao(botao_iniciar, mouse_x, mouse_y):
                            self.sfxBotao.play()
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
                                            self.board.colocarCarta(Carta(player1), linha, coluna)
                                            vez=2
                                        else:
                                            self.board.colocarCarta(Carta(player2), linha, coluna)
                                            vez=1
                                        self.sfxColocarCarta.play()

                                    # Teste de troca de cores na captura + Pontuação
                                    else:
                                        if self.board.slots[linha][coluna].dono.numPlayer == 1:
                                            self.board.slots[linha][coluna].dono.downPoint()
                                            self.board.slots[linha][coluna].switchDono(player2)
                                            self.board.slots[linha][coluna].dono.upPoint()
                                           
                                        else:
                                            self.board.slots[linha][coluna].dono.downPoint()
                                            self.board.slots[linha][coluna].switchDono(player1)
                                            self.board.slots[linha][coluna].dono.upPoint()



            if not self.jogo_iniciado:
                self.menu_inicial.desenharMenu()
            else:
                self.board.desenharTabuleiro()

            # Condição de parada do jogo
            if self.board.cartasColocadas == 9:

                #Verificação de vitória
                if self.checarVitoria(player1,player2) == 1:
                    self.sfxVitoria.play()
                elif self.checarVitoria(player1,player2) == 2:
                    self.sfxPlus.play()
                else:
                    self.sfxEmpate.play()

                # Reset do jogo
                self.jogo_iniciado = False
                self.board = Tabuleiro(self.tela, self.imagemSlot, self.imagemBorda, self.largura, self.altura)
                self.player1 = Player(1)
                self.player2 = Player(2)

            pygame.display.update()

if __name__ == "__main__":
    game = Jogo()
    game.run()