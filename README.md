# Proyecto 1 - CI6450 Inteligencia Artificial para Videojuegos

Este repositorio contiene la implementación del **Proyecto 1** de la materia **CI6450 - Inteligencia Artificial para Videojuegos** (Universidad Simón Bolívar, Septiembre-Diciembre 2024). En este proyecto, se desarrollan algoritmos cinemáticos y dinámicos de movimiento para personajes dentro de un videojuego.

## Algoritmos Implementados

Los siguientes algoritmos fueron implementados para uno o más personajes, con el objetivo de interactuar con el jugador:

1. **Kinematic Arriving**
2. **Kinematic Flee** (El personaje se aleja hasta una distancia determinada)
3. **Kinematic Wandering**
4. **Dynamic Seek**
5. **Dynamic Flee** (El personaje se aleja hasta una distancia determinada)
6. **Dynamic Arrive**
7. **Align**
8. **Velocity Matching**
9. **Face** (5 personajes mirando al jugador desde distintos lugares del mundo)
10. **Pursue and Evade - Look Where You're Going** (Demostración de persecución y evasión)
11. **Dynamic Wander** (5 personajes al mismo tiempo)

### Algoritmos Adicionales
Además, se implementaron los siguientes algoritmos:

1. **Path Following** (Seguimiento de una ruta geométrica simple visible en pantalla)
2. **Separation** (10 personajes aplican velocity matching mientras se mantienen separados)
3. **Collision Avoidance** Deben haber al menos 10 personajes aplicando dynamic wander mientras se evitan entre ellos.
4. **Obstacle and Wall Avoidance** Debe haber al menos un personaje simplemente movi´ endose hacia adelante dentro de un área limitada por paredes y con obstáculos dentro de ella.

## Requisitos

Para ejecutar el proyecto, necesitarás lo siguiente:
- **Python 3.x**
- **Pygame** (Para la visualización de los personajes y sus movimientos)

### Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/EliezerMCR/IAForGames-proyecto1
2. Instala las dependencias:
   ```bash
   pip install pygame
3. Ejecuta el proyecto:
   ```bash
   python main.py

