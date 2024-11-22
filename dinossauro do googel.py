import pygame
import random

# Definições gerais do jogo
screen_width = 1535
screen_height = 789
fps = 60
gravity = 0.2
tree_speed = 5
boost_duration = 5
boost_cooldown = 0
boost_duration_left = 0
score_increment = 1
speed_increment = 0.5
score_threshold = 300
speed_counter = 0
fundo = 9800
music_playing = True

# Cores
white = (255, 255, 255)
black = (0, 0, 0)

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Carregamento das imagens
background_img = pygame.image.load("fundo2.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (9800, screen_height))
dash = pygame.image.load('Dash.png').convert_alpha()
on = pygame.image.load('Música-ON.png').convert_alpha()
off = pygame.image.load('Música-OFF.png').convert_alpha()
hit = pygame.image.load('HitBoxDino.png').convert_alpha()
hitar = pygame.image.load('HitBoxArvore.png').convert_alpha()
dinosaur_imgs = [
    pygame.image.load("dinosaur1.png").convert_alpha(),
    pygame.image.load("dinosaur2.png").convert_alpha(),
    pygame.image.load("dinosaur3.png").convert_alpha(),
    pygame.image.load("dinosaur2.png").convert_alpha()
]
tree_imgs = [
    pygame.image.load("tree1.png").convert_alpha(),
    pygame.image.load("tree2.png").convert_alpha(),
    pygame.image.load("tree3.png").convert_alpha(),
    pygame.image.load("tree2.png").convert_alpha()
]
game_over_img = pygame.image.load("game_over.png").convert_alpha()
exit_img = pygame.image.load("exit.png").convert_alpha()

# Carregamento das músicas
pygame.mixer.music.set_volume(0.5)

telas = 1

music_list = [
    "back-in-black.mp3",
    "Crazy-Train.mp3",
    "Enter-Sandman.mp3",
    "Eye-Of-The-Tiger.mp3",
    "Highway-to-Hell.mp3",
    "Immigrant-Song.mp3",
    "jump.mp3",
    "Paranoid.mp3",
    "Rock-You-Like-a-Hurricane.mp3",
    "Runnin-with-the-Devil.mp3",
    "The-Trooper.mp3",
    "Thunderstruck.mp3",
    "We-Will-Rock-You.mp3",
    "Welcome-To-The-Jungle.mp3",
    "You-Give-Love-A-Bad-Name.mp3"
]

current_music = random.choice(music_list)
velocidade_antes = 5

# Classe da Hit Box

class HitBox(pygame.sprite.Sprite):
    def __init__(self, dinosaur):
        super().__init__()
        self.image = hit
        self.rect = self.image.get_rect()
        self.dinosaur = dinosaur

    def update(self):
        self.rect.midbottom = self.dinosaur.rect.midbottom


# Classe do Dinossauro
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = dinosaur_imgs
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect.center = (100, screen_height // 2)
        self.velocity = 2
        self.jump_cooldown = 0
        self.score = 0
        self.boost_timer = 0
        self.hit_box = HitBox(self)
        all_sprites.add(self.hit_box)  # Adiciona a hit box ao grupo de sprites

    def update(self):
        global speed_counter, tree_speed
        self.velocity += gravity
        self.rect.y += self.velocity
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.velocity = 0
            self.jump_cooldown = 0

        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        self.score += score_increment

        if self.boost_timer > 0:
            self.boost_timer -= 1
            if self.boost_timer == 0:
                tree_speed = 5

        if self.score % 10 == 0:
            self.update_dinosaur_image()

        speed_counter += score_increment
        if speed_counter >= score_threshold:
            tree_speed += speed_increment
            speed_counter = 0

    def update_dinosaur_image(self):
        global tree_speed, boost_cooldown, boost_duration_left, velocidade_antes, dash
        if boost_duration_left == 0:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]
        else:
            self.image = dash

    def jump(self):
        if self.jump_cooldown == 0 and self.rect.bottom == screen_height:
            self.velocity = -10
            self.jump_cooldown = 98

    def boost_speed(self):
        global tree_speed, boost_cooldown, boost_duration_left, velocidade_antes
        if boost_duration_left == 0 and boost_cooldown == 0:
            velocidade_antes = tree_speed
            boost_duration_left = boost_duration * 4
            tree_speed = tree_speed * 2
            boost_cooldown = 300

    def draw_score(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, black)
        screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

    def draw_high_score(self, screen, high_score):
        font = pygame.font.Font(None, 36)
        high_score_text = font.render("High Score: " + str(high_score), True, black)
        screen.blit(high_score_text, (screen_width - high_score_text.get_width() - 10, 50))


# hit box das arvores

class TreeHitBox(pygame.sprite.Sprite):
    def __init__(self, tree):
        super().__init__()
        self.image = hitar
        self.rect = self.image.get_rect()
        self.tree = tree

    def update(self):
        self.rect.midbottom = self.tree.rect.midbottom


# Classe da Árvore
class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = tree_imgs  # lista de imagens
        self.current_image = 0  # índice da imagem atual
        self.image = self.images[self.current_image]  # imagem atual
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = screen_height - self.rect.height
        self.image_counter = 0  # contador para controlar a troca de imagens
        self.image_change_interval = 15  # intervalo de troca de imagens das árvores
        self.hit_box = TreeHitBox(self)
        all_sprites.add(self.hit_box)  # Adiciona a hit box ao grupo de sprites

    def update(self):
        global tree_speed
        if tree_boost:
            self.rect.x -= tree_speed * 2
        else:
            self.rect.x -= tree_speed

        if self.rect.right < 0:
            self.kill()

        self.image_counter += 1
        if self.image_counter >= self.image_change_interval:
            self.image_counter = 0
            self.update_image()

    def update_image(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]


all_sprites = pygame.sprite.Group()
trees = pygame.sprite.Group()

dinosaur = Dinosaur()
all_sprites.add(dinosaur)

tree_boost = False

running = True
background_x = 0
game_over = False


def play_random_music():
    global current_music, music_playing

    if not pygame.mixer.music.get_busy():
        if music_playing:
            new_music = random.choice(music_list)
            current_music = new_music
            pygame.mixer.music.load("musicas.mp3/" + current_music)
            pygame.mixer.music.play()

    if not pygame.mixer.music.get_busy() and music_playing:
        new_music = random.choice(music_list)
        current_music = new_music

        print(current_music)
        pygame.mixer.music.load("musicas.mp3/" + current_music)
        pygame.mixer.music.play()


# Carregar o high score
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.readline())
            return high_score
    except FileNotFoundError:
        return 0

# Salvar o high score
def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

high_score = load_high_score()


while running:
    play_random_music()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                music_playing = not music_playing  # Alterna o estado da música (ligado/desligado)
                if music_playing:
                    pygame.mixer.music.unpause()  # Retoma a música se estiver pausada
                else:
                    pygame.mixer.music.pause()  # Pausa a música se estiver tocando
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_SPACE:
                if game_over:
                    current_music = ""
                    game_over = False
                    all_sprites.empty()
                    trees.empty()
                    dinosaur = Dinosaur()
                    all_sprites.add(dinosaur)
                    tree_speed = 5
                    boost_cooldown = 0
                    boost_duration_left = 0
                    speed_counter = 0
                    background_x = 0
                    screen.blit(background_img, (0, 0))
                    pygame.mixer.music.stop()
                    play_random_music()
                else:
                    dinosaur.jump()
            elif event.key == pygame.K_RIGHT:
                tree_boost = True
                dinosaur.boost_speed()
            elif event.key == pygame.K_DOWN:
                gravity = 0.7
            elif event.key == pygame.K_LEFT:
                if game_over:
                    running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                gravity = 0.2

    if not game_over:
        all_sprites.update()

        collision = pygame.sprite.spritecollide(dinosaur.hit_box, trees, False)
        if collision:
            game_over = True

        if random.randrange(100) < 1:
            tree = Tree()
            all_sprites.add(tree)
            trees.add(tree)

        if pygame.sprite.spritecollide(dinosaur, trees, False):
            game_over = True

            # Atualizar o high score
            if dinosaur.score > high_score:
                high_score = dinosaur.score
                save_high_score(high_score)

        screen.blit(background_img, (background_x, 0))
        screen.blit(background_img, (background_x + fundo, 0))

        background_x -= tree_speed

        if background_x <= -fundo:
            background_x = 0

        all_sprites.draw(screen)

        dinosaur.draw_score(screen)
        dinosaur.draw_high_score(screen, high_score)
    else:
        screen.blit(game_over_img, (screen_width // 2 - game_over_img.get_width() // 2, screen_height // 2 - game_over_img.get_height() // 2 - 100))
        screen.blit(exit_img, (screen_width // 2 - exit_img.get_width() // 2, screen_height // 2 + game_over_img.get_height() // 2 + game_over_img.get_height() - 90))


        pygame.display.flip()

    # Desenhar a imagem de música ligada ou desligada no canto superior esquerdo
    if music_playing:
        screen.blit(on, (10, 10))
    else:
        screen.blit(off, (10, 10))

    pygame.display.flip()
    clock.tick(fps)

    if boost_cooldown > 0:
        boost_cooldown -= 1

    if boost_duration_left > 0:
        boost_duration_left -= 1
        if boost_duration_left == 0:
            tree_speed = velocidade_antes

pygame.mixer.music.stop()
pygame.quit()