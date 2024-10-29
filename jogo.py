from configs import *
from tabuleiro import *
from player import *
from menu import *
from carta import *
from mesa import *
from random import randint
import time

def carregarImagens():
    """
    Carrega todas as imagens necessárias para o jogo

    :return bg (pygame.Surface): A imagem de fundo do jogo. 
    :return imagemSlot (pygame.Surface): A imagem do slot. 
    :return imagemBorda (pygame.Surface): A borda do tabuleiro, que divide os slots. 
    :return logo (pygame.Surface): A logo do jogo. 
    :return bIni (pygame.Surface): A imagem do botão "Iniciar". 
    :return bSair (pygame.Surface): A imagem do botão "Sair". 
    :return cartaViradaBlue (pygame.Surface): A imagem do verso das cartas azuis. 
    :return cartaViradaRed (pygame.Surface): A imagem do verso das cartas vermelhas. 
    :return imgPlus (pygame.Surface): A imagem da captura "Plus". 
    :return bgLetras (pygame.Surface): O background para a troca de turnos durante o jogo. 
    :return imgWinP1 (pygame.Surface): Uma imagem para ser mostrada quando a vitória for do Player 1.
    :return imgWinP2 (pygame.Surface): Uma imagem para ser mostrada quando a vitória for do Player 2.
    """
    icon = pygame.image.load(os.path.join('imagens', 'icon.ico'))
    pygame.display.set_icon(icon)

    bg = pygame.image.load(os.path.join('imagens', 'fundo.png'))

    imagemSlot = pygame.image.load(os.path.join('imagens', 'slot.png'))
    imagemBorda = pygame.image.load(os.path.join('imagens', 'borda.png'))
    logo = pygame.image.load(os.path.join('imagens', 'logo.png'))
    logo = pygame.transform.smoothscale(logo, (400, 400))

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

    bgLetras = pygame.image.load(os.path.join('imagens', 'bgLetras.png'))
    bgLetras = pygame.transform.smoothscale(bgLetras,(257,50))

    imgWinP1 = pygame.image.load(os.path.join('imagens', 'winP1.png')) 
    imgWinP2 = pygame.image.load(os.path.join('imagens', 'winP2.png'))

    return bg, imagemSlot, imagemBorda, logo, bIni, bSair, cartaViradaBlue, cartaViradaRed, imgPlus, bgLetras, imgWinP1, imgWinP2

def carregarSfxs():
    """
    Carrega todas as faixas de áudio necessárias para o jogo.

    :return sfxCaptura (pygame.mixer.Sound): Efeito sonoro para a captura de cartas.
    :return sfxColocarCarta (pygame.mixer.Sound): Efeito sonoro para ser acionado quando uma carta é colocada no tabuleiro.
    :return sfxPlus (pygame.mixer.Sound): Efeito sonoro para ser acionado quando uma captura é feito pela regra "Plus".
    :return sfxVitoria (pygame.mixer.Sound): Efeito sonoro para vitórias.
    :return sfxBotao (pygame.mixer.Sound): Efeito sonoro para o clique de botões.
    :return sfxEmpate (pygame.mixer.Sound): Efeito sonoro para empates.
    :return sfxWinP1 (pygame.mixer.Sound): Efeito sonoro para a vitória do Player 1.
    :return sfxWinP2 (pygame.mixer.Sound): Efeito sonoro para a vitória do Player 1.
    :return sfxCardPick (pygame.mixer.Sound): Efeito sonoro para ser acionado quando uma carta é escolhida.
    """
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
        """
        Inicializa as configurações essenciais para o andamento do jogo. Ao iniciar, o jogo não está iniciado.
        
        :param larguraTela (int): The width of the screen.
        :param alturaTela (int): The height of the screen.

        Returns:
        None
        """
        pygame.init()
        self.telaPrincipal = pygame.display.set_mode((larguraTela, alturaTela), pygame.FULLSCREEN)
        pygame.display.set_caption("Triple Triad")
        self.fps = pygame.time.Clock()
        self.running = True
        self.jogoIniciado = False

        self.bg, self.imagemSlot, self.imagemBorda, self.logo, self.bIni, self.bSair, self.cartaViradaBlue,self.cartaViradaRed, self.imgPlus, self.bgLetras, self.imgWinP1, self.imgWinP2 = carregarImagens()


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
        self.menuInicial = Menu(self.telaPrincipal, self.bg, self.logo, self.bIni, self.bSair)
        self.distribuindo = False
        self.animacaoPlusAtiva = False

        self.l = None
        self.r = None

        self.mesa = None
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(loops=-1)

    @staticmethod
    def checarVitoria(p1, p2):
        """
        Checa o vencedor baseado na pontuação dos Players.

        :param p1 (Player): O player 1.
        :param p2 (Player): O player 2.

        :return int 1: Se o Player 1 venceu
        :return int 2: Se o Player 2 venceu
        :return None: Se foi empate
        """
        if p1.pontos > p2.pontos:
            return 1
        elif p2.pontos > p1.pontos:
            return 2
        else:
            return None

    @staticmethod
    def switchTurno(turno):
        """
        Troca de turno do Player 1 para o Player 2 e vice versa.

        :param turno (int): The current player's turn. It should be either 1 or 2.
        
        :return int 1: Se o turno atual for 2
        :return int 2: Se o turno atual for 1
        """
        if turno == 1:
            return 2
        else:
            return 1

    def swap(self):
        """
        Seleciona 1 carta aleatoriamente de cada player e as troca.

        :return None:
        """
        i = randint(0,4)
        c1 = self.player1.cartasSelecionadas.pop(i)
        c1.switchDono(self.player2)
        i = randint(0,4)
        c2 = self.player2.cartasSelecionadas.pop(i)
        c2.switchDono(self.player1)
        self.player1.cartasSelecionadas.append(c2)
        self.player2.cartasSelecionadas.append(c1)


    def animarImagem(self, larguraTela):
        """
        Anima o nome "Plus" na tela.

        :param larguraTela (int): The width of the screen.

        :return None:
        """
        self.animacaoX += self.velAnimacao

        if self.animacaoX >= self.telaPrincipal.get_width() / 2 - 350 and self.animacaoPlusAtiva and self.trava:
            time.sleep(1)
            self.trava=False

        # Check if the image has exited the screen
        if self.animacaoX > larguraTela:
            self.animacaoPlusAtiva = False  # Reset the animation
            self.animacaoX = -self.imgPlus.get_width()
            self.trava = True


    def renderizar(self, img):
        """
        Renderiza a imagem do "Plus" na tela.

        :param img (pygame.Surface): The image to be rendered on the screen.

        :return None:
        """
        tempSurface = pygame.Surface(self.telaPrincipal.get_size())
        tempSurface.blit(self.telaPrincipal, (0, 0))
        self.animarImagem(self.telaPrincipal.get_width())
        tempSurface.blit(img, (self.animacaoX, self.animacaoY))
        self.telaPrincipal.blit(tempSurface, (0, 0))
        pygame.display.flip()


    def processarEventoClique(self, posMouse, vez):
        """
        Processa os clicks da carta e verifica se alguma carta foi selecionada.

        :param posMouse (tuple): As coordenadas do mouse.
        :param vez (int): O turno dos Players.

        :return tuple: Uma tupla com a carta selecionada e o indicador de seleção de carta. Se nenhuma carta foi selecionada, a tupla retorna (None,False)
        """
        cartas = self.player1.cartasSelecionadas if vez == 1 else self.player2.cartasSelecionadas

        for carta in cartas:
            pygame.display.flip()
            if carta.rect.collidepoint(posMouse):
                carta.selected = True
                print(f'Carta selecionada')
                return carta,True 

        return None,False


    def processarHover(self, posMouse, vez):
        """
        Processa o evento Hover nas cartas. Se o mouse estiver sobre a carta, a carta é destacada.

        :param posMouse (tuple): The coordinates of the mouse cursor.
        :param vez (int): The turn of the players. It should be either 1 or 2.

        :return None:
        """
        cartas = self.player1.cartasSelecionadas if vez == 1 else self.player2.cartasSelecionadas

        for carta in cartas:
            if carta and carta.rect.collidepoint(posMouse):
                carta.hovered = True
            elif carta:
                carta.hovered = False

        return None


    def run(self):
        """
        Função principal que executa o loop do jogo Triple Triad.

        O método `run` controla todo o ciclo de eventos do jogo, incluindo a detecção de cliques, animação de cartas,
        atualização da interface do jogador e controle de turnos. Além disso, lida com as condições de vitória, pontuação
        e reinicialização do jogo.

        Atributos:
            turno (int): Identifica o turno atual do jogador. Alterna entre 1 e 2.
            cartaSelecionada (Carta): Armazena a carta atualmente selecionada pelo jogador.
            placed (bool): Flag para verificar se a carta foi colocada com sucesso no tabuleiro.

        Eventos:
            - Detecta cliques de mouse e interações com o teclado.
            - Verifica a seleção de cartas e a colocação correta no tabuleiro.
            - Executa animações de movimento de cartas ao serem colocadas.
            - Verifica e processa a captura de cartas de acordo com as regras do jogo.
            - Exibe pontuações, turnos e condições de vitória.
            - Permite reinicializar o jogo após o término.

        Lógica de jogo:
            - Inicia o jogo após a interação no menu inicial.
            - Alterna o turno entre os jogadores.
            - Verifica as condições de vitória ou empate após a colocação de 9 cartas no tabuleiro.
            - Reproduz efeitos sonoros e visuais como captura de cartas e vitória.
            - Reinicializa o tabuleiro e as pontuações quando o jogo termina.

        :param None:
        :return None:

        Saída:
            - Atualiza a tela do jogo com o estado atual.
            - Reinicializa o jogo se uma condição de fim for atendida (como vitória ou empate).
        """

        turno = 1
        cartaSelecionada = None
        placed = False
        
        while self.running:
            self.fps.tick(30)
            mouseX, mouseY = pygame.mouse.get_pos()
            self.processarHover((mouseX,mouseY),turno)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Sai do modo fullscreen
                        pygame.quit()
                        exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    print(f"Mouse clicked at: ({mouseX}, {mouseY})")

                    if not self.jogoIniciado and not self.distribuindo:
                        bIniciar, bSair = self.menuInicial.desenharMenu()
                        if self.menuInicial.clickBotao(bIniciar, mouseX, mouseY):
                            self.sfxBotao.play()
                            self.mesa = Mesa(self.player1, self.player2)
                            self.mesa.distribuirCartas(self.telaPrincipal, self.bg,self.bgX,self.bgY, self.sfxCardPick, self.player1,self.player2,self.bgLetras)
                            self.swap()
                            self.jogoIniciado = True

                        elif self.menuInicial.clickBotao(bSair, mouseX, mouseY):
                            pygame.quit()
                            exit()
                    else:
                        if not self.select:
                            cartaSelecionada,self.select = self.processarEventoClique((mouseX, mouseY), turno)
                            placed = False
                            if cartaSelecionada:
                                print("Select recebeu true")
                                self.sfxCardPick.play()
                                
                        else:
                            if cartaSelecionada:
                                for (linha, coluna), slot in self.board.slots.items():
                                    print(f"Checking slot at ({linha}, {coluna}) with rect: {slot['rect']}")
                                    if slot['rect'].collidepoint(mouseX,mouseY):
                                        posInicial = cartaSelecionada.pos
                                        posFinal = slot['rect'].topleft
                                        
                                        print(f"Slot at ({linha}, {coluna}) was clicked.")
                                        if self.board.slots[(linha, coluna)]['carta'] is None:
                                            self.l = linha
                                            self.c = coluna
                                            placed = True
                                            cartaSelecionada.animarMovimento(self.telaPrincipal, posInicial, posFinal, self.bg, turno, self.bgX, self.bgY, self.board)
                                            self.sfxColocarCarta.play()
                                            cartaSelecionada.visual = cartaSelecionada.desenharCarta(200,200)
                                            self.board.colocarCarta(cartaSelecionada, linha, coluna, turno)
                                            self.select = False
                                            captura, plus = self.board.verificarVizinhas(linha, coluna, cartaSelecionada, self.sfxCaptura,self.bg, turno, self.bgX, self.bgY, self.board)
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
                                            placed = False
                                    else:
                                        print("Problema na seleção de slot")            
                                if not placed:
                                    cartaSelecionada.selected = False
                                    cartaSelecionada,self.select = self.processarEventoClique((mouseX, mouseY), turno)
                                else:
                                    c = True
                                    while c:
                                        
                                        self.telaPrincipal.blit(Mesa.confirmPlayer(self.telaPrincipal,turno-1,self.bg,self.bgX,self.bgY),(0,0))
                                        
                                        for event in pygame.event.get():
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                c = False
                                        pygame.display.update()
                            else:
                                print("Problema na seleção da carta")                       
            if not self.jogoIniciado:
                self.menuInicial.desenharMenu()
            else:
                self.board.desenharTabuleiro(self.bg, turno, self.bgX, self.bgY)
                if self.l is not None and self.c is not None:
                    pygame.draw.rect(self.telaPrincipal, (0, 255, 0), self.board.slots[(self.l, self.c)]['carta'].rect, width=1)
                self.player1.desenharPontuacao(self.telaPrincipal, LARGURA_TELA*0.1, 20)  # Exibe a pontuação do player 1 no canto superior esquerdo
                self.player2.desenharPontuacao(self.telaPrincipal, LARGURA_TELA * 0.8, 20)  # Exibe a pontuação do player 2 logo abaixo
                Mesa.desenharTurno(self.telaPrincipal,self.player1,self.player2,turno-1,False,self.bgLetras)

            # Game end condition
            if self.board.cartasColocadas == 9:
                # Victory check
                if self.checarVitoria(self.player1, self.player2) == 1:
                    self.sfxWinP1.play()
                    self.board.desenharVitoria(self.imgWinP1,self.bgX,self.bgY)
                    pygame.display.update()

                elif self.checarVitoria(self.player1, self.player2) == 2:
                    self.sfxWinP2.play()
                    self.board.desenharVitoria(self.imgWinP2,self.bgX,self.bgY)
                    pygame.display.update()
                else:
                    self.sfxEmpate.play()
                time.sleep(5)

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