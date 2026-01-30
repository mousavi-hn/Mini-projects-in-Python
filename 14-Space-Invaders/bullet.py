import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to resemble a bullet fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet at the ship's current location"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet at (0,0) then correct its position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullet's position as a float
        self.y = float(self.rect.y)

    def update(self, ai_game):
        """Move the bullet up the screen"""
        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y
        # Getting rid of disappeared bullets
        for bullet in ai_game.bullets.copy():
            if bullet.rect.bottom <= 0:
                ai_game.bullets.remove(bullet)

        ai_game._check_bullet_alien_collisions()

    def draw_bullet(self):
        """Draw the bullet into the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)