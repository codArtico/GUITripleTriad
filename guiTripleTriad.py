import pygame
from pygame.locals import *
from sys import exit
import os

pygame.init()  # Inicia o pygame

# Configurações da fonte e título
fonte = pygame.font.SysFont('arial', 40, True, False)  # Fonte, tamanho, negrito, itálico
pygame.display.set_caption("Triple Triad")  # Nome do jogo

# Configurações da tela
largura = 1550
altura = 800
tela = pygame.display.set_mode((largura, altura))  # Define o modo janela
fps = pygame.time.Clock()  # Controlador de FPS
running = True
jogo_iniciado = False  # Variável que controla se o jogo começou ou não

def carregarImagens():
    # Muda o ícone do jogo
    iconCaminho = os.path.join('imagens', 'icon.ico')
    icon = pygame.image.load(iconCaminho)
    pygame.display.set_icon(icon)

    # Muda o bg do jogo
    bgCaminho = os.path.join('imagens', 'fundo.png')
    bg = pygame.image.load(bgCaminho)

    # Carrega imagens dos slots
    slotCaminho = os.path.join('imagens', 'slot.jpg')
    imagemSlot = pygame.image.load(slotCaminho)

    # Carrega imagem da borda
    bordaCaminho = os.path.join('imagens', 'grama.jpg')
    imagemBorda = pygame.image.load(bordaCaminho)

    logoCaminho = os.path.join('imagens', 'logo.png')
    logo = pygame.image.load(logoCaminho)
    logo = pygame.transform.scale(logo, (400, 400))

    # Configurações do botão
    botaoLargura = (600, 600)  # Tamanho original do botão
    botaoCaminho = os.path.join('imagens', 'botao.png')
    botao = pygame.image.load(botaoCaminho)
    botao = pygame.transform.scale(botao, botaoLargura)
    bIniCaminho = os.path.join('imagens', 'iniciar.png')
    bIni = pygame.image.load(bIniCaminho)
    bIni = pygame.transform.scale(bIni, (550,140))
    bSairCaminho = os.path.join('imagens', 'sair.png')
    bSair = pygame.image.load(bSairCaminho)
    bSair = pygame.transform.scale(bSair, (550,140))

    return bg, imagemSlot, imagemBorda, logo, botao, bIni, bSair

bg, imagemSlot, imagemBorda, logo, botao, bIni, bSair = carregarImagens()

# Definindo cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Config do tabuleiro
linhas, colunas = 3, 3
tamanhoSlotAltura = altura // 1.2 // linhas
tamanhoSlotLargura = tamanhoSlotAltura
tamanhoBorda = 5

# Tamanho do tabuleiro
larguraTabuleiro = tamanhoSlotLargura * colunas  # Largura total do tabuleiro
alturaTabuleiro = tamanhoSlotAltura * linhas  # Altura total do tabuleiro

offset_x = (largura - larguraTabuleiro) // 2  # Deslocamento pra centralizar o tabuleiro
offset_y = (altura - alturaTabuleiro) // 2  # Deslocamento pra centralizar o tabuleiro

# Função para desenhar o tabuleiro
def desenharTabuleiro():
    tela.blit(bg, (0, 0))
    for linha in range(linhas):
        for coluna in range(colunas):
            pos_x = offset_x + coluna * tamanhoSlotLargura
            pos_y = offset_y + linha * tamanhoSlotAltura

            # Redimensiona as imagens dos slots e das bordas
            imagemSlotRedimensionada = pygame.transform.scale(imagemSlot, (tamanhoSlotLargura, tamanhoSlotAltura))
            imagemBordaRedimensionada = pygame.transform.scale(imagemBorda, (tamanhoSlotLargura + 2 * tamanhoBorda, tamanhoSlotAltura + 2 * tamanhoBorda))

            # Desenha a imagem da borda ao redor dos slots
            tela.blit(imagemBordaRedimensionada, (pos_x - tamanhoBorda, pos_y - tamanhoBorda))

            # Desenha a imagem no slot
            tela.blit(imagemSlotRedimensionada, (pos_x, pos_y))

# Função para desenhar o menu inicial
def desenharMenu():
    tela.blit(bg, (0, 0)) # Exibe o fundo da tela Inicial
    tela.blit(logo, (580, 0))  # Exibe o título no topo

    # Botão "Iniciar"
    botaoIniciarPosX = 480
    botaoIniciarPosY = 120
    botaoIniciarPos = (botaoIniciarPosX, botaoIniciarPosY)
    tela.blit(botao, botaoIniciarPos)
    tela.blit(bIni,(510,330))

    # Botão "Sair"
    botaoSairPosX = botaoIniciarPosX
    botaoSairPosY = botaoIniciarPosY + 150  # Ajuste a posição do botão "Sair"
    botaoSairPos = (botaoSairPosX, botaoSairPosY)
    tela.blit(botao, botaoSairPos)
    tela.blit(bSair,(510,480))

    # Define as áreas clicáveis (apenas para verificar cliques)
    area_iniciar = (botaoIniciarPosX+37, botaoIniciarPosY+220, 540, 130)
    area_sair = (botaoSairPosX+37, botaoSairPosY+220, 540, 130)

    return area_iniciar, area_sair

while running:
    fps.tick(30)  # Definindo o FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if not jogo_iniciado:
                # Desenha o menu e detecta cliques nos botões
                botao_iniciar, botao_sair_menu = desenharMenu()

                # Verifica se clicou no botão "Iniciar"
                if botao_iniciar[0] <= mouse_x <= botao_iniciar[0] + 600 and botao_iniciar[1] <= mouse_y <= botao_iniciar[1] + 305:
                    jogo_iniciado = True

                # Verifica se clicou no botão "Sair"
                if botao_sair_menu[0] <= mouse_x <= botao_sair_menu[0] + 600 and botao_sair_menu[1] <= mouse_y <= botao_sair_menu[1] + 305:
                    pygame.quit()
                    exit()

    if not jogo_iniciado:
        desenharMenu()  # Desenha o menu se o jogo não começou
    else:
        desenharTabuleiro()  # Desenha o tabuleiro se o jogo começou

    pygame.display.update()  # Atualiza a tela
