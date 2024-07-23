
import pygame
import math

WIDTH, HEIGHT = 1650, 1000
GREY = (100, 100, 100)  # Orbit path color

class CelestialBody:
    def __init__(self, name, color, radius, distance_from_sun_au, mass, orbital_period=None, diameter=None, surface_gravity=None, atmosphere=None, num_moons=None, avg_temp_day=None, avg_temp_night=None):
        self.name = name
        self.color = color
        self.radius = radius
        self.mass = mass
        self.orbital_period = orbital_period
        self.diameter = diameter
        self.surface_gravity = surface_gravity
        self.atmosphere = atmosphere
        self.num_moons = num_moons
        self.avg_temp_day = avg_temp_day
        self.avg_temp_night = avg_temp_night
        self.angle = 0  # Starting angle
        self.laps = 0  # Tracks the number of complete orbits
        self.distance_from_sun = distance_from_sun_au * 200  # Conversion from AU to pixels
        if name == "Jupiter":
            self.distance_from_sun = distance_from_sun_au * 90
        elif name == "Saturn":
            self.distance_from_sun = distance_from_sun_au * 65
        elif name == "Uranus":
            self.distance_from_sun = distance_from_sun_au * 45
        elif name == "Neptune":
            self.distance_from_sun = distance_from_sun_au * 35

        # Initialize position centered in the window
        self.x = WIDTH / 2 + self.distance_from_sun * math.cos(math.radians(self.angle))
        self.y = HEIGHT / 2 + self.distance_from_sun * math.sin(math.radians(self.angle))

    def update_position(self, delta_time):
        if self.orbital_period is not None:
            previous_angle = self.angle
            self.angle += (360 / self.orbital_period) * delta_time
            self.angle = self.angle % 360
            if self.angle < previous_angle:  # This implies a wrap-around, hence a complete orbit
                self.laps += 1
            self.x = WIDTH / 2 + self.distance_from_sun * math.cos(math.radians(self.angle))
            self.y = HEIGHT / 2 + self.distance_from_sun * math.sin(math.radians(self.angle))

    def draw(self, surface, zoom_factor):
        pygame.draw.circle(surface, self.color, (int(WIDTH // 2 + (self.x - WIDTH // 2) * zoom_factor), int(HEIGHT // 2 + (self.y - HEIGHT // 2) * zoom_factor)), int(self.radius * zoom_factor))

    def check_hover(self, mouse_x, mouse_y, zoom_factor):
        distance = math.sqrt(((mouse_x - WIDTH // 2) / zoom_factor + WIDTH // 2 - self.x) ** 2 + ((mouse_y - HEIGHT // 2) / zoom_factor + HEIGHT // 2 - self.y) ** 2)
        return distance <= self.radius * zoom_factor

    def get_info(self):
        if self.orbital_period is not None:
            details = (
                f"Planet {self.name}\n"
                f"Mass: {self.mass:.2e} kg\n"
                f"Orbit: {self.distance_from_sun / 250:.2f} AU\n"
                f"Orbital Period: {self.orbital_period:.2f} days\n"
                f"Diameter: {self.diameter} km\n"
                f"Surface Gravity: {self.surface_gravity} g\n"
                f"Atmosphere: {self.atmosphere}\n"
                f"Number of Moons: {self.num_moons}\n"
                f"Average Temp (Day): {self.avg_temp_day} °C\n"
                f"Average Temp (Night): {self.avg_temp_night} °C\n"
            )
            return details
        else:
            return f"{self.name}: Mass: {self.mass:.2e} kg"

class Moon(CelestialBody):
    def __init__(self, name, color, radius, distance_from_parent_au, mass, orbital_period, parent):
        super().__init__(name, color, radius, distance_from_parent_au, mass, orbital_period)
        self.parent = parent

    def update_position(self, delta_time):
        if self.orbital_period is not None:
            previous_angle = self.angle
            self.angle += (360 / self.orbital_period) * delta_time
            self.angle = self.angle % 360
            if self.angle < previous_angle:  # This implies a wrap-around, hence a complete orbit
                self.laps += 1
            self.x = self.parent.x + self.distance_from_sun * math.cos(math.radians(self.angle))
            self.y = self.parent.y + self.distance_from_sun * math.sin(math.radians(self.angle))

    def draw_orbit(self, surface, zoom_factor):
        pygame.draw.circle(surface, GREY, (int(WIDTH // 2 + (self.parent.x - WIDTH // 2) * zoom_factor), int(HEIGHT // 2 + (self.parent.y - HEIGHT // 2) * zoom_factor)), int(self.distance_from_sun * zoom_factor), 1)

