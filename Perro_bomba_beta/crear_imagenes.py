import pygame
import os

# Inicializar Pygame
pygame.init()

# Crear la carpeta assets si no existe
if not os.path.exists('assets'):
    os.makedirs('assets')

# Crear imagen para el jugador (azul)
jugador_img = pygame.Surface((32, 32))
jugador_img.fill((0, 0, 255))
pygame.draw.circle(jugador_img, (255, 255, 255), (16, 16), 8)
pygame.image.save(jugador_img, os.path.join('assets', 'jugador.png'))
print("Imagen del jugador creada")

# Crear imagen para el enemigo (rojo)
enemigo_img = pygame.Surface((30, 30))
enemigo_img.fill((255, 0, 0))
pygame.draw.circle(enemigo_img, (255, 255, 255), (15, 15), 6)
pygame.image.save(enemigo_img, os.path.join('assets', 'enemigo.png'))
print("Imagen del enemigo creada")

# Crear imagen para la bomba (negro)
bomba_img = pygame.Surface((32, 32))
bomba_img.fill((0, 0, 0))
pygame.draw.circle(bomba_img, (255, 255, 255), (16, 16), 10)
pygame.image.save(bomba_img, os.path.join('assets', 'bomba.png'))
print("Imagen de la bomba creada")

# Crear imagen para el bloque (gris)
bloque_img = pygame.Surface((40, 40))
bloque_img.fill((100, 100, 100))
pygame.draw.rect(bloque_img, (50, 50, 50), (0, 0, 40, 40), 2)
pygame.image.save(bloque_img, os.path.join('assets', 'bloque.png'))
print("Imagen del bloque creada")

# Crear imagen para el bloque destructible (marrón)
bloque_destructible_img = pygame.Surface((40, 40))
bloque_destructible_img.fill((139, 69, 19))  # Color marrón
pygame.draw.rect(bloque_destructible_img, (160, 82, 45), (0, 0, 40, 40), 2)  # Borde más claro
pygame.image.save(bloque_destructible_img, os.path.join('assets', 'bloque_destructible.png'))
print("Imagen del bloque destructible creada")

# Crear imagen para la explosión (naranja/rojo)
explosion_img = pygame.Surface((32, 32))
explosion_img.fill((255, 140, 0))  # Naranja
pygame.draw.circle(explosion_img, (255, 69, 0), (16, 16), 12)  # Centro rojo
pygame.image.save(explosion_img, os.path.join('assets', 'explosion.png'))
print("Imagen de la explosión creada")

print("Todas las imágenes han sido creadas correctamente") 