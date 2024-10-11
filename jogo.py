import pygame
import time
from random import randint
from pygame.locals import *
from sys import exit
import os
from tabuleiro import Tabuleiro
from menu import Menu
from carta import Carta
from player import Player
from mesa import Mesa

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

        self.bg, self.imagemSlot, self.imagemBorda, self.logo, self.botao, self.bIni, self.bSair, self.cartaViradaBlue,self.cartaViradaRed, self.imgPlus = self.carregarImagens()

        self.posicao_animacao_x = -self.imgPlus.get_width()  # Começa fora da tela à esquerda
        self.posicao_animacao_y = (self.altura - self.imgPlus.get_height()) // 2  # Centralizado verticalmente
        self.velocidade_animacao = 30
        self.trava = True

        self.sfxCaptura, self.sfxColocarCarta, self.sfxPlus, self.sfxVitoria, self.sfxBotao, self.sfxEmpate, self.sfxWinP1, self.sfxWinP2, self.sfxCardPick = self.carregarSfxs()

        self.player1 = Player(1)
        self.player2 = Player(2)

        self.board = Tabuleiro(self.tela, self.imagemSlot, self.imagemBorda, self.largura, self.altura, self.player1, self.player2, self.cartaViradaBlue, self.cartaViradaRed)
        self.menu_inicial = Menu(self.tela, self.bg, self.logo, self.botao, self.bIni, self.bSair)
        self.distribuindo = False
        self.animacaoPlusAtiva = False

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

        cartaViradaBlue = pygame.image.load(os.path.join('imagens', 'versoCartaBlue.png'))
        cartaViradaBlue= pygame.transform.smoothscale(cartaViradaBlue, (175,175))

        cartaViradaRed = pygame.image.load(os.path.join('imagens', 'versoCartaRed.png'))
        cartaViradaRed = pygame.transform.smoothscale(cartaViradaRed, (175, 175))

        imgPlus = pygame.image.load(os.path.join('imagens', 'imgPlus.png'))
        imgPlus= pygame.transform.smoothscale(imgPlus, (800, 800))

        return bg, imagemSlot, imagemBorda, logo, botao, bIni, bSair, cartaViradaBlue, cartaViradaRed, imgPlus

    def carregarSfxs(self):
        sfxCaptura = pygame.mixer.Sound(os.path.join('audios','capture.mp3'))
        sfxColocarCarta = pygame.mixer.Sound(os.path.join('audios','placeCard.mp3'))
        sfxPlus = pygame.mixer.Sound(os.path.join('audios','plus.mp3'))
        sfxVitoria = pygame.mixer.Sound(os.path.join('audios','victory.mp3'))
        sfxBotao = pygame.mixer.Sound(os.path.join('audios','button.wav'))
        sfxEmpate = pygame.mixer.Sound(os.path.join('audios','tie.ogg'))
        sfxWinP1 = pygame.mixer.Sound(os.path.join('audios','WinP1.mp3'))
        sfxWinP2 = pygame.mixer.Sound(os.path.join('audios','WinP2.mp3'))
        sfxCardPick = pygame.mixer.Sound(os.path.join('audios','cardPick.wav'))

        return sfxCaptura, sfxColocarCarta, sfxPlus, sfxVitoria, sfxBotao, sfxEmpate, sfxWinP1, sfxWinP2, sfxCardPick

    def selecionar_cartas(self):
        # Seleciona cartas para cada jogador
        for player in [self.player1, self.player2]:
            print(f"Jogador {player.numPlayer}, selecione suas cartas:")
            for i in range(5):  # Cada jogador escolhe 5 cartas
                carta = None
                while carta is None:
                    # Exibir as cartas disponíveis no baralho do jogador
                    for index, c in enumerate(player.deck):
                        print(f"{index + 1}: {c}")  # Aqui você precisa implementar a representação de string da carta

                    # Solicitar que o jogador escolha uma carta
                    escolha = input(f"Escolha a carta {i + 1}: ")
                    if escolha.isdigit() and 1 <= int(escolha) <= len(player.deck):
                        carta = player.deck[int(escolha) - 1]
                        player.cartas_selecionadas.append(carta)  # Adiciona a carta selecionada
                        player.deck.remove(carta)  # Remove a carta do baralho
                    else:
                        print("Escolha inválida, tente novamente.")

        # Depois que ambos os jogadores escolherem suas cartas, distribui as cartas na mesa
        self.mesa = Mesa(self.player1, self.player2)  # Cria uma nova mesa
        self.mesa.distribuir_cartas(self.tela)  # Distribui as cartas

    def swap(self):
        i = randint(0,4)
        c1 = self.player1.cartas_selecionadas.pop(i)
        c1.switchDono(self.player2)
        i = randint(0,4)
        c2 = self.player2.cartas_selecionadas.pop(i)
        c2.switchDono(self.player1)
        self.player1.cartas_selecionadas.append(c2)
        self.player2.cartas_selecionadas.append(c1)

    def animarImagem(self):
        self.posicao_animacao_x += self.velocidade_animacao

        if self.posicao_animacao_x >= self.tela.get_width() / 2 - 350 and self.animacaoPlusAtiva and self.trava:
            time.sleep(2)
            self.trava=False

        # Verifica se a imagem saiu da tela
        if self.posicao_animacao_x > self.largura:
            self.animacaoPlusAtiva = False # Reinicia a animação
            self.posicao_animacao_x = -self.imgPlus.get_width()
            self.trava = True


    def renderizar(self, img):
        self.limparTela()
        self.animarImagem()  # Atualiza a posição da imagem
        self.tela.blit(img, (self.posicao_animacao_x, self.posicao_animacao_y))  # Desenha a imagem na tela
        pygame.display.flip()  # Atualiza a tela

    def processarEventoClique(self, posicao_mouse, vez):
        print("Iniciou processamento de clique")
        cartas = self.player1.cartas_selecionadas if vez == 1 else self.player2.cartas_selecionadas
        numCartas = self.player1.numCartas if vez == 1 else self.player2.numCartas

        alturaTela = self.tela.get_height()
        posX = 50 if vez == 1 else self.tela.get_width() // 2 + 550
        posY = alturaTela // 2 - 300

        print(f"Posição do clique: {posicao_mouse}")

        for i in range(numCartas):
            rect_carta = pygame.Rect(posX, posY, 175, 175)

            print(f"Verificando carta {i}: Retângulo = {rect_carta}")

            # Verifica se o clique foi dentro da área da carta
            if rect_carta.collidepoint(posicao_mouse):
                print(f"Carta {i} foi clicada!")
                return i  # Retorna o índice da carta clicada

            posY += 200
            if vez == 1 and i == 2 and numCartas > 3:  # Ajusta para a segunda linha para o player Blue
                posX += 150
                posY = alturaTela // 2 - 200
            elif vez == 2 and i == 2 and numCartas > 3:  # Ajusta para a segunda linha para o player Red
                posX -= 150
                posY = alturaTela // 2 - 200

        print("Nenhuma carta foi clicada")
        return None  # Nenhuma carta foi clicada

    @staticmethod
    def checarVitoria(p1, p2):
        if p1.pontos > p2.pontos:
            return 1
        elif p2.pontos > p1.pontos:
            return 2
        else:
            return None

    def limparTela(self): 
        self.tela.blit(self.bg, (0, 0))

    def run(self):
        vez = 1  # 1 para jogador 1, 2 para jogador 2
        carta_selecionada = None  # Armazena a carta selecionada

        while self.running:
            self.fps.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if not self.jogo_iniciado and not self.distribuindo:
                        botao_iniciar, botao_sair_menu = self.menu_inicial.desenharMenu()
                        if self.menu_inicial.click_botao(botao_iniciar, mouse_x, mouse_y):
                            self.sfxBotao.play()
                            self.mesa = Mesa(self.player1, self.player2)
                            self.mesa.distribuir_cartas(self.tela, self.bg, self.sfxCardPick)
                            self.swap()
                            self.limparTela()
                            self.jogo_iniciado = True
                            
                        elif self.menu_inicial.click_botao(botao_sair_menu, mouse_x, mouse_y):
                            pygame.quit()
                            exit()
                    else:
                        # Se uma carta foi selecionada
                        if carta_selecionada:
                            # Verifica se um slot foi clicado
                            for linha in range(self.board.linhas):
                                for coluna in range(self.board.colunas):
                                    slot_rect = pygame.Rect(
                                        self.board.offset_x + coluna * self.board.tamanhoSlotLargura,
                                        self.board.offset_y + linha * self.board.tamanhoSlotAltura,
                                        self.board.tamanhoSlotLargura,
                                        self.board.tamanhoSlotAltura
                                    )
                                    if slot_rect.collidepoint(mouse_x, mouse_y):
                                        if self.board.slots[linha][coluna] is None:  # Verifica se o slot está vazio
                                            self.board.colocarCarta(carta_selecionada, linha, coluna, vez)
                                            captura,plus = self.board.verificarVizinhas(linha,coluna,carta_selecionada)
                                            if captura:
                                                if plus:
                                                    self.sfxPlus.play()
                                                    self.animacaoPlusAtiva = True
                                                else:
                                                    self.sfxCaptura.play()
                                            if vez == 1:
                                                self.player1.cartas_selecionadas.remove(carta_selecionada)  # Retira a carta do jogador 1
                                                vez = 2  # Troca para o jogador 2
                                            else:
                                                self.player2.cartas_selecionadas.remove(carta_selecionada)  # Retira a carta do jogador 2
                                                vez = 1  # Troca para o jogador 1

                                            carta_selecionada = None  # Reseta a carta selecionada
                                            print(f'Pontuação p1: {self.player1.pontos}')
                                            print(f'Pontuação p2: {self.player2.pontos}')
                                            break  # Sai do loop após colocar a carta
                                        else:
                                            print("Slot já ocupado, escolha outro.")                   
                        else:
                            # Verifica se uma carta foi clicada
                            indice_carta_selecionada = self.processarEventoClique((mouse_x, mouse_y), vez)
                            
                            if indice_carta_selecionada is not None:
                                if vez == 1:
                                    carta_selecionada = self.player1.cartas_selecionadas[indice_carta_selecionada]  # Seleciona a carta do jogador 1
                                else:
                                    carta_selecionada = self.player2.cartas_selecionadas[indice_carta_selecionada]  # Seleciona a carta do jogador 2

                if not self.jogo_iniciado:
                    self.menu_inicial.desenharMenu()
                else:
                    self.board.desenharTabuleiro(self.bg, vez)

                # Condição de parada do jogo
                if self.board.cartasColocadas == 9:
                    # Verificação de vitória
                    if self.checarVitoria(self.player1, self.player2) == 1:
                        self.sfxWinP1.play()
                    elif self.checarVitoria(self.player1, self.player2) == 2:
                        self.sfxWinP2.play()
                    else:
                        self.sfxEmpate.play()

                    # Reinicia o jogo
                    self.jogo_iniciado = False
                    self.player1 = Player(1)
                    self.player2 = Player(2)
                    self.board = Tabuleiro(self.tela, self.imagemSlot, self.imagemBorda, self.largura, self.altura, self.player1, self.player2, self.cartaViradaBlue, self.cartaViradaRed)
            
            if self.animacaoPlusAtiva:
                    self.animarImagem()  # Atualiza a posição da animação
                    self.renderizar(self.imgPlus)

            pygame.display.update()



if __name__ == "__main__":
    game = Jogo()
    game.run()
