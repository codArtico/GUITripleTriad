import pygame
import time
import os
from os.path import join
from random import randint
from carta import Carta
from random import randint
from sys import exit
from tabuleiro import Tabuleiro
from menu import Menu
from player import Player
from mesa import Mesa


pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join('audios', 'theme.mp3'))

LARGURA_TELA, ALTURA_TELA = 1366, 768

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