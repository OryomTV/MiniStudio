import pygame

pygame.init()

screen_width = 800
screen_height = 600

grid_size = 20
grid_width = screen_width/grid_size
grid_height = screen_height/grid_size


fondEcranMenu = pygame.image.load("Image/moutagneBackgound.png")
fondEcranMenu = pygame.transform.scale(fondEcranMenu,(800,600))

UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.isPlaying = False
        self.length = 1
        self.position = [screen_width // 2, screen_height // 2]
        self.direction = RIGHT

    def turn(self, point):
        self.direction = point

    def update(self):
        pass

    def move(self):
        current = self.position
        x, y = self.direction
        new = (current[0] + x * grid_size), (current[1] + y * grid_size)
        self.position = new

    def draw(self, surface):
        r = pygame.Rect(self.position, (grid_size,grid_size))
        pygame.draw.rect(surface, (0,255,0), r)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                if event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                if event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                if event.key == pygame.K_LEFT:
                    self.turn(LEFT)




screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake")


    clock = pygame.time.Clock()

    snake = Snake()

    while True:

        if snake.isPlaying:
            #Le code principal ici 
            screen.fill((255,255,255))
            snake.handle_keys()
            snake.move()
            snake.draw(screen)

        else:
            #Ecran principal
            screen.blit(fondEcranMenu,(0,0))

        pygame.display.update()

        clock.tick(10)

if __name__ == "__main__":
    main()