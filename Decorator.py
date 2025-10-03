import pygame


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


class Personaje(PersonajeAbstracto):
    def __init__(self, x, y, ancho_ventana):
        self._x = x
        self.y = y
        self.velocidad = 5  # Velocidad de movimiento
        self.ancho_ventana = ancho_ventana
        self._ancho = 50  # Ancho del personaje
        self._alto = 50  # Alto del personaje

        # Cargar los sprites
        self._sprites = []
        for i in range(1, 10):  # Del 1 al 9
            ruta = f"Imagenes\\Sprite{i}.png"
            imagen = pygame.image.load(ruta)
            # Escalar la imagen al tamaño del personaje
            imagen = pygame.transform.scale(imagen, (self._ancho, self._alto))
            self._sprites.append(imagen)

        # Variables para la animación
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 5  # Cambia de sprite cada 5 frames

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def ancho(self):
        return self._ancho

    @ancho.setter
    def ancho(self, value):
        self._ancho = value

    @property
    def alto(self):
        return self._alto

    @alto.setter
    def alto(self, value):
        self._alto = value

    @property
    def sprites(self):
        return self._sprites

    @sprites.setter
    def sprites(self, value):
        self._sprites = value

    def mover(self):
        # Mover hacia la derecha
        self._x += self.velocidad

        # Si llega al borde derecho, regresar al lado izquierdo
        if self._x > self.ancho_ventana:
            self._x = -self._ancho

    def animacion(self):
        # Incrementar el contador de animación
        self.contador_animacion += 1

        # Cambiar de frame cuando el contador alcanza la velocidad de animación
        if self.contador_animacion >= self.velocidad_animacion:
            self.frame_actual = (self.frame_actual + 1) % len(self._sprites)
            self.contador_animacion = 0

    def dibujar(self, ventana):
        # Dibujar el sprite actual
        ventana.blit(self._sprites[self.frame_actual], (self._x, self.y))


class DecoratorTeletransporte(Decorator):
    def __init__(self, personaje, distancia_salto=100):
        super().__init__(personaje)
        self.distancia_salto = distancia_salto
        self.contador = 0
        self.frecuencia = 30  # Cada 30 frames hace un salto

    def mover(self):
        self.__personaje__.mover()
        self.contador += 1

        # Cada cierto tiempo, hacer un "salto" hacia adelante
        if self.contador >= self.frecuencia:
            # Ahora funciona porque x está delegado
            self.__personaje__.x += self.distancia_salto
            self.contador = 0

    def animacion(self):
        self.__personaje__.animacion()

    def dibujar(self, ventana):
        self.__personaje__.dibujar(ventana)


class DecoratorRetroceso(Decorator):
    def __init__(self, personaje, distancia_salto=80):
        super().__init__(personaje)
        self.distancia_salto = distancia_salto
        self.contador = 0
        self.frecuencia = 40  # Cada 40 frames hace un salto hacia atrás

    def mover(self):
        self.__personaje__.mover()
        self.contador += 1

        # Cada cierto tiempo, hacer un "salto" hacia atrás
        if self.contador >= self.frecuencia:
            # Ahora funciona porque x está delegado
            self.__personaje__.x -= self.distancia_salto
            self.contador = 0

    def animacion(self):
        self.__personaje__.animacion()

    def dibujar(self, ventana):
        self.__personaje__.dibujar(ventana)


class DecoratorAgrandarSprite(Decorator):
    def __init__(self, personaje, factor_escala=1.5):
        super().__init__(personaje)
        self.factor_escala = factor_escala  # 1.5 = 150% del tamaño original

        # Guardar el tamaño original (ahora con properties funciona)
        self.ancho_original = self.__personaje__.ancho
        self.alto_original = self.__personaje__.alto

        # Aplicar el nuevo tamaño
        nuevo_ancho = int(self.__personaje__.ancho * factor_escala)
        nuevo_alto = int(self.__personaje__.alto * factor_escala)

        self.__personaje__.ancho = nuevo_ancho
        self.__personaje__.alto = nuevo_alto

        # Re-escalar todos los sprites
        sprites_actuales = self.__personaje__.sprites
        self.sprites_agrandados = []
        for sprite in sprites_actuales:
            sprite_agrandado = pygame.transform.scale(sprite, (nuevo_ancho, nuevo_alto))
            self.sprites_agrandados.append(sprite_agrandado)

        # Reemplazar los sprites
        self.__personaje__.sprites = self.sprites_agrandados

    def mover(self):
        self.__personaje__.mover()

    def animacion(self):
        self.__personaje__.animacion()

    def dibujar(self, ventana):
        self.__personaje__.dibujar(ventana)
