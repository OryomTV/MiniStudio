import pygame

class Collectible(pygame.sprite.Sprite):

    def __init__(self,cheminImage,posX,posY):
        # Coordonnée
        self.posX = posX
        self.posY = posY

        # Taille (actuellement il font tous la meme taille)
        self.object_width = 400
        self.object_height = 160

        # Creation du rectangle qui contient l'image 
        self.object_image = pygame.image.load(cheminImage)
        self.object_image = pygame.transform.scale(self.object_image, (self.object_width, self.object_height)) 
        self.object_rect = self.object_image.get_rect()
        self.object_rect.x = self.posX
        self.object_rect.y = self.posY

        # Etat du collectible 
        self.object_etat = True # True si l'object n'est pas recupérer 
        
    def update(self,posJoueurX,posJoueurY):
        if self.object_etat:
            if self.object_rect.collidepoint(posJoueurX, posJoueurY):
                self.object_etat = False
                print("Object recuperer")
                return True
        return False
    



