from configs import *

class Menu:
    """
    Classe que representa o menu principal do jogo Triple Triad.
    O menu exibe uma tela com um fundo, um logotipo e botões para iniciar o jogo ou sair.
    """

    def __init__(self, tela, bg, logo, bIni, bSair):
        """
        Inicializa o menu com os elementos necessários.

        :param tela: A superfície da tela onde o menu será desenhado.
        :type tela: pygame.Surface
        :param bg: A imagem de fundo do menu.
        :type bg: pygame.Surface
        :param logo: A imagem do logotipo do jogo.
        :type logo: pygame.Surface
        :param bIni: A imagem do botão "Iniciar".
        :type bIni: pygame.Surface
        :param bSair: A imagem do botão "Sair".
        :type bSair: pygame.Surface
        """
        self.tela = tela  # Superfície da tela
        self.bg = bg  # Imagem de fundo
        self.logo = logo  # Imagem do logotipo
        self.bIni = bIni  # Botão "Iniciar"
        self.bSair = bSair  # Botão "Sair"

        # Definindo versões alternativas dos botões para o efeito de hover
        self.bIniHover = pygame.transform.smoothscale(bIni, (int(350 * 1.2), int(85 * 1.2)))
        self.bSairHover = pygame.transform.smoothscale(bSair, (int(350 * 1.2), int(85 * 1.2)))

    def desenharMenu(self):
        """
        Desenha o menu na tela, incluindo o fundo, logotipo e botões.
        Verifica se o mouse está sobre os botões e aplica o efeito de hover.

        :return: Tupla contendo as áreas dos botões "Iniciar" e "Sair".
        :rtype: tuple
        """
        # Dimensões da tela
        larguraTela, alturaTela = self.tela.get_size()

        # Dimensões da imagem de fundo
        bgLargura, bgAltura = self.bg.get_size()

        # Calcular a posição para centralizar a imagem de fundo
        bgX = (larguraTela - bgLargura) // 2
        bgY = (alturaTela - bgAltura) // 2

        # Desenhar o fundo
        self.tela.blit(self.bg, (bgX, bgY))

        # Definindo proporções relativas para logo e botões
        larguraLogo = int(larguraTela * 0.3)  # 30% da largura da tela
        alturaLogo = int(larguraLogo * (self.logo.get_height() / self.logo.get_width()))  # Mantém a proporção

        bIniLargura = int(larguraTela * 0.3) // 1.1   # 30% da largura da tela
        bIniAltura = int(alturaTela * 0.13) // 1.1  # 10% da altura da tela

        bsairLargura = bIniLargura  # O botão Sair tem a mesma largura que o botão Iniciar
        bSairAltura = bIniAltura  # O botão Sair tem a mesma altura que o botão Iniciar

        # Calcular posições centrais dinâmicas
        logoX = (larguraTela - larguraLogo) // 2
        logoY = int(alturaTela * 0.02)  # 2% do topo da tela

        bIniX = (larguraTela - bIniLargura) // 2  # Botão Iniciar
        bIniY = int(alturaTela * 0.45)  # 45% da altura da tela

        bSairX = (larguraTela - bsairLargura) // 2  # Botão Sair
        bSairY = int(alturaTela * 0.6)  # 60% da altura da tela

        # Redimensionar os botões
        self.bIni = pygame.transform.smoothscale(self.bIni, (bIniLargura, bIniAltura))
        self.bSair = pygame.transform.smoothscale(self.bSair, (bsairLargura, bSairAltura))

        # Desenhar o logotipo
        self.tela.blit(pygame.transform.smoothscale(self.logo, (larguraLogo, alturaLogo)), (logoX, logoY))

        # Obtém a posição do mouse
        mouseX, mouseY = pygame.mouse.get_pos()

        # Verifica se o mouse está sobre o botão "Iniciar"
        if self.isHover(mouseX, mouseY, (bIniX, bIniY, bIniLargura, bIniAltura)):
            self.tela.blit(self.bIniHover, (bIniX, bIniY))  # Mostra a versão hover
        else:
            self.tela.blit(self.bIni, (bIniX, bIniY))  # Mostra a versão normal

        # Verifica se o mouse está sobre o botão "Sair"
        if self.isHover(mouseX, mouseY, (bSairX, bSairY, bsairLargura, bSairAltura)):
            self.tela.blit(self.bSairHover, (bSairX, bSairY))  # Mostra a versão hover
        else:
            self.tela.blit(self.bSair, (bSairX, bSairY))  # Mostra a versão normal

        areaIni = (bIniX, bIniY, bIniLargura, bIniAltura)
        areaSair = (bSairX, bSairY, bsairLargura, bSairAltura)
        return areaIni, areaSair

    @staticmethod
    def isHover(mouseX, mouseY, rect):
        """
        Verifica se a posição do mouse está sobre um retângulo específico.

        :param mouseX: A posição X do mouse.
        :type mouseX: int
        :param mouseY: A posição Y do mouse.
        :type mouseY: int
        :param rect: As coordenadas e dimensões do retângulo (x, y, largura, altura).
        :type rect: tuple
        :return: True se o mouse estiver sobre o retângulo, False caso contrário.
        :rtype: bool
        """
        return rect[0] <= mouseX <= rect[0] + rect[2] and rect[1] <= mouseY <= rect[1] + rect[3]

    def clickBotao(self, area, mouseX, mouseY):
        """
        Verifica se houve um clique em um botão específico.

        :param area: A área do botão (x, y, largura, altura).
        :type area: tuple
        :param mouseX: A posição X do mouse.
        :type mouseX: int
        :param mouseY: A posição Y do mouse.
        :type mouseY: int
        :return: True se o botão foi clicado, False caso contrário.
        :rtype: bool
        """
        return self.isHover(mouseX, mouseY, area)