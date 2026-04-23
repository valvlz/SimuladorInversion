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
        self.data = None
        self.actualizar_datos()

    def get_precio_actual(self):
        """
        Retorna el último precio de cierre de la acción.
        """
        return float(self.data["Close"].iloc[-1].item())

    def __str__(self):
        return self.ticker

    def __repr__(self):
        return self.ticker
    
    def get_precio_dia(self):
        """
        Retorna precio de cierre, mínimo y máximo del último día.
        """
        ultimo = self.data.iloc[-1]

        return {
            "close": float(ultimo["Close"].item()),
            "low": float(ultimo["Low"].item()),
            "high": float(ultimo["High"].item())
        }
    
    def get_dividendos(self, dias=30):
        """
        Retorna los dividendos en los últimos N días.
        """
        ticker = yf.Ticker(self.ticker)
        dividendos = ticker.dividends.tail(dias)

        return dividendos
    
    def actualizar_datos(self):
        self.data = yf.download(self.ticker, period="1y")


class RentaFija(Activo):
    """
    Representa un activo de renta fija.
    """

    def __init__(self, tasa_anual, capital):
        super().__init__("RentaFija")
        self.tasa = tasa_anual
        self.capital = capital
    
    def valor_actual(self, dias):
        """
        Interés compuesto diario.
        """
        tasa_diaria = self.tasa / 365
        return self.capital * (1 + tasa_diaria) ** dias