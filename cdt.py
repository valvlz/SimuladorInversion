from datetime import datetime, timedelta

class CDT:
    def __init__(self, capital, tasa_anual, dias_plazo, fecha_inicio=None):
        self.capital = capital
        self.tasa_anual = tasa_anual
        self.dias_plazo = dias_plazo

        self.fecha_inicio = fecha_inicio if fecha_inicio else datetime.today()
        self.fecha_fin = self.fecha_inicio + timedelta(days=dias_plazo)

        self.valor_actual = capital
        self.interes_acumulado = 0
        self.dias_transcurridos = 0

    def actualizar(self, fecha_actual=None):

        if fecha_actual is None:
            fecha_actual = datetime.today()

        # no pasar del vencimiento
        fecha = min(fecha_actual, self.fecha_fin)

        self.dias_transcurridos = (fecha - self.fecha_inicio).days

        tasa_diaria = self.tasa_anual / 365

        self.interes_acumulado = self.capital * tasa_diaria * self.dias_transcurridos
        self.valor_actual = self.capital + self.interes_acumulado

        return self.valor_actual

    def es_vencido(self):
        return datetime.today() >= self.fecha_fin