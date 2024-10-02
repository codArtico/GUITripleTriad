class Menu:
    def __init__(self, tela, bg, logo, botao, bIni, bSair):
        self.tela = tela
        self.bg = bg
        self.logo = logo
        self.botao = botao
        self.bIni = bIni
        self.bSair = bSair

    def desenharMenu(self):
        self.tela.blit(self.bg, (0, 0))
        self.tela.blit(self.logo, (580, 0))
        self.tela.blit(self.botao, (480, 120))
        self.tela.blit(self.bIni, (510, 330))
        self.tela.blit(self.botao, (480, 270))
        self.tela.blit(self.bSair, (510, 480))

        area_iniciar = (480 + 37, 120 + 220, 540, 130)
        area_sair = (480 + 37, 270 + 220, 540, 130)
        return area_iniciar, area_sair

    def click_botao(self, area, mouse_x, mouse_y):
        return area[0] <= mouse_x <= area[0] + area[2] and area[1] <= mouse_y <= area[1] + area[3]