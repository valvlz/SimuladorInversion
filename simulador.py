from portafolio import Portafolio
from activos import Accion
# PRUEBAS RÁPIDAS #
# Crear portafolio
p = Portafolio(10000)

# Crear activo
aapl = Accion("AAPL")

precio = aapl.get_precio_actual()

print("\n--- COMPRA ---")
p.comprar(aapl, 2, precio)
p.resumen()

print("\n--- COMPRA EXCESIVA ---")
p.comprar(aapl, 100000, precio)

print("\n--- VENTA ---")
p.vender(aapl, 1, precio)
p.resumen()

print("\n--- VENTA INVÁLIDA ---")
p.vender(aapl, 100, precio)

print("\n--- VALOR TOTAL ---")
print(p.calcular_valor())

print("\n--- SIMULACIÓN ---")
hist = p.simular()
print(hist.tail())


precio_real = aapl.get_precio_actual()

print("\n--- COMPRA FUERA DE RANGO (ALTO) ---")
p.comprar(aapl, 1, precio_real * 10)

print("\n--- COMPRA FUERA DE RANGO (BAJO) ---")
p.comprar(aapl, 1, precio_real * 0.1)

print("\n--- VENTA FUERA DE RANGO ---")
p.vender(aapl, 1, precio_real * 0.1)

print("\n--- RENTABILIDAD ---")
rent = p.calcular_rentabilidad()
print(f"{rent*100:.2f}%")

print("\n--- DIVIDENDOS ---")
div = p.calcular_dividendos()
print(div)

print("\n--- CREAR CDT ---")
print(p.agregar_cdt(2000, 0.10, 30))

print("\n--- CDTs EN PORTAFOLIO ---")
for cdt in p.cdts:
    print(f"Capital: {cdt.capital} | Valor actual: {cdt.actualizar()}")

print("\n--- VALOR TOTAL CON CDT ---")
print(p.calcular_valor())

print("\n--- CAPITAL RESTANTE ---")
print(p.capital)

print("\n--- PORTAFOLIO FINAL COMPLETO ---")
p.resumen()
print("Valor total:", p.calcular_valor())
print("CDTs:", len(p.cdts))

print("\n--- CDT TEST ---")

p.agregar_cdt(2000, 0.10, 30)

from datetime import datetime, timedelta

for cdt in p.cdts:
    print("Día 0:", cdt.actualizar())

    print("Día 10:", cdt.actualizar(
        cdt.fecha_inicio + timedelta(days=10)
    ))

    print("Día 30:", cdt.actualizar(
        cdt.fecha_inicio + timedelta(days=30)
    ))
