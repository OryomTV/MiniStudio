import pygame
import math



from player import Player
from player import Enemy
from player import Boss
from ground import Ground
from collectible import Collectible

class Game:

    def __init__(self):

        # Create window of the game
        pygame.display.set_caption("Shining")
        self.screen = pygame.display.set_mode((1920, 1080))
        self.background = pygame.image.load("Asset/Untitled_Artwork.jpg")
        self.rect = self.background.get_rect()

        # Load button for launch the game
        self.play = pygame.image.load("Asset/bouton_jouer.png")
        self.play = pygame.transform.scale(self.play, (400, 160))
        self.play_rect = self.play.get_rect()
        self.play_rect.x = math.ceil(self.screen.get_width() / 2.5)
        self.play_rect.y = math.ceil(self.screen.get_height() / 2)

        # Load button for option 
        self.parametre = pygame.image.load("Asset/bouton_parametres.png")
        self.parametre = pygame.transform.scale(self.parametre, (380, 111))
        self.parametre_rect = self.parametre.get_rect()
        self.parametre_rect.x = math.ceil(self.screen.get_width() / 2.46)
        self.parametre_rect.y = math.ceil(self.screen.get_height() / 1.45)


        # Load button for quit the game
        self.quit = pygame.image.load("Asset/bouton_quitter.png")
        self.quit = pygame.transform.scale(self.quit, (300, 100))
        self.quit_rect = self.quit.get_rect()
        self.quit_rect.x = math.ceil(self.screen.get_width() / 2.37)
        self.quit_rect.y = math.ceil(self.screen.get_height() / 1.2)

        # Define if the game has started or not
        self.is_playing = False

        # Generate player
        self.player = Player(100, 500, "Asset/Llusern.png", 200, 160, self)
        self.enemy = Enemy(900, 450, "Asset/Pangolin.png", 150, 200, self)
        self.ground = Ground(0, 900, 1920, 180, (0, 0, 0))

        # Generate different groups
        self.all_player = pygame.sprite.Group()
        self.all_player.add(self.player)

        self.all_enemies = pygame.sprite.Group()
        self.all_enemies.add(self.enemy)

        self.all_grounds = pygame.sprite.Group()
        self.all_grounds.add(self.ground)

        # Gravity
        self.gravity = 0.5

        # Velocity jump
        self.jump_velocity = -15
        self.vertical_velocity = 0

        self.delta_time = 0.0

        #DoubleSaut
        self.toucheRelacherSaut = False
        self.doubleSaut = False
        self.isGrounded = True
        self.time_since_last_jump = 0.0 
        self.cooldown_jump_time = 0.5

        #Dash
        self.cooldown_dash_time = 2
        self.time_since_last_dash = 0.0
        self.dash_dispo = True
        self.dash_time = 0.5
        self.dash_velocity = 0
        self.air_resistance = 1

        self.pressed = {}

    def start(self):
        self.is_playing = True

    def update(self):
        # Application of my player image
        self.screen.blit(self.player.image, self.player.rect)

        # Application of the monster image
        for enemy in self.all_enemies:
            self.screen.blit(enemy.image, enemy.rect)

        # Application of the set of images of my monsters group
        self.all_enemies.draw(self.screen)

        # Application of the set of images of my grounds group
        self.all_grounds.draw(self.screen)

        #Verifie en permanenece si le joueur est au sol ou pas
        if self.player.position[1] >= self.ground.rect.y - self.player.rect.height:
            self.isGrounded = True
            self.toucheRelacherSaut = False
            self.doubleSaut = False
        else:
            self.isGrounded = False
        
        #dash dispo apres que le cooldown soit fini et qu'il soit au sol (isGrounded)
        if self.time_since_last_dash >= self.cooldown_dash_time and self.isGrounded:
            self.dash_dispo = True

    def apply_gravity(self):
        if self.player.position[1] < self.ground.rect.y - self.player.rect.height:
            self.vertical_velocity += self.gravity
            self.player.position[1] += self.vertical_velocity
        else:
            self.vertical_velocity = 0
            self.player.position[1] = self.ground.rect.y - self.player.rect.height

        if self.dash_velocity != 0:
            self.player.position[0] += self.dash_velocity

            if self.dash_velocity > 0 :
                self.dash_velocity -= self.air_resistance
            elif self.dash_velocity < 0 :
                self.dash_velocity += self.air_resistance

    def handle_input(self):
        self.pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.toucheRelacherSaut = True

        if self.pressed[pygame.K_q] and self.player.rect.x > 0:
            self.player.move_left()
            self.jump()
            self.dash("G")

        elif self.pressed[pygame.K_d] and self.player.rect.x + self.player.rect.width < self.screen.get_width():
            self.player.move_right()
            self.jump()
            self.dash("D")

        if self.pressed[pygame.K_SPACE]:  # Oui ces dégeu me demande pas pk si tu fais que un seul appel de jump ya pas 
            self.jump() # de double saut avec le neutral jump (sans imput q et d ), suprime la condition et l'instruction a l'interieur pour essayer
        self.jump()


    def jump(self):
        if  self.pressed[pygame.K_SPACE] and self.isGrounded:
            self.vertical_velocity = self.jump_velocity
            self.player.position[1] += self.jump_velocity
            self.doubleSaut = True
            self.time_since_last_jump = 0.0 

        elif self.pressed[pygame.K_SPACE] and self.doubleSaut and self.time_since_last_jump >= self.cooldown_jump_time:
            self.vertical_velocity = self.jump_velocity
            self.player.position[1] += self.jump_velocity
            self.doubleSaut = False
        else:
            self.time_since_last_jump += self.delta_time
    
    def dash(self,direction):
        if self.pressed[pygame.K_LSHIFT] and self.dash_dispo and direction != None:
            if direction == "G":
                self.dash_velocity = -30
            else: 
                self.dash_velocity = 30

            self.time_since_last_dash = 0.0 
            self.dash_dispo = False
        else:
            self.time_since_last_dash += self.delta_time


    def run(self):

        clock = pygame.time.Clock()

        fraise = Collectible("Asset/collectibleTest.png",1000,600)
        sephiroth = Boss(1000,0)

        # boucle du jeu
        running = True

        while running:

            self.player.update()
            self.screen.blit(self.background, (0, 0))

            # Check if game has started or not
            if self.is_playing:
                # Trigger game instructions
                self.update()

                
                if fraise.object_etat:
                    self.screen.blit(fraise.object_image, fraise.object_rect)
                    fraise.update(self.player.position[0],self.player.position[1])
                self.screen.blit(sephiroth.image, sephiroth.rect)
                sephiroth.update(self.delta_time)

            else:
                # Add welcome screen
                self.screen.blit(self.play, self.play_rect)
                self.screen.blit(self.parametre, self.parametre_rect)
                self.screen.blit(self.quit, self.quit_rect)

            self.apply_gravity()
            self.handle_input()



            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if mouse collides with the play button
                    if self.play_rect.collidepoint(event.pos):
                        # Launch the game
                        self.start()

                    if self.quit_rect.collidepoint(event.pos):
                        running = False

            self.delta_time = clock.tick(120) / 1000.0

        pygame.quit()
