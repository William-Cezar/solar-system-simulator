import pygame
import math

WIDTH, HEIGHT = 1650, 1000
GREY = (100, 100, 100)

import pygame
import math

WIDTH, HEIGHT = 1650, 1000

class CelestialBody:
    def __init__(self, name, color, radius, distance_from_sun_au, mass, orbital_period=None, diameter=None, surface_gravity=None, atmosphere=None, num_moons=None, avg_temp_day=None, avg_temp_night=None):
        """
        Initialize a CelestialBody instance.

        Args:
            name (str): Name of the celestial body.
            color (tuple): Color representation (RGB) of the celestial body.
            radius (int): Radius of the celestial body.
            distance_from_sun_au (float): Distance from the Sun in astronomical units (AU).
            mass (float): Mass of the celestial body in kilograms.
            orbital_period (float, optional): Orbital period in Earth days. Defaults to None.
            diameter (int, optional): Diameter of the celestial body in kilometers. Defaults to None.
            surface_gravity (float, optional): Surface gravity relative to Earth. Defaults to None.
            atmosphere (str, optional): Description of the atmosphere. Defaults to None.
            num_moons (int, optional): Number of moons orbiting the celestial body. Defaults to None.
            avg_temp_day (int, optional): Average daytime temperature in Celsius. Defaults to None.
            avg_temp_night (int, optional): Average nighttime temperature in Celsius. Defaults to None.
        """       
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
        self.angle = 0
        self.laps = 0
        self.distance_from_sun = distance_from_sun_au * 250  # Conversion from AU to pixels

        # Initialize position centered in the window
        self.x = WIDTH / 2 + self.distance_from_sun * math.cos(math.radians(self.angle))
        self.y = HEIGHT / 2 + self.distance_from_sun * math.sin(math.radians(self.angle))

    def update_position(self, delta_time):
        """
        Update the position of the celestial body based on its orbital period.

        Args:
            delta_time (float): Time elapsed since the last update in seconds.
        """
        if self.orbital_period is not None:
            previous_angle = self.angle
            self.angle += (360 / self.orbital_period) * delta_time
            self.angle = self.angle % 360
            if self.angle < previous_angle:
                self.laps += 1
            self.x = WIDTH / 2 + self.distance_from_sun * math.cos(math.radians(self.angle))
            self.y = HEIGHT / 2 + self.distance_from_sun * math.sin(math.radians(self.angle))

    def draw(self, surface):
        """
        Draw the celestial body on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the celestial body on.
        """       
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def check_hover(self, mouse_x, mouse_y):
        """
        Check if the mouse is hovering over the celestial body.

        Args:
            mouse_x (int): X-coordinate of the mouse.
            mouse_y (int): Y-coordinate of the mouse.

        Returns:
            bool: True if the mouse is hovering over the celestial body, False otherwise.
        """      
        distance = math.sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        return distance <= self.radius

    def get_info(self):
        """
        Get detailed information about the celestial body.

        Returns:
            str: A string containing detailed information about the celestial body.
        """       
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
            details = (
                f"Star {self.name}\n"
                f"Star Type G-type main-sequence star (G2V)\n"
                f"Mass: {self.mass:.2e} kg\n"
                f"Diameter: 1.392 million km\n"
                f"Surface Temperature: Approximately 5,500 °C\n"
                f"Age: Around 4.6 billion years\n"
            )
            return details


class Moon:
    def __init__(self, name, color, radius, distance_from_parent_au, mass, orbital_period, parent):
        self.name = name
        self.color = color
        self.radius = radius
        self.mass = mass
        self.orbital_period = orbital_period
        self.parent = parent
        self.angle = 0
        self.laps = 0
        self.distance_from_parent = distance_from_parent_au * 250  # Conversion from AU to pixels

        # Initialize position centered on the parent
        self.update_position(0)

    def update_position(self, delta_time):
        if self.orbital_period is not None:
            previous_angle = self.angle
            self.angle += (360 / self.orbital_period) * delta_time
            self.angle = self.angle % 360
            if self.angle < previous_angle:
                self.laps += 1
            self.x = self.parent.x + self.distance_from_parent * math.cos(math.radians(self.angle))
            self.y = self.parent.y + self.distance_from_parent * math.sin(math.radians(self.angle))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def draw_orbit(self, surface):
        pygame.draw.circle(surface, GREY, (int(self.parent.x), int(self.parent.y)), int(self.distance_from_parent), 1)
