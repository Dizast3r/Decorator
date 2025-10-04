import pygame
import random


class PersonajeAbstracto():
    def mover(self):
        pass

    def animacion(self):
        pass

    @property
    def x(self):
        pass

    @x.setter
    def x(self, value):
        pass


class Decorator(PersonajeAbstracto):
    def __init__(self, personaje):
        self.__personaje__ = personaje

    def mover(self):
        self.__personaje__.mover()

    def animacion(self):
        self.__personaje__.animacion()

    # Delegar el acceso a x
    @property
    def x(self):
        return self.__personaje__.x

    @x.setter
    def x(self, value):
        self.__personaje__.x = value

    # Delegar otros atributos necesarios
    @property
    def ancho(self):
        return self.__personaje__.ancho

    @ancho.setter
    def ancho(self, value):
        self.__personaje__.ancho = value

    @property
    def alto(self):
        return self.__personaje__.alto

    @alto.setter
    def alto(self, value):
        self.__personaje__.alto = value

    @property
    def sprites(self):
        return self.__personaje__.sprites

    @sprites.setter
    def sprites(self, value):
        self.__personaje__.sprites = value

    @property
    def y(self):
        return self.__personaje__.y

    @y.setter
    def y(self, value):
        self.__personaje__.y = value


class Personaje(PersonajeAbstracto):
    def __init__(self, x, y, ancho_ventana):
        self._x = x
        self._y = y
        self.velocidad = 5
        self.ancho_ventana = ancho_ventana
        self._ancho = 50
        self._alto = 50

        # Cargar los sprites originales
        self.sprites_originales = []
        for i in range(1, 10):
            ruta = f"Imagenes\\Sprite{i}.png"
            imagen = pygame.image.load(ruta)
            self.sprites_originales.append(imagen)

        # Crear sprites escalados
        self._sprites = []
        for img in self.sprites_originales:
            imagen_escalada = pygame.transform.scale(img, (self._ancho, self._alto))
            self._sprites.append(imagen_escalada)

        # Variables para la animación
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 5

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def ancho(self):
        return self._ancho

    @ancho.setter
    def ancho(self, value):
        self._ancho = value
        # Re-escalar sprites cuando cambia el ancho
        self._sprites = []
        for img in self.sprites_originales:
            imagen_escalada = pygame.transform.scale(img, (self._ancho, self._alto))
            self._sprites.append(imagen_escalada)

    @property
    def alto(self):
        return self._alto

    @alto.setter
    def alto(self, value):
        self._alto = value
        # Re-escalar sprites cuando cambia el alto
        self._sprites = []
        for img in self.sprites_originales:
            imagen_escalada = pygame.transform.scale(img, (self._ancho, self._alto))
            self._sprites.append(imagen_escalada)

    @property
    def sprites(self):
        return self._sprites

    @sprites.setter
    def sprites(self, value):
        self._sprites = value

    def mover(self):
        self._x += self.velocidad
        if self._x > self.ancho_ventana:
            self._x = -self._ancho

    def animacion(self):
        self.contador_animacion += 1
        if self.contador_animacion >= self.velocidad_animacion:
            self.frame_actual = (self.frame_actual + 1) % len(self._sprites)
            self.contador_animacion = 0

    def dibujar(self, ventana):
        ventana.blit(self._sprites[self.frame_actual], (self._x, self._y))

    def get_rect(self):
        """Devuelve el rectángulo de colisión del personaje"""
        return pygame.Rect(self._x, self._y, self._ancho, self._alto)


class PowerUp:
    """Clase para representar los power-ups en el camino"""
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo  # 'teletransporte', 'retroceso', 'agrandar'
        self.radio = 20
        self.activo = True
        
        # Colores según el tipo
        if tipo == 'teletransporte':
            self.color = (0, 255, 255)  # Cian
        elif tipo == 'retroceso':
            self.color = (255, 100, 255)  # Rosa/Magenta
        else:  # agrandar
            self.color = (255, 255, 0)  # Amarillo
        
        # Efecto de pulsación
        self.pulso = 0
        self.direccion_pulso = 1

    def actualizar(self):
        """Actualizar la animación de pulsación"""
        self.pulso += self.direccion_pulso * 0.5
        if self.pulso > 5:
            self.direccion_pulso = -1
        elif self.pulso < 0:
            self.direccion_pulso = 1

    def dibujar(self, ventana):
        """Dibujar el power-up como un círculo brillante"""
        if self.activo:
            radio_actual = int(self.radio + self.pulso)
            # Círculo exterior (más transparente)
            s = pygame.Surface((radio_actual * 3, radio_actual * 3), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, 50), (radio_actual * 1.5, radio_actual * 1.5), radio_actual * 1.5)
            ventana.blit(s, (self.x - radio_actual * 1.5, self.y - radio_actual * 1.5))
            
            # Círculo principal
            pygame.draw.circle(ventana, self.color, (int(self.x), int(self.y)), radio_actual, 0)
            # Borde
            pygame.draw.circle(ventana, (255, 255, 255), (int(self.x), int(self.y)), radio_actual, 2)

    def get_rect(self):
        """Devuelve el rectángulo de colisión"""
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

    def colisiona_con(self, personaje):
        """Verifica si colisiona con el personaje"""
        if not self.activo:
            return False
        
        rect_powerup = self.get_rect()
        rect_personaje = personaje.get_rect()
        return rect_powerup.colliderect(rect_personaje)


class DecoratorTeletransporte(Decorator):
    """Teletransporte que ocurre UNA SOLA VEZ al activarse"""
    def __init__(self, personaje, distancia_salto=120):
        super().__init__(personaje)
        self.distancia_salto = distancia_salto
        self.efecto_aplicado = False

    def mover(self):
        self.__personaje__.mover()
        
        # Aplicar teletransporte solo una vez
        if not self.efecto_aplicado:
            self.__personaje__.x += self.distancia_salto
            self.efecto_aplicado = True
            print(f"  → ¡Teletransporte activado! Salto de {self.distancia_salto}px adelante")

    def animacion(self):
        self.__personaje__.animacion()

    def dibujar(self, ventana):
        self.__personaje__.dibujar(ventana)

    def get_rect(self):
        return self.__personaje__.get_rect()


class DecoratorRetroceso(Decorator):
    """Retroceso que ocurre UNA SOLA VEZ al activarse"""
    def __init__(self, personaje, distancia_salto=80):
        super().__init__(personaje)
        self.distancia_salto = distancia_salto
        self.efecto_aplicado = False

    def mover(self):
        self.__personaje__.mover()
        
        # Aplicar retroceso solo una vez
        if not self.efecto_aplicado:
            self.__personaje__.x -= self.distancia_salto
            self.efecto_aplicado = True
            print(f"  → ¡Retroceso activado! Salto de {self.distancia_salto}px atrás")

    def animacion(self):
        self.__personaje__.animacion()

    def dibujar(self, ventana):
        self.__personaje__.dibujar(ventana)

    def get_rect(self):
        return self.__personaje__.get_rect()


class DecoratorAgrandarSprite(Decorator):
    """Agranda el sprite x3 durante 5 segundos y luego vuelve a la normalidad"""
    def __init__(self, personaje, factor_escala=4.5):
        super().__init__(personaje)
        self.factor_escala = factor_escala
        
        # Guardar dimensiones originales antes de agrandar
        self.ancho_original = self.__personaje__.ancho
        self.alto_original = self.__personaje__.alto
        
        # Calcular nuevas dimensiones (triple del tamaño)
        nuevo_ancho = int(self.ancho_original * self.factor_escala)
        nuevo_alto = int(self.alto_original * self.factor_escala)
        
        # Aplicar agrandamiento inmediatamente
        self.__personaje__.ancho = nuevo_ancho
        self.__personaje__.alto = nuevo_alto
        
        # Control de tiempo: 4 segundos a 60 FPS = 300 frames
        self.duracion_frames = 240
        self.contador_tiempo = 0
        self.efecto_activo = True
        
        print(f"  → ¡Agrandamiento activado! Tamaño x{self.factor_escala} durante 5 segundos")

    def mover(self):
        self.__personaje__.mover()
        
        # Contar frames mientras el efecto está activo
        if self.efecto_activo:
            self.contador_tiempo += 1
            
            # Después de 5 segundos, volver al tamaño original
            if self.contador_tiempo >= self.duracion_frames:
                self.__personaje__.ancho = self.ancho_original
                self.__personaje__.alto = self.alto_original
                self.efecto_activo = False
                print(f"  → Efecto de agrandamiento terminado. Volviendo a tamaño normal")

    def animacion(self):
        self.__personaje__.animacion()

    def dibujar(self, ventana):
        self.__personaje__.dibujar(ventana)

    def get_rect(self):
        return self.__personaje__.get_rect()