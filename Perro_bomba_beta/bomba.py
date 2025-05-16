# bomba.py
import pygame
import os

class Bomba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 32
        self.alto = 32
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
        # Temporizadores y estados
        self.frame_actual = 0
        self.FRAMES_ESPERA = 180
        self.FRAMES_EXPLOSION = 30
        self.estado = "ESPERANDO"
        self.rango_explosion = 2
        self.explosiones = []
        
        # Cargar imagen de la bomba
        try:
            self.imagen = pygame.image.load(os.path.join('assets', 'bomba.png'))
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
            print("Imagen de la bomba cargada correctamente")
        except Exception as e:
            print(f"Error al cargar imagen de bomba: {e}")
            self.imagen = pygame.Surface((self.ancho, self.alto))
            self.imagen.fill((255, 0, 0))
        
        # Crear un sonido simple
        try:
            # Intentar crear un sonido simple usando pygame
            self.sonido_explosion = pygame.mixer.Sound(os.path.join('assets', 'explosion.wav'))
            self.sonido_explosion.set_volume(1.0)
            print("Sonido de explosión cargado")
        except:
            # Si falla, crear un tono simple
            tamaño_buffer = 4096
            self.sonido_explosion = pygame.mixer.Sound(buffer=bytes([127] * tamaño_buffer))
            self.sonido_explosion.set_volume(1.0)
            print("Sonido de explosión creado")

    def actualizar(self, jugador, enemigos, bloques):
        self.frame_actual += 1
        
        if self.estado == "ESPERANDO":
            if self.frame_actual >= self.FRAMES_ESPERA:
                print("¡BOOM! - EXPLOSIÓN INICIADA")
                self.estado = "EXPLOTANDO"
                self.frame_actual = 0
                # Reproducir el sonido
                try:
                    self.sonido_explosion.play()
                    print("Reproduciendo sonido de explosión")
                except Exception as e:
                    print(f"Error al reproducir sonido: {e}")
                self.explotar(jugador, enemigos, bloques)
                
        elif self.estado == "EXPLOTANDO":
            if self.frame_actual >= self.FRAMES_EXPLOSION:
                print("Fin de la explosión")
                self.estado = "TERMINADA"
                self.explosiones.clear()

    def explotar(self, jugador, enemigos, bloques):
        self.explosiones = []
        # Agregar centro de la explosión
        self.explosiones.append((self.x, self.y))
        
        # Verificar daño en el centro de la explosión
        rect_centro = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        
        # Verificar daño al jugador en el centro
        if not jugador.invulnerable and rect_centro.colliderect(jugador.rect):
            jugador.recibir_danio(50)
            jugador.activar_invulnerabilidad()
        
        # Verificar daño a enemigos en el centro
        for enemigo in enemigos:
            if not enemigo.muerto and rect_centro.colliderect(enemigo.rect):
                enemigo.recibir_danio(50)
        
        # Crear explosiones en las cuatro direcciones
        direcciones = [(1,0), (-1,0), (0,1), (0,-1)]
        
        for dx, dy in direcciones:
            for i in range(1, self.rango_explosion + 1):
                x = self.x + i * dx * self.ancho
                y = self.y + i * dy * self.alto
                rect_explosion = pygame.Rect(x, y, self.ancho, self.alto)
                
                # Verificar colisiones con bloques
                bloque_colisionado = None
                for bloque in bloques:
                    if rect_explosion.colliderect(bloque.rect):
                        bloque_colisionado = bloque
                        break
                
                if bloque_colisionado:
                    if bloque_colisionado.destructible:
                        self.explosiones.append((x, y))
                        bloques.remove(bloque_colisionado)
                    break
                else:
                    self.explosiones.append((x, y))
                
                # Verificar daño al jugador
                if not jugador.invulnerable and rect_explosion.colliderect(jugador.rect):
                    jugador.recibir_danio(50)
                    jugador.activar_invulnerabilidad()
                
                # Verificar daño a enemigos
                for enemigo in enemigos:
                    if not enemigo.muerto and rect_explosion.colliderect(enemigo.rect):
                        enemigo.recibir_danio(50)
                
                # Verificar colisión con otras bombas
                for bomba in jugador.bombas:
                    if bomba != self and bomba.estado == "ESPERANDO" and rect_explosion.colliderect(bomba.rect):
                        print("¡Bomba alcanzada por explosión!")
                        bomba.detonar_inmediatamente(jugador, enemigos, bloques)

    def detonar_inmediatamente(self, jugador, enemigos, bloques):
        """Método para hacer explotar la bomba inmediatamente"""
        if self.estado == "ESPERANDO":
            print("¡Detonación en cadena!")
            self.estado = "EXPLOTANDO"
            self.frame_actual = 0
            try:
                self.sonido_explosion.play()
            except Exception as e:
                print(f"Error al reproducir sonido: {e}")
            self.explotar(jugador, enemigos, bloques)

    def dibujar(self, pantalla):
        if self.estado == "ESPERANDO":
            # Dibujar la bomba
            pantalla.blit(self.imagen, self.rect)
            pygame.draw.rect(pantalla, (255, 0, 0), self.rect, 2)
        elif self.estado == "EXPLOTANDO":
            # Dibujar explosión
            for pos_x, pos_y in self.explosiones:
                # Borde negro para contraste
                pygame.draw.rect(pantalla, (0, 0, 0), 
                               (pos_x-2, pos_y-2, self.ancho+4, self.alto+4))
                # Relleno rojo
                pygame.draw.rect(pantalla, (255, 0, 0), 
                               (pos_x, pos_y, self.ancho, self.alto))