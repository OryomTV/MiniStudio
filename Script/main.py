import pygame

pygame.init()

screen_width = 800
screen_height = 600

grid_size = 20
grid_width = screen_width/grid_size
grid_height = screen_height/grid_size

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
JUMP = (0, -5)

class Square:
    def __init__(self):
        self.position = [screen_width // 2, screen_height - grid_size]
        self.direction = RIGHT
        self.jumping = False
        self.jump_count = 10

    def turn(self, point):
        self.direction = point

    def move(self):
        current = self.position
        x, y = self.direction
        new = [current[0] + x * grid_size, current[1]]
        self.position = new

        if self.jumping:
            self.jump()

    def draw(self, surface):
        r = pygame.Rect(self.position, (grid_size,grid_size))
        pygame.draw.rect(surface, (0,255,0), r)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    self.jumping = True
                if event.key == pygame.K_d:
                    self.turn(RIGHT)
                if event.key == pygame.K_q:
                    self.turn(LEFT)

    def jump(self):
        if self.jump_count >= -10:
            neg = 1
            if self.jump_count < 0:
                neg = -1
            y_movement = (self.jump_count ** 2) * 0.5 * neg
            new_position = [self.position[0], self.position[1] - y_movement]
            self.position = new_position
            self.jump_count -= 1
        else:
            self.jump_count = 10
            self.jumping = False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jumping Square")

def main():
    clock = pygame.time.Clock()

    square = Square()

    while True:
        screen.fill((255,255,255))
        square.handle_keys()
        square.move()
        square.draw(screen)

        pygame.display.update()

        clock.tick(30)

if __name__ == "__main__":
    main()
