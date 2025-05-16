# bloque.py

import pygame
import os

class Bloque:
    def __init__(self, x, y, destructible=False):
        self.x = x
        self.y = y
        self.ancho = 40  # Tamaño del bloque
        self.alto = 40   # Tamaño del bloque
        self.destructible = destructible
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
        # Cargar la textura del bloque según si es destructible o no
        try:
            if destructible:
                self.textura = pygame.image.load(os.path.join('assets', 'bloque_destructible.png'))
            else:
                self.textura = pygame.image.load(os.path.join('assets', 'bloque.png'))
            self.textura = pygame.transform.scale(self.textura, (self.ancho, self.alto))
            if destructible:
                print("Imagen del bloque destructible cargada correctamente")
            else:
                print("Imagen del bloque indestructible cargada correctamente")
        except Exception as e:
            print(f"No se pudo cargar la imagen del bloque: {e}")
            self.textura = None
            # Color diferente para bloques destructibles
            self.color = (139, 69, 19) if destructible else (64, 64, 64)

    def dibujar(self, pantalla):
        if self.textura:
            pantalla.blit(self.textura, self.rect)
        else:
            pygame.draw.rect(pantalla, self.color, self.rect)
