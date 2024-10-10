import pygame
class Tabuleiro:
    def __init__(self, tela, imagem_slot, imagem_borda, largura, altura,p1,p2):
        self.tela = tela
        self.imagemSlot = imagem_slot
        self.imagemBorda = imagem_borda
        self.linhas, self.colunas = 3, 3
        self.tamanhoSlotAltura = altura // 1.2 // self.linhas
        self.tamanhoSlotLargura = self.tamanhoSlotAltura
        self.tamanhoBorda = 5
        self.larguraTabuleiro = self.tamanhoSlotLargura * self.colunas
        self.alturaTabuleiro = self.tamanhoSlotAltura * self.linhas
        self.offset_x = (largura - self.larguraTabuleiro) // 2
        self.offset_y = (altura - self.alturaTabuleiro) // 2

        # Inicializa os slots do tabuleiro
        self.slots = [[None for _ in range(self.colunas)] for _ in range(self.linhas)]
        self.cartasColocadas = 0

        self.p1=p1
        self.p2=p2

    def desenharTabuleiro(self):
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                pos_x = self.offset_x + coluna * self.tamanhoSlotLargura
                pos_y = self.offset_y + linha * self.tamanhoSlotAltura
                slot = pygame.transform.scale(self.imagemSlot, (self.tamanhoSlotLargura, self.tamanhoSlotAltura))
                borda = pygame.transform.scale(self.imagemBorda, (self.tamanhoSlotLargura + 2 * self.tamanhoBorda, self.tamanhoSlotAltura + 2 * self.tamanhoBorda))
                self.tela.blit(borda, (pos_x - self.tamanhoBorda, pos_y - self.tamanhoBorda))
                self.tela.blit(slot, (pos_x, pos_y))

                # Desenha a carta se existir
                if self.slots[linha][coluna] is not None:
                    carta = self.slots[linha][coluna]
                    self.tela.blit(carta.visual, (pos_x, pos_y))

    def colocarCarta(self, carta, linha, coluna):
        if 0 <= linha < self.linhas and 0 <= coluna < self.colunas:
            self.slots[linha][coluna] = carta  # Coloca a carta no slot
            self.cartasColocadas +=1

    def verificarVizinhas(self, linha, coluna, carta):
        captura = False
        direcoes = {
            "cima": (-1, 0),
            "baixo": (1, 0),
            "esquerda": (0, -1),
            "direita": (0, 1),
        }

        somas = []
        cartasAdj = {}
        oposto = {
            "cima": "baixo",
            "baixo": "cima",
            "esquerda": "direita",
            "direita": "esquerda",
        }

        for direcao, (dx, dy) in direcoes.items():
            ax, ay = linha + dx, coluna + dy

            if 0 <= ax < 3 and 0 <= ay < 3 and self.slots[ax][ay]:
                cartaAdjacente = self.slots[ax][ay]

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
                        carta.dono.upPoint() # Atualiza a pontuação do jogador que capturou a carta
                        self.getAdversario(carta.dono).downPoint()# Atualiza a pontuação do adversário
                        print(
                            f"Carta na posição {ax},{ay} capturada pela regra padrão!"
                        )
                        captura = True

                soma = valorAtual + valorAdjacente
                somas.append((direcao, soma))
                cartasAdj[direcao] = cartaAdjacente

        # Implementação da regra PLUS
        soma_dict = {}
        for direcao, soma in somas:
            if soma not in soma_dict:
                soma_dict[soma] = []
            soma_dict[soma].append(direcao)
            print(f'CArta add: {direcao}')


        # Verifica se há múltiplas direções com o mesmo valor de soma
        for soma, direcoes_lista in soma_dict.items():
            if len(direcoes_lista) > 1:
                for direcao in direcoes_lista:
                    cartaAdj = cartasAdj[direcao]
                    if cartaAdj.dono != carta.dono:
                        cartaAdj.switchDono(carta.dono)
                        carta.dono.upPoint()
                        self.getAdversario(carta.dono).downPoint()
                        print(
                            f"Carta na posicao {direcao} capturada pela regra PLUS!"
                        )
                        captura = True
        
        return captura

    def getAdversario(self, p):
        return self.p1 if p == self.p2 else self.p2