# characters.py

import math
import pygame


class SteeringOutput:
    def __init__(self):
        self.linear = pygame.math.Vector2(0, 0)  # Aceleración lineal
        # Aceleración angular en radianes por segundo cuadrado
        self.angular: float = 0.0


class KinematicSteeringOutput:
    def __init__(self):
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation = 0.0


class Static:
    def __init__(self, position=None, orientation=0.0):
        self.position = position if position is not None else pygame.math.Vector2(
            0, 0)
        self.orientation = orientation  # En radianes

    def newOrientation(self, current: float, velocity: pygame.math.Vector2):
        if velocity.length() > 0:
            return math.atan2(-velocity.y, velocity.x)
        return current


class Kinematic:
    def __init__(self):
        self.position = pygame.math.Vector2(0, 0)
        self.orientation: float = 0.0  # En radianes
        self.velocity = pygame.math.Vector2(0, 0)
        self.rotation: float = 0.0     # Rotación en radianes por segundo

        self.max_speed = 200.0  # Velocidad máxima
        self.max_rotation = math.pi  # Rotación máxima

        self.max_acceleration = 100.0  # Aceleración máxima
        self.max_angular_acceleration = math.pi  # Aceleración angular máxima
        # Coeficiente de fricción para la velocidad
        self.drag = 0.98

    def update(self, steering: SteeringOutput, time: float):
        # Aplicar drag a la velocidad
        self.velocity *= self.drag

        # Actualizar posición y orientación
        self.position += self.velocity * time
        self.orientation += self.rotation * time
        self.orientation = map_to_range(self.orientation)

        # Actualizar velocidad y rotación
        self.velocity += steering.linear * time
        self.rotation += steering.angular * time
        self.orientation = map_to_range(self.orientation)

        # Limitar la velocidad máxima
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # Limitar la rotación máxima
        self.rotation = max(-self.max_rotation,
                            min(self.rotation, self.max_rotation))

    def update_kinematic(self, steering: KinematicSteeringOutput, time: float):
        # Actualizar posición y orientación
        self.position += steering.velocity * time
        self.orientation += steering.rotation * time
        self.orientation = map_to_range(self.orientation)

        # Actualizar velocidad y rotación
        self.velocity = steering.velocity
        self.rotation = steering.rotation

    # BORRAR
    def newOrientation(self, current: float, velocity: pygame.math.Vector2):
        if velocity.length() > 0:
            return math.atan2(-velocity.y, velocity.x)
        return current


def map_to_range(angle: float) -> float:
    angle = (angle + math.pi) % (2 * math.pi) - math.pi
    return angle
