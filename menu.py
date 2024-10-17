from configs import *

class Menu:
    def __init__(self, tela, bg, logo, botao, bIni, bSair):
        self.tela = tela
        self.bg = bg
        self.logo = logo
        self.botao = botao
        self.bIni = bIni
        self.bSair = bSair

        # Definindo versões alternativas dos botões para o efeito de hover
        self.bIni_hover = pygame.transform.smoothscale(bIni, (int(350 * 1.2), int(85 * 1.2)))
        self.bSair_hover = pygame.transform.smoothscale(bSair, (int(350 * 1.2), int(85 * 1.2)))

    def desenharMenu(self):

        # Dimensões da tela
        tela_largura, tela_altura = self.tela.get_size()

        # Dimensões da imagem de fundo
        bg_largura, bg_altura = self.bg.get_size()

        # Calcular a posição para centralizar a imagem de fundo
        bg_pos_x = (tela_largura - bg_largura) // 2
        bg_pos_y = (tela_altura - bg_altura) // 2

        # Desenhe o fundo
        self.tela.blit(self.bg, (bg_pos_x, bg_pos_y))

        # Dimensões da tela
        tela_largura, tela_altura = self.tela.get_size()

        # Defina proporções relativas para logo e botões
        logo_largura = int(tela_largura * 0.3)  # 50% da largura da tela
        logo_altura = int(logo_largura * (self.logo.get_height() / self.logo.get_width()))  # Mantém a proporção

        bIni_largura = int(tela_largura * 0.3) // 1.1   # 30% da largura da tela
        bIni_altura = int(tela_altura * 0.13) // 1.1 # 10% da altura da tela

        bSair_largura = bIni_largura  # O botão Sair tem a mesma largura que o botão Iniciar
        bSair_altura = bIni_altura  # O botão Sair tem a mesma altura que o botão Iniciar

        # Calcular posições centrais dinâmicas
        logo_pos_x = (tela_largura - logo_largura) // 2
        logo_pos_y = int(tela_altura * 0.02)  # 10% do topo da tela

        bIni_pos_x = (tela_largura - bIni_largura) // 2  # Botão Iniciar
        bIni_pos_y = int(tela_altura * 0.45)  # 40% da altura da tela

        bSair_pos_x = (tela_largura - bSair_largura) // 2  # Botão Sair
        bSair_pos_y = int(tela_altura * 0.6)  # 60% da altura da tela

        # Redimensionar os botões
        self.bIni = pygame.transform.smoothscale(self.bIni, (bIni_largura, bIni_altura))
        self.bSair = pygame.transform.smoothscale(self.bSair, (bSair_largura, bSair_altura))

        # Desenhar o logotipo
        self.tela.blit(pygame.transform.smoothscale(self.logo, (logo_largura, logo_altura)), (logo_pos_x, logo_pos_y))

        # Obtém a posição do mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Verifica se o mouse está sobre o botão "Iniciar"
        if self.is_hover(mouse_x, mouse_y, (bIni_pos_x, bIni_pos_y, bIni_largura, bIni_altura)):
            self.tela.blit(self.bIni_hover, (bIni_pos_x, bIni_pos_y))  # Mostra a versão hover
        else:
            self.tela.blit(self.bIni, (bIni_pos_x, bIni_pos_y))  # Mostra a versão normal

        # Verifica se o mouse está sobre o botão "Sair"
        if self.is_hover(mouse_x, mouse_y, (bSair_pos_x, bSair_pos_y, bSair_largura, bSair_altura)):
            self.tela.blit(self.bSair_hover, (bSair_pos_x, bSair_pos_y))  # Mostra a versão hover
        else:
            self.tela.blit(self.bSair, (bSair_pos_x, bSair_pos_y))  # Mostra a versão normal

        area_iniciar = (bIni_pos_x, bIni_pos_y, bIni_largura, bIni_altura)
        area_sair = (bSair_pos_x, bSair_pos_y, bSair_largura, bSair_altura)
        return area_iniciar, area_sair

    # Função para verificar se o mouse está sobre um botão
    @staticmethod
    def is_hover(mouse_x, mouse_y, rect):
        return rect[0] <= mouse_x <= rect[0] + rect[2] and rect[1] <= mouse_y <= rect[1] + rect[3]

    # Função para verificar clique no botão
    def click_botao(self, area, mouse_x, mouse_y):
        return self.is_hover(mouse_x, mouse_y, area)
