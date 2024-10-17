from configs import *

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
    def __init__(self, tela, imagem_slot, imagem_borda, largura, altura, p1, p2, cartaViradaBlue, cartaViradaRed):
        self.tela = tela
        self.imagemSlot = imagem_slot
        self.imagemBorda = imagem_borda
        self.imagemCartaViradaBlue = cartaViradaBlue
        self.imagemCartaViradaRed = cartaViradaRed
        self.linhas, self.colunas = 3, 3
        self.altura_slot = altura // 1.2 // self.linhas
        self.largura_slot = self.altura_slot
        self.tamanhoBorda = 5
        self.larguraTabuleiro = self.largura_slot * self.colunas
        self.alturaTabuleiro = self.altura_slot * self.linhas
        self.offset_x = (largura - self.larguraTabuleiro) // 2
        self.offset_y = (altura - self.alturaTabuleiro) // 2

        # Inicializa os slots do tabuleiro
        self.slots = {}
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                rect = pygame.Rect(self.offset_x + coluna * self.largura_slot,
                                   self.offset_y + linha * self.altura_slot,
                                   self.largura_slot, self.altura_slot)
                self.slots[(linha, coluna)] = {'rect': rect, 'carta': None}
                print(f'Slot criado em: {self.slots[(linha,coluna)]['rect']}')
        self.cartasColocadas = 0

        self.p1 = p1
        self.p2 = p2

    def processarCliqueTabuleiro(self, posicao_mouse, carta_selecionada, turno):
        # Itera pelos slots do tabuleiro para verificar se o clique foi em um slot válido
        for (linha, coluna), slot in self.slots.items():  # Corrigido para usar self.slots diretamente
            if slot['rect'].collidepoint(posicao_mouse):  # Verifica se o clique está dentro do retângulo do slot
                # Tenta colocar a carta no slot
                if self.colocarCarta(carta_selecionada, linha, coluna, turno):  # Usando self.colocarCarta diretamente
                    print(f"Carta colocada no slot: linha {linha}, coluna {coluna}")
                    return True  # Carta colocada com sucesso
        print("Nenhum slot disponível foi clicado.")  # Mensagem para depuração se nenhum slot foi clicado
        return False  # Nenhum slot disponível foi clicado


    def desenharTabuleiro(self, bg, turno):
        self.tela.blit(bg, (0, 0))
        self.desenhar_cartas_blue(turno)
        self.desenhar_cartas_red(turno)

        for (linha, coluna), slot in self.slots.items():
            pos_x = self.offset_x + coluna * self.largura_slot
            pos_y = self.offset_y + linha * self.altura_slot
            slot['rect'].topleft = (pos_x, pos_y)
            slot = pygame.transform.scale(self.imagemSlot, (self.largura_slot, self.altura_slot))
            borda = pygame.transform.scale(self.imagemBorda, (
            self.largura_slot + 2 * self.tamanhoBorda, self.altura_slot + 2 * self.tamanhoBorda))
            self.tela.blit(borda, (pos_x - self.tamanhoBorda, pos_y - self.tamanhoBorda))
            self.tela.blit(slot, self.slots[(linha, coluna)]['rect'].topleft)

            # Desenha a carta se existir
            if self.slots[(linha, coluna)]['carta'] is not None:
                carta = self.slots[(linha, coluna)]['carta']
                self.tela.blit(carta.visual, carta.rect)

    def colocarCarta(self, carta, linha, coluna, turno):
        # Verifica se o slot está vazio antes de colocar a carta
        if self.slots[(linha, coluna)]['carta'] is None:
            self.slots[(linha, coluna)]['carta'] = carta
            carta.dono = self.p1 if turno == 1 else self.p2
            carta.rect.center = self.slots[(linha, coluna)]['rect'].center
            print(f"Carta colocada em: linha {linha}, coluna {coluna}")
            self.cartasColocadas += 1
            # Remove a carta da mão do jogador atual
            if turno == 1:
                self.p1.cartas_selecionadas.remove(carta)
            elif turno == 2:
                self.p2.cartas_selecionadas.remove(carta)
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
        soma_dict = {}
        for direcao, soma in somas:
            if soma not in soma_dict:
                soma_dict[soma] = []
            soma_dict[soma].append(direcao)

        # Verifica se há múltiplas direções com o mesmo valor de soma
        for soma, direcoes_lista in soma_dict.items():
            if len(direcoes_lista) > 1:
                for direcao in direcoes_lista:
                    cartaAdj = cartasAdj[direcao]
                    if cartaAdj.dono != carta.dono:
                        cartaAdj.switchDono(carta.dono)
                        carta.dono.upPoint()
                        self.getAdversario(carta.dono).downPoint()
                        captura = True
                        plus = True

        return captura, plus

    def desenhar_cartas_blue(self, turno):
        alturaTela = self.tela.get_height()
        posX = 50
        posY = alturaTela // 2 - 300
        if turno == 1:
            cartas = self.p1.cartas_selecionadas
        else:
            cartas = [self.imagemCartaViradaBlue] * self.p1.numCartas

        for i in range(len(cartas)):
            if isinstance(cartas[i], pygame.Surface):
                carta_img = cartas[i]
            else:
                carta_img = cartas[i].visual
                cartas[i].rect.center = (posX, posY)
            carta_img = pygame.transform.smoothscale(carta_img, (
            175, 175))  # Garante que a imagem da carta seja dimensionada corretamente
            self.tela.blit(carta_img, (posX, posY))

            posY += 200
            if i == 2 and len(cartas) > 3:
                posX += 150
                posY = alturaTela // 2 - 200

    def desenhar_cartas_red(self, turno):
        alturaTela = self.tela.get_height()
        larguraTela = self.tela.get_width()

        posX = larguraTela - 225
        posY = alturaTela // 2 - 300  # Altura da linha de 2

        if turno == 2:
            cartas = self.p2.cartas_selecionadas
        else:
            cartas = [self.imagemCartaViradaRed] * self.p2.numCartas

        for i in range(len(cartas)):
            if isinstance(cartas[i], pygame.Surface):
                carta_img = cartas[i]
            else:
                carta_img = cartas[i].visual
                cartas[i].rect.center = (posX, posY)  # Criar o retângulo com as dimensões corretas
            carta_img = pygame.transform.smoothscale(carta_img, (
                175, 175))  # Garante que a imagem da carta seja dimensionada corretamente
            self.tela.blit(carta_img, (posX, posY))

            posY += 200
            if i == 2 and len(cartas) > 3:
                posX -= 150
                posY = alturaTela // 2 - 200

    def getAdversario(self, p):
        return self.p1 if p == self.p2 else self.p2