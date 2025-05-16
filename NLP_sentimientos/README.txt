Analizador de Sentimientos en Español
====================================

Descripción
-----------
Esta aplicación es una herramienta de análisis de sentimientos que utiliza inteligencia artificial para evaluar el tono emocional de textos en español. Está construida con Python, utilizando la biblioteca Transformers y el modelo BERT multilingüe para proporcionar análisis precisos de sentimientos.

Características
--------------
- Interfaz gráfica intuitiva construida con Tkinter
- Análisis de sentimientos en tiempo real
- Soporte para texto en español
- Visualización de resultados con puntuación porcentual

Funcionamiento del Sistema de Puntuación
--------------------------------------
El análisis se realiza utilizando el modelo "nlptown/bert-base-multilingual-uncased-sentiment", que evalúa el texto en una escala de 1 a 5 estrellas:

1 estrella: Muy negativo
2 estrellas: Negativo
3 estrellas: Neutral
4 estrellas: Positivo
5 estrellas: Muy positivo

La puntuación se muestra en dos componentes:
1. Label (Etiqueta): Indica la clasificación del sentimiento en estrellas
2. Score (Puntuación): Se muestra como un porcentaje de confianza, indicando qué tan seguro está el modelo de su predicción

Por ejemplo:
- Un resultado de "5 stars (95%)" indica un sentimiento muy positivo con un 95% de confianza
- Un resultado de "1 star (87%)" indica un sentimiento muy negativo con un 87% de confianza

Uso
---
1. Ejecute la aplicación
2. Escriba o pegue el texto que desea analizar en el campo de texto
3. Haga clic en "Analizar Sentimiento"
4. El resultado aparecerá debajo del botón, mostrando la clasificación y el porcentaje de confianza

Requisitos
----------
- Python 3.x
- Transformers
- Tkinter (incluido en Python)