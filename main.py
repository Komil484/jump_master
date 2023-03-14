import pygame
import random
from sys import exit


class Enemy:
    enemies = []

    def __init__(self, enemy_option=0):
        self.speed = 6
        if enemy_option == 0:
            enemy_option = random.randint(1, 4)
        self.surf = pygame.image.load("assets/images/enemy" + str(enemy_option) + ".png").convert_alpha()
        self.rect = self.surf.get_rect(bottomleft=(800, 300))
        self.rect.inflate_ip(-28, 0)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

    def move(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.surf.get_width():
            global game_score
            game_score += 1
            self.enemies.remove(self)


class GameStates:
    title_screen = 0
    initialization = 1
    game_active = 2
    game_over = 3


# parameters
game_score = 0
mouse_pos = (0, 0)
player_gravity = 0.5
player_upward_velocity = 0
is_player_on_ground = True
game_state = GameStates.title_screen
create_enemy_event = pygame.USEREVENT + 1
enemy_spawn_timer = 0

# initialization
random.seed()

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Jump Master")
pygame.display.set_icon(pygame.image.load("assets/icon.png").convert_alpha())

clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/fonts/sunny.otf", 80)

sky_surf = pygame.image.load("assets/images/sky.png").convert()
ground_surf = pygame.image.load("assets/images/ground.png").convert()

score_surf = game_font.render(str(game_score), True, "Black")
score_rect = score_surf.get_rect(midtop=(400, 20))

player_surf = pygame.image.load("assets/images/player.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(100, 300))


def render_game():
    global screen
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    screen.blit(score_surf, score_rect)
    screen.blit(player_surf, player_rect)
    for enemy in Enemy.enemies:
        enemy.draw(screen)


def try_jump():
    global is_player_on_ground
    if not is_player_on_ground:
        return None
    is_player_on_ground = False
    global player_upward_velocity
    player_upward_velocity = 15


def add_enemy():
    Enemy.enemies.append(Enemy())


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_state == GameStates.game_active:

        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            try_jump()
        if keys[pygame.K_l]:
            add_enemy()

        # Enemy
        enemy_spawn_timer -= clock.get_time()
        if enemy_spawn_timer <= 0:
            add_enemy()
            enemy_spawn_timer = random.randint(1000, 1800)

        for enemy in Enemy.enemies:
            enemy.move()

        # Player
        if not is_player_on_ground:
            player_upward_velocity -= player_gravity
            player_rect.y -= player_upward_velocity
            if player_rect.bottom >= 300:
                is_player_on_ground = True
                player_upward_velocity = 0
                player_rect.bottom = 300

        for enemy in Enemy.enemies:
            if player_rect.colliderect(enemy.rect):
                game_state = GameStates.game_over

        # Rendering
        score_surf = game_font.render(str(game_score), True, "Black")
        render_game()

    elif game_state == GameStates.initialization:
        Enemy.enemies.clear()
        game_score = 0
        game_state = GameStates.game_active

    elif game_state == GameStates.game_over:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        current_score_surf = game_font.render("Your score is: " + str(game_score), True, "Black")
        screen.blit(current_score_surf, current_score_surf.get_rect(midtop=(400, 70)))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = GameStates.initialization

    else:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        start_prompt = game_font.render("Press space to start", True, "Black")
        screen.blit(start_prompt, start_prompt.get_rect(midtop=(400, 70)))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = GameStates.initialization

    pygame.display.update()
    clock.tick(60)
