import pygame
from pygame.locals import *
from sys import exit
from random import randint
import os

pygame.init()  # Inicia o pygame


fonte = pygame.font.SysFont('arial', 40, True, False)  # Fonte, tamanho, negrito, itálico
pygame.display.set_caption("Triple Triad")  # Muda o nome em cima do jogo

# Configs de tela
largura = 1550
altura = 800
tela = pygame.display.set_mode((largura, altura))  # Seta o tamanho da Janela
fps = pygame.time.Clock() # Define o FPS
running = True

# Muda o icone do jogo
iconCaminho = os.path.join('imagens', 'icon.ico')
icon = pygame.image.load(iconCaminho)
pygame.display.set_icon(icon)

# Muda o bg do jogo
bgCaminho = os.path.join('imagens', 'fundo.png')
bg = pygame.image.load(bgCaminho)

# Definindo cores
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#Config do tabuleiro {

 #Tamanho do slot e da Borda
linhas,colunas = 3,3
tamanhoSlotAltura = altura // 2 // linhas
tamanhoSlotLargura = tamanhoSlotAltura
tamanhoBorda = 2

 #Cores do slot e da borda
corBorda = BLACK
corSlot = WHITE

 #Tamanho do tabuleiro
larguraTabuleiro = tamanhoSlotLargura * colunas  # Largura total do tabuleiro
alturaTabuleiro = tamanhoSlotAltura * linhas  # Altura total do tabuleiro

offset_x = (largura - larguraTabuleiro) // 2  # Deslocamento pra centralizar o tabuleiro
offset_y = (altura - alturaTabuleiro) // 2 # Deslocamento pra centralizar o tabuleiro

# }

def desenharTabuleiro():
    tela.fill(WHITE)  # Preenche o fundo da tela de branco
    tela.blit(bg,(0,0))
    for linha in range(linhas):
        for coluna in range(colunas):
            pygame.draw.rect(tela, corSlot, (offset_x + coluna * tamanhoSlotLargura, offset_y + linha * tamanhoSlotAltura, tamanhoSlotLargura, tamanhoSlotAltura)) # Desenha todos os slots

            pygame.draw.rect(tela, corBorda, (offset_x + coluna * tamanhoSlotLargura, offset_y + linha * tamanhoSlotAltura, tamanhoSlotLargura, tamanhoSlotAltura), tamanhoBorda) # Desenha todas as bordas

while running:
    fps.tick(30) # Setando FPS
        
    for event in pygame.event.get():  # Código para o botão de fechar funcionar
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Chamada do tabuleiro
    desenharTabuleiro()
    
     # Atualizando tela
    pygame.display.update()