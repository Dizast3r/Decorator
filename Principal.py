import sys
import util
from pygame.locals import *
from random import choice, randint
from Decorator import *
import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sistema de Decoradores - Personajes con Power-ups")

    # Cargar imagen de fondo y escalarla al tamaño de la ventana
    background_image = util.cargar_imagen('imagenes/fondo.jpg', optimizar=True)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.mouse.set_visible(True)

    # Crear personaje inicial
    posicion_y = SCREEN_HEIGHT - 50 - 110
    personaje = Personaje(x=100, y=posicion_y, ancho_ventana=SCREEN_WIDTH)

    ejecutando = True
    clock = pygame.time.Clock()

    # Lista de power-ups activos
    powerups = []
    
    # Contador para generar nuevos power-ups
    contador_spawn = 0
    frecuencia_spawn = 120  # Cada 2 segundos aparece un nuevo power-up

    # Contador de decoradores aplicados
    capas_decoradores = 0

    # Mostrar instrucciones en consola
    print("=== SISTEMA DE POWER-UPS ===")
    print("Los power-ups aparecen en la línea de recorrido:")
    print("  🔵 CIAN - Teletransporte (saltos adelante)")
    print("  🟣 ROSA - Retroceso (saltos atrás)")
    print("  🟡 AMARILLO - Agrandar sprite")
    print("Colisiona con ellos para obtener sus efectos")
    print("ESC - Salir")
    print("============================")

    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    ejecutando = False
                    sys.exit()

        # Generar nuevos power-ups
        contador_spawn += 1
        if contador_spawn >= frecuencia_spawn:
            # Elegir tipo aleatorio
            tipo = choice(['teletransporte', 'retroceso', 'agrandar'])
            
            # Posición aleatoria en X (delante del personaje o en cualquier lugar)
            pos_x = randint(100, SCREEN_WIDTH - 100)
            
            # Mismo Y que el personaje (en su línea de recorrido)
            pos_y = posicion_y + 25  # Centro del personaje
            
            nuevo_powerup = PowerUp(pos_x, pos_y, tipo)
            powerups.append(nuevo_powerup)
            contador_spawn = 0

        # Actualizar power-ups
        for powerup in powerups:
            powerup.actualizar()
            
            # Verificar colisión con el personaje
            if powerup.colisiona_con(personaje):
                powerup.activo = False
                
                # Aplicar el decorador correspondiente
                if powerup.tipo == 'teletransporte':
                    personaje = DecoratorTeletransporte(personaje, distancia_salto=100)
                    print(f"✨ Power-up TELETRANSPORTE recogido! (Capa {capas_decoradores + 1})")
                elif powerup.tipo == 'retroceso':
                    personaje = DecoratorRetroceso(personaje, distancia_salto=80)
                    print(f"✨ Power-up RETROCESO recogido! (Capa {capas_decoradores + 1})")
                else:  # agrandar
                    personaje = DecoratorAgrandarSprite(personaje, factor_escala=1.2)
                    print(f"✨ Power-up AGRANDAR recogido! (Capa {capas_decoradores + 1})")
                
                capas_decoradores += 1

        # Eliminar power-ups inactivos
        powerups = [p for p in powerups if p.activo]

        # Actualizar movimiento y animación del personaje
        personaje.mover()
        personaje.animacion()

        # Dibujar todo
        screen.blit(background_image, (0, 0))
        
        # Dibujar power-ups
        for powerup in powerups:
            powerup.dibujar(screen)
        
        # Dibujar personaje
        personaje.dibujar(screen)

        # Mostrar contador de decoradores en pantalla
        font = pygame.font.Font(None, 36)
        texto = font.render(f"Decoradores activos: {capas_decoradores}", True, (255, 255, 255))
        texto_sombra = font.render(f"Decoradores activos: {capas_decoradores}", True, (0, 0, 0))
        screen.blit(texto_sombra, (22, 22))
        screen.blit(texto, (20, 20))

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    game()