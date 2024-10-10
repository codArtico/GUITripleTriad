class Player:
    def __init__(self, nump):
        self.pontos = 5
        self.numPlayer = nump
        self.deck = []
        self.cartas_selecionadas = []  # Atributo para armazenar cartas selecionadas
        self.numCartas = 5

    def downPoint(self):
        self.pontos -= 1
    
    def upPoint(self):
        self.pontos += 1
