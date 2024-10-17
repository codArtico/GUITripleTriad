import pygame
import os


pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join('audios', 'theme.mp3'))

LARGURA_TELA, ALTURA_TELA = 1366,768

oposto = {
    "cima": "baixo",
    "baixo": "cima",
    "esquerda": "direita",
    "direita": "esquerda",
}

direcoes = {
    "cima": (-1, 0),
    "baixo": (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1),
}