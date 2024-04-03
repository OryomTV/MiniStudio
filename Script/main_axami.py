import pygame
import math 
pygame.init()

screen_width = 800
screen_height = 600

grid_size = 20
grid_width = screen_width/grid_size
grid_height = screen_height/grid_size

#Importer le background 
fondEcranMenu = pygame.image.load("Image/moutagneBackgound.png")
fondEcranMenu = pygame.transform.scale(fondEcranMenu,(screen_width,screen_height))



#Importer l'image play du boutton
play_button = pygame.image.load("Image/bouttonMenu.png")
play_button = pygame.transform.scale(play_button,(360,180))
play_button_rect = play_button.get_rect()
play_button_rect.x =  math.ceil(screen_width / 4)
play_button_rect.y =  math.ceil(screen_width / 3)

#Importer l'image du boutton quit
quit_button = pygame.image.load("Image/bouttonQuitMenu.png")
quit_button = pygame.transform.scale(quit_button,(200,200))
quit_button_rect = quit_button.get_rect()
quit_button_rect.x =  math.ceil(screen_width / 4)
quit_button_rect.y =  math.ceil(screen_width / 2)




# Création de la surface pour le menu pause 

pause_rectangle = pygame.Surface((200, 100), pygame.SRCALPHA)
pause_rectangle.fill((0,0,255))

opacite = 128  
pause_rectangle.set_alpha(opacite)



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
        self.pause = False

    def turn(self, point):
        self.direction = point

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
                if event.key == pygame.K_z:
                    self.pause = True    




screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

def main():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake")


    clock = pygame.time.Clock()

    snake = Snake()

    while True:

        if snake.isPlaying and not snake.pause:
            #Le code principal ici 
            screen.fill((255,255,255))
            snake.handle_keys()
            snake.move()
            snake.draw(screen)

        elif snake.pause:            
            #Menu pause
            screen.fill((255,255,255))
            snake.draw(screen)
            screen.blit(pause_rectangle, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        snake.pause = False
        else:
            #Ecran principal
            screen.blit(fondEcranMenu,(0,0))
            screen.blit(play_button,play_button_rect)
            screen.blit(quit_button,quit_button_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if play_button_rect.collidepoint(event.pos):
                        snake.isPlaying = True
                    elif quit_button_rect.collidepoint(event.pos):
                        pygame.quit()

                elif event.type == pygame.QUIT:
                    pygame.quit()


                        

        pygame.display.update()

        clock.tick(10)

if __name__ == "__main__":
    main()