import pygame
import os

class Menu:
    def __init__(self, tela, bg, logo, botao, bIni, bSair):
        self.tela = tela
        self.bg = bg
        self.logo = logo
        self.botao = botao
        self.bIni = bIni
        self.bSair = bSair

        # Defina versões alternativas dos botões para o efeito de hover
        self.bIni_hover = pygame.transform.scale(bIni, (550*1.2, 140*1.2))
        self.bSair_hover = pygame.transform.scale(bSair, (550*1.2, 140*1.2))

    def desenharMenu(self):
        self.tela.blit(self.bg, (0, 0))
        self.tela.blit(self.logo, (580, 0))

        # Obtém a posição do mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Verifica se o mouse está sobre o botão "Iniciar"
        if self.is_hover(mouse_x, mouse_y, (510, 330, 550, 140)):
            self.tela.blit(self.bIni_hover, (465, 300))  # Mostra a versão hover
        else:
            self.tela.blit(self.bIni, (510, 330))  # Mostra a versão normal

        # Verifica se o mouse está sobre o botão "Sair"
        if self.is_hover(mouse_x, mouse_y, (510, 480, 550, 140)):
            self.tela.blit(self.bSair_hover, (465, 450))  # Mostra a versão hover
        else:
            self.tela.blit(self.bSair, (510, 480))  # Mostra a versão normal

        area_iniciar = (510, 330, 550, 140)
        area_sair = (510, 480, 550, 140)
        return area_iniciar, area_sair

    # Função para verificar se o mouse está sobre um botão
    def is_hover(self, mouse_x, mouse_y, rect):
        return rect[0] <= mouse_x <= rect[0] + rect[2] and rect[1] <= mouse_y <= rect[1] + rect[3]

    # Função para verificar clique no botão
    def click_botao(self, area, mouse_x, mouse_y):
        return self.is_hover(mouse_x, mouse_y, area)