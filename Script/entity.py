import pygame
from random import randint
from Constants import *


class Entity(pygame.sprite.Sprite):

    def __init__(self, pos, game):
        super().__init__()
        self.game = game

        self.position = list(pos)
        self.velocity = (2, 0)

        self.old_position = self.position.copy()

        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

    def move_right(self):
        self.position[0] += self.velocity[0]
        if self.check_collisions(self.game.all_grounds):
            self.position[0] -= self.velocity[0]
        self.image = pygame.transform.flip(self.original_image, False, False)


    def move_left(self):
        self.position[0] -= self.velocity[0]
        if self.check_collisions(self.game.all_grounds):
            self.position[0] += self.velocity
        self.image = pygame.transform.flip(self.original_image, True, False)


    def update_entity(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        self.position[0] += frame_movement[0]
        entity_rect = self.rect
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.position[0] = entity_rect.x
        
        self.position[1] += frame_movement[1]
        entity_rect = self.rect
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.velocity[1] = 0
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                    self.velocity[1] = 0
                self.position[1] = entity_rect.y
        
        self.velocity = (self.velocity[0], min(5, self.velocity[1] + 0.1))
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity = (self.velocity[0], 0)

    def render(self, surf):
        surf.blit(self.image, self.position)

class Player(Entity):

    def __init__(self, game, pos, width, height):
        super().__init__(pos, game)

        # Information about player
        self.var_anim = 0
        self.original_image = pygame.image.load(WALK_ANIM_PATHS[self.var_anim]).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.original_image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect(midbottom=self.position)
        self.bigger_rect = self.rect.copy()
        self.bigger_rect.inflate_ip(30, 30)


        #Jump
        self.jump_force = -500
        self.velocity = [500, 0]
        self.doubleSaut = True
        self.time_since_last_jump = 0.0
        self.cooldown_jump_time = 0.3

        #Dash
        self.time_since_last_dash = 0.0 
        self.dash_dispo = True
        self.air_resistance = 2
        self.dash_velocity = 0
        self.cooldown_dash_time = 2.0
        self.onDash = True

        self.facingRight = True
        self.movement = 0


        self.relevant_anim = ""
        self.relevant_anim_frame_count = 0
        self.current_anim_frame = 0
        self.anims = {
            "Walking": LoadAnimFolder(WALK_ANIM_PATHS, (width, height)),
            "Idle": [pygame.transform.scale(pygame.image.load(WALK_ANIM_PATHS[0]), (width, height))],
            "Jumping": [pygame.transform.scale(pygame.image.load("Assets\Entities\Llursen-Saut-1.png"), (width, height))],
            "Falling": [pygame.transform.scale(pygame.image.load("Assets\Entities\Llursen-Saut-2.png"), (width, height))]
        }

    def get_relevant_anim(self):
        if not self.collisions["down"]:
            if self.velocity[1] > 50:
                return "Falling"
            elif self.velocity[1] < 0:
                return "Jumping"

        if self.movement != 0:
            print("returned Walking")
            return "Walking"
        else:
            return "Idle"

    def UpdateSprite(self):

        self.current_anim_frame += .08

        relevant_anim = self.get_relevant_anim()
        if self.relevant_anim != relevant_anim: # new animation
            # self.current_anim_frame = 0 # start this anim from 0
            self.relevant_anim = relevant_anim
            self.relevant_anim_frame_count = len(self.anims[relevant_anim])

        raw_unflipped_sprite = self.anims[relevant_anim][int(self.current_anim_frame) % self.relevant_anim_frame_count]
        return pygame.transform.flip(raw_unflipped_sprite, not self.facingRight, False)

    def check_collisions(self, group):
        for other_sprite in group:
            if self != other_sprite and pygame.sprite.collide_rect(self, other_sprite):
                return True
        return False

    def draw(self, surface):
        # Load image
        # surf = pygame.Surface((self.rect.width, self.rect.height))
        # surf.fill((255, 0, 0))
        # surface.blit(surf, self.rect)
        surface.blit(self.image, self.rect)
        # surface.blit(pygame.transform.flip(self.image, not self.facingRight, False), self.rect)
        
    def Update(self, tilemap, movement, should_jump, should_dash, dash_direction, delta_time, plateformes):
        self.rect.midbottom = self.position
        # self.bigger_rect.center = self.rect.center
        self.ApplyGravity(tilemap,delta_time)
        if should_jump:
            self.TryToJump()
        else:
            if self.velocity[1] < 0:
                self.velocity = self.velocity[0], self.velocity[1] * .9
        self.move_player(tilemap, movement, delta_time, plateformes)
        self.time_since_last_jump += delta_time
        self.time_since_last_dash += delta_time

        if self.collisions["down"] and self.time_since_last_dash >= self.cooldown_dash_time:
            self.dash_dispo = True

        if should_dash and self.dash_dispo:
            self.TryToDash(dash_direction)
            self.dash_dispo = False

        self.image = self.UpdateSprite()
        
    def TryToJump(self):
        if self.collisions["down"]:
            self.velocity = (self.velocity[0], self.jump_force)
            self.doubleSaut = True
            self.time_since_last_jump = 0.0
        elif self.doubleSaut and self.time_since_last_jump >= self.cooldown_jump_time: 
            self.velocity = (self.velocity[0], self.jump_force)
            self.doubleSaut = False
        
    def TryToDash(self, mouvement):
        if  not mouvement:
            self.dash_velocity = 30 
        else:
            self.dash_velocity = -30
        self.time_since_last_dash = 0.0 
        self.dash_dispo = False     

    def ApplyGravity(self, tilemap, delta_time):
        self.velocity = (self.velocity[0], self.velocity[1] + GRAVITY * delta_time)
        
        if self.dash_velocity != 0:
            self.onDash = True
            collision_detected = False
            for rect in tilemap.physics_rects_around(self.rect.midbottom):
                if rect.collidepoint(self.rect.x, self.rect.y):
                    collision_detected = True
                    self.dash_velocity = 0
                    break

            if not collision_detected:
                self.rect.x += self.dash_velocity
                if self.dash_velocity > 0 :
                    self.dash_velocity -= self.air_resistance
                    self.image = self.original_image
                elif self.dash_velocity < 0 :
                    self.dash_velocity += self.air_resistance
                    self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.onDash = False
        
    def move_player(self, tilemap, movement, delta_time, plateformes):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        if movement > 0:
            self.facingRight = True
        elif movement < 0:
            self.facingRight = False

        self.movement = movement

        frame_movement = (movement * self.velocity[0],  self.velocity[1]) # movement[1] + 
        
        self.rect.x += frame_movement[0] * delta_time
        entity_rect = self.rect
        for rect in tilemap.physics_rects_around(self.rect.midbottom) + plateformes:
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
        
        self.rect.y += frame_movement[1] * delta_time
        entity_rect = self.rect
        for rect in tilemap.physics_rects_around(self.rect.midbottom) + plateformes:
            if entity_rect.colliderect(rect):
            #     if hasattr(rect, "childingMethod"):
                    # rect.childingMethod(self)
                self.velocity = (self.velocity[0], 0)
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
        
        self.position = self.rect.midbottom
        # self.velocity = (self.velocity[0], min(5, self.velocity[1] + 0.1))


class Enemy(Entity):

    def __init__(self, game, pos, image_path, width, height,  type, direction, max_distance):
        super().__init__(pos, game)

        # Information about enemy
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.original_image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.distance_moved = 0
        self.direction_X = direction[0]
        self.direction_Y = direction[1]
        self.max_distance = max_distance
        self.type = type
        self.animation = 0
        self.Alive = True

    def move(self, speed):
        if self.type == "Tatoo":
            self.rect.x += speed * self.direction_X

            if self.max_distance is not None:
                self.distance_moved += speed

            if self.max_distance is not None and self.distance_moved >= self.max_distance:
                self.direction_X *= -1
                self.distance_moved = 0 - self.distance_moved

        elif self.type == "Bat":
            speed *= 2
            self.rect.x += speed * self.direction_X
            self.rect.y += speed * self.direction_Y

            if randint(1, 100) <= 5:
                self.direction_X *= -1

            if randint(1, 100) <= 2:
                self.direction_Y *= -1

        if self.direction_X > 0:
            # If moving up, flip the image vertically
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            # Otherwise, keep the original image
            self.image = self.original_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
