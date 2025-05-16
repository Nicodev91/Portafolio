# jugador.py

import pygame
import os
import bomba
import time

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 32  # ancho del jugador (más pequeño que los bloques)
        self.alto = 32   # alto del jugador (más pequeño que los bloques)
        self.velocidad = 3  # Velocidad reducida para movimiento más suave
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)  # Creamos el rectángulo para el jugador
        self.bombas = []  # Lista para almacenar las bombas colocadas
        self.vida = 150  # Vida inicial del jugador
        self.invulnerable = False  # Estado de invulnerabilidad
        self.tiempo_invulnerabilidad = 0
        self.duracion_invulnerabilidad = 60  # 60 frames = 1 segundo
        self.muerto = False  # Estado de muerte
        self.tiempo_muerte = 0  # Tiempo de muerte restante
        self.bomba_actual = None  # Para rastrear la bomba que acabamos de colocar
        
        # Cargar la imagen del jugador
        try:
            self.imagen = pygame.image.load(os.path.join('assets', 'jugador.png'))
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
            print("Imagen del jugador cargada correctamente")
        except Exception as e:
            print(f"No se pudo cargar la imagen del jugador: {e}")
            # Si no se encuentra la imagen, crear un rectángulo azul
            self.imagen = pygame.Surface((self.ancho, self.alto))
            self.imagen.fill((0, 0, 255))

    def manejar_movimiento(self, teclas, bloques):
        if self.muerto:
            return  # No mover si está muerto
            
        # Guardamos la posición original para evitar sobrepasar los límites
        original_x = self.x
        original_y = self.y

        # Movimiento del jugador con las teclas WASD
        if teclas[pygame.K_a]:  # A - Izquierda
            self.x -= self.velocidad
        if teclas[pygame.K_d]:  # D - Derecha
            self.x += self.velocidad
        if teclas[pygame.K_w]:  # W - Arriba
            self.y -= self.velocidad
        if teclas[pygame.K_s]:  # S - Abajo
            self.y += self.velocidad

        # Actualizar el rectángulo con la nueva posición
        self.rect.x = self.x
        self.rect.y = self.y

        # Verificar colisiones con bloques
        for bloque in bloques:
            if self.rect.colliderect(bloque.rect):
                # Si colide con un bloque, revertimos el movimiento
                self.x = original_x
                self.y = original_y
                self.rect.x = self.x
                self.rect.y = self.y
                break
                
        # Verificar colisiones con bombas
        for bomba in self.bombas:
            if bomba.estado == "ESPERANDO" and self.rect.colliderect(bomba.rect):
                # Si es la bomba que acabamos de colocar y estamos sobre ella, permitir el movimiento
                if bomba == self.bomba_actual:
                    continue
                    
                # Si ya nos alejamos de la bomba actual, tratarla como las demás
                if self.bomba_actual and not self.rect.colliderect(self.bomba_actual.rect):
                    self.bomba_actual = None
                    
                # Si es otra bomba o ya nos alejamos de la actual, revertir el movimiento
                if bomba != self.bomba_actual:
                    self.x = original_x
                    self.y = original_y
                    self.rect.x = self.x
                    self.rect.y = self.y
                break

    def colocar_bomba(self):
        if self.muerto:
            return  # No colocar bombas si está muerto
            
        # Crear una nueva bomba en la posición del jugador
        nueva_bomba = bomba.Bomba(self.x, self.y)
        self.bombas.append(nueva_bomba)
        # Establecer esta bomba como la bomba actual
        self.bomba_actual = nueva_bomba

    def actualizar_bombas(self, enemigos, bloques):
        # Crear una copia de la lista para poder modificarla mientras iteramos
        bombas_activas = self.bombas[:]
        
        for bomba in bombas_activas:
            bomba.actualizar(self, enemigos, bloques)
            if bomba.estado == "TERMINADA":
                if bomba == self.bomba_actual:
                    self.bomba_actual = None
                self.bombas.remove(bomba)
                
        # Actualizar estado de invulnerabilidad
        if self.invulnerable:
            self.tiempo_invulnerabilidad -= 1
            if self.tiempo_invulnerabilidad <= 0:
                self.invulnerable = False
                
        # Actualizar estado de muerte
        if self.muerto:
            tiempo_actual = time.time()
            if tiempo_actual >= self.tiempo_muerte:
                self.muerto = False
                self.vida = 150  # Restaurar vida al revivir

    def recibir_danio(self, cantidad):
        if not self.invulnerable and not self.muerto:
            print(f"Jugador recibió {cantidad} de daño. Vida anterior: {self.vida}")  # Debug
            self.vida -= cantidad
            print(f"Vida actual: {self.vida}")  # Debug
            if self.vida <= 0:
                self.morir()
            else:
                self.activar_invulnerabilidad()

    def activar_invulnerabilidad(self):
        self.invulnerable = True
        self.tiempo_invulnerabilidad = self.duracion_invulnerabilidad

    def morir(self):
        self.muerto = True
        self.tiempo_muerte = time.time() + 30  # 30 segundos de muerte

    def dibujar(self, pantalla):
        if not self.muerto:
            # Si está invulnerable, hacer parpadeo
            if self.invulnerable and int(time.time() * 5) % 2 == 0:
                # No dibujar si está parpadeando
                pass
            else:
                pantalla.blit(self.imagen, self.rect)
        
        # Dibujar barra de vida
        if not self.muerto:
            ancho_barra = 40
            alto_barra = 5
            x_barra = self.rect.x
            y_barra = self.rect.y - 10
            porcentaje_vida = self.vida / 150
            pygame.draw.rect(pantalla, (255, 0, 0), (x_barra, y_barra, ancho_barra, alto_barra))
            pygame.draw.rect(pantalla, (0, 255, 0), (x_barra, y_barra, ancho_barra * porcentaje_vida, alto_barra))
