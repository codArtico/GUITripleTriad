from configs import *
from carta import Carta

direcoes = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

oposto = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}

class Tabuleiro:
    def __init__(self, tela, imgSlot, imgBorda, largura, altura, p1, p2, cartaViradaBlue, cartaViradaRed):
        """
        Inicializa a classe Tabuleiro com os parâmetros dados.
 
        :param tela (pygame.Surface): A superficie (ou surface) onde o tabuleiro será desenhado.
        :param imgSlot (pygame.Surface): A imagem dos slots do tabuleiro.
        :param imgBorda (pygame.Surface): A borda do tabuleiro e divisória dos slots.
        :param largura (int): A largura do tabuleiro.
        :param altura (int): A altura do tabuleiro.
        :param p1 (Player):  O Player 1.
        :param p2 (Player): O Player 2.
        :param cartaViradaBlue (pygame.Surface): A imagem da carta virada para baixo.
        :param cartaViradaRed (pygame.Surface): A imagem da carta virada para baixo.
        """
        self.tela = tela
        self.imagemSlot = imgSlot
        self.imagemBorda = imgBorda
        self.imagemCartaViradaBlue = cartaViradaBlue
        self.imagemCartaViradaRed = cartaViradaRed
        self.linhas, self.colunas = 3, 3

        # Proporções para largura e altura do slot
        slotProp = 0.15  # Porcentagem da largura da tela
        self.larguraSlot = int(largura * slotProp)
        self.alturaSlot = self.larguraSlot  # Mantém proporção quadrada

        self.tamanhoBorda = 5
        self.larguraTabuleiro = self.larguraSlot * self.colunas
        self.alturaTabuleiro = self.alturaSlot * self.linhas

        # Centralização do tabuleiro
        self.offsetX = (largura - self.larguraTabuleiro) // 2
        self.offsetY = (altura - self.alturaTabuleiro) // 2

        # Inicializa os slots do tabuleiro
        self.slots = {}
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                rect = pygame.Rect(self.offsetX + coluna * self.larguraSlot,
                                    self.offsetY + linha * self.alturaSlot,
                                    self.larguraSlot, self.alturaSlot)
                self.slots[(linha, coluna)] = {'rect': rect, 'carta': None}

        self.cartasColocadas = 0
        self.p1 = p1
        self.p2 = p2

    def processarCliqueTabuleiro(self, posicaoMouse, cartaSelecionada, turno):
        """
        Processa o clique do mouse no tabuleiro.

        :param posicaoMouse (tuple): As coordenadas do clique do mouse.
        :param cartaSelecionada (Carta): A carta que está selecionada pelo Player.
        :param turno (int): O turno atual.

        :return bool: True se a carta for colocada corretamente no tabuleiro, False se não.
        """
        # Itera pelos slots do tabuleiro para verificar se o clique foi em um slot válido
        for (linha, coluna), slot in self.slots.items():  # Corrigido para usar self.slots diretamente
            if slot['rect'].collidepoint(posicaoMouse):  # Verifica se o clique está dentro do retângulo do slot
                # Tenta colocar a carta no slot
                if self.colocarCarta(cartaSelecionada, linha, coluna, turno):  # Usando self.colocarCarta diretamente
                    print(f"Carta colocada no slot: linha {linha}, coluna {coluna}")
                    return True  # Carta colocada com sucesso
        print("Nenhum slot disponível foi clicado.")  # Mensagem para depuração se nenhum slot foi clicado
        return False  # Nenhum slot disponível foi clicado


    def desenharVitoria(self,img,bgX,bgY):
        self.tela.blit(img,(bgX,bgY))
    def desenharVitoria(self, img, bgX, bgY):
        """
        Desenha a imagem do Player vitorioso na tela.

        :param img (pygame.Surface): A imagem que será mostrada na tela.
        :param bgX (int): A coordenada X da imagem do background.
        :param bgY (int): A coordenada Y da imagem do background.

        :return None:
        """
        self.tela.blit(img, (bgX, bgY))


    def desenharTabuleiro(self, bg, turno, bgX, bgY):
        """
        Desenha o tabuleiro, com os slots e as cartas.

        :param bg (pygame.Surface): The background image to be drawn on the game board.
        :param turno (int): The current player's turn.
        :param bgX (int): The x-coordinate of the background image.
        :param bgY (int): The y-coordinate of the background image.

        :return None:
        """
        self.tela.blit(bg, (bgX, bgY))
        self.desenharCartasBlue(turno)
        self.desenharCartasRed(turno)

        for (linha, coluna), slot in self.slots.items():
            posX = self.offsetX + coluna * self.larguraSlot
            posY = self.offsetY + linha * self.alturaSlot
            slot['rect'].topleft = (posX, posY)

            # Redimensionar e desenhar a borda
            borda = pygame.transform.scale(self.imagemBorda, (
                self.larguraSlot + 2 * self.tamanhoBorda, self.alturaSlot + 2 * self.tamanhoBorda))
            self.tela.blit(borda, (posX - self.tamanhoBorda, posY - self.tamanhoBorda))

            # Redimensionar e desenhar o slot
            imgSlot = pygame.transform.scale(self.imagemSlot, (self.larguraSlot, self.alturaSlot))
            self.tela.blit(imgSlot, slot['rect'].topleft)

            # Desenha a carta se existir
            if slot['carta'] is not None:
                carta = slot['carta']
                # Redimensionar a carta para manter a proporção
                newLargura = int(self.larguraSlot * 0.8)  # Ajuste conforme necessário
                newAltura = int(self.alturaSlot * 0.8)  # Ajuste conforme necessário
                carta.visual = pygame.transform.smoothscale(carta.visual, (newLargura, newAltura))
                carta.rect = pygame.Rect(posX + (self.larguraSlot - newLargura) // 2, 
                                         posY + (self.alturaSlot - newAltura) // 2, newLargura, newAltura)
                self.tela.blit(carta.visual, carta.rect.topleft)


    def colocarCarta(self, carta, linha, coluna, turno):
        """
        Coloca a carta em uma linha e coluna específica.

        :param carta (Carta): A carta que será colocada no tabuleiro.
        :param linha (int): A linha que a carta será colocada.
        :param coluna (int): A coluna que a carta será colocada.
        :param turno (int): O turno atual.

        :return bool: True se a carta for colocada com sucesso no tabuleiro, False se não.
        """
        # Check if the slot is empty before placing the card
        if self.slots[(linha, coluna)]['carta'] is None:
            # Set the size of the card's rect to 175x175
            carta.rect = pygame.Rect(0, 0, 175, 175)  # Adjust to 175x175
            carta.rect.center = self.slots[(linha, coluna)]['rect'].center  # Center the card's rect

            self.slots[(linha, coluna)]['carta'] = carta
            carta.dono = self.p1 if turno == 1 else self.p2
            print(f"Carta colocada em: linha {linha}, coluna {coluna}")
            self.cartasColocadas += 1

            # Remove the card from the current player's hand
            if turno == 1:
                self.p1.cartasSelecionadas.remove(carta)
            elif turno == 2:
                self.p2.cartasSelecionadas.remove(carta)
            return True
        else:
            print("O slot já está ocupado!")  # Debug message if the slot is already occupied
        return False


    def verificarVizinhas(self, linha, coluna, carta, somCaptura, bg, turno, bgX, bgY, tabuleiro):
        """
        Checa as cartas adjacentes e captura as cartas de acordo com as regras do jogo.

        :param linha (int): O indice da linha da carta.
        :param coluna (int): O indice da coluna da carta.
        :param carta (Carta): A carta a ser checada suas adjacências..
        :param somCaptura (pygame.mixer.Sound): O som a ser tocada quando uma catura padrão é realizada.
        :param bg (pygame.Surface): A tela de background.
        :param turno (int): O turno atual.
        :param bgX (int): A coordenada x do background.
        :param bgY (int): A coordenada y do background.
        :param tabuleiro (Tabuleiro): O tabbuleiro do jogo.

        :return captura (bool): True se alguma carta foi capturada, False se não.
        :return (bool): True se a regra PLUS foi aplicada, False se não.
        """
        captura = False
        plus = False

        somas = []
        cartasAdj = {}

        # Iterate over the directions to find adjacent cards
        for direcao, (dx, dy) in direcoes.items():
            ax, ay = linha + dx, coluna + dy

            if 0 <= ax < 3 and 0 <= ay < 3 and self.slots[(ax, ay)]['carta'] is not None:
                cartaAdjacente = self.slots[(ax, ay)]['carta']

                valorAtual = carta.valores[direcao]
                valorAdjacente = cartaAdjacente.valores[oposto[direcao]]

                # Convertendo valores 'A' para 10
                if valorAtual == "A":
                    valorAtual = 10
                if valorAdjacente == "A":
                    valorAdjacente = 10

                if valorAtual > valorAdjacente and cartaAdjacente.dono != carta.dono:
                    # Captura a carta adjacente
                    cartaAdjacente = cartaAdjacente.animaCaptura(self.tela,carta.dono, bg, turno, bgX, bgY, tabuleiro)


                    carta.dono.upPoint()  # Atualiza a pontuação do jogador que capturou a carta
                    self.getAdversario(carta.dono).downPoint()  # Atualiza a pontuação do adversário
                    captura = True

                soma = valorAtual + valorAdjacente
                somas.append((direcao, soma))
                cartasAdj[direcao] = cartaAdjacente

        # Implementação da regra PLUS
        somaDict = {}
        for direcao, soma in somas:
            if soma not in somaDict:
                somaDict[soma] = []
            somaDict[soma].append(direcao)

        # Check if there are multiple directions with the same sum value (PLUS rule)
        for soma, direcoesLista in somaDict.items():
            if len(direcoesLista) > 1:
                for direcao in direcoesLista:
                    cartaAdj = cartasAdj[direcao]
                    if cartaAdj.dono != carta.dono:
                        # Captura cards adjacent according to the PLUS rule
                        cartaAdj = cartaAdj.animaCaptura(self.tela,carta.dono, bg, turno, bgX, bgY, tabuleiro)
                        somCaptura.play()
                        carta.dono.upPoint()
                        self.getAdversario(carta.dono).downPoint()
                        print(f'{carta.dono.pontos} x {self.getAdversario(carta.dono).pontos}')
                        captura = True
                        plus = True

        return captura, plus


    def desenharCartasBlue(self, turno):
        """
        Desenha as cartas do Player 1 (Blue) na tela, redimensionando e verificando interações com o mouse.

        :param turno (int): O turno atual (1 ou 2).
        
        :return None:
        """
        alturaTela = self.tela.get_height()
        larguraTela = self.tela.get_width()
        posX = larguraTela - larguraTela + 50
        posY = alturaTela // 2 - 300
        mousePos = pygame.mouse.get_pos()
        
        if turno == 1:
            cartas = self.p1.cartasSelecionadas
        else:
            cartas = [self.imagemCartaViradaBlue] * self.p1.numCartas

        for i in range(len(cartas)):
            # Verifica se a carta é uma instância da classe Carta
            if isinstance(cartas[i], Carta):
                if cartas[i].rect.collidepoint(mousePos):
                    cartas[i].hovered = True
                else:
                    cartas[i].hovered = False

                if not cartas[i].selected:
                    imgCarta = cartas[i].visual
                    imgCarta = pygame.transform.smoothscale(imgCarta, (175, 175))  # Redimensiona a imagem da carta

                else:
                    imgCarta = cartas[i]
                    imgCarta = imgCarta.desenharCarta(202,202)
                    
                # Redimensiona o rect da carta
                newLargura = 120
                newAltura = 150
                # Cria um novo rect centralizado na posição da carta
                cartas[i].rect = pygame.Rect(0, 0, newLargura, newAltura)
                cartas[i].rect.center = (posX + 87.5, posY + 87.5)  # Centraliza o rect em relação à carta

                imgRect = imgCarta.get_rect(center=cartas[i].rect.center)
                cartas[i].pos = imgRect.topleft

                if cartas[i].hovered:
                    overlay = imgCarta.copy()  # Copia a imagem da carta para aplicar uma sobreposição
                    overlay.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)  # Clareamento leve
                    self.tela.blit(overlay, imgRect.topleft)
                    
                else:
                    self.tela.blit(imgCarta, imgRect.topleft)
        
            else:
                imgCarta = cartas[i]
                imgCarta = pygame.transform.smoothscale(imgCarta, (175, 175))

                # Cria um rect para a imagem da carta virada com largura reduzida
                newLargura = 120  # Define a nova largura desejada
                newAltura = 150   # Define a nova altura desejada
                rect = pygame.Rect(0, 0, newLargura, newAltura)
                rect.center = (posX + 87.5, posY + 87.5)  # Centraliza o rect
                imgRect = imgCarta.get_rect(center=rect.center)

            # Desenha a carta na tela
                self.tela.blit(imgCarta, imgRect.topleft)

            # Atualiza a posição para a próxima carta
            posY += 200
            if i == 2 and len(cartas) > 3:
                posX += 150
                posY = alturaTela // 2 - 200

    def desenharCartasRed(self, turno):
        """
        Desenha as cartas do Player 2 (Red) na tela, redimensionando e verificando interações com o mouse.

        :param turno (int): O turno atual (1 ou 2).
        
        :return None:
        """
        alturaTela = self.tela.get_height()
        larguraTela = self.tela.get_width()

        posX = larguraTela - 180
        posY = alturaTela // 2 - 300  # Altura da linha de 2

        mousePos = pygame.mouse.get_pos()

        if turno == 2:
            cartas = self.p2.cartasSelecionadas
        else:
            cartas = [self.imagemCartaViradaRed] * self.p2.numCartas

        for i in range(len(cartas)):
            # Verifica se a carta é uma instância da classe Carta
            if isinstance(cartas[i], Carta):
                if cartas[i].rect.collidepoint(mousePos):
                    cartas[i].hovered = True
                else:
                    cartas[i].hovered = False

                if not cartas[i].selected:
                    imgCarta = cartas[i].visual
                    imgCarta = pygame.transform.smoothscale(imgCarta, (175, 175))  # Redimensiona a imagem da carta
                else:
                    imgCarta = cartas[i].desenharCarta(202, 202)

                # Cria um rect manualmente para a carta com tamanho 120x150
                cartas[i].rect = pygame.Rect(0, 0, 120, 150)
                cartas[i].rect.center = (posX + 60, posY + 75)  # Centraliza o rect

                # Desenha a carta na tela
                imgRect = imgCarta.get_rect(center=cartas[i].rect.center)
                cartas[i].pos = imgRect.topleft

                # Aplica uma sobreposição ao hover
                if cartas[i].hovered:
                    overlay = imgCarta.copy()  # Copia a imagem da carta para aplicar uma sobreposição
                    overlay.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_ADD)  # Clareamento leve
                    self.tela.blit(overlay, imgRect.topleft)
                else:
                    self.tela.blit(imgCarta, imgRect.topleft)

            else:
                # Desenha a carta virada se não for instância de Carta
                imgCarta = pygame.transform.smoothscale(cartas[i], (175, 175))
                rect = pygame.Rect(0, 0, 120, 150)
                rect.center = (posX + 60, posY + 75)
                imgRect = imgCarta.get_rect(center=rect.center)
                self.tela.blit(imgCarta, imgRect.topleft)

            # Atualiza a posição para a próxima carta
            posY += 200
            if i == 2 and len(cartas) > 3:
                posX -= 150
                posY = alturaTela // 2 - 200

    def getAdversario(self, p):
        '''
        Retorna o adversário de um player.

        :param p (Player): O player de referência.
        :return (Player): O adversário do player. Player 2 se o Player 1 foi informado e vice-versa.
        '''
        return self.p1 if p == self.p2 else self.p2