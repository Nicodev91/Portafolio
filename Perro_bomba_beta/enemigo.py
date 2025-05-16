# enemigo.py

import pygame
import os
import time
import random

class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 30  # Tamaño del enemigo
        self.alto = 30   # Tamaño del enemigo
        self.velocidad = 2
        self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        self.tiempo_cambio_direccion = 0
        self.intervalo_cambio_direccion = 60  # Cambiar dirección cada 60 frames
        self.bomba_actual = None
        self.vida = 50  # Vida inicial del enemigo
        self.muerto = False  # Estado de muerte
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)  # Rectángulo para colisiones
        self.tiempo_ultimo_danio = 0  # Para controlar el tiempo entre daños
        self.intervalo_danio = 60  # Frames entre cada daño (1 segundo a 60 FPS)
        
        # Cargar imagen del enemigo
        try:
            self.imagen = pygame.image.load(os.path.join('assets', 'enemigo.png'))
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
            print("Imagen del enemigo cargada correctamente")
        except Exception as e:
            print(f"No se pudo cargar la imagen del enemigo: {e}")
            # Si no se encuentra la imagen, crear un rectángulo rojo
            self.imagen = pygame.Surface((self.ancho, self.alto))
            self.imagen.fill((255, 0, 0))

    def mover(self, bloques, bombas, jugador):
        if self.muerto:
            return
            
        # Actualizar el tiempo para cambio de dirección
        self.tiempo_cambio_direccion += 1
        if self.tiempo_cambio_direccion >= self.intervalo_cambio_direccion:
            self.direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
            self.tiempo_cambio_direccion = 0

        # Incrementar el contador de tiempo entre daños
        self.tiempo_ultimo_danio += 1

        # Guardamos la posición original para evitar sobrepasar los límites
        original_x = self.x
        original_y = self.y

        # Calcular nueva posición
        if self.direccion == 'arriba':
            self.y -= self.velocidad
        elif self.direccion == 'abajo':
            self.y += self.velocidad
        elif self.direccion == 'izquierda':
            self.x -= self.velocidad
        elif self.direccion == 'derecha':
            self.x += self.velocidad

        # Actualizar el rectángulo con la nueva posición
        self.rect.x = self.x
        self.rect.y = self.y

        # Verificar colisiones con bloques y revertir si es necesario
        for bloque in bloques:
            if self.rect.colliderect(bloque.rect):
                self.x = original_x
                self.y = original_y
                self.rect.x = self.x
                self.rect.y = self.y
                break

        # Verificar colisión con el jugador y aplicar daño
        if not jugador.muerto and not jugador.invulnerable:
            if self.rect.colliderect(jugador.rect):
                if self.tiempo_ultimo_danio >= self.intervalo_danio:
                    print(f"¡Colisión! Enemigo en ({self.x}, {self.y}), Jugador en ({jugador.x}, {jugador.y})")  # Debug
                    jugador.recibir_danio(50)
                    self.tiempo_ultimo_danio = 0

    def actualizar_bomba_actual(self, bomba):
        # Actualizar la referencia a la bomba actual si el enemigo está sobre ella
        if bomba and self.rect.colliderect(bomba.rect):
            self.bomba_actual = bomba
        elif self.bomba_actual == bomba:
            self.bomba_actual = None

    def recibir_danio(self, cantidad):
        if not self.muerto:
            self.vida -= cantidad
            if self.vida <= 0:
                self.morir()

    def morir(self):
        self.muerto = True

    def dibujar(self, pantalla):
        if not self.muerto:
            pantalla.blit(self.imagen, self.rect)
            
            # Dibujar barra de vida
            ancho_barra = 40
            alto_barra = 5
            x_barra = self.x
            y_barra = self.y - 10
            porcentaje_vida = self.vida / 50
            pygame.draw.rect(pantalla, (255, 0, 0), (x_barra, y_barra, ancho_barra, alto_barra))
            pygame.draw.rect(pantalla, (0, 255, 0), (x_barra, y_barra, ancho_barra * porcentaje_vida, alto_barra))
