class Carta:

    def lerValores(self,arquivo):
        valores = {}

        try:
            with open(arquivo, 'r') as dados:
                for linha in dados:
                    chave,valor = linha.strip().split('=')
                    valores[chave] = valor

        except FileNotFoundError:
            print(f'Erro: O arquivo {arquivo} não foi encontrado')
        except ValueError:
            print("Erro: Problema ao processar os dados do arquivo.")

        return valores
    
    def __init__(self,cima,direita,baixo,esquerda):
        self.cor = None
        self.valores = {
            'cima': cima,
            'direita': direita,
            'baixo': baixo,
            'esquerda': esquerda,
            
        }
        self.dono = None

    