import pygame
import sys
import jugador
import bloque
import enemigo
import time
import random

# Inicializar Pygame y el sistema de sonido  // que odna la rama-beta
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Sistema de sonido inicializado")

# Establecer el color de fondo
COLOR_FONDO = (25, 25, 112)  # Blanco, cambiado del azul oscuro anterior

# Definir el tamaño del grid y las celdas
GRID_COLS = 20  # Reducido para un mapa más pequeño
GRID_ROWS = 15  # Reducido para un mapa más pequeño
CELL_SIZE = 40  # Tamaño de cada celda 

# Ajustar el tamaño de la pantalla
ANCHO_PANTALLA = GRID_COLS * CELL_SIZE
ALTO_PANTALLA = GRID_ROWS * CELL_SIZE
 
# Crear la pantalla 
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Bomberman en Python")

# Reloj para controlar FPS
reloj = pygame.time.Clock()  #Probando rama-beta

# Primero creamos los bloques
bloques = []

# Crear el patrón de bloques (simplificado)
for row in range(GRID_ROWS):
    for col in range(GRID_COLS):
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        
        # Agregar bloques en los bordes (indestructibles)
        if row == 0 or row == GRID_ROWS-1 or col == 0 or col == GRID_COLS-1:
            bloques.append(bloque.Bloque(x, y, destructible=False))
            continue
            
        # Patrón de bloques internos indestructibles
        if row % 2 == 0 and col % 2 == 0:
            bloques.append(bloque.Bloque(x, y, destructible=False))
            continue
            
        # Agregar bloques destructibles con 60% de probabilidad en espacios vacíos
        # Evitamos poner bloques cerca del jugador al inicio
        if (col > 2 or row > 2) and random.random() < 0.6:
            bloques.append(bloque.Bloque(x, y, destructible=True))

# Crear jugador en una posición segura (siempre en la esquina superior izquierda)
mi_jugador = jugador.Jugador(CELL_SIZE, CELL_SIZE)

# Crear enemigos en posiciones seguras predefinidas
enemigos = []
posiciones_posibles_enemigos = [
    # Enemigos originales en las esquinas
    (CELL_SIZE * (GRID_COLS-2), CELL_SIZE),  # Esquina superior derecha
    (CELL_SIZE, CELL_SIZE * (GRID_ROWS-2)),  # Esquina inferior izquierda
    (CELL_SIZE * (GRID_COLS-2), CELL_SIZE * (GRID_ROWS-2)),  # Esquina inferior derecha
    
    # Nuevos enemigos más centrados
    (CELL_SIZE * 5, CELL_SIZE * 5),          # Centro-izquierda
    (CELL_SIZE * (GRID_COLS-6), CELL_SIZE * 5),  # Centro-derecha
    (CELL_SIZE * 5, CELL_SIZE * (GRID_ROWS-6)),  # Centro-abajo-izquierda
    (CELL_SIZE * (GRID_COLS-6), CELL_SIZE * (GRID_ROWS-6)),  # Centro-abajo-derecha
]

def hay_bloque_en_posicion(x, y, bloques):
    """Verifica si hay un bloque en la posición dada"""
    for bloque in bloques:
        if bloque.rect.x == x and bloque.rect.y == y:
            return True
    return False

def encontrar_posicion_libre(x, y, bloques, radio=2):
    """Busca una posición libre cerca de las coordenadas dadas"""
    for dx in range(-radio, radio + 1):
        for dy in range(-radio, radio + 1):
            nueva_x = x + dx * CELL_SIZE
            nueva_y = y + dy * CELL_SIZE
            # Verificar que la posición esté dentro del mapa
            if (CELL_SIZE < nueva_x < ANCHO_PANTALLA - CELL_SIZE and 
                CELL_SIZE < nueva_y < ALTO_PANTALLA - CELL_SIZE):
                if not hay_bloque_en_posicion(nueva_x, nueva_y, bloques):
                    return nueva_x, nueva_y
    return None

# Crear enemigos solo en posiciones donde no hay bloques destructibles
for pos in posiciones_posibles_enemigos:
    x, y = pos
    if not hay_bloque_en_posicion(x, y, bloques):
        enemigos.append(enemigo.Enemigo(x, y))
        print(f"Enemigo creado en posición original ({x}, {y})")
    else:
        # Buscar una posición cercana libre
        nueva_posicion = encontrar_posicion_libre(x, y, bloques)
        if nueva_posicion:
            nueva_x, nueva_y = nueva_posicion
            enemigos.append(enemigo.Enemigo(nueva_x, nueva_y))
            print(f"Enemigo creado en posición alternativa ({nueva_x}, {nueva_y})")
        else:
            print(f"No se pudo crear enemigo cerca de ({x}, {y})")

# Al inicio del archivo, después de las importaciones
pygame.font.init()  # Inicializar el módulo de fuentes

# Crear la fuente para el mensaje de Game Over
fuente_grande = pygame.font.Font(None, 74)  # None usa la fuente por defecto, 74 es el tamaño
fuente_pequeña = pygame.font.Font(None, 36)  # Fuente más pequeña para el segundo mensaje

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mi_jugador.colocar_bomba()
                print("Bomba colocada")
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Obtenemos las teclas presionadas
    teclas = pygame.key.get_pressed()

    # Manejar el movimiento del jugador
    mi_jugador.manejar_movimiento(teclas, bloques)
    
    # Mover enemigos y eliminar los muertos
    enemigos_vivos = []
    for enemigo in enemigos:
        if not enemigo.muerto:
            enemigo.mover(bloques, mi_jugador.bombas, mi_jugador)
            enemigos_vivos.append(enemigo)
    enemigos = enemigos_vivos

    # Actualizar las bombas
    mi_jugador.actualizar_bombas(enemigos, bloques)

    # Llenamos la pantalla con el color de fondo
    pantalla.fill(COLOR_FONDO)

    # 1. Primero dibujamos los bloques
    for bloque in bloques:
        bloque.dibujar(pantalla)

    # 2. Dibujamos el jugador
    mi_jugador.dibujar(pantalla)

    # 3. Dibujamos los enemigos
    for enemigo in enemigos:
        enemigo.dibujar(pantalla)

    # 4. Dibujamos las bombas
    for bomba in mi_jugador.bombas:
        bomba.dibujar(pantalla)

    # Verificar victoria (cuando no hay enemigos)
    if len(enemigos) == 0:
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("Eres una máquina, perrooooo", True, (255, 0, 0))
        rect_texto = texto.get_rect()
        rect_texto.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2)
        pantalla.blit(texto, rect_texto)
    
    # Si el jugador está muerto, mostrar Game Over
    if mi_jugador.vida <= 0:
        fuente = pygame.font.Font(None, 74)
        texto_game_over = fuente.render("Game Over", True, (0, 0, 0))
        texto_mensaje = fuente.render("Fuiste bueno", True, (0, 0, 0))
        
        rect_game_over = texto_game_over.get_rect()
        rect_mensaje = texto_mensaje.get_rect()
        
        rect_game_over.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 40)
        rect_mensaje.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 40)
        
        pantalla.blit(texto_game_over, rect_game_over)
        pantalla.blit(texto_mensaje, rect_mensaje)

    # Actualizamos la pantalla
    pygame.display.flip()
    reloj.tick(60)
