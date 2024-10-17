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
        # Itera pelos slots do tabuleiro para verificar se o clique foi em um slot válido
        for (linha, coluna), slot in self.slots.items():  # Corrigido para usar self.slots diretamente
            if slot['rect'].collidepoint(posicaoMouse):  # Verifica se o clique está dentro do retângulo do slot
                # Tenta colocar a carta no slot
                if self.colocarCarta(cartaSelecionada, linha, coluna, turno):  # Usando self.colocarCarta diretamente
                    print(f"Carta colocada no slot: linha {linha}, coluna {coluna}")
                    return True  # Carta colocada com sucesso
        print("Nenhum slot disponível foi clicado.")  # Mensagem para depuração se nenhum slot foi clicado
        return False  # Nenhum slot disponível foi clicado


    def desenharTabuleiro(self, bg, turno, bgX, bgY):
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
    # Verifica se o slot está vazio antes de colocar a carta
        if self.slots[(linha, coluna)]['carta'] is None:
            # Define o tamanho do rect da carta para 175x175
            carta.rect = pygame.Rect(0, 0, 175, 175)  # Altere para 175x175
            carta.rect.center = self.slots[(linha, coluna)]['rect'].center  # Centraliza o rect da carta
            
            self.slots[(linha, coluna)]['carta'] = carta
            carta.dono = self.p1 if turno == 1 else self.p2
            print(f"Carta colocada em: linha {linha}, coluna {coluna}")
            self.cartasColocadas += 1
            
            # Remove a carta da mão do jogador atual
            if turno == 1:
                self.p1.cartasSelecionadas.remove(carta)
            elif turno == 2:
                self.p2.cartasSelecionadas.remove(carta)
            return True
        else:
            print("O slot já está ocupado!")  # Mensagem de depuração se o slot estiver ocupado
        return False

    def verificarVizinhas(self, linha, coluna, carta):
        captura = False
        plus = False

        somas = []
        cartasAdj = {}

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

                if valorAtual > valorAdjacente:
                    if cartaAdjacente.dono != carta.dono:
                        cartaAdjacente.switchDono(carta.dono)
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

        # Verifica se há múltiplas direções com o mesmo valor de soma
        for soma, direcoesLista in somaDict.items():
            if len(direcoesLista) > 1:
                for direcao in direcoesLista:
                    cartaAdj = cartasAdj[direcao]
                    if cartaAdj.dono != carta.dono:
                        cartaAdj.switchDono(carta.dono)
                        carta.dono.upPoint()
                        self.getAdversario(carta.dono).downPoint()
                        captura = True
                        plus = True

        return captura, plus

    def desenharCartasBlue(self, turno):
        alturaTela = self.tela.get_height()
        larguraTela = self.tela.get_width()
        posX = larguraTela - larguraTela + 50
        posY = alturaTela // 2 - 300

        if turno == 1:
            cartas = self.p1.cartasSelecionadas
        else:
            cartas = [self.imagemCartaViradaBlue] * self.p1.numCartas

        for i in range(len(cartas)):
            # Verifica se a carta é uma instância da classe Carta
            if isinstance(cartas[i], Carta):
                imgCarta = cartas[i].visual
                imgCarta = pygame.transform.smoothscale(imgCarta, (175, 175))  # Redimensiona a imagem da carta
                
                # Redimensiona o rect da carta
                newLargura = 120
                newAltura = 150
                # Cria um novo rect centralizado na posição da carta
                cartas[i].rect = pygame.Rect(0, 0, newLargura, newAltura)
                cartas[i].rect.center = (posX + 87.5, posY + 87.5)  # Centraliza o rect em relação à carta

            else:
                imgCarta = cartas[i]
                imgCarta = pygame.transform.smoothscale(imgCarta, (175, 175))

                # Cria um rect para a imagem da carta virada com largura reduzida
                newLargura = 120  # Define a nova largura desejada
                newAltura = 150   # Define a nova altura desejada
                rect = pygame.Rect(0, 0, newLargura, newAltura)
                rect.center = (posX + 87.5, posY + 87.5)  # Centraliza o rect

            # Desenha a carta na tela
            self.tela.blit(imgCarta, (posX, posY))

            # Atualiza a posição para a próxima carta
            posY += 200
            if i == 2 and len(cartas) > 3:
                posX += 150
                posY = alturaTela // 2 - 200



    def desenharCartasRed(self, turno):
        alturaTela = self.tela.get_height()
        larguraTela = self.tela.get_width()

        posX = larguraTela - 180
        posY = alturaTela // 2 - 300  # Altura da linha de 2

        if turno == 2:
            cartas = self.p2.cartasSelecionadas
        else:
            cartas = [self.imagemCartaViradaRed] * self.p2.numCartas

        for i in range(len(cartas)):
            # Verifica se a carta é uma instância da classe Carta
            if isinstance(cartas[i], Carta):
                imgCarta = cartas[i].visual
                imgCarta = pygame.transform.smoothscale(imgCarta, (175, 175))  # Redimensiona a imagem da carta
                
                # Cria um rect para a carta com tamanho 120x150
                cartas[i].rect = imgCarta.get_rect(size=(120, 150))
                cartas[i].rect.center = (posX + 60, posY + 75)  # Centraliza o rect

                # Desenha a carta na tela usando seu rect
                # Desloca a imagem para que fique centralizada no rect
                imgRect = imgCarta.get_rect(center=cartas[i].rect.center)
                self.tela.blit(imgCarta, imgRect.topleft)
            else:
                imgCarta = cartas[i]
                imgCarta = pygame.transform.smoothscale(imgCarta, (175, 175))

                # Se for uma imagem de carta virada, cria um rect para ela com tamanho 120x150
                rect = imgCarta.get_rect(size=(120, 150))
                rect.center = (posX + 60, posY + 75)  # Centraliza o rect

                # Desenha a carta na tela usando o rect criado
                imgRect = imgCarta.get_rect(center=rect.center)
                self.tela.blit(imgCarta, imgRect.topleft)

            # Atualiza a posição para a próxima carta
            posY += 200
            if i == 2 and len(cartas) > 3:
                posX -= 150
                posY = alturaTela // 2 - 200


    def getAdversario(self, p):
        return self.p1 if p == self.p2 else self.p2