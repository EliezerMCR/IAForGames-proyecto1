# drawing.py

import pygame
import math
from utils import YELLOW


def draw_pacman(surface, position, orientation, radius=20, color=YELLOW):
    # Ángulo de apertura de la boca (en radianes)
    mouth_opening_angle = math.radians(70)

    # Calcular los ángulos inicial y final del cuerpo (excluyendo la boca)
    start_angle = orientation + mouth_opening_angle / 2
    end_angle = orientation - mouth_opening_angle / 2

    # Nos aseguramos que end_angle sea mayor que start_angle
    if end_angle <= start_angle:
        end_angle += 2 * math.pi

    # Generar puntos para el cuerpo de Pac-Man
    num_points = 30
    angle_step = (end_angle - start_angle) / num_points

    # Lista de puntos para el polígono (boca) de Pac-Man
    points = []

    # Generar puntos a lo largo del arco del cuerpo de Pac-Man
    for i in range(num_points + 1):
        angle = start_angle + i * angle_step
        x = position.x + radius * math.cos(angle)
        y = position.y - radius * math.sin(angle)
        points.append((x, y))

    # Añadir el centro para cerrar el polígono
    points.append((position.x, position.y))

    # Dibujar el cuerpo de Pac-Man con la boca en forma de arco
    pygame.draw.polygon(surface, color, points)


class Button:
    def __init__(self, text, pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = font
        self.bg = bg
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        """Cambiar el texto cuando el usuario pasa el mouse sobre el botón"""
        self.text = text
        self.image = self.font.render(self.text, True, pygame.Color("White"))
        self.size = self.image.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.image, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            return True
        return False


class Path:
    def __init__(self, waypoints):
        # Lista de puntos que forman el camino
        self.waypoints: pygame.math.Vector2 = waypoints
