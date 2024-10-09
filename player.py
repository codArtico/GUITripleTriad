class Player:
    def __init__(self,nump):
        self.pontos = 5
        self.numPlayer = nump

    def downPoint(self):
        self.pontos -= 1
    
    def upPoint(self):
        self.pontos +=1