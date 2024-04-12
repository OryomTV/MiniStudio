import pygame

GRAVITY = 850
WALK_ANIM_PATHS = ['Assets/Entities/Llursen-1.png', 'Assets/Entities/Llursen-2.png', "Assets/Entities/Llursen-3.png", "Assets/Entities/Llursen-4.png"]

def LoadAnimFolder(folder_as_list, optional_size_constraint = None):
   if optional_size_constraint is None:
        return [pygame.image.load(file) for file in folder_as_list]
   else:
        return [pygame.transform.scale(pygame.image.load(file), optional_size_constraint) for file in folder_as_list]