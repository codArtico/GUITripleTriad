class Player:
    def __init__(self, nump):
        self.deck = []
        self.pontos = 5
        self.numPlayer = nump
        self.cartasSelecionadas = []  # Atributo para armazenar cartas selecionadas
        self.numCartas = 5

    def downPoint(self):
        self.pontos -= 1

    def upPoint(self):
        self.pontos += 1
