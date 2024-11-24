import pygame
import random

# Inicializar Pygame
pygame.init()

# Inicializar el módulo de sonido
pygame.mixer.init()

# Configuración de la pantalla
ancho_pantalla = 600
alto_pantalla = 400
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Juego de la Viborita Mejorado")

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)
verde = (0, 255, 0)
rojo = (255, 0, 0)
gris = (169, 169, 169)

# Tamaño del bloque de la serpiente y fuente del texto
tamaño_bloque = 10
fuente = pygame.font.SysFont("comicsansms", 25)

# Cargar música y efectos de sonido
pygame.mixer.music.load("The Ninth Realm.mp3")  # Música de fondo
pygame.mixer.music.set_volume(0.5)  # Volumen de la música
sonido_comer = pygame.mixer.Sound("uwu.mp3")  # Sonido al comer fruta
sonido_colision = pygame.mixer.Sound("bruh.mp3")  # Sonido de colisión
sonido_comer.set_volume(0.7)
sonido_colision.set_volume(0.7)

# Función para mostrar un mensaje
def mostrar_mensaje(msg, color, posicion):
    texto = fuente.render(msg, True, color)
    pantalla.blit(texto, posicion)

# Función para dibujar un botón
def dibujar_boton(x, y, ancho, alto, color, texto, color_texto):
    pygame.draw.rect(pantalla, color, [x, y, ancho, alto])
    texto_boton = fuente.render(texto, True, color_texto)
    texto_rect = texto_boton.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(texto_boton, texto_rect)
    return (x, y, ancho, alto)

# Función para reiniciar el juego
def reiniciar_juego():
    x = ancho_pantalla // 2
    y = alto_pantalla // 2
    x_cambio = 0
    y_cambio = 0
    lista_serpiente = []
    largo_serpiente = 1
    puntuacion = 0
    velocidad_serpiente = 15

    # Generar obstáculos evitando la posición inicial de la serpiente
    num_obstaculos = 5
    obstaculos = []
    for _ in range(num_obstaculos):
        while True:
            x_obstaculo = round(random.randrange(0, ancho_pantalla - tamaño_bloque) / 10.0) * 10.0
            y_obstaculo = round(random.randrange(0, alto_pantalla - tamaño_bloque) / 10.0) * 10.0
            # Asegurarse de que los obstáculos no estén donde aparece la serpiente
            if [x_obstaculo, y_obstaculo] != [x, y] and [x_obstaculo, y_obstaculo] not in obstaculos:
                obstaculos.append([x_obstaculo, y_obstaculo])
                break

    # Generar fruta inicial evitando la posición de los obstáculos
    while True:
        x_fruta = round(random.randrange(0, ancho_pantalla - tamaño_bloque) / 10.0) * 10.0
        y_fruta = round(random.randrange(0, alto_pantalla - tamaño_bloque) / 10.0) * 10.0
        if [x_fruta, y_fruta] not in obstaculos and [x_fruta, y_fruta] != [x, y]:
            break

    return x, y, x_cambio, y_cambio, lista_serpiente, largo_serpiente, puntuacion, velocidad_serpiente, obstaculos, x_fruta, y_fruta

# Bucle principal del juego
def juego():
    # Reproducir música de fondo en bucle
    pygame.mixer.music.play(-1)

    # Reiniciar variables iniciales
    x, y, x_cambio, y_cambio, lista_serpiente, largo_serpiente, puntuacion, velocidad_serpiente, obstaculos, x_fruta, y_fruta = reiniciar_juego()

    reloj = pygame.time.Clock()
    juego_terminado = False
    juego_cerrado = False

    while not juego_terminado:
        while juego_cerrado:
            pantalla.fill(blanco)

            # Mostrar mensaje de derrota
            mostrar_mensaje("¡Perdiste!", rojo, (ancho_pantalla // 2 - 80, alto_pantalla // 4))

            # Dibujar botones
            boton_reiniciar = dibujar_boton(150, 200, 150, 50, verde, "Reiniciar (C)", blanco)
            boton_salir = dibujar_boton(300, 200, 150, 50, rojo, "Salir (Q)", blanco)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    juego_terminado = True
                    juego_cerrado = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Verificar clic en botones
                    if boton_reiniciar[0] <= mouse_x <= boton_reiniciar[0] + boton_reiniciar[2] and boton_reiniciar[1] <= mouse_y <= boton_reiniciar[1] + boton_reiniciar[3]:
                        x, y, x_cambio, y_cambio, lista_serpiente, largo_serpiente, puntuacion, velocidad_serpiente, obstaculos, x_fruta, y_fruta = reiniciar_juego()
                        juego_cerrado = False
                    if boton_salir[0] <= mouse_x <= boton_salir[0] + boton_salir[2] and boton_salir[1] <= mouse_y <= boton_salir[1] + boton_salir[3]:
                        juego_terminado = True
                        juego_cerrado = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        x, y, x_cambio, y_cambio, lista_serpiente, largo_serpiente, puntuacion, velocidad_serpiente, obstaculos, x_fruta, y_fruta = reiniciar_juego()
                        juego_cerrado = False
                    if event.key == pygame.K_q:
                        juego_terminado = True
                        juego_cerrado = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego_terminado = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_cambio == 0:
                    x_cambio = -tamaño_bloque
                    y_cambio = 0
                elif event.key == pygame.K_RIGHT and x_cambio == 0:
                    x_cambio = tamaño_bloque
                    y_cambio = 0
                elif event.key == pygame.K_UP and y_cambio == 0:
                    y_cambio = -tamaño_bloque
                    x_cambio = 0
                elif event.key == pygame.K_DOWN and y_cambio == 0:
                    y_cambio = tamaño_bloque
                    x_cambio = 0

        # Movimiento de la serpiente
        x += x_cambio
        y += y_cambio

        # Detectar colisión con bordes
        if x >= ancho_pantalla or x < 0 or y >= alto_pantalla or y < 0:
            pygame.mixer.Sound.play(sonido_colision)  # Sonido de colisión
            juego_cerrado = True

        # Detectar colisión con obstáculos
        if [x, y] in obstaculos:
            pygame.mixer.Sound.play(sonido_colision)  # Sonido de colisión
            juego_cerrado = True

        pantalla.fill(negro)

        # Dibujar fruta
        pygame.draw.rect(pantalla, rojo, [x_fruta, y_fruta, tamaño_bloque, tamaño_bloque])

        # Detectar colisión con la fruta
        if x == x_fruta and y == y_fruta:
            pygame.mixer.Sound.play(sonido_comer)  # Sonido al comer fruta
            puntuacion += 1
            largo_serpiente += 1
            # Reubicar fruta
            while True:
                x_fruta = round(random.randrange(0, ancho_pantalla - tamaño_bloque) / 10.0) * 10.0
                y_fruta = round(random.randrange(0, alto_pantalla - tamaño_bloque) / 10.0) * 10.0
                if [x_fruta, y_fruta] not in obstaculos and [x_fruta, y_fruta] not in lista_serpiente:
                    break

        # Dibujar obstáculos
        for obstaculo in obstaculos:
            pygame.draw.rect(pantalla, gris, [obstaculo[0], obstaculo[1], tamaño_bloque, tamaño_bloque])

        # Actualizar cuerpo de la serpiente
        lista_serpiente.append([x, y])
        if len(lista_serpiente) > largo_serpiente:
            del lista_serpiente[0]

        # Dibujar la serpiente
        for bloque in lista_serpiente:
            pygame.draw.rect(pantalla, verde, [bloque[0], bloque[1], tamaño_bloque, tamaño_bloque])

        # Detectar colisión con la propia serpiente
        if [x, y] in lista_serpiente[:-1]:
            pygame.mixer.Sound.play(sonido_colision)  # Sonido de colisión
            juego_cerrado = True

        pygame.display.update()
        reloj.tick(velocidad_serpiente)

    pygame.quit()

# Iniciar el juego
juego()
