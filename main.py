import pygame
import sys
from models import CelestialBody, Moon
from datetime import datetime

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
BEIGE = (245, 245, 220)  # Beige for Jupiter
GOLD = (255, 215, 0)    # Gold for Saturn
CYAN = (0, 255, 255)    # Cyan for Uranus
DEEP_BLUE = (0, 0, 139) # Deep Blue for Neptune


def simulate_solar_system(planets, moons):
    simulation_start_time = pygame.time.get_ticks()  # Get the start time of the simulation
    speed_multiplier = 1
    selected_planet = None

    zoom_factor = 1.0  # Initialize zoom factor
    running = True

    while running:
        current_time = pygame.time.get_ticks()
        total_seconds_elapsed = (current_time - simulation_start_time) / 1000.0  # Total seconds since start

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    speed_multiplier += 0.1  # Increase speed
                elif event.key == pygame.K_DOWN:
                    speed_multiplier -= 0.1  # Decrease speed
                elif event.key == pygame.K_SPACE:
                    speed_multiplier = 1.0  # Reset speed to normal
                elif event.key == pygame.K_EQUALS:  # '+' key for zoom in
                    zoom_factor += 0.1
                elif event.key == pygame.K_MINUS:  # '-' key for zoom out
                    zoom_factor -= 0.1
                    if zoom_factor < 0.1:  # Prevent zooming out too much
                        zoom_factor = 0.1
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for planet in planets:
                    if planet.check_hover(mouse_x, mouse_y, zoom_factor):
                        selected_planet = planet
        screen.fill((0, 0, 0))  # Clear screen

        # Draw orbits for planets
        for planet in planets[1:]:  # Skip the sun for orbit drawing
            pygame.draw.circle(screen, GREY, (WIDTH // 2, HEIGHT // 2), int(planet.distance_from_sun * zoom_factor), 1)

        # Draw orbits for moons
        for moon in moons:
            moon.draw_orbit(screen, zoom_factor)

        # Update and draw each planet
        for planet in planets:
            planet.update_position(clock.get_time() / 1000.0 * speed_multiplier)
            planet.draw(screen, zoom_factor)

        # Update and draw each moon
        for moon in moons:
            moon.update_position(clock.get_time() / 1000.0 * speed_multiplier)
            moon.draw(screen, zoom_factor)

        # Position for elapsed time and laps display
        for index, planet in enumerate(planets):
            if planet.orbital_period is not None:
                lap_info = f"{planet.name}: {planet.laps} Laps, Time: {total_seconds_elapsed:.2f} sec"
                lap_label = font.render(lap_info, True, WHITE)
                pygame.draw.circle(screen, planet.color, (10, 20 + index * 40), 5)  # Small circle
                screen.blit(lap_label, (30, 10 + index * 40)) 

        if selected_planet:
                    lines = selected_planet.get_info().split('\n')
                    for i, line in enumerate(lines):
                        info_surf = font.render(line, 1, WHITE)
                        screen.blit(info_surf, (WIDTH - info_surf.get_width() - 10, 10 + i * 30))
        pygame.display.flip()
        clock.tick(FPS)  # Maintain the frame rate

# Initialize planets and the Sun
sun = CelestialBody("Sun", YELLOW, 45, 0, 1.989e30, None)
earth = CelestialBody("Earth", BLUE, 10, 1, 5.97e24, 365.25, diameter=12742, surface_gravity=1, atmosphere="78% Nitrogen, 21% Oxygen", num_moons=1, avg_temp_day=15, avg_temp_night=-18)
mars = CelestialBody("Mars", RED, 8, 1.5, 6.39e23, 687, diameter=6779, surface_gravity=0.38, atmosphere="95% Carbon Dioxide", num_moons=2, avg_temp_day=-20, avg_temp_night=-70)
mercury = CelestialBody("Mercury", LIGHT_GRAY, 5, 0.39, 3.30e23, 88, diameter=4879, surface_gravity=0.38, atmosphere="Thin, trace amounts", num_moons=0, avg_temp_day=430, avg_temp_night=-180)
venus = CelestialBody("Venus", ORANGE, 9, 0.72, 4.87e24, 225, diameter=12104, surface_gravity=0.9, atmosphere="96.5% Carbon Dioxide", num_moons=0, avg_temp_day=460, avg_temp_night=460)
jupiter = CelestialBody("Jupiter", BEIGE, 16, 5.2, 1.898e27, 4331, diameter=139820, surface_gravity=2.53, atmosphere="90% Hydrogen, 10% Helium", num_moons=79, avg_temp_day=-108, avg_temp_night=-108)
saturn = CelestialBody("Saturn", GOLD, 13.5, 9.58, 5.68e26, 10759, diameter=116460, surface_gravity=1.07, atmosphere="96% Hydrogen, 3% Helium", num_moons=83, avg_temp_day=-139, avg_temp_night=-139)
uranus = CelestialBody("Uranus", CYAN, 12, 19.22, 8.68e25, 30687, diameter=50724, surface_gravity=0.89, atmosphere="82.5% Hydrogen, 15.2% Helium", num_moons=27, avg_temp_day=-195, avg_temp_night=-195)
neptune = CelestialBody("Neptune", DEEP_BLUE, 11.5, 30.05, 1.02e26, 60190, diameter=49244, surface_gravity=1.14, atmosphere="80% Hydrogen, 19% Helium", num_moons=14, avg_temp_day=-201, avg_temp_night=-201)


# Initialize Moons
moon = Moon("Moon", LIGHT_GRAY, 3, 0.08257, 7.35e22, 10, earth)
deimos = Moon("Deimos", LIGHT_GRAY, 3, 0.08257, 7.35e22, 10, mars)
phobos = Moon("Phobos", LIGHT_GRAY, 3, 0.16257, 7.35e22, 9, mars)
callisto = Moon("Callisto", LIGHT_GRAY, 3, 0.1257, 7.35e22, 9.2, jupiter)
amalthea = Moon("Amalthea", LIGHT_GRAY, 3, 0.16, 7.35e22, 8.5, jupiter)
europa = Moon("Europa", LIGHT_GRAY, 3, 0.21, 7.35e22, 8.32, jupiter)
io = Moon("Io", LIGHT_GRAY, 3, 0.24, 7.35e22, 8.1, jupiter)
ganymede = Moon("Ganymede", LIGHT_GRAY, 3, 0.27, 7.35e22, 7.8, jupiter)

simulate_solar_system([sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune ], [moon, deimos, phobos, callisto, amalthea, europa, io, ganymede])
