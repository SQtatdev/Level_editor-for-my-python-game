import pygame


class Button():
    def __init__(self, image, scale = 1):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rectangle = self.image.get_rect()
        self.is_clicked = False

        

    def draw(self, surface, xy):
        self.rectangle.topleft = xy
        surface.blit(self.image, (self.rectangle.x, self.rectangle.y))

    def clicked(self):
        action = False

        cursor_position = pygame.mouse.get_pos()

        if self.rectangle.collidepoint(cursor_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.is_clicked == False:
                self.is_clicked = action = True

        if pygame.mouse.get_pressed()[0] ==0:
            self.is_clicked = False

        return action
    