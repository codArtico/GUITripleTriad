import pygame
from baralho import *

#unusable
def testBaralho():
    caminho = "cartas/valoresTeste.txt"
    b = Baralho(caminho)

    c1 = b.deck[0]
    c2 = b.deck[1]
    c3 = b.deck[2]

    
    print('Primeira Carta: \n')
    print(c1.valores['cima'])
    print(c1.valores['direita'])
    print(c1.valores['baixo'])
    print(c1.valores['esquerda'])

    print('\nSegunda Carta: \n')
    print(c2.valores['cima'])
    print(c2.valores['direita'])
    print(c2.valores['baixo'])
    print(c2.valores['esquerda'])

    print('\nTerceira Carta: \n')
    print(c3.valores['cima'])
    print(c3.valores['direita'])
    print(c3.valores['baixo'])
    print(c3.valores['esquerda'])

def testMoldura(num):
    pygame.init()
    largura, altura = 1550, 800
    tamanhoSlotAltura = altura // 1.2 // 3
    tamanhoSlotLargura = tamanhoSlotAltura
    tela = pygame.display.set_mode((largura, altura))

    moldura = pygame.image.load('imagens/moldura.png').convert_alpha()  # Use .convert_alpha() para manter a transparência
    moldura = pygame.transform.scale(moldura, (tamanhoSlotLargura, tamanhoSlotAltura))
    moldura_colorida = moldura.copy()
    if num == 0:
        # Aplica o filtro azul
        moldura_colorida.fill((0, 0, 255), special_flags=pygame.BLEND_MULT)  # Azul
    else:
        # Aplica o filtro vermelho
        moldura_colorida.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)  # Vermelho

    tela.fill((0, 0, 0))
    tela.blit(moldura_colorida, (0, 0))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

def testeCriarCarta():
    pygame.init()
    largura, altura = 1550, 800
    tela = pygame.display.set_mode((largura, altura))
    carta = Carta(3) # Se 1, então: Blue // Se não, então: Red
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        tela.fill((0,128,128))
        tela.blit(carta.visual, (500, 500))
        pygame.display.flip()

#testMoldura(1)
testeCriarCarta()