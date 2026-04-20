import tkinter as tk
from activos import Accion
from portafolio import Portafolio

portafolio = Portafolio(10000)

def comprar():
    try:
        ticker = entry_ticker.get()
        cantidad = int(entry_cantidad.get())

        accion = Accion(ticker)
        precio = accion.get_precio_actual()

        portafolio.comprar(accion, cantidad, precio)

        label_resultado.config(text=f"Compra realizada: {cantidad} de {ticker}")
    except:
        label_resultado.config(text="Error en la compra")

def ver_portafolio():
    texto = f"Capital: {round(portafolio.capital, 2)}\n"
    texto += f"Posiciones: {portafolio.posiciones}"
    label_resultado.config(text=texto)

def ver_valor_total():
    valor = portafolio.calcular_valor()
    label_resultado.config(text=f"Valor total: {round(valor, 2)}")

def salir():
    ventana.destroy()


#Ventana principal
ventana = tk.Tk()
ventana.title("Simulador de Portafolio")
ventana.geometry("400x400")  # tamaño más grande

#Título
tk.Label(ventana, text="Simulador de Portafolio", font=("Arial", 16)).pack(pady=10)

#Inputs
frame_inputs = tk.Frame(ventana)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Ticker:").grid(row=0, column=0, padx=5, pady=5)
entry_ticker = tk.Entry(frame_inputs)
entry_ticker.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
entry_cantidad = tk.Entry(frame_inputs)
entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

#Botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

tk.Button(frame_botones, text="Comprar", width=15, command=comprar).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Ver portafolio", width=15, command=ver_portafolio).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_botones, text="Valor total", width=15, command=ver_valor_total).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Salir", width=15, command=salir).grid(row=1, column=1, padx=5, pady=5)

#Resultado
label_resultado = tk.Label(ventana, text="", justify="left")
label_resultado.pack(pady=20)

ventana.mainloop()