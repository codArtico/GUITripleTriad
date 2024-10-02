import pygame
from pygame.locals import *

class Tabuleiro:
    def __init__(self, tela, imagemSlot, imagemBorda, largura, altura):
        self.tela = tela
        self.imagemSlot = imagemSlot
        self.imagemBorda = imagemBorda
        self.linhas, self.colunas = 3, 3
        self.tamanhoSlotAltura = altura // 1.2 // self.linhas
        self.tamanhoSlotLargura = self.tamanhoSlotAltura
        self.tamanhoBorda = 5
        self.larguraTabuleiro = self.tamanhoSlotLargura * self.colunas
        self.alturaTabuleiro = self.tamanhoSlotAltura * self.linhas
        self.offset_x = (largura - self.larguraTabuleiro) // 2
        self.offset_y = (altura - self.alturaTabuleiro) // 2

    def desenharTabuleiro(self):
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                pos_x = self.offset_x + coluna * self.tamanhoSlotLargura
                pos_y = self.offset_y + linha * self.tamanhoSlotAltura
                slot = pygame.transform.scale(self.imagemSlot, (self.tamanhoSlotLargura, self.tamanhoSlotAltura))
                borda = pygame.transform.scale(self.imagemBorda, (self.tamanhoSlotLargura + 2 * self.tamanhoBorda, self.tamanhoSlotAltura + 2 * self.tamanhoBorda))
                self.tela.blit(borda, (pos_x - self.tamanhoBorda, pos_y - self.tamanhoBorda))
                self.tela.blit(slot, (pos_x, pos_y))
