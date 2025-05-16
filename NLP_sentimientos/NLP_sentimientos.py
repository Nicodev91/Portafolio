import tkinter as tk
from transformers import pipeline

# Cargar el modelo una sola vez
analizador = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Función que se llama al hacer clic en el botón
def analizar_sentimiento():
    texto = entrada_texto.get("1.0", tk.END).strip()
    if texto:
        resultado = analizador(texto)[0]
        salida.set(f"Resultado: {resultado['label']} ({round(resultado['score'] * 100, 2)}%)")
    else:
        salida.set("Por favor, ingresa un texto para analizar.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Análisis de Sentimientos en Español")
ventana.geometry("500x300")

# Elementos de la GUI
tk.Label(ventana, text="Escribe tu texto:").pack(pady=10)

entrada_texto = tk.Text(ventana, height=6, width=50)
entrada_texto.pack()

tk.Button(ventana, text="Analizar Sentimiento", command=analizar_sentimiento).pack(pady=10)

salida = tk.StringVar()
tk.Label(ventana, textvariable=salida, font=("Helvetica", 12)).pack(pady=10)

# Iniciar la app
ventana.mainloop()
