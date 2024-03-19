import pygame
import numpy as np

# Define the function
def f(x, y):
    return x**2 + y**2

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 600, 600
RESOLUTION = 100

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Compute the function values
x_values = np.linspace(-2, 2, RESOLUTION)
y_values = np.linspace(-2, 2, RESOLUTION)
z_values = np.array([[f(x, y) for x in x_values] for y in y_values])

# Define the Marching Squares algorithm
def marching_squares(x, y, z):
    contours = []
    for i in range(len(x)-1):
        for j in range(len(y)-1):
            square = [(i, j, z[j][i]), (i+1, j, z[j][i+1]), (i+1, j+1, z[j+1][i+1]), (i, j+1, z[j+1][i])]
            square = sorted(square, key=lambda v: v[2])
            if square[1][2] > 0:
                contours.append(((square[0][0]+square[1][0])/2, (square[0][1]+square[1][1])/2))
            if square[2][2] > 0:
                contours.append(((square[2][0]+square[3][0])/2, (square[2][1]+square[3][1])/2))
    return contours

# Compute the contours
contours = marching_squares(x_values, y_values, z_values)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the contour lines
    for i in range(0, len(contours), 2):
        pygame.draw.line(screen, (255, 0, 0), (WIDTH*contours[i][0]/RESOLUTION, HEIGHT*contours[i][1]/RESOLUTION), (WIDTH*contours[i+1][0]/RESOLUTION, HEIGHT*contours[i+1][1]/RESOLUTION))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
