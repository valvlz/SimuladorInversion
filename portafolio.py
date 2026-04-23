from activos import Accion
from cdt import CDT

class Portafolio:
    """
    Clase que representa un portafolio de inversión.
    Permite gestionar el capital disponible y las posiciones en activos.
    """

    def __init__(self, capital_inicial):
        """
        Inicializa el portafolio con un capital inicial.

        :param capital_inicial: dinero disponible para invertir
        """
        self.capital = capital_inicial
        self.capital_inicial = capital_inicial
        self.cdts = []
        self.posiciones = {}
        self.comision = 0.001  # comisión del broker
        

    def comprar(self, activo, cantidad, precio):
        """
        Realiza la compra de un activo si hay capital suficiente.

        :param activo: activo a comprar
        :param cantidad: número de unidades
        :param precio: precio por unidad
        """
        precios = activo.get_precio_dia()

        high = precios["high"]
        low = precios["low"]

        # vALIDACIÓN 
        if precio > high:
            return f"Orden rechazada: precio ({precio:.2f}) supera el HIGH del día ({high:.2f})"

        if precio < low:
            return f"Orden rechazada: precio ({precio:.2f}) está por debajo del LOW del día ({low:.2f})"

        costo = cantidad * precio * (1 + self.comision)

        if costo > self.capital:
            return "Orden rechazada: capital insuficiente"
        
        self.capital -= costo
        ticker = activo.ticker

        if ticker in self.posiciones:
            pos = self.posiciones[ticker]

            nueva_cantidad = pos["cantidad"] + cantidad
            nuevo_precio = (
                (pos["cantidad"] * pos["precio_promedio"] + cantidad * precio)
                / nueva_cantidad
            )

            self.posiciones[ticker] = {
                "cantidad": nueva_cantidad,
                "precio_promedio": nuevo_precio
            }
        else:
            self.posiciones[ticker] = {
                "cantidad": cantidad,
                "precio_promedio": precio
            }
        return "Compra realizada"

    def vender(self, activo, cantidad, precio):
        """
        Realiza la venta de un activo si se tienen suficientes unidades.

        :param activo: activo a vender
        :param cantidad: número de unidades
        :param precio: precio por unidad
        """

        precios = activo.get_precio_dia()

        if precio < precios["low"]:
            return "No puedes vender por debajo del mínimo del día"

        if precio > precios["high"]:
            return "No puedes vender por encima del máximo del día"

        ticker = activo.ticker
    
        if ticker not in self.posiciones:
            return "No tienes este activo"

        if self.posiciones[ticker]["cantidad"] < cantidad:
            return "No tienes suficientes unidades para vender"

        ingreso = cantidad * precio * (1 - self.comision)
        self.capital += ingreso
        
        self.posiciones[ticker]["cantidad"] -= cantidad

        # Elimina el activo si ya no quedan unidades
        if self.posiciones[ticker]["cantidad"] == 0:
            del self.posiciones[ticker]
    
    def agregar_cdt(self, capital, tasa_anual, dias_plazo):
        if capital > self.capital:
            return "No hay suficiente capital"

        self.capital -= capital

        nuevo_cdt = CDT(capital, tasa_anual, dias_plazo)
        self.cdts.append(nuevo_cdt)

        return "CDT creado exitosamente"

    def calcular_valor(self):
        """
        Calcula el valor total del portafolio sumando el capital disponible
        y el valor actual de los activos en cartera.
        """
        total = self.capital

        for ticker, data in self.posiciones.items():
            try:
                accion = Accion(ticker)
                precio = accion.get_precio_actual()
                total += precio * data["cantidad"]
            except:
                print(f"Error obteniendo precio de {ticker}")
        
        total += self.valor_total_cdts()

        return total
    
    def simular(self, dias=30):
        """
        Simula la evolución del portafolio en los últimos N días.
        """
        import pandas as pd
        from datetime import datetime, timedelta

        fecha_base = datetime.today()
        fecha_simulada = fecha_base + timedelta(days=dias)

        series = []

        if not hasattr(self, "_cache"):
            self._cache = {}

        for ticker, data_pos in self.posiciones.items():
            try:
                if ticker not in self._cache:
                    self._cache[ticker] = Accion(ticker)

                accion = self._cache[ticker]

                data = accion.data["Close"].tail(dias).squeeze()
                cantidad = data_pos["cantidad"]

                valor = data * cantidad
                valor.name = ticker

                series.append(valor)

            except Exception as e:
                print(f"Error con {ticker}: {e}")

        if not series:
            return None

        df = pd.concat(series, axis=1)
        df = df.ffill().fillna(0)

        total = df.sum(axis=1)

        total_cdts = 0

        for cdt in self.cdts:
            total_cdts += cdt.actualizar(fecha_simulada)

        total = total + self.capital + total_cdts

        return total
    
    def resumen(self):

        print(f"Capital disponible: {self.capital}")

        for ticker, data in self.posiciones.items():
            print(f"{ticker} -> Cantidad: {data['cantidad']} | Precio Promedio: {data['precio_promedio']:.2f}")
    
    def calcular_rentabilidad(self):

        valor_actual = self.calcular_valor()
        dividendos = self.calcular_dividendos()
        inversion_inicial = self.capital_inicial

        rentabilidad = (valor_actual + dividendos - inversion_inicial) / inversion_inicial

        return rentabilidad
    
    def calcular_dividendos(self, dias=30):

        total_dividendos = 0

        for ticker, data in self.posiciones.items():
            try:
                accion = Accion(ticker)
                dividendos = accion.get_dividendos(dias)

                cantidad = data["cantidad"]

                total_dividendos += (dividendos.sum() * cantidad)

            except Exception as e:
                print(f"Error con dividendos de {ticker}: {e}")

        return total_dividendos
    

    
    def valor_total_cdts(self):
        total = 0

        for cdt in self.cdts:
            total += cdt.actualizar()

        return total