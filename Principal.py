import sys
import util
from pygame.locals import *
from random import choice
from Decorator import *
import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sistema de Decoradores - Personajes")

    # Cargar imagen de fondo y escalarla al tamaño de la ventana
    background_image = util.cargar_imagen('imagenes/fondo.jpg', optimizar=True)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.mouse.set_visible(True)

    # Crear personaje inicial (sin decoradores)
    # Posición Y calculada para estar cerca del suelo
    # SCREEN_HEIGHT - alto_personaje - margen_del_suelo
    posicion_y = SCREEN_HEIGHT - 50 - 20  # 50 es el alto del personaje, 20 es el margen
    personaje = Personaje(x=100, y=posicion_y, ancho_ventana=SCREEN_WIDTH)

    ejecutando = True
    clock = pygame.time.Clock()

    # Contador para aplicar decoradores automáticamente
    contador_decorador = 0
    frecuencia_decorador = 180  # Cada 180 frames (3 segundos a 60 FPS)

    # Contador de capas de decoradores
    capas_decoradores = 0

    # Mostrar instrucciones en consola
    print("=== DECORADORES AUTOMÁTICOS ===")
    print("El personaje se envolverá automáticamente cada 3 segundos")
    print("Decoradores disponibles: Teletransporte, Retroceso, Agrandar")
    print("ESC - Salir")
    print("===============================")

    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
                sys.exit()

            if event.type == KEYDOWN:
                # Salir
                if event.key == K_ESCAPE:
                    ejecutando = False
                    sys.exit()

        # Incrementar contador
        contador_decorador += 1

        # Aplicar un decorador aleatorio cada cierto tiempo
        if contador_decorador >= frecuencia_decorador:
            # Elegir un decorador aleatorio
            decorador_aleatorio = choice([1, 2, 3])

            if decorador_aleatorio == 1:
                personaje = DecoratorTeletransporte(personaje, distancia_salto=100)
                print(f"✓ Capa {capas_decoradores + 1}: Teletransporte aplicado")
            elif decorador_aleatorio == 2:
                personaje = DecoratorRetroceso(personaje, distancia_salto=80)
                print(f"✓ Capa {capas_decoradores + 1}: Retroceso aplicado")
            else:
                personaje = DecoratorAgrandarSprite(personaje, factor_escala=1.2)
                print(f"✓ Capa {capas_decoradores + 1}: Agrandar aplicado")

            capas_decoradores += 1
            contador_decorador = 0

        # Actualizar movimiento y animación
        personaje.mover()
        personaje.animacion()

        # CRÍTICO: Dibujar el fondo primero para limpiar todo
        screen.blit(background_image, (0, 0))

        # Luego dibujar el personaje
        personaje.dibujar(screen)

        pygame.display.flip()  # Usar flip() en lugar de update()
        clock.tick(60)  # 60 FPS


if __name__ == '__main__':
    game()