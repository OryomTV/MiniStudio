import os
import pygame

BASE_IMG_PATH = '../Assets/Tuto/'


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((255, 255, 255))
    return img


def load_images(path, size=(16, 16)):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        img = load_image(path + '/' + img_name)
        img = pygame.transform.scale(img, size)
        images.append(img)
    return images
