from configs import *

class Menu:
    def __init__(self, tela, bg, logo, bIni, bSair):
        self.tela = tela
        self.bg = bg
        self.logo = logo
        self.bIni = bIni
        self.bSair = bSair

        # Definindo versões alternativas dos botões para o efeito de hover
        self.bIniHover = pygame.transform.smoothscale(bIni, (int(350 * 1.2), int(85 * 1.2)))
        self.bSairHover = pygame.transform.smoothscale(bSair, (int(350 * 1.2), int(85 * 1.2)))

    def desenharMenu(self):

        # Dimensões da tela
        larguraTela, alturaTela = self.tela.get_size()

        # Dimensões da imagem de fundo
        bgLargura, bgAltura = self.bg.get_size()

        # Calcular a posição para centralizar a imagem de fundo
        bgX = (larguraTela - bgLargura) // 2
        bgY = (alturaTela - bgAltura) // 2

        # Desenhe o fundo
        self.tela.blit(self.bg, (bgX, bgY))

        # Dimensões da tela
        larguraTela, alturaTela = self.tela.get_size()

        # Defina proporções relativas para logo e botões
        larguraLogo = int(larguraTela * 0.3)  # 50% da largura da tela
        alturaLogo = int(larguraLogo * (self.logo.get_height() / self.logo.get_width()))  # Mantém a proporção

        bIniLargura = int(larguraTela * 0.3) // 1.1   # 30% da largura da tela
        bIniAltura = int(alturaTela * 0.13) // 1.1 # 10% da altura da tela

        bsairLargura = bIniLargura  # O botão Sair tem a mesma largura que o botão Iniciar
        bSairAltura = bIniAltura  # O botão Sair tem a mesma altura que o botão Iniciar

        # Calcular posições centrais dinâmicas
        logoX = (larguraTela - larguraLogo) // 2
        logoY = int(alturaTela * 0.02)  # 10% do topo da tela

        bIniX = (larguraTela - bIniLargura) // 2  # Botão Iniciar
        bIniY = int(alturaTela * 0.45)  # 40% da altura da tela

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

    # Função para verificar se o mouse está sobre um botão
    @staticmethod
    def isHover(mouseX, mouseY, rect):
        return rect[0] <= mouseX <= rect[0] + rect[2] and rect[1] <= mouseY <= rect[1] + rect[3]

    # Função para verificar clique no botão
    def clickBotao(self, area, mouseX, mouseY):
        return self.isHover(mouseX, mouseY, area)
