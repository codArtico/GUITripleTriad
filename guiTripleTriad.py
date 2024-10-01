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

while True:
    tela.fill((0, 0, 0))
        
    for event in pygame.event.get():  # Código para o botão de fechar funcionar
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
     # Atualizando tela
    pygame.display.update()