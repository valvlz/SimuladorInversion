from activos import Accion
from portafolio import Portafolio

def menu():
    print("\n--- Simulador de Portafolio ---")
    print("1. Comprar acción")
    print("2. Vender acción")
    print("3. Ver portafolio")
    print("4. Ver valor total")
    print("5. Salir")


def main():
    portafolio = Portafolio(10000)

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ticker = input("Ingrese el ticker: ")
            cantidad = int(input("Cantidad: "))

            accion = Accion(ticker)
            precio = accion.get_precio_actual()

            portafolio.comprar(accion, cantidad, precio)
            print("Compra realizada")

        elif opcion == "2":
            ticker = input("Ingrese el ticker: ")
            cantidad = int(input("Cantidad: "))

            accion = Accion(ticker)
            precio = accion.get_precio_actual()

            portafolio.vender(accion, cantidad, precio)
            print("Venta realizada")

        elif opcion == "3":
            print("Posiciones:", portafolio.posiciones)
            print("Capital:", round(portafolio.capital, 2))

        elif opcion == "4":
            valor = portafolio.calcular_valor()
            print("Valor total:", round(valor, 2))

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()