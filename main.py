from activos import Accion
from portafolio import Portafolio

# Crear portafolio
portafolio = Portafolio(10000)

# Crear acción
accion = Accion("AAPL")

# Obtener precio usando el método (mejor práctica)
precio = accion.get_precio_actual()

# Comprar
portafolio.comprar(accion, 5, precio)

# Calcular valor total
valor_total = portafolio.calcular_valor()

# Mostrar resultados
print("Capital restante:", round(portafolio.capital, 2))
print("Posiciones:", portafolio.posiciones)
print("Valor total del portafolio:", round(valor_total, 2))