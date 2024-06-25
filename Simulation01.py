import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
UAV_RADIUS = 10
TARGET_RADIUS = 10
OBSTACLE_RADIUS = 15
UAV_COLOR = (0, 0, 0)
TARGET_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (255, 0, 0)
BG_COLOR = (255, 255, 255)
NUM_UAVS = 6
NUM_OBSTACLES = 10
UAV_SPEED = 2.25
OBSTACLE_SPEED = 1.25
SIMULATION_TIME = 60  # Duration of the simulation in seconds

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('UAV Navigation Simulation')
clock = pygame.time.Clock()

# Utility Functions
def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def unit_vector(vec):
    norm = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
    return (vec[0] / norm, vec[1] / norm) if norm != 0 else (0, 0)

# Classes
class UAV:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y

    def move(self, uavs, obstacles):
        target_vec = (self.target_x - self.x, self.target_y - self.y)
        target_dir = unit_vector(target_vec)

        # Avoid obstacles
        for obstacle in obstacles:
            if distance((self.x, self.y), (obstacle.x, obstacle.y)) < OBSTACLE_RADIUS + UAV_RADIUS * 3:
                avoid_vec = (self.x - obstacle.x, self.y - obstacle.y)
                avoid_dir = unit_vector(avoid_vec)
                target_dir = (target_dir[0] + avoid_dir[0], target_dir[1] + avoid_dir[1])

        # Avoid other UAVs
        for uav in uavs:
            if uav != self and distance((self.x, self.y), (uav.x, uav.y)) < UAV_RADIUS * 2:
                avoid_vec = (self.x - uav.x, self.y - uav.y)
                avoid_dir = unit_vector(avoid_vec)
                target_dir = (target_dir[0] + avoid_dir[0], target_dir[1] + avoid_dir[1])

        target_dir = unit_vector(target_dir)
        self.x += target_dir[0] * UAV_SPEED
        self.y += target_dir[1] * UAV_SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, UAV_COLOR, (int(self.x), int(self.y)), UAV_RADIUS)
        pygame.draw.circle(screen, TARGET_COLOR, (int(self.target_x), int(self.target_y)), TARGET_RADIUS)

    def has_reached_target(self):
        return distance((self.x, self.y), (self.target_x, self.target_y)) < TARGET_RADIUS

class Obstacle:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy
        # Bounce off walls
        if self.x <= OBSTACLE_RADIUS or self.x >= WIDTH - OBSTACLE_RADIUS:
            self.dx = -self.dx
        if self.y <= OBSTACLE_RADIUS or self.y >= HEIGHT - OBSTACLE_RADIUS:
            self.dy = -self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, OBSTACLE_COLOR, (int(self.x), int(self.y)), OBSTACLE_RADIUS)

# Simulation setup
uavs = []
for _ in range(NUM_UAVS):
    x = random.randint(UAV_RADIUS, WIDTH // 3)  # Start from the left third of the screen
    y = random.randint(UAV_RADIUS, HEIGHT - UAV_RADIUS)
    target_x = random.randint(WIDTH * 2 // 3, WIDTH - TARGET_RADIUS)  # Target on the right third of the screen
    target_y = random.randint(TARGET_RADIUS, HEIGHT - TARGET_RADIUS)
    uavs.append(UAV(x, y, target_x, target_y))

obstacles = []
for _ in range(NUM_OBSTACLES):
    x = WIDTH // 2  # Start obstacles from the middle area horizontally
    y = random.randint(OBSTACLE_RADIUS, HEIGHT - OBSTACLE_RADIUS)
    dx = random.choice([-OBSTACLE_SPEED, OBSTACLE_SPEED])
    dy = random.choice([-OBSTACLE_SPEED, OBSTACLE_SPEED])
    obstacles.append(Obstacle(x, y, dx, dy))

# Simulation loop
start_time = pygame.time.get_ticks()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    for uav in uavs:
        uav.move(uavs, obstacles)
        uav.draw(screen)

    for obstacle in obstacles:
        obstacle.move()
        obstacle.draw(screen)

    pygame.display.flip()
    clock.tick(30)

    # Check if all UAVs have reached their targets
    if all(uav.has_reached_target() for uav in uavs):
        print("All UAVs have reached their targets.")
        running = False

    # Check if simulation time has elapsed
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    if elapsed_time >= SIMULATION_TIME:
        print("Simulation time has elapsed.")
        running = False

pygame.quit()
