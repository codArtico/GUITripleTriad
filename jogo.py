from configs import *

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
    def __init__(self, largura_tela, altura_tela):
        pygame.init()
        self.tela_principal = pygame.display.set_mode((largura_tela, altura_tela), pygame.FULLSCREEN)
        pygame.display.set_caption("Triple Triad")
        self.fps = pygame.time.Clock()
        self.running = True
        self.jogo_iniciado = False

        self.bg, self.imagemSlot, self.imagemBorda, self.logo, self.botao, self.bIni, self.bSair, self.cartaViradaBlue,self.cartaViradaRed, self.imgPlus = carregarImagens()

        
        # Dimensões da imagem de fundo
        self.bg_largura, self.bg_altura = self.bg.get_size()

            # Calcular a posição para centralizar a imagem de fundo
        self.bg_pos_x = (LARGURA_TELA - self.bg_largura) // 2
        self.bg_pos_y = (ALTURA_TELA - self.bg_altura) // 2

        self.posicao_animacao_x = -self.imgPlus.get_width()  # Começa fora da tela à esquerda
        self.posicao_animacao_y = (largura_tela - self.imgPlus.get_height()) // 2  # Centralizado verticalmente
        self.velocidade_animacao = 30
        self.trava = True
        self.select = False

        self.sfxCaptura, self.sfxColocarCarta, self.sfxPlus, self.sfxVitoria, self.sfxBotao, self.sfxEmpate, self.sfxWinP1, self.sfxWinP2, self.sfxCardPick = carregarSfxs()

        self.player1 = Player(1)
        self.player2 = Player(2)

        self.board = Tabuleiro(self.tela_principal, self.imagemSlot, self.imagemBorda, largura_tela, altura_tela, self.player1, self.player2, self.cartaViradaBlue, self.cartaViradaRed)
        self.menu_inicial = Menu(self.tela_principal, self.bg, self.logo, self.botao, self.bIni, self.bSair)
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
        c1 = self.player1.cartas_selecionadas.pop(i)
        c1.switchDono(self.player2)
        i = randint(0,4)
        c2 = self.player2.cartas_selecionadas.pop(i)
        c2.switchDono(self.player1)
        self.player1.cartas_selecionadas.append(c2)
        self.player2.cartas_selecionadas.append(c1)


    def animar_imagem(self, largura_tela):
        self.posicao_animacao_x += self.velocidade_animacao

        if self.posicao_animacao_x >= self.tela_principal.get_width() / 2 - 350 and self.animacaoPlusAtiva and self.trava:
            time.sleep(2)
            self.trava=False

        # Verifica se a imagem saiu da tela
        if self.posicao_animacao_x > largura_tela:
            self.animacaoPlusAtiva = False # Reinicia a animação
            self.posicao_animacao_x = -self.imgPlus.get_width()
            self.trava = True

    def renderizar(self, img):
        superficie_temporaria = pygame.Surface(self.tela_principal.get_size())
        superficie_temporaria.blit(self.tela_principal, (0, 0))
        self.animar_imagem(self.tela_principal.get_width())
        superficie_temporaria.blit(img, (self.posicao_animacao_x, self.posicao_animacao_y))
        self.tela_principal.blit(superficie_temporaria, (0, 0))
        pygame.display.flip()

    def processarEventoClique(self, posicao_mouse, vez):
        cartas = self.player1.cartas_selecionadas if vez == 1 else self.player2.cartas_selecionadas

        for carta in cartas:
            pygame.draw.rect(self.tela_principal, (255, 0, 0), carta.rect, 2)
            pygame.display.flip()
            if carta.rect.collidepoint(posicao_mouse):
                print(f'Carta selecionada')
                return carta  # Retorna a carta clicada

        return None

    def run(self):
        turno = 1  # 1 for player 1, 2 for player 2
        carta_selecionada = None

        while self.running:
            self.fps.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Sai do modo fullscreen
                        pygame.quit()
                        exit()


                # if event.type == pygame.VIDEORESIZE:
                #     self.tela_principal = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")

                    if not self.jogo_iniciado and not self.distribuindo:
                        botao_iniciar, botao_sair_menu = self.menu_inicial.desenharMenu()
                        if self.menu_inicial.click_botao(botao_iniciar, mouse_x, mouse_y):
                            self.sfxBotao.play()
                            self.mesa = Mesa(self.player1, self.player2)
                            self.mesa.distribuir_cartas(self.tela_principal, self.bg,self.bg_pos_x,self.bg_pos_y, self.sfxCardPick)
                            self.swap()
                            self.jogo_iniciado = True

                        elif self.menu_inicial.click_botao(botao_sair_menu, mouse_x, mouse_y):
                            pygame.quit()
                            exit()
                    else:
                        if not self.select:
                            carta_selecionada = self.processarEventoClique((mouse_x, mouse_y), turno)
                            if carta_selecionada:
                                self.select = True
                                print("Select recebeu true")
                        else:
                            if carta_selecionada:
                                for (linha, coluna), slot in self.board.slots.items():
                                    print(f"Checking slot at ({linha}, {coluna}) with rect: {slot['rect']}")
                                    if slot['rect'].collidepoint(mouse_x,mouse_y):
                                        print(f"Slot at ({linha}, {coluna}) was clicked.")
                                        if self.board.slots[(linha, coluna)]['carta'] is None:  # Check if the slot is empty
                                            self.board.colocarCarta(carta_selecionada, linha, coluna, turno)
                                            self.select = False
                                            captura, plus = self.board.verificarVizinhas(linha, coluna, carta_selecionada)
                                            if captura:
                                                if plus:
                                                    self.sfxPlus.play()
                                                    self.animacaoPlusAtiva = True
                                                else:
                                                    self.sfxCaptura.play()
                                            if turno == 1:
                                                if carta_selecionada in self.player1.cartas_selecionadas:
                                                    self.player1.cartas_selecionadas.remove(carta_selecionada)  # Remove a carta do jogador 1
                                                else:
                                                    print("Erro: Carta selecionada não está na lista de cartas_selecionadas do jogador 1")
                                            else:
                                                if carta_selecionada in self.player2.cartas_selecionadas:
                                                    self.player2.cartas_selecionadas.remove(carta_selecionada)  # Remove a carta do jogador 2
                                                else:
                                                    print("Erro: Carta selecionada não está na lista de cartas_selecionadas do jogador 2")

                                            carta_selecionada = None  # Reset the selected card
                                            turno = self.switchTurno(turno)
                                            break  # Exit the loop after placing the card
                                                
                                    else:
                                        print("Problema na seleção de slot")            
                            else:
                                print("Problema na seleção da carta")                        
            if not self.jogo_iniciado:
                self.menu_inicial.desenharMenu()
            else:
                self.board.desenharTabuleiro(self.bg, turno, self.bg_pos_x, self.bg_pos_y)

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
                self.jogo_iniciado = False
                self.player1 = Player(1)
                self.player2 = Player(2)
                
                # Recrie o tabuleiro com as dimensões originais
                self.board = Tabuleiro(self.tela_principal, self.imagemSlot, self.imagemBorda, LARGURA_TELA,
                                    ALTURA_TELA, self.player1, self.player2, self.cartaViradaBlue,
                                    self.cartaViradaRed)

            if self.animacaoPlusAtiva:
                self.animar_imagem(LARGURA_TELA)
                self.renderizar(self.imgPlus)

            pygame.display.update()


if __name__ == "__main__":
    game = Jogo(LARGURA_TELA, ALTURA_TELA)
    game.run()