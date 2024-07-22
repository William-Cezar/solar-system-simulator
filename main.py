import pygame
import sys
from models import CelestialBody, Moon

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((1650, 1000))
pygame.display.set_caption("Solar System Simulation")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Constants for window size and frames per second
WIDTH, HEIGHT = 1650, 1000
FPS = 60

# Define color constants
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # Sun
BLUE = (0, 0, 255)      # Earth
RED = (255, 0, 0)       # Mars
LIGHT_GRAY = (200, 200, 200)  # Mercury
ORANGE = (255, 165, 0)  # Venus
GREY = (100, 100, 100)  # Orbit path color

def simulate_solar_system(planets, moons):
    """
    Simulate the solar system with planets and moons.

    Args:
        planets (list): List of planet objects.
        moons (list): List of moon objects.
    """ 
    simulation_start_time = pygame.time.get_ticks()
    speed_multiplier = 1
    planet_info = None
    running = True

    while running:
        current_time = pygame.time.get_ticks()
        total_seconds_elapsed = (current_time - simulation_start_time) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    speed_multiplier += 0.1
                elif event.key == pygame.K_DOWN:
                    speed_multiplier -= 0.1
                elif event.key == pygame.K_SPACE:
                    speed_multiplier = 1.0
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                planet_info = None
                for planet in planets:
                    if planet.check_hover(mouse_x, mouse_y):
                        planet_info = planet.get_info()

        screen.fill((0, 0, 0))

        for planet in planets[1:]:  # Skip the sun for orbit drawing
            pygame.draw.circle(screen, GREY, (WIDTH // 2, HEIGHT // 2), planet.distance_from_sun, 1)

        # Draw orbits for moons
        for moon in moons:
            moon.draw_orbit(screen)

        # Update and draw each planet
        for planet in planets:
            planet.update_position(clock.get_time() / 1000.0 * speed_multiplier)
            planet.draw(screen)
            label = font.render(planet.name, 1, WHITE)
            label_pos_x = planet.x + 10 if planet.name != "Sun" else planet.x + 40
            screen.blit(label, (label_pos_x, planet.y - 10))

        # Update and draw each moon
        for moon in moons:
            moon.update_position(clock.get_time() / 1000.0 * speed_multiplier)
            moon.draw(screen)
            label = font.render(moon.name, 1, WHITE)
            screen.blit(label, (moon.x + 10, moon.y - 10))

        # Position for elapsed time and laps display
        for index, planet in enumerate(planets):
            if planet.orbital_period is not None:
                lap_info = f"{planet.name}: {planet.laps} Laps around the Sun, Time Elapsed: {total_seconds_elapsed:.2f} sec"
                lap_label = font.render(lap_info, True, WHITE)
                screen.blit(lap_label, (20, 10 + index * 40))

        # Show hovered planet's info
        if planet_info:
                lines = planet_info.split('\n')
                for i, line in enumerate(lines):
                    info_surf = font.render(line, 1, WHITE)
                    screen.blit(info_surf, (WIDTH - info_surf.get_width() - 10, 10 + i * 30))
        pygame.display.flip()
        clock.tick(FPS)

# Initialize planets and the Sun
sun = CelestialBody("Sun", YELLOW, 30, 0, 1.989e30, None)
earth = CelestialBody("Earth", BLUE, 10, 1, 5.97e24, 365.25, diameter=12742, surface_gravity=1, atmosphere="78% Nitrogen, 21% Oxygen", num_moons=1, avg_temp_day=15, avg_temp_night=-18)
mars = CelestialBody("Mars", RED, 8, 1.5, 6.39e23, 687, diameter=6779, surface_gravity=0.38, atmosphere="95% Carbon Dioxide", num_moons=2, avg_temp_day=-20, avg_temp_night=-70)
mercury = CelestialBody("Mercury", LIGHT_GRAY, 5, 0.39, 3.30e23, 88, diameter=4879, surface_gravity=0.38, atmosphere="Thin, trace amounts", num_moons=0, avg_temp_day=430, avg_temp_night=-180)
venus = CelestialBody("Venus", ORANGE, 9, 0.72, 4.87e24, 225, diameter=12104, surface_gravity=0.9, atmosphere="96.5% Carbon Dioxide", num_moons=0, avg_temp_day=460, avg_temp_night=460)

# Initialize Moons
moon = Moon("Moon", LIGHT_GRAY, 3, 0.08257, 7.35e22, 10, earth)
deimos = Moon("Deimos", LIGHT_GRAY, 3, 0.08257, 7.35e22, 10, mars)
phobos = Moon("Phobos", LIGHT_GRAY, 3, 0.16257, 7.35e22, 9, mars)
simulate_solar_system([sun, mercury, venus, earth, mars], [moon, deimos, phobos])
