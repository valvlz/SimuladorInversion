import yfinance as yf

class Activo:
    """
    Clase base para los activos financieros.
    """

    def __init__(self, nombre):
        self.nombre = nombre

    def get_valor(self, fecha):
        raise NotImplementedError


class Accion(Activo):
    """
    Representa una acción del mercado.
    """

    def __init__(self, ticker):
        super().__init__(ticker)
        self.ticker = ticker
        self.data = yf.download(ticker, period="1mo")

    def get_precio_actual(self):
        """
        Retorna el último precio de cierre de la acción.
        """
        return self.data["Close"].iloc[-1].values[0]

    def __str__(self):
        return self.ticker

    def __repr__(self):
        return self.ticker


class RentaFija(Activo):
    """
    Representa un activo de renta fija.
    """

    def __init__(self, tasa_anual, capital):
        super().__init__("RentaFija")
        self.tasa = tasa_anual
        self.capital = capital