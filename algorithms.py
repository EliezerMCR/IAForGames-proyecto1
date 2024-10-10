# algorithms.py

from characters import Kinematic, SteeringOutput, Static, KinematicSteeringOutput, map_to_range
from drawing import Path
import math
import pygame
import random

# Implementación de los algoritmos de movimiento


class KinematicSeek:
    def __init__(self, character: Kinematic, target: Static, max_speed: float):
        self.character: Kinematic = character
        self.target: Static = target
        self.max_speed: float = max_speed

    def get_steering(self) -> KinematicSteeringOutput:
        result: KinematicSteeringOutput = KinematicSteeringOutput()

        # Obtener la dirección al objetivo
        result.velocity = self.target.position - self.character.position

        # Asegurarse de que la velocidad no sea cero antes de normalizar
        if result.velocity.length() > 0:
            # Obtener la velocidad máxima en esa dirección
            result.velocity = result.velocity.normalize() * self.max_speed

            # Encaramos en la dirección que queremos movernos
            self.character.orientation = self.character.newOrientation(
                self.character.orientation, result.velocity)

        else:
            result.velocity = pygame.math.Vector2(0, 0)

        # La rotación no se necesita en este caso
        result.rotation = 0.0
        return result


class KinematicFlee(KinematicSeek):
    def __init__(self, character: Kinematic, target: Static, max_speed: float):
        super().__init__(character, target, max_speed)

    def get_steering(self) -> KinematicSteeringOutput:
        result: KinematicSteeringOutput = KinematicSteeringOutput()

        # Obtener la dirección opuesta al objetivo
        result.velocity = self.character.position - self.target.position

        if result.velocity.length() > 0:
            # Obtener la velocidad máxima en esa dirección
            result.velocity = result.velocity.normalize() * self.max_speed

            # Encaramos en la dirección que queremos movernos
            self.character.orientation = self.character.newOrientation(
                self.character.orientation, result.velocity)
        else:
            result.velocity = pygame.math.Vector2(0, 0)

        # La rotación no se necesita en este caso
        result.rotation = 0.0
        return result


class KinematicArrive:
    def __init__(self, character: Kinematic, target: Static, max_speed: float, radius: float, time_to_target: float):
        self.character: Kinematic = character
        self.target: Static = target
        self.max_speed: float = max_speed
        self.radius: float = radius
        self.time_to_target: float = time_to_target

    def get_steering(self) -> KinematicSteeringOutput:
        result: KinematicSteeringOutput = KinematicSteeringOutput()

        # Obtener la dirección al objetivo
        result.velocity = self.target.position - self.character.position
        distance: float = result.velocity.length()

        # Comprobar si estamos dentro del radio
        if distance < self.radius:
            result.velocity = pygame.math.Vector2(0, 0)
            result.rotation = 0.0
            return result

        # Necesitamos movernos hacia nuestro objetivo en el tiempo especificado
        if self.time_to_target > 0:
            result.velocity = result.velocity.normalize() * (distance / self.time_to_target)
        else:
            result.velocity = result.velocity.normalize() * self.max_speed

        # Si es muy rápido, limitamos la velocidad a la máxima
        if result.velocity.length() > self.max_speed:
            result.velocity = result.velocity.normalize() * self.max_speed

        # Encaramos en la dirección que queremos movernos
        self.character.orientation = self.character.newOrientation(
            self.character.orientation, result.velocity)

        # La rotación no se necesita en este caso
        result.rotation = 0.0
        return result


class KinematicWander:
    def __init__(self, character: Kinematic, max_speed: float, max_rotation: float):
        self.character: Kinematic = character
        self.max_speed: float = max_speed
        self.max_rotation: float = max_rotation

    def get_steering(self) -> KinematicSteeringOutput:
        result: KinematicSteeringOutput = KinematicSteeringOutput()

        # Obtenemos la velocidad desde el vector formado por la orientación del personaje
        result.velocity = pygame.math.Vector2(
            self.max_speed * math.cos(self.character.orientation),
            -self.max_speed * math.sin(self.character.orientation)
        )

        # Cambiamos la orientación de forma aleatoria
        self.character.orientation += random.uniform(-self.max_rotation,
                                                     self.max_rotation)

        # Aseguramos que la orientación está en el rango [-pi, pi]
        self.character.orientation = map_to_range(
            self.character.orientation)

        # La rotación no se necesita en este caso
        result.rotation = 0.0
        return result


class DynamicSeek:
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float):
        self.character: Kinematic = character
        self.target: Static = target
        self.max_acceleration: float = max_acceleration

    def get_steering(self) -> SteeringOutput:
        result: SteeringOutput = SteeringOutput()

        # Obtener la dirección al objetivo
        result.linear = self.target.position - self.character.position

        # Asegurarse de que estamos yendo a la máxima aceleración
        if result.linear.length() > 0:
            result.linear = result.linear.normalize() * self.max_acceleration
        else:
            result.linear = pygame.math.Vector2(0, 0)

        # No necesitamos rotación en este caso
        result.angular = 0.0
        return result


class DynamicFlee(DynamicSeek):
    def __init__(self, character: Kinematic, target: Static, max_acceleration: float):
        super().__init__(character, target, max_acceleration)

    def get_steering(self) -> SteeringOutput:
        result: SteeringOutput = SteeringOutput()

        # Obtener la dirección opuesta al objetivo
        result.linear = self.character.position - self.target.position

        # Asegurarse de que estamos yendo a la máxima aceleración
        if result.linear.length() > 0:
            result.linear = result.linear.normalize() * self.max_acceleration
        else:
            result.linear = pygame.math.Vector2(0, 0)

        # No necesitamos rotación en este caso
        result.angular = 0.0
        return result


class DynamicArrive:
    def __init__(self, character: Kinematic, target: Static, max_acceleration: float, max_speed: float, target_radius: float, slow_radius: float, time_to_target: float):
        self.character: Kinematic = character
        self.target: Static = target
        self.max_acceleration: float = max_acceleration
        self.max_speed: float = max_speed
        self.target_radius: float = target_radius
        self.slow_radius: float = slow_radius
        self.time_to_target: float = time_to_target

    def get_steering(self) -> SteeringOutput:
        result: SteeringOutput = SteeringOutput()

        # Obtener la dirección al objetivo
        direction: pygame.math.Vector2 = self.target.position - self.character.position
        distance: float = direction.length()

        # Comprobar si estamos dentro del radio
        if distance < self.target_radius:
            result.linear = pygame.math.Vector2(0, 0)
            result.angular = 0.0
            # Establecer la velocidad del personaje a cero
            self.character.velocity = pygame.math.Vector2(0, 0)
            return result

        # Si estamos en el radio lento, reducimos la velocidad
        if distance > self.slow_radius:
            target_speed: float = self.max_speed
        else:
            target_speed = self.max_speed * distance / self.slow_radius

        # La velocidad objetivo combina dirección y velocidad
        if direction.length() > 0:
            target_velocity: pygame.math.Vector2 = direction.normalize() * target_speed
        else:
            target_velocity = pygame.math.Vector2(0, 0)

        # La aceleración intenta llegar a la velocidad objetivo
        result.linear = (target_velocity -
                         self.character.velocity) / self.time_to_target

        # Verificamos que la aceleración no sea demasiado grande
        if result.linear.length() > self.max_acceleration:
            result.linear = result.linear.normalize() * self.max_acceleration

        # No necesitamos rotación en este caso
        result.angular = 0.0
        return result


class Align:
    def __init__(self, character: Kinematic, target: Static, max_rotation: float, max_angular_acceleration: float, target_radius: float, slow_radius: float, time_to_target: float = 0.1):
        self.character: Kinematic = character
        self.target: Static = target
        self.max_rotation: float = max_rotation
        self.max_angular_acceleration: float = max_angular_acceleration
        self.target_radius: float = target_radius
        self.slow_radius: float = slow_radius
        self.time_to_target: float = time_to_target

    def get_steering(self) -> SteeringOutput:
        result: SteeringOutput = SteeringOutput()

        # Obtener la diferencia de orientación
        rotation: float = self.target.orientation - self.character.orientation
        rotation = map_to_range(rotation)
        rotation_size: float = abs(rotation)

        # Comprobar si estamos dentro del radio de destino
        if rotation_size < self.target_radius:
            result.angular = 0.0
            result.linear = pygame.math.Vector2(0, 0)
            return result

        # Determinar la rotación objetivo
        if rotation_size > self.slow_radius:
            target_rotation: float = self.max_rotation
        else:
            target_rotation = self.max_rotation * rotation_size / self.slow_radius

        # Ajustar la dirección
        target_rotation *= rotation / rotation_size

        # Calcular la aceleración angular
        result.angular = (target_rotation -
                          self.character.rotation) / self.time_to_target

        # Limitar la aceleración angular
        angular_acceleration: float = abs(result.angular)
        if angular_acceleration > self.max_angular_acceleration:
            result.angular = (
                result.angular / angular_acceleration) * self.max_angular_acceleration

        # No necesitamos aceleración lineal
        result.linear = pygame.math.Vector2(0, 0)
        return result


class VelocityMatching:
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float, time_to_target: float):
        self.character: Kinematic = character
        self.target: Kinematic = target
        self.max_acceleration: float = max_acceleration
        self.time_to_target: float = time_to_target

    def get_steering(self) -> SteeringOutput:
        result: SteeringOutput = SteeringOutput()

        # Obtenemos la velocidad objetivo
        result.linear = (self.target.velocity -
                         self.character.velocity) / self.time_to_target

        # Verificamos que la aceleración no sea demasiado grande
        if result.linear.length() > self.max_acceleration:
            result.linear = result.linear.normalize() * self.max_acceleration

        # No necesitamos rotación en este caso
        result.angular = 0.0
        return result


class Face(Align):
    def __init__(self, character: Kinematic, target_position: pygame.math.Vector2, max_rotation: float, max_angular_acceleration: float, target_radius: float, slow_radius: float, time_to_target: float = 0.1):
        dummy_target: Static = Static()
        super().__init__(character, dummy_target, max_rotation,
                         max_angular_acceleration, target_radius, slow_radius, time_to_target)
        self.target_position: pygame.math.Vector2 = target_position

    def get_steering(self) -> SteeringOutput:
        # Calcular la dirección hacia el objetivo
        direction: pygame.math.Vector2 = self.target_position - self.character.position
        if direction.length() == 0:
            result = SteeringOutput()
            result.angular = 0.0
            result.linear = pygame.math.Vector2(0, 0)
            return result

        # Calcular la orientación objetivo
        self.target.orientation = math.atan2(-direction.y, direction.x)

        # Delegar a Align
        return super().get_steering()


class Pursue(DynamicSeek):
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float, max_prediction: float):
        super().__init__(character, target, max_acceleration)
        self.max_prediction: float = max_prediction

    def get_steering(self) -> SteeringOutput:
        # Calcular el vector a la posición objetivo
        direction: pygame.math.Vector2 = self.target.position - self.character.position
        distance: float = direction.length()

        # Calcular nuestra velocidad
        speed: float = self.character.velocity.length()

        # Calcular el tiempo de predicción
        if speed <= distance / self.max_prediction:
            prediction: float = self.max_prediction
        else:
            prediction = distance / speed

        # Calcular la posición objetivo predicha
        predicted_target: Static = Static()
        predicted_target.position = self.target.position + \
            self.target.velocity * prediction

        # Crear un comportamiento DynamicSeek hacia la posición predicha
        seek_behavior: DynamicSeek = DynamicSeek(
            self.character, predicted_target, self.max_acceleration)
        return seek_behavior.get_steering()


class Evade(DynamicFlee):
    def __init__(self, character: Kinematic, target: Kinematic, max_acceleration: float, max_prediction: float):
        super().__init__(character, target, max_acceleration)
        self.max_prediction: float = max_prediction

    def get_steering(self) -> SteeringOutput:
        # Calcular el vector a la posición objetivo
        direction: pygame.math.Vector2 = self.target.position - self.character.position
        distance: float = direction.length()

        # Calcular nuestra velocidad
        speed: float = self.character.velocity.length()

        # Calcular el tiempo de predicción
        if speed <= distance / self.max_prediction:
            prediction: float = self.max_prediction
        else:
            prediction = distance / speed

        # Calcular la posición objetivo predicha
        predicted_target: Static = Static()
        predicted_target.position = self.target.position + \
            self.target.velocity * prediction

        # Crear un comportamiento DynamicFlee hacia la posición predicha
        flee_behavior: DynamicFlee = DynamicFlee(
            self.character, predicted_target, self.max_acceleration)
        return flee_behavior.get_steering()


class LookWhereYouAreGoing:
    def __init__(self, character: Kinematic, max_rotation: float, max_angular_acceleration: float, target_radius: float, slow_radius: float):
        self.character = character
        self.max_rotation = max_rotation
        self.max_angular_acceleration = max_angular_acceleration
        self.target_radius = target_radius
        self.slow_radius = slow_radius

    def get_steering(self) -> SteeringOutput:
        # Si no hay velocidad, no cambiamos la orientación
        if self.character.velocity.length() == 0:
            return SteeringOutput()

        # Calcular orientación objetivo basada en la dirección de la velocidad
        orientation = math.atan2(-self.character.velocity.y,
                                 self.character.velocity.x)
        target = Static()
        target.orientation = orientation

        # Usar Align para rotar hacia la orientación objetivo
        behavior = Align(
            self.character,
            target,
            max_rotation=self.max_rotation,
            max_angular_acceleration=self.max_angular_acceleration,
            target_radius=self.target_radius,
            slow_radius=self.slow_radius
        )
        return behavior.get_steering()


class DynamicWander(Face):
    def __init__(self, character: Kinematic, wander_offset: float, wander_radius: float, wander_rate: float, max_acceleration: float, max_rotation: float, max_angular_acceleration: float, target_radius: float, slow_radius: float):
        # Inicializamos Face con una posición de objetivo vacía (la calcularemos en get_steering)
        super().__init__(character, pygame.math.Vector2(), max_rotation,
                         max_angular_acceleration, target_radius, slow_radius)
        self.wander_offset: float = wander_offset
        self.wander_radius: float = wander_radius
        self.wander_rate: float = wander_rate
        self.max_acceleration: float = max_acceleration
        self.wander_orientation: float = 0.0

    def get_steering(self) -> SteeringOutput:
        # Actualizar la orientación del wander
        self.wander_orientation += random.uniform(-1, 1) * self.wander_rate

        # Calcular la orientación combinada
        target_orientation: float = self.wander_orientation + self.character.orientation

        # Calcular el centro del círculo de wander
        character_orientation_vector: pygame.math.Vector2 = pygame.math.Vector2(
            math.cos(self.character.orientation),
            -math.sin(self.character.orientation)
        )
        circle_center: pygame.math.Vector2 = self.character.position + \
            self.wander_offset * character_orientation_vector

        # Calcular la posición del target en el círculo
        target_orientation_vector: pygame.math.Vector2 = pygame.math.Vector2(
            math.cos(target_orientation),
            -math.sin(target_orientation)
        )
        self.target_position = circle_center + \
            self.wander_radius * target_orientation_vector

        # Delegar a Face para obtener el steering angular
        steering: SteeringOutput = super().get_steering()

        # Establecer la aceleración lineal al máximo en la dirección de la orientación actual
        steering.linear = self.max_acceleration * character_orientation_vector

        return steering


class PathFollowing:
    def __init__(self, character: Kinematic, path: Path, path_offset: float, max_acceleration: float):
        self.character = character
        self.path = path
        self.path_offset = path_offset
        self.max_acceleration = max_acceleration
        self.current_segment = 0

    def get_steering(self) -> SteeringOutput:
        if self.current_segment >= len(self.path.waypoints):
            self.current_segment = 0  # Reiniciar al inicio de la ruta

        target_point = self.path.waypoints[self.current_segment]

        # Verificar si el personaje está cerca del punto objetivo
        distance = (target_point - self.character.position).length()
        if distance < self.path_offset:
            # Mover al siguiente punto
            self.current_segment += 1
            if self.current_segment >= len(self.path.waypoints):
                self.current_segment = 0
            target_point = self.path.waypoints[self.current_segment]

        # Crear un target estático en el punto objetivo
        target = Static()
        target.position = target_point

        # Utilizar DynamicSeek para moverse hacia el target
        behavior = DynamicSeek(self.character, target, self.max_acceleration)
        return behavior.get_steering()

# algorithms.py (Agregar al final del archivo)


class Separation:
    def __init__(self, character: Kinematic, targets: list, threshold: float, decay_coefficient: float, max_acceleration: float):
        self.character = character
        self.targets = targets  # Lista de Kinematic (otros personajes)
        self.threshold = threshold
        self.decay_coefficient = decay_coefficient
        self.max_acceleration = max_acceleration

    def get_steering(self) -> SteeringOutput:
        result = SteeringOutput()
        for target in self.targets:
            if target is self.character:
                continue
            direction = self.character.position - target.position
            distance = direction.length()
            if distance < self.threshold:
                # Calcular la fuerza de repulsión
                strength = min(self.decay_coefficient /
                               (distance * distance), self.max_acceleration)
                # Sumar a la aceleración total
                result.linear += direction.normalize() * strength
        # Limitar la aceleración máxima
        if result.linear.length() > self.max_acceleration:
            result.linear = result.linear.normalize() * self.max_acceleration
        result.angular = 0.0
        return result


class CollisionAvoidance:
    def __init__(self, character: Kinematic, targets: list, max_acceleration: float):
        self.character = character
        self.targets: list[Kinematic] = targets
        self.max_acceleration = max_acceleration

    def get_steering(self) -> SteeringOutput:
        result = SteeringOutput()
        shortest_time = float('inf')
        first_target = None
        first_min_separation = 0.0
        first_distance = 0.0
        first_relative_pos = pygame.math.Vector2()
        first_relative_vel = pygame.math.Vector2()

        for target in self.targets:
            if target is self.character:
                continue

            # Calcular la posición y velocidad relativa
            relative_pos = target.position - self.character.position
            relative_vel = target.velocity - self.character.velocity
            relative_speed = relative_vel.length()
            if relative_speed == 0:
                continue

            time_to_collision = - \
                relative_pos.dot(relative_vel) / (relative_speed ** 2)

            # Verificar si colisionarán
            distance = relative_pos.length()
            min_separation = distance - relative_speed * time_to_collision

            # Definir un umbral de colisión
            collision_radius = 50.0  # Ajusta este valor según sea necesario

            if min_separation > 2 * collision_radius:
                continue

            if 0 < time_to_collision < shortest_time:
                shortest_time = time_to_collision
                first_target = target
                first_min_separation = min_separation
                first_distance = distance
                first_relative_pos = relative_pos
                first_relative_vel = relative_vel

        if first_target is None:
            # No hay colisiones inminentes
            return result

        if first_min_separation <= 0 or first_distance < 2 * collision_radius:
            # Ya estamos en colisión, dirigirnos directamente lejos del target
            relative_pos = first_target.position - self.character.position
        else:
            # De lo contrario, dirigirnos hacia la futura posición de colisión
            relative_pos = first_relative_pos + first_relative_vel * shortest_time

        # Calcular la aceleración para evitar la colisión
        result.linear = -relative_pos.normalize() * self.max_acceleration
        result.angular = 0.0
        return result


class ObstacleAvoidance:
    def __init__(self, character: Kinematic, obstacles: list, avoid_distance: float, lookahead: float, max_acceleration: float):
        self.character = character
        self.obstacles = obstacles  # Lista de diccionarios con 'position' y 'radius'
        self.avoid_distance = avoid_distance
        self.lookahead = lookahead
        self.max_acceleration = max_acceleration

    def get_steering(self) -> SteeringOutput:
        result = SteeringOutput()

        # Vector de la dirección del personaje
        ray_vector = self.character.velocity.normalize() * self.lookahead

        closest_obstacle = None
        closest_distance = float('inf')
        closest_point = None

        for obstacle in self.obstacles:
            # Vector al obstáculo
            obstacle_vector = obstacle['position'] - self.character.position

            # Proyección del obstáculo en el rayo
            projection = obstacle_vector.dot(ray_vector.normalize())

            if 0 < projection < self.lookahead:
                closest = self.character.position + ray_vector.normalize() * projection
                distance = (obstacle['position'] - closest).length()
                if distance < obstacle['radius']:
                    if projection < closest_distance:
                        closest_distance = projection
                        closest_obstacle = obstacle
                        closest_point = closest

        if closest_obstacle is not None:
            # Calcular steering de evitación
            result.linear = closest_point - closest_obstacle['position']
            result.linear = result.linear.normalize() * self.max_acceleration
            result.angular = 0.0
            return result
        else:
            # No hay colisión, seguir adelante
            result.linear = pygame.math.Vector2(0, 0)
            result.angular = 0.0
            return result
