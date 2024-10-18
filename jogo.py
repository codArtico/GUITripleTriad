from configs import *
from tabuleiro import *
from player import *
from menu import *
from carta import *
from mesa import *
from random import randint
import time

def carregarImagens():
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
    cartaViradaBlue = pygame.transform.smoothscale(cartaViradaBlue, (175, 175))

    cartaViradaRed = pygame.image.load(os.path.join('imagens', 'versoCartaRed.png'))
    cartaViradaRed = pygame.transform.smoothscale(cartaViradaRed, (175, 175))

    imgPlus = pygame.image.load(os.path.join('imagens', 'imgPlus.png'))
    imgPlus = pygame.transform.smoothscale(imgPlus, (800, 800))

    return bg, imagemSlot, imagemBorda, logo, botao, bIni, bSair, cartaViradaBlue, cartaViradaRed, imgPlus

def carregarSfxs():
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

# Classe Game para gerenciar o fluxo do jogo
class Jogo:
    def __init__(self, larguraTela, alturaTela):
        pygame.init()
        self.telaPrincipal = pygame.display.set_mode((larguraTela, alturaTela), pygame.FULLSCREEN)
        pygame.display.set_caption("Triple Triad")
        self.fps = pygame.time.Clock()
        self.running = True
        self.jogoIniciado = False

        self.bg, self.imagemSlot, self.imagemBorda, self.logo, self.botao, self.bIni, self.bSair, self.cartaViradaBlue,self.cartaViradaRed, self.imgPlus = carregarImagens()

        
        # Dimensões da imagem de fundo
        self.bgLargura, self.bgAltura = self.bg.get_size()

            # Calcular a posição para centralizar a imagem de fundo
        self.bgX = (larguraTela - self.bgLargura) // 2
        self.bgY = (alturaTela - self.bgAltura) // 2

        self.animacaoX = -self.imgPlus.get_width()  # Começa fora da tela à esquerda
        self.animacaoY = (alturaTela - self.imgPlus.get_height()) // 2  # Centralizado verticalmente
        self.velAnimacao = 30
        self.trava = True
        self.select = False

        self.sfxCaptura, self.sfxColocarCarta, self.sfxPlus, self.sfxVitoria, self.sfxBotao, self.sfxEmpate, self.sfxWinP1, self.sfxWinP2, self.sfxCardPick = carregarSfxs()

        self.player1 = Player(1)
        self.player2 = Player(2)

        self.board = Tabuleiro(self.telaPrincipal, self.imagemSlot, self.imagemBorda, larguraTela, alturaTela, self.player1, self.player2, self.cartaViradaBlue, self.cartaViradaRed)
        self.menuInicial = Menu(self.telaPrincipal, self.bg, self.logo, self.botao, self.bIni, self.bSair)
        self.distribuindo = False
        self.animacaoPlusAtiva = False

        self.mesa = None
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(loops=-1)


    @staticmethod
    def checarVitoria(p1, p2):
        if p1.pontos > p2.pontos:
            return 1
        elif p2.pontos > p1.pontos:
            return 2
        else:
            return None
        
    @staticmethod
    def switchTurno(turno):
        if turno == 1:
            return 2
        else:
            return 1

    def swap(self):
        i = randint(0,4)
        c1 = self.player1.cartasSelecionadas.pop(i)
        c1.switchDono(self.player2)
        i = randint(0,4)
        c2 = self.player2.cartasSelecionadas.pop(i)
        c2.switchDono(self.player1)
        self.player1.cartasSelecionadas.append(c2)
        self.player2.cartasSelecionadas.append(c1)


    def animarImagem(self, larguraTela):
        self.animacaoX += self.velAnimacao

        if self.animacaoX >= self.telaPrincipal.get_width() / 2 - 350 and self.animacaoPlusAtiva and self.trava:
            time.sleep(1)
            self.trava=False

        # Verifica se a imagem saiu da tela
        if self.animacaoX > larguraTela:
            self.animacaoPlusAtiva = False # Reinicia a animação
            self.animacaoX = -self.imgPlus.get_width()
            self.trava = True

    def renderizar(self, img):
        tempSurface = pygame.Surface(self.telaPrincipal.get_size())
        tempSurface.blit(self.telaPrincipal, (0, 0))
        self.animarImagem(self.telaPrincipal.get_width())
        tempSurface.blit(img, (self.animacaoX, self.animacaoY))
        self.telaPrincipal.blit(tempSurface, (0, 0))
        pygame.display.flip()

    def processarEventoClique(self, posMouse, vez):
        cartas = self.player1.cartasSelecionadas if vez == 1 else self.player2.cartasSelecionadas

        for carta in cartas:
            pygame.draw.rect(self.telaPrincipal, (255, 0, 0), carta.rect, 2)
            pygame.display.flip()
            if carta.rect.collidepoint(posMouse):
                carta.selected = True
                print(f'Carta selecionada')
                return carta  # Retorna a carta clicada

        return None

    def run(self):
        turno = 1  # 1 for player 1, 2 for player 2
        cartaSelecionada = None

        while self.running:
            self.fps.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Sai do modo fullscreen
                        pygame.quit()
                        exit()


                # if event.type == pygame.VIDEORESIZE:
                #     self.telaPrincipal = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    print(f"Mouse clicked at: ({mouseX}, {mouseY})")

                    if not self.jogoIniciado and not self.distribuindo:
                        bIniciar, bSair = self.menuInicial.desenharMenu()
                        if self.menuInicial.clickBotao(bIniciar, mouseX, mouseY):
                            self.sfxBotao.play()
                            self.mesa = Mesa(self.player1, self.player2)
                            self.mesa.distribuirCartas(self.telaPrincipal, self.bg,self.bgX,self.bgY, self.sfxCardPick)
                            self.swap()
                            self.jogoIniciado = True

                        elif self.menuInicial.clickBotao(bSair, mouseX, mouseY):
                            pygame.quit()
                            exit()
                    else:
                        if not self.select:
                            cartaSelecionada = self.processarEventoClique((mouseX, mouseY), turno)
                            if cartaSelecionada:
                                self.select = True
                                print("Select recebeu true")
                        else:
                            if cartaSelecionada:
                                for (linha, coluna), slot in self.board.slots.items():
                                    print(f"Checking slot at ({linha}, {coluna}) with rect: {slot['rect']}")
                                    if slot['rect'].collidepoint(mouseX,mouseY):
                                        posInicial = cartaSelecionada.pos
                                        posFinal = slot['rect'].topleft
                                        cartaSelecionada.animarMovimento(self.telaPrincipal, posInicial, posFinal, self.bg, turno, self.bgX, self.bgY, self.board)
                                        print(f"Slot at ({linha}, {coluna}) was clicked.")
                                        if self.board.slots[(linha, coluna)]['carta'] is None:  # Check if the slot is empty
                                            cartaSelecionada.visual = cartaSelecionada.desenharCarta(200,200)
                                            self.board.colocarCarta(cartaSelecionada, linha, coluna, turno)
                                            self.select = False
                                            captura, plus = self.board.verificarVizinhas(linha, coluna, cartaSelecionada)
                                            if captura:
                                                if plus:
                                                    self.sfxPlus.play()
                                                    self.animacaoPlusAtiva = True
                                                else:
                                                    self.sfxCaptura.play()

                                            if turno == 1:
                                                self.player1.numCartas -= 1
                                                
                                            else:
                                                self.player2.numCartas -= 1

                                            cartaSelecionada = None  # Reset the selected card
                                            turno = self.switchTurno(turno)
                                            break  # Exit the loop after placing the card
                                                
                                    else:
                                        print("Problema na seleção de slot")            
                            else:
                                print("Problema na seleção da carta")                        
            if not self.jogoIniciado:
                self.menuInicial.desenharMenu()
            else:
                self.board.desenharTabuleiro(self.bg, turno, self.bgX, self.bgY)
                self.player1.desenharPontuacao(self.telaPrincipal, LARGURA_TELA*0.1, 20)  # Exibe a pontuação do player 1 no canto superior esquerdo
                self.player2.desenharPontuacao(self.telaPrincipal, LARGURA_TELA * 0.8, 20)  # Exibe a pontuação do player 2 logo abaixo

            # Game end condition
            if self.board.cartasColocadas == 9:
                # Victory check
                if self.checarVitoria(self.player1, self.player2) == 1:
                    self.sfxWinP1.play()
                elif self.checarVitoria(self.player1, self.player2) == 2:
                    self.sfxWinP2.play()
                else:
                    self.sfxEmpate.play()

                #Restart the game
                self.jogoIniciado = False
                self.player1 = Player(1)
                self.player2 = Player(2)
                
                # Recrie o tabuleiro com as dimensões originais
                self.board = Tabuleiro(self.telaPrincipal, self.imagemSlot, self.imagemBorda, LARGURA_TELA,
                                    ALTURA_TELA, self.player1, self.player2, self.cartaViradaBlue,
                                    self.cartaViradaRed)

            if self.animacaoPlusAtiva:
                self.animarImagem(LARGURA_TELA)
                self.renderizar(self.imgPlus)

            pygame.display.update()


if __name__ == "__main__":
    game = Jogo(LARGURA_TELA, ALTURA_TELA)
    game.run()