class Retangulo:
    """
    Classe para representar um item retangular.
    Armazena suas dimensões e um ID para rastreamento.
    """
    def __init__(self, id, largura, altura):
        self.id = id
        self.largura = largura
        self.altura = altura

    def __repr__(self):
        return f"Ret(id={self.id}, l={self.largura}, a={self.altura})"