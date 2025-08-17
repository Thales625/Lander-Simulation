import numpy as np

from spline import SplineCubic

class Terrain:
    def from_file(filename="terrain.npz", scale=0.5):
        data = np.load(filename)
        return SplineCubic(scale*data["x"], scale*data["y"])
   
    def from_sine_wave(seed=1, n_harmonics=5):
        np.random.seed(seed)

        def f(x):
            v = 0
            for _ in range(n_harmonics):
                A = np.random.uniform(1., 1.05)     # height
                B = np.random.uniform(0.05, 0.5)    # frequency
                C = np.random.uniform(0.0, 2*np.pi) # phase
                v += A * (np.sin(B * x + C) + 1)
            return v

        f.min_x = 0
        f.max_x = 1000
        
        return f


if __name__ == "__main__":
    import pygame

    WIDTH, HEIGHT = 800, 600
    FPS = 30
    DX = 10

    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Draw terrain")
    clock = pygame.time.Clock()

    # store points
    terrain_points = []

    running = True
    drawing = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left button down
                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left button up
                    drawing = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == 13: # ENTER
                    # SAVE
                    running = False
                    break
                if event.key == 27 or event.key == 113: # ESC or Q
                    exit()

        if drawing:
            mx, my = pygame.mouse.get_pos()
            terrain_points.append((mx, my))

        screen.fill((0, 0, 0))
        if len(terrain_points) > 1:
            pygame.draw.lines(screen, (0, 255, 0), False, terrain_points, 2)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

    if not terrain_points:
        print("Empty points")
        exit()

    # sort points by x
    terrain_points = sorted(terrain_points, key=lambda p: p[0])
    points_x = [p[0] for p in terrain_points]
    points_y = [p[1] for p in terrain_points]

    # interpolate points
    x_min, x_max = min(points_x), max(points_x)
    x_uniform = np.arange(x_min, x_max, DX)
    y_uniform = np.interp(x_uniform, points_x, points_y)

    # save file
    np.savez("terrain.npz", x=x_uniform-np.min(x_uniform), y=y_uniform-np.min(y_uniform))

    print(f"Saved terrain with {len(x_uniform)} points!")