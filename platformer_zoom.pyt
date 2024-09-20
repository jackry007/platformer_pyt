import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.change_x = 0
        self.change_y = 0
        self.walls = None  # This will store the wall sprites
        self.is_sprinting = False

    def changespeed(self, x, y):
        """Change the speed of the player."""
        self.change_x = x
        self.change_y = y

    def update(self):
        """Update the player position."""
        self.rect.x += self.change_x

        # Check for horizontal collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        # Check for vertical collisions
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer with Zoom")

all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

# Adding some walls
wall = Wall(100, 100, 50, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(150, 200, 50, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(0, 0, SCREEN_WIDTH, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(0, 0, 10, SCREEN_HEIGHT)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

# Create the player
player = Player(50, 50)
player.walls = wall_list
all_sprite_list.add(player)

clock = pygame.time.Clock()

# Movement speed variables
speed_normal = 3
speed_sprint = 6

# Track which keys are held down
keys_held = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_UP: False,
    pygame.K_DOWN: False,
}
shift_held = False

# Camera offset
camera_x = 0
camera_y = 0

# Zoom factor
zoom = (
    3.0  # Change this value to zoom in or out. Values > 1 zoom in, values < 1 zoom out.
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_held = True  # Enable sprint

            if event.key in keys_held:
                keys_held[event.key] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                shift_held = False  # Disable sprint

            if event.key in keys_held:
                keys_held[event.key] = False

    # Determine the movement speed based on whether shift is held
    move_speed = speed_sprint if shift_held else speed_normal

    # Update player speed based on which keys are held
    x_change = (keys_held[pygame.K_RIGHT] - keys_held[pygame.K_LEFT]) * move_speed
    y_change = (keys_held[pygame.K_DOWN] - keys_held[pygame.K_UP]) * move_speed
    player.changespeed(x_change, y_change)

    # Update all sprites
    all_sprite_list.update()

    # Update the camera position to follow the player
    camera_x = player.rect.centerx - SCREEN_WIDTH // (2 * zoom)
    camera_y = player.rect.centery - SCREEN_HEIGHT // (2 * zoom)

    # Clear the screen
    screen.fill(BLACK)

    # Draw all sprites with zoom and camera offset
    for sprite in all_sprite_list:
        sprite_rect = sprite.rect.copy()
        # Adjust position based on camera and zoom
        sprite_rect.x = (sprite.rect.x - camera_x) * zoom
        sprite_rect.y = (sprite.rect.y - camera_y) * zoom
        # Adjust size based on zoom
        sprite_rect.width = sprite.rect.width * zoom
        sprite_rect.height = sprite.rect.height * zoom

        # Draw the sprite with scaling
        scaled_image = pygame.transform.scale(
            sprite.image, (sprite_rect.width, sprite_rect.height)
        )
        screen.blit(scaled_image, sprite_rect.topleft)

    # Flip the screen
    pygame.display.flip()

    # Limit to 60 FPS
    clock.tick(60)

pygame.quit()
