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
        self.posiciones = {}
        self.comision = 0.001  # comisión del broker

    def comprar(self, activo, cantidad, precio):
        """
        Realiza la compra de un activo si hay capital suficiente.

        :param activo: activo a comprar
        :param cantidad: número de unidades
        :param precio: precio por unidad
        """
        costo = cantidad * precio * (1 + self.comision)

        if costo > self.capital:
            print("No hay suficiente capital para la compra")
            return

        self.capital -= costo
        self.posiciones[activo] = self.posiciones.get(activo, 0) + cantidad

    def vender(self, activo, cantidad, precio):
        """
        Realiza la venta de un activo si se tienen suficientes unidades.

        :param activo: activo a vender
        :param cantidad: número de unidades
        :param precio: precio por unidad
        """
        if self.posiciones.get(activo, 0) < cantidad:
            print("No tienes suficientes unidades para vender")
            return

        ingreso = cantidad * precio * (1 - self.comision)
        self.capital += ingreso
        self.posiciones[activo] -= cantidad

        # Elimina el activo si ya no quedan unidades
        if self.posiciones[activo] == 0:
            del self.posiciones[activo]

    def calcular_valor(self):
        """
        Calcula el valor total del portafolio sumando el capital disponible
        y el valor actual de los activos en cartera.

        :return: valor total del portafolio
        """
        total = self.capital

        for activo, cantidad in self.posiciones.items():
            precio = activo.get_precio_actual()
            total += precio * cantidad

        return total