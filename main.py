# main.py

import pygame
import sys
import math
import random
from characters import Kinematic, Static, SteeringOutput, KinematicSteeringOutput, map_to_range
from algorithms import *
from drawing import Path, Button, draw_pacman
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simulación de Algoritmos de Movimiento")
    clock = pygame.time.Clock()

    while True:
        # Mostrar menú y obtener elección del usuario
        algorithm_choice = display_menu(screen, clock)

        if algorithm_choice == 0:
            break  # Salir del programa

        # Ejecutar el algoritmo seleccionado
        if algorithm_choice == 1:
            run_kinematic_arrive(screen, clock)
        elif algorithm_choice == 2:
            run_kinematic_flee(screen, clock)
        elif algorithm_choice == 3:
            run_kinematic_wander(screen, clock)
        elif algorithm_choice == 4:
            run_dynamic_seek(screen, clock)
        elif algorithm_choice == 5:
            run_dynamic_flee(screen, clock)
        elif algorithm_choice == 6:
            run_dynamic_arrive(screen, clock)
        elif algorithm_choice == 7:
            run_align(screen, clock)
        elif algorithm_choice == 8:
            run_velocity_matching(screen, clock)
        elif algorithm_choice == 9:
            run_face(screen, clock)
        elif algorithm_choice == 10:
            run_pursue_and_evade(screen, clock)
        elif algorithm_choice == 11:
            run_dynamic_wander(screen, clock)
        elif algorithm_choice == 12:
            run_path_following(screen, clock)
        elif algorithm_choice == 13:
            run_separation(screen, clock)
        elif algorithm_choice == 14:
            run_collision_avoidance(screen, clock)
        elif algorithm_choice == 15:
            run_obstacle_avoidance(screen, clock)
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

    pygame.quit()
    sys.exit()


def display_menu(screen, clock) -> int:
    pygame.display.set_caption("Menú Principal")

    font = pygame.font.SysFont(None, 36)
    title_font = pygame.font.SysFont(None, 48)

    # Lista de opciones del menú
    menu_options = [
        "Kinematic Arrive",
        "Kinematic Flee",
        "Kinematic Wander",
        "Dynamic Seek",
        "Dynamic Flee",
        "Dynamic Arrive",
        "Align",
        "Velocity Matching",
        "Face",
        "Pursue and Evade - Look Where You're Going",
        "Dynamic Wander",
        "Path Following",
        "Separation",
        "Collision Avoidance",
        "Obstacle and Wall Avoidance",
        "Salir"
    ]

    # Crear botones para cada opción
    buttons: list[Button] = []
    for idx, option in enumerate(menu_options):
        button = Button(
            text=f"{idx + 1}. {option}",
            pos=(50, 100 + idx * 40),
            font=font,
            bg="black"
        )
        buttons.append(button)

    running = True
    while running:
        screen.fill((0, 0, 0))  # Fondo negro

        # Mostrar el título
        title_text = title_font.render(
            "Seleccione el algoritmo a utilizar:", True, pygame.Color("White"))
        screen.blit(title_text, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return 0  # Salir del programa
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, button in enumerate(buttons):
                    if button.click(event):
                        if idx == len(menu_options) - 1:
                            return 0  # Salir
                        else:
                            return idx + 1  # Retornar la opción seleccionada

        # Mostrar los botones
        for button in buttons:
            button.show(screen)

        pygame.display.flip()
        clock.tick(60)


def run_kinematic_arrive(screen, clock):
    print("Ejecutando Kinematic Arrive. El personaje se moverá hacia el mouse.")
    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(random.uniform(
        0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    character.orientation = random.uniform(0, 2 * math.pi)
    character.max_speed = 200.0

    # Configurar target
    target = Static()
    # Actualizaremos target.position con la posición del mouse

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar posición del target a la posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        target.position = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])

        # Aplicar comportamiento Kinematic Arrive
        behavior = KinematicArrive(
            character, target, character.max_speed, radius=50.0, time_to_target=0.25)
        steering = behavior.get_steering()
        character.update_kinematic(steering, delta_time)

        # Mantener al personaje dentro de los límites de la pantalla
        character.position.x = max(0, min(character.position.x, SCREEN_WIDTH))
        character.position.y = max(0, min(character.position.y, SCREEN_HEIGHT))

        # Dibujar en pantalla
        screen.fill(BLACK)
        draw_pacman(screen, character.position, character.orientation)
        pygame.draw.circle(
            screen, WHITE, (int(target.position.x), int(target.position.y)), 5)
        pygame.display.flip()


def run_kinematic_flee(screen, clock):
    print("Ejecutando Kinematic Flee. El personaje se alejará del mouse hasta una distancia determinada.")
    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(random.uniform(
        0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    character.orientation = random.uniform(0, 2 * math.pi)
    character.max_speed = 200.0

    # Configurar target
    target = Static()
    # Actualizaremos target.position con la posición del mouse

    # Definir la distancia máxima de huida
    max_flee_distance = 100.0  # El personaje huirá hasta estar a 100 unidades del target

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar posición del target a la posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        target.position = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])

        # Calcular distancia al target
        distance = (character.position - target.position).length()

        if distance < max_flee_distance:
            # Aplicar comportamiento Kinematic Flee
            behavior = KinematicFlee(character, target, character.max_speed)
            steering = behavior.get_steering()
            character.update_kinematic(steering, delta_time)
        else:
            # Sin steering, el personaje se detiene
            steering = KinematicSteeringOutput()
            character.update_kinematic(steering, delta_time)

        # Mantener al personaje dentro de los límites de la pantalla
        character.position.x = max(0, min(character.position.x, SCREEN_WIDTH))
        character.position.y = max(0, min(character.position.y, SCREEN_HEIGHT))

        # # Mantener al personaje dentro de los límites de la pantalla (toroidal)
        # character.position.x = character.position.x % SCREEN_WIDTH
        # character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        draw_pacman(screen, character.position, character.orientation)
        pygame.draw.circle(
            screen, WHITE, (int(target.position.x), int(target.position.y)), 5)
        pygame.display.flip()


def run_kinematic_wander(screen, clock):
    print("Ejecutando Kinematic Wander. El personaje vagará aleatoriamente.")
    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    character.orientation = random.uniform(0, 2 * math.pi)
    character.max_speed = 150.0
    character.max_rotation = math.pi  # Rotación máxima por actualización

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Aplicar comportamiento Kinematic Wander
        behavior = KinematicWander(
            character, character.max_speed, 2 * character.max_rotation * delta_time)
        steering = behavior.get_steering()
        character.update_kinematic(steering, delta_time)

        # Mantener al personaje dentro de los límites de la pantalla (toroidal)
        character.position.x = character.position.x % SCREEN_WIDTH
        character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        draw_pacman(screen, character.position, character.orientation)
        pygame.display.flip()


def run_dynamic_seek(screen, clock):
    print("Ejecutando Dynamic Seek. El personaje buscará al mouse.")
    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(random.uniform(
        0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    character.orientation = random.uniform(0, 2 * math.pi)
    character.max_speed = 200.0
    character.max_acceleration = 150.0

    # Configurar target
    target = Kinematic()
    # Actualizaremos target.position con la posición del mouse

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar posición del target a la posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        target.position = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])

        # Aplicar comportamiento Dynamic Seek
        behavior = DynamicSeek(character, target, character.max_acceleration)
        steering = behavior.get_steering()
        character.update(steering, delta_time)

       # Aplicar Look Where You're Going al personaje para que mire hacia donde se dirige
        behavior_look = LookWhereYouAreGoing(
            character,
            max_rotation=character.max_rotation,
            max_angular_acceleration=character.max_acceleration,
            target_radius=0.01,
            slow_radius=math.pi / 4
        )
        steering_look = behavior_look.get_steering()
        character.update(steering_look, delta_time)

        # Mantener al personaje dentro de los límites de la pantalla (toroidal)
        # character.position.x = character.position.x % SCREEN_WIDTH
        # character.position.y = character.position.y % SCREEN_HEIGHT

        # Mantener al personaje dentro de los límites de la pantalla
        character.position.x = max(0, min(character.position.x, SCREEN_WIDTH))
        character.position.y = max(0, min(character.position.y, SCREEN_HEIGHT))

        # Dibujar en pantalla
        screen.fill(BLACK)
        draw_pacman(screen, character.position, character.orientation)
        pygame.draw.circle(
            screen, WHITE, (int(target.position.x), int(target.position.y)), 5)
        pygame.display.flip()


def run_dynamic_flee(screen, clock):
    print("Ejecutando Dynamic Flee. El personaje se alejará del mouse hasta una distancia determinada.")
    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(random.uniform(
        0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    character.orientation = random.uniform(0, 2 * math.pi)
    character.max_speed = 200.0
    character.max_acceleration = 200.0

    # Configurar target
    target = Kinematic()
    # Actualizaremos target.position con la posición del mouse

    # Definir la distancia máxima de huida
    max_flee_distance = 200.0  # El personaje huirá hasta estar a 200 unidades del target

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar posición del target a la posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        target.position = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])

        # Calcular distancia al target
        distance = (character.position - target.position).length()

        if distance < max_flee_distance:
            # Aplicar comportamiento Dynamic Flee
            behavior = DynamicFlee(
                character, target, character.max_acceleration)
            steering = behavior.get_steering()
            character.update(steering, delta_time)
        else:
            # Sin steering, el personaje continúa con su velocidad actual
            steering = SteeringOutput()
            character.update(steering, delta_time)

        # Aplicar Look Where You're Going al personaje para que mire hacia donde se dirige
        behavior_look = LookWhereYouAreGoing(
            character,
            max_rotation=character.max_rotation,
            max_angular_acceleration=character.max_acceleration,
            target_radius=0.01,
            slow_radius=math.pi / 4
        )
        steering_look = behavior_look.get_steering()
        character.update(steering_look, delta_time)

        # Mantener al personaje dentro de los límites de la pantalla (toroidal)
        character.position.x = character.position.x % SCREEN_WIDTH
        character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        draw_pacman(screen, character.position, character.orientation)
        pygame.draw.circle(
            screen, WHITE, (int(target.position.x), int(target.position.y)), 5)
        pygame.display.flip()


def run_dynamic_arrive(screen, clock):
    print("Ejecutando Dynamic Arrive. El personaje llegará al mouse de manera suave.")
    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(random.uniform(
        0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    character.orientation = random.uniform(0, 2 * math.pi)
    character.max_speed = 200.0
    character.max_acceleration = 100.0
    character.drag = 1.0  # Sin fricción

    # Configurar target
    target = Kinematic()
    # Actualizaremos target.position con la posición del mouse

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar posición del target a la posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        target.position = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])

        # Aplicar comportamiento Dynamic Arrive
        behavior = DynamicArrive(character, target, character.max_acceleration,
                                 character.max_speed, target_radius=40.0, slow_radius=250.0, time_to_target=0.1)
        steering = behavior.get_steering()
        character.update(steering, delta_time)

        # Aplicar Look Where You're Going al personaje para que mire hacia donde se dirige
        behavior_look = LookWhereYouAreGoing(
            character,
            max_rotation=character.max_rotation,
            max_angular_acceleration=character.max_acceleration,
            target_radius=0.01,
            slow_radius=math.pi / 4
        )
        steering_look = behavior_look.get_steering()
        character.update(steering_look, delta_time)

        # Mantener al personaje dentro de los límites de la pantalla (toroidal)
        character.position.x = character.position.x % SCREEN_WIDTH
        character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        draw_pacman(screen, character.position, character.orientation)
        pygame.draw.circle(
            screen, WHITE, (int(target.position.x), int(target.position.y)), 5)
        pygame.display.flip()


def run_align(screen, clock):
    print("Ejecutando Align. El personaje rotará para mirar hacia el mouse.")
    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(
        SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Centro de la pantalla
    character.orientation = random.uniform(0, 2 * math.pi)
    character.rotation = 0.0
    character.max_rotation = math.pi  # Velocidad máxima de rotación
    character.max_angular_acceleration = math.pi  # Aceleración angular máxima

    # Configurar target
    target = Kinematic()

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Calcular orientación objetivo basada en la posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(
            mouse_pos[0], mouse_pos[1]) - character.position
        if direction.length() > 0:
            target.orientation = math.atan2(-direction.y, direction.x)
        else:
            target.orientation = character.orientation

        # Aplicar comportamiento Align
        behavior = Align(character, target, max_rotation=character.max_rotation,
                         max_angular_acceleration=character.max_angular_acceleration, target_radius=0.01, slow_radius=math.pi / 3)
        steering = behavior.get_steering()
        character.update(steering, delta_time)

        # Dibujar en pantalla
        screen.fill(BLACK)
        draw_pacman(screen, character.position, character.orientation)
        pygame.draw.circle(
            screen, WHITE, (int(mouse_pos[0]), int(mouse_pos[1])), 5)
        pygame.display.flip()


def run_velocity_matching(screen, clock):
    print("Ejecutando Velocity Matching. El personaje igualará su velocidad a la de otro.")
    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(100, SCREEN_HEIGHT / 2)
    character.orientation = 0.0
    character.velocity = pygame.math.Vector2(0, 0)
    character.max_speed = 200.0
    character.max_acceleration = 100.0

    # Configurar target moviéndose con velocidad constante
    target = Kinematic()
    target.position = pygame.math.Vector2(300, SCREEN_HEIGHT / 2)
    target.orientation = 0.0
    target.velocity = pygame.math.Vector2(
        100, 0)  # Moviéndose hacia la derecha
    target.max_speed = 200.0

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar posición del target
        target.position += target.velocity * delta_time
        target.position.x = target.position.x % SCREEN_WIDTH
        target.position.y = target.position.y % SCREEN_HEIGHT

        # Aplicar comportamiento Velocity Matching
        behavior = VelocityMatching(
            character, target, character.max_acceleration, time_to_target=0.1)
        steering = behavior.get_steering()
        character.update(steering, delta_time)

        # Mantener al personaje dentro de los límites de la pantalla (toroidal)
        character.position.x = character.position.x % SCREEN_WIDTH
        character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        # Dibujar target
        pygame.draw.circle(
            screen, WHITE, (int(target.position.x), int(target.position.y)), 5)
        # Dibujar personaje
        draw_pacman(screen, character.position, character.orientation)
        pygame.display.flip()


def run_face(screen, clock):
    print("Ejecutando Face. 5 personajes mirarán al mouse desde distintos lugares.")
    # Configurar personajes
    characters: list[Kinematic] = []
    for _ in range(5):
        character = Kinematic()
        character.position = pygame.math.Vector2(random.uniform(
            0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
        character.orientation = random.uniform(0, 2 * math.pi)
        character.rotation = 0.0
        character.max_rotation = math.pi  # Velocidad máxima de rotación
        character.max_angular_acceleration = math.pi  # Aceleración angular máxima
        characters.append(character)

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar cada personaje
        for character in characters:
            # Calcular posición objetivo (posición del mouse)
            mouse_pos = pygame.mouse.get_pos()
            target_position = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])
            behavior = Face(
                character,
                target_position,
                max_rotation=character.max_rotation,
                max_angular_acceleration=character.max_angular_acceleration,
                target_radius=0.01,
                slow_radius=math.pi / 4
            )
            steering = behavior.get_steering()
            character.update(steering, delta_time)

        # Dibujar en pantalla
        screen.fill(BLACK)
        for character in characters:
            draw_pacman(screen, character.position, character.orientation)
        pygame.display.flip()


def run_pursue_and_evade(screen, clock):
    print("Ejecutando Pursue and Evade. Un personaje persigue al jugador mientras otro lo evade.")

    # Configurar perseguidor
    pursuer = Kinematic()
    pursuer.position = pygame.math.Vector2(random.uniform(
        0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    pursuer.orientation = random.uniform(0, 2 * math.pi)
    pursuer.velocity = pygame.math.Vector2(0, 0)
    pursuer.max_speed = 200.0
    pursuer.max_acceleration = 100.0
    pursuer.max_rotation = math.pi
    pursuer.max_angular_acceleration = math.pi
    pursuer.drag = 0.98  # Aplicar fricción si es necesario

    # Configurar evasor
    evader = Kinematic()
    evader.position = pygame.math.Vector2(random.uniform(
        0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    evader.orientation = random.uniform(0, 2 * math.pi)
    evader.velocity = pygame.math.Vector2(0, 0)
    evader.max_speed = 200.0
    evader.max_acceleration = 100.0
    evader.max_rotation = math.pi
    evader.max_angular_acceleration = math.pi
    evader.drag = 0.98  # Aplicar fricción si es necesario

    # El jugador es controlado por la posición del mouse
    player = Kinematic()
    mouse_pos = pygame.mouse.get_pos()
    player.position = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])
    player.velocity = pygame.math.Vector2(0, 0)

    previous_player_position = player.position

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar posición del jugador y calcular su velocidad
        mouse_pos = pygame.mouse.get_pos()
        new_player_position = pygame.math.Vector2(mouse_pos[0], mouse_pos[1])
        player.velocity = (new_player_position - player.position) / delta_time
        player.position = new_player_position

        # Actualizar perseguidor
        behavior_pursue = Pursue(
            pursuer, player, pursuer.max_acceleration, max_prediction=2.0)
        steering_pursue = behavior_pursue.get_steering()

        # Aplicar Look Where You're Going al perseguidor
        behavior_look_pursuer = LookWhereYouAreGoing(
            pursuer,
            max_rotation=pursuer.max_rotation,
            max_angular_acceleration=pursuer.max_angular_acceleration,
            target_radius=0.01,
            slow_radius=math.pi / 4
        )
        steering_look_pursuer = behavior_look_pursuer.get_steering()

        # Combinar los steering
        steering_pursuer = SteeringOutput()
        steering_pursuer.linear = steering_pursue.linear
        steering_pursuer.angular = steering_look_pursuer.angular

        pursuer.update(steering_pursuer, delta_time)

        # Limitar la velocidad y rotación máxima del perseguidor
        if pursuer.velocity.length() > pursuer.max_speed:
            pursuer.velocity = pursuer.velocity.normalize() * pursuer.max_speed
        pursuer.rotation = max(-pursuer.max_rotation,
                               min(pursuer.rotation, pursuer.max_rotation))

        # Actualizar evasor
        behavior_evade = Evade(
            evader, player, evader.max_acceleration, max_prediction=2.0)
        steering_evade = behavior_evade.get_steering()

        # Aplicar Look Where You're Going al evasor
        behavior_look_evader = LookWhereYouAreGoing(
            evader,
            max_rotation=evader.max_rotation,
            max_angular_acceleration=evader.max_angular_acceleration,
            target_radius=0.01,
            slow_radius=math.pi / 4
        )
        steering_look_evader = behavior_look_evader.get_steering()

        # Combinar los steering
        steering_evader = SteeringOutput()
        steering_evader.linear = steering_evade.linear
        steering_evader.angular = steering_look_evader.angular

        evader.update(steering_evader, delta_time)

        # Limitar la velocidad y rotación máxima del evasor
        if evader.velocity.length() > evader.max_speed:
            evader.velocity = evader.velocity.normalize() * evader.max_speed
        evader.rotation = max(-evader.max_rotation,
                              min(evader.rotation, evader.max_rotation))

        # Mantener personajes dentro de los límites de la pantalla (toroidal)
        pursuer.position.x = max(0, min(pursuer.position.x, SCREEN_WIDTH))
        pursuer.position.y = min(pursuer.position.y, SCREEN_HEIGHT)
        evader.position.x = max(0, min(evader.position.x, SCREEN_WIDTH))
        evader.position.y = min(evader.position.y, SCREEN_HEIGHT)

        # Dibujar en pantalla
        screen.fill(BLACK)
        # Dibujar jugador (posición del mouse)
        pygame.draw.circle(
            screen, WHITE, (int(player.position.x), int(player.position.y)), 5)
        # Dibujar perseguidor
        draw_pacman(screen, pursuer.position, pursuer.orientation,
                    color=(255, 0, 0))  # Rojo para perseguidor
        # Dibujar evasor
        draw_pacman(screen, evader.position, evader.orientation,
                    color=(0, 0, 255))  # Azul para evasor
        pygame.display.flip()


def run_dynamic_wander(screen, clock):
    print("Ejecutando Dynamic Wander. 5 personajes vagarán aleatoriamente.")
    # Configurar personajes
    characters: list[Kinematic] = []
    for _ in range(5):
        character = Kinematic()
        character.position = pygame.math.Vector2(random.uniform(
            0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
        character.orientation = random.uniform(0, 2 * math.pi)
        character.max_speed = 200.0
        character.max_acceleration = 100.0
        character.max_rotation = math.pi
        character.max_angular_acceleration = math.pi
        characters.append(character)

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        for character in characters:
            # Aplicar comportamiento Dynamic Wander
            behavior = DynamicWander(
                character,
                wander_offset=100.0,
                wander_radius=80.0,
                wander_rate=math.pi / 4,
                max_acceleration=character.max_acceleration,
                max_rotation=character.max_rotation,
                max_angular_acceleration=character.max_angular_acceleration,
                target_radius=0.01,
                slow_radius=math.pi / 4
            )
            steering = behavior.get_steering()
            character.update(steering, delta_time)
            # Mantener personaje dentro de los límites de la pantalla (toroidal)
            character.position.x = character.position.x % SCREEN_WIDTH
            character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        for character in characters:
            draw_pacman(screen, character.position, character.orientation)
        pygame.display.flip()


def run_path_following(screen, clock):
    print("Ejecutando Path Following. El personaje seguirá una ruta definida.")

    # Crear una ruta circular
    center = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    radius = 200
    num_points = 36  # Número de puntos en el círculo
    waypoints = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        waypoints.append(pygame.math.Vector2(x, y))
    path = Path(waypoints)

    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(random.uniform(
        0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    # Asegurar que el personaje inicia fuera del círculo
    while (character.position - center).length() < radius:
        character.position = pygame.math.Vector2(random.uniform(
            0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
    character.orientation = random.uniform(0, 2 * math.pi)
    character.velocity = pygame.math.Vector2(0, 0)
    character.max_speed = 200.0
    character.max_acceleration = 100.0

    # Crear comportamiento PathFollowing
    behavior = PathFollowing(
        character, path, path_offset=10.0, max_acceleration=character.max_acceleration)

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Obtener steering
        steering = behavior.get_steering()
        character.update(steering, delta_time)

        # Limitar la velocidad máxima
        if character.velocity.length() > character.max_speed:
            character.velocity = character.velocity.normalize() * character.max_speed

        # Mantener al personaje dentro de los límites de la pantalla (toroidal)
        character.position.x = character.position.x % SCREEN_WIDTH
        character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        # Dibujar la ruta
        for i in range(len(path.waypoints)):
            start_point = path.waypoints[i]
            end_point = path.waypoints[(i + 1) % len(path.waypoints)]
            pygame.draw.line(screen, WHITE, (start_point.x,
                             start_point.y), (end_point.x, end_point.y), 2)

        # Dibujar personaje
        draw_pacman(screen, character.position, character.orientation)
        pygame.display.flip()


def run_separation(screen, clock):
    print("Ejecutando Separation. Los personajes aplican Velocity Matching hacia el jugador mientras se mantienen separados y evitan colisionar con el jugador.")

    # Crear 10 personajes
    characters: list[Kinematic] = []
    for _ in range(10):
        character = Kinematic()
        character.position = pygame.math.Vector2(random.uniform(
            0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
        character.orientation = random.uniform(0, 2 * math.pi)
        character.velocity = pygame.math.Vector2(0, 0)
        character.max_speed = 200.0
        character.max_acceleration = 100.0
        character.drag = 0.98  # Aplicar fricción
        characters.append(character)

    # Crear el jugador que aplica Dynamic Wander
    player = Kinematic()
    player.position = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.orientation = random.uniform(0, 2 * math.pi)
    player.velocity = pygame.math.Vector2(0, 0)
    player.max_speed = 150.0
    player.max_acceleration = 50.0
    player.max_rotation = math.pi
    player.max_angular_acceleration = math.pi
    player.drag = 0.98  # Aplicar fricción

    # Comportamiento Dynamic Wander para el jugador
    player_behavior = DynamicWander(
        player,
        wander_offset=100.0,
        wander_radius=50.0,
        wander_rate=math.pi / 4,
        max_acceleration=player.max_acceleration,
        max_rotation=player.max_rotation,
        max_angular_acceleration=player.max_angular_acceleration,
        target_radius=0.01,
        slow_radius=math.pi / 4
    )

    # Agregar el jugador a la lista de targets para Separation
    all_targets = characters + [player]

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Actualizar el jugador
        steering_player = player_behavior.get_steering()
        player.update(steering_player, delta_time)

        # Limitar la velocidad máxima del jugador
        if player.velocity.length() > player.max_speed:
            player.velocity = player.velocity.normalize() * player.max_speed

        # Aplicar fricción al jugador
        player.velocity *= player.drag

        # Mantener al jugador dentro de los límites de la pantalla (toroidal)
        player.position.x = player.position.x % SCREEN_WIDTH
        player.position.y = player.position.y % SCREEN_HEIGHT

        for character in characters:
            # Aplicar Velocity Matching hacia el jugador
            behavior_vm = VelocityMatching(
                character, player, character.max_acceleration, time_to_target=0.1)
            steering_vm = behavior_vm.get_steering()

            # Aplicar Separation de otros personajes y del jugador
            behavior_sep = Separation(character, all_targets, threshold=20.0,
                                      decay_coefficient=1000.0, max_acceleration=character.max_acceleration)
            steering_sep = behavior_sep.get_steering()

            # Combinar los comportamientos
            steering = SteeringOutput()
            steering.linear = steering_vm.linear + steering_sep.linear
            # Limitar la aceleración máxima
            if steering.linear.length() > character.max_acceleration:
                steering.linear = steering.linear.normalize() * character.max_acceleration
            steering.angular = 0.0

            character.update(steering, delta_time)

            # Limitar la velocidad máxima
            if character.velocity.length() > character.max_speed:
                character.velocity = character.velocity.normalize() * character.max_speed

            # Aplicar fricción
            character.velocity *= character.drag

            # Aplicar Look Where You're Going al personaje para que mire hacia donde se dirige
            behavior_look = LookWhereYouAreGoing(
                character,
                max_rotation=character.max_rotation,
                max_angular_acceleration=character.max_acceleration,
                target_radius=0.01,
                slow_radius=math.pi / 4
            )
            steering_look = behavior_look.get_steering()
            character.update(steering_look, delta_time)

            # Mantener al personaje dentro de los límites de la pantalla (toroidal)
            character.position.x = character.position.x % SCREEN_WIDTH
            character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        # Dibujar jugador en un color diferente (verde)
        draw_pacman(screen, player.position,
                    player.orientation, color=(0, 255, 0))
        # Dibujar personajes
        for character in characters:
            draw_pacman(screen, character.position, character.orientation)
        pygame.display.flip()


def run_collision_avoidance(screen, clock):
    print("Ejecutando Collision Avoidance. 10 personajes aplican Dynamic Wander mientras se evitan entre ellos.")

    # Crear 10 personajes
    characters = []
    for _ in range(10):
        character = Kinematic()
        character.position = pygame.math.Vector2(random.uniform(
            0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
        character.orientation = random.uniform(0, 2 * math.pi)
        # Inicializar con una velocidad aleatoria
        speed = random.uniform(50, 100)
        direction = pygame.math.Vector2(
            math.cos(character.orientation), -math.sin(character.orientation))
        character.velocity = direction * speed
        character.max_speed = 200.0
        character.max_acceleration = 100.0
        character.max_rotation = math.pi
        character.max_angular_acceleration = math.pi
        character.drag = 0.98  # Aplicar fricción
        characters.append(character)

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        for character in characters:
            # Aplicar Dynamic Wander
            behavior_wander = DynamicWander(
                character,
                wander_offset=50.0,
                wander_radius=30.0,
                wander_rate=math.pi / 4,
                max_acceleration=character.max_acceleration,
                max_rotation=character.max_rotation,
                max_angular_acceleration=character.max_angular_acceleration,
                target_radius=0.01,
                slow_radius=math.pi / 4
            )
            steering_wander = behavior_wander.get_steering()

            # Aplicar Collision Avoidance para evitar colisiones
            behavior_ca = CollisionAvoidance(
                character, characters, max_acceleration=character.max_acceleration)
            steering_ca = behavior_ca.get_steering()

            # Combinar los comportamientos
            steering = SteeringOutput()
            steering.linear = steering_wander.linear + steering_ca.linear
            # Limitar la aceleración máxima
            if steering.linear.length() > character.max_acceleration:
                steering.linear = steering.linear.normalize() * character.max_acceleration
            steering.angular = steering_wander.angular  # Usamos el angular de wander

            character.update(steering, delta_time)

            # Limitar la velocidad máxima
            if character.velocity.length() > character.max_speed:
                character.velocity = character.velocity.normalize() * character.max_speed

            # Aplicar fricción
            character.velocity *= character.drag

            # Mantener al personaje dentro de los límites de la pantalla (toroidal)
            character.position.x = character.position.x % SCREEN_WIDTH
            character.position.y = character.position.y % SCREEN_HEIGHT

        # Dibujar en pantalla
        screen.fill(BLACK)
        for character in characters:
            draw_pacman(screen, character.position, character.orientation)
        pygame.display.flip()


def run_obstacle_avoidance(screen, clock):
    print("Ejecutando Obstacle and Wall Avoidance. Un personaje se mueve evitando obstáculos y paredes.")

    # Definir obstáculos (círculos)
    obstacles = []
    num_obstacles = 5
    for _ in range(num_obstacles):
        obstacle = {
            'position': pygame.math.Vector2(random.uniform(100, SCREEN_WIDTH - 100), random.uniform(100, SCREEN_HEIGHT - 100)),
            'radius': 30
        }
        obstacles.append(obstacle)

    # Configurar personaje
    character = Kinematic()
    character.position = pygame.math.Vector2(random.uniform(
        50, SCREEN_WIDTH - 50), random.uniform(50, SCREEN_HEIGHT - 50))
    character.orientation = random.uniform(0, 2 * math.pi)
    character.velocity = pygame.math.Vector2(
        100 * math.cos(character.orientation), -100 * math.sin(character.orientation))
    character.max_speed = 200.0
    character.max_acceleration = 100.0

    running = True
    while running:
        delta_time = clock.tick(60) / 1000.0  # Delta time en segundos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        # Aplicar Obstacle Avoidance
        behavior = ObstacleAvoidance(character, obstacles, avoid_distance=50.0,
                                     lookahead=50.0, max_acceleration=character.max_acceleration)
        steering = behavior.get_steering()

        # Si no hay steering, seguir adelante
        if steering.linear.length() == 0:
            steering.linear = character.velocity.normalize() * character.max_acceleration

        character.update(steering, delta_time)

        # Limitar la velocidad máxima
        if character.velocity.length() > character.max_speed:
            character.velocity = character.velocity.normalize() * character.max_speed

        # Evitar paredes (reflexión simple)
        if character.position.x < 0 or character.position.x > SCREEN_WIDTH:
            character.velocity.x = -character.velocity.x
            character.position.x = max(
                0, min(character.position.x, SCREEN_WIDTH))
        if character.position.y < 0 or character.position.y > SCREEN_HEIGHT:
            character.velocity.y = -character.velocity.y
            character.position.y = max(
                0, min(character.position.y, SCREEN_HEIGHT))

        # Dibujar en pantalla
        screen.fill(BLACK)
        # Dibujar obstáculos
        for obstacle in obstacles:
            pygame.draw.circle(screen, (128, 128, 128), (int(
                obstacle['position'].x), int(obstacle['position'].y)), obstacle['radius'])
        # Dibujar personaje
        draw_pacman(screen, character.position, character.orientation)
        pygame.display.flip()


if __name__ == "__main__":
    main()
