import pygame
from pygame.locals import *
from sys import exit
import os
from tabuleiro import Tabuleiro
from menu import Menu

pygame.init()

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
        self.sfxCaptura,self.sfxColocarCarta,self.sfxPlus,self.sfxVitoria = self.carregarSfxs()

        self.board = Tabuleiro(self.tela, self.imagemSlot, self.imagemBorda, self.largura, self.altura)
        self.menu_inicial = Menu(self.tela, self.bg, self.logo, self.botao, self.bIni, self.bSair)

        pygame.mixer.music.load(os.path.join('audios', 'theme.mp3'))
        pygame.mixer.music.play(-1)
        
    def carregarImagens(self):
        icon = pygame.image.load(os.path.join('imagens', 'icon.ico'))
        pygame.display.set_icon(icon)

        bg = pygame.image.load(os.path.join('imagens', 'fundo.png'))
        imagemSlot = pygame.image.load(os.path.join('imagens', 'slot.jpg'))
        imagemBorda = pygame.image.load(os.path.join('imagens', 'grama.jpg'))
        logo = pygame.image.load(os.path.join('imagens', 'logo.png'))
        logo = pygame.transform.scale(logo, (400, 400))

        botao = pygame.image.load(os.path.join('imagens', 'botao.png'))
        botao = pygame.transform.scale(botao, (600, 600))
        bIni = pygame.image.load(os.path.join('imagens', 'iniciar.png'))
        bIni = pygame.transform.scale(bIni, (550, 140))
        bSair = pygame.image.load(os.path.join('imagens', 'sair.png'))
        bSair = pygame.transform.scale(bSair, (550, 140))

        return bg, imagemSlot, imagemBorda, logo, botao, bIni, bSair
    
    def carregarSfxs():
        sfxCaptura = pygame.mixer.Sound(os.path.join('audios','capture.mp3'))
        sfxColocarCarta = pygame.mixer.Sound(os.path.join('audios','placeCard.mp3'))
        sfxPlus = pygame.mixer.Sound(os.path.join('audios','plus.mp3'))
        sfxVitoria = pygame.mixer.Sound(os.path.join('audios','victory.mp3'))

        return sfxCaptura,sfxColocarCarta,sfxPlus,sfxVitoria
    
    def run(self):
        while self.running:
            self.fps.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if not self.jogo_iniciado:
                        botao_iniciar, botao_sair_menu = self.menu_inicial.desenharMenu()
                        if self.menu_inicial.click_botao(botao_iniciar, mouse_x, mouse_y):
                            self.jogo_iniciado = True
                        elif self.menu_inicial.click_botao(botao_sair_menu, mouse_x, mouse_y):
                            pygame.quit()
                            exit()

            if not self.jogo_iniciado:
                self.menu_inicial.desenharMenu()
            else:
                self.board.desenharTabuleiro()

            pygame.display.update()

if __name__ == "__main__":
    game = Jogo()
    game.run()