import pygame
import sys
import os

from objects import *


def load_image(name, mult):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    image = pygame.transform.scale(image, (image.get_width() * mult, image.get_height() * mult))
    return image


def terminate():
    pygame.quit()
    sys.exit()


def nothing():
    pass


def levels_func(n):
    if n == 0:
        return nothing
    if n == 1:
        return level1
    if n == 2:
        return level2
    return level3


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def generate_level(level, tile_group, trap_group, all_sprites):
    fires_coords = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
                img = IMAGES['box']
            elif level[y][x] == '1':
                img = IMAGES['bot_left']
            elif level[y][x] == '2':
                img = IMAGES['bot_mid']
            elif level[y][x] == '3':
                img = IMAGES['bot_right']
            elif level[y][x] == '4':
                img = IMAGES['mid_left']
            elif level[y][x] == '5':
                img = IMAGES['mid_mid']
            elif level[y][x] == '6':
                img = IMAGES['mid_right']
            elif level[y][x] == '7':
                img = IMAGES['top-left']
            elif level[y][x] == '8':
                img = IMAGES['top-mid']
            elif level[y][x] == '9':
                img = IMAGES['top_right']
            elif level[y][x] == 'd':
                img = IMAGES['dirt']
                Tile(img, 8, img.get_width() // 8 * x, img.get_height() * y, tile_group, all_sprites)
                continue
            elif level[y][x] == 'u':
                img = IMAGES['underdirt']
            elif level[y][x] == 'g':
                img = IMAGES['gun']
                Tile(img, 4, img.get_width() // 4 * x, img.get_height() * y, tile_group, all_sprites)
                fires_coords.append([img.get_width() // 4 * x, img.get_height() * (y - 1)])
                continue
            elif level[y][x] == '^':
                img = IMAGES['spike']
                Tile(img, 1, img.get_width() * x, img.get_height() * y, trap_group, all_sprites)
                continue
            elif level[y][x] == '>':
                img = pygame.transform.rotate(IMAGES['spike'], 270)
                Tile(img, 1, img.get_width() * x, img.get_height() * y, trap_group, all_sprites)
                continue
            elif level[y][x] == 'v':
                img = pygame.transform.rotate(IMAGES['spike'], 180)
                Tile(img, 1, img.get_width() * x, img.get_height() * y, trap_group, all_sprites)
                continue
            elif level[y][x] == '<':
                img = pygame.transform.rotate(IMAGES['spike'], 90)
                Tile(img, 1, img.get_width() * x, img.get_height() * y, trap_group, all_sprites)
                continue
            elif level[y][x] == '@':
                player_coords = (48 * x, 48 * y)
                continue
            elif level[y][x] == '$':
                money_coords = (48 * x, 48 * y)
                continue
            elif level[y][x] == '#':
                child_coords = (48 * x, 48 * y)
                continue
            else:
                continue
            Tile(img, 1, img.get_width() * x, img.get_height() * y, tile_group, all_sprites)
    return [player_coords, money_coords, child_coords, fires_coords]


def write_file():
    with open('data/data.txt', 'w') as file:
        file.write(' '.join(map(str, DATA['open_levels'])) + '\n')
        file.write(' '.join(map(str, DATA['collected_coins'])) + '\n')
        file.write(' '.join(map(str, DATA['level_times'])) + '\n')


def dog_dialog():
    images = []
    for i in range(1, 9):
        images.append(load_image(f'dialogs/dog_dialog{i}.png', 1))
    index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                index += 1
        if index == len(images):
            break
        SCREEN.blit(images[index], (0, 0))
        pygame.display.flip()


def pig_dialog():
    images = []
    for i in range(1, 10):
        images.append(load_image(f'dialogs/pig_dialog{i}.png', 1))
    index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                index += 1
        if index == len(images):
            break
        SCREEN.blit(images[index], (0, 0))
        pygame.display.flip()


def chicken_dialog():
    images = []
    for i in range(1, 6):
        images.append(load_image(f'dialogs/chicken_dialog{i}.png', 1))
    index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                index += 1
        if index == len(images):
            break
        SCREEN.blit(images[index], (0, 0))
        pygame.display.flip()


def start_screen():
    bg = IMAGES['bg']
    SCREEN.blit(bg, (0, 0))

    buttons_group = pygame.sprite.Group()
    btn_play = IMAGES['btn_play']
    Button(btn_play, (WIDTH - btn_play.get_width()) // 2, 300, levels_menu, buttons_group)

    font = pygame.font.Font(None, 128)
    string_rendered = font.render('PETS-DASH', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 150
    intro_rect.x = (WIDTH - intro_rect.width) // 2
    SCREEN.blit(string_rendered, intro_rect)
    buttons_group.draw(SCREEN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons_group:
                    button.update()
        pygame.display.flip()
        CLOCK.tick(FPS)


def levels_menu():
    bg = IMAGES['bg']
    SCREEN.blit(bg, (0, 0))

    buttons_group = pygame.sprite.Group()
    btns = [(IMAGES[f'btn{i + 1}'], i + 1) if elem else (IMAGES['btn_locked'], 0)
            for i, elem in enumerate(DATA['open_levels'])]
    for i, btn in enumerate(btns):
        Button(btn[0], 260 + i * (btn[0].get_width() + 260), 300, levels_func(btn[1]), buttons_group)
    Button(IMAGES['btn_back'], 0, 0, start_screen, buttons_group)
    buttons_group.draw(SCREEN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons_group:
                    button.update()
        pygame.display.flip()
        CLOCK.tick(FPS)


def level1():
    bg = IMAGES['bg']
    SCREEN.blit(bg, (0, 0))

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    trap_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()

    Button(IMAGES['btn_back'], 0, 0, levels_menu, buttons_group)

    Border(0, 0, WIDTH, 0, tile_group, all_sprites)
    Border(0, HEIGHT, WIDTH, HEIGHT, tile_group, all_sprites)
    Border(0, 0, 0, HEIGHT, tile_group, all_sprites)
    Border(WIDTH, 0, WIDTH, HEIGHT, tile_group, all_sprites)

    player_coords, money_coords, child_coords, _ = generate_level(load_level('level1.txt'),
                                                                  tile_group, trap_group, all_sprites)
    player = Player(IMAGES['dog'], 2, player_coords[0], player_coords[1], 2, player_group)
    money = Tile(IMAGES['bone'], 1, money_coords[0], money_coords[1], all_sprites)
    finish = Tile(IMAGES['mini_dog'], 1, child_coords[0], child_coords[1], all_sprites)
    is_collected_money = False
    is_finish = False

    all_sprites.draw(SCREEN)
    player_group.draw(SCREEN)

    right = False
    left = False
    up = False
    new_up = False
    running = True
    start_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons_group:
                    button.update()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                new_up = not up
                up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                up = False
        player_group.update(right, left, up, new_up, tile_group)
        new_up = False

        if pygame.sprite.collide_rect(player, money):
            money.kill()
            is_collected_money = True
        if pygame.sprite.collide_rect(player, finish):
            is_finish = True
            running = False
        for trap in trap_group:
            if pygame.sprite.collide_mask(player, trap):
                running = False

        SCREEN.blit(bg, (0, 0))
        buttons_group.draw(SCREEN)
        all_sprites.draw(SCREEN)
        all_sprites.update()
        player_group.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)
    if is_finish:
        if is_collected_money:
            DATA['collected_coins'][0] = 1
        DATA['open_levels'][1] = 1
        DATA['level_times'][0] = (pygame.time.get_ticks() - start_time) / 1000
        write_file()
        dog_dialog()
        levels_menu()
    level1()


def level2():
    bg = IMAGES['bg']
    SCREEN.blit(bg, (0, 0))

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    trap_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()

    Button(IMAGES['btn_back'], 0, 0, levels_menu, buttons_group)
    player_coords, money_coords, child_coords, fire_coords = generate_level(load_level('level2.txt'),
                                                                            tile_group, trap_group, all_sprites)
    player = Player(IMAGES['pig'], 2, player_coords[0], player_coords[1], 1, player_group)
    money = Tile(IMAGES['acorn'], 1, money_coords[0], money_coords[1], all_sprites)
    finish = Tile(IMAGES['mini_pig'], 1, child_coords[0], child_coords[1], all_sprites)
    is_collected_money = False
    is_finish = False

    is_create_fire = [0] * 16
    is_create_fire[8] = 1
    index_fire = 0

    all_sprites.draw(SCREEN)
    player_group.draw(SCREEN)

    right = False
    left = False
    up = False
    new_up = False
    running = True

    start_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons_group:
                    button.update()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                new_up = not up
                up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                up = False
        player_group.update(right, left, up, new_up, tile_group)
        new_up = False

        if pygame.sprite.collide_rect(player, money):
            money.kill()
            is_collected_money = True
        if pygame.sprite.collide_rect(player, finish):
            is_finish = True
            running = False
        if is_create_fire[index_fire]:
            for coord in fire_coords:
                Fire(IMAGES['fire'], coord[0], coord[1], trap_group, all_sprites)
        index_fire = (index_fire + 1) % len(is_create_fire)
        for trap in trap_group:
            if pygame.sprite.collide_mask(player, trap):
                running = False
        SCREEN.blit(bg, (0, 0))
        buttons_group.draw(SCREEN)
        all_sprites.draw(SCREEN)
        all_sprites.update()
        player_group.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)
    if is_finish:
        if is_collected_money:
            DATA['collected_coins'][1] = 1
        DATA['open_levels'][2] = 1
        DATA['level_times'][1] = (pygame.time.get_ticks() - start_time) / 1000
        write_file()
        pig_dialog()
        levels_menu()
    level2()


def level3():
    bg = IMAGES['bg']
    SCREEN.blit(bg, (0, 0))

    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    trap_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()

    Button(IMAGES['btn_back'], 0, 0, levels_menu, buttons_group)
    player_coords, money_coords, child_coords, _ = generate_level(load_level('level3.txt'),
                                                                  tile_group, trap_group, all_sprites)
    player = Player(IMAGES['chicken'], 4, player_coords[0], player_coords[1], -1, player_group)
    money = Tile(IMAGES['seeds'], 1, money_coords[0], money_coords[1], all_sprites)
    finish = Tile(IMAGES['mini_chicken'], 1, child_coords[0], child_coords[1], all_sprites)
    is_collected_money = False
    is_finish = False

    all_sprites.draw(SCREEN)
    player_group.draw(SCREEN)

    right = False
    left = False
    up = False
    new_up = False
    running = True

    start_time = pygame.time.get_ticks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons_group:
                    button.update()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                new_up = not up
                up = True
            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right = False
            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left = False
            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                up = False
        player_group.update(right, left, up, new_up, tile_group)
        new_up = False

        if pygame.sprite.collide_rect(player, money):
            money.kill()
            is_collected_money = True
        if pygame.sprite.collide_rect(player, finish):
            is_finish = True
            running = False
        for trap in trap_group:
            if pygame.sprite.collide_mask(player, trap):
                running = False

        SCREEN.blit(bg, (0, 0))
        buttons_group.draw(SCREEN)
        all_sprites.draw(SCREEN)
        all_sprites.update()
        player_group.draw(SCREEN)
        pygame.display.flip()
        CLOCK.tick(FPS)
    if is_finish:
        if is_collected_money:
            DATA['collected_coins'][2] = 1
        DATA['level_times'][2] = (pygame.time.get_ticks() - start_time) / 1000
        write_file()
        chicken_dialog()
        end()
    level3()


def end():
    bg = IMAGES['bg']
    SCREEN.blit(bg, (0, 0))

    buttons_group = pygame.sprite.Group()
    Button(IMAGES['btn_back'], 0, 0, levels_menu, buttons_group)

    font = pygame.font.Font(None, 64)
    string_rendered = font.render(f"Собрано монет: {sum(DATA['collected_coins'])}", True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 150
    intro_rect.x = (WIDTH - intro_rect.width) // 2
    SCREEN.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 64)
    string_rendered = font.render(f"1 уровень пройден за: {DATA['level_times'][0]} секунд",
                                  True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 200
    intro_rect.x = (WIDTH - intro_rect.width) // 2
    SCREEN.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 64)
    string_rendered = font.render(f"2 уровень пройден за: {DATA['level_times'][1]} секунд",
                                  True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 250
    intro_rect.x = (WIDTH - intro_rect.width) // 2
    SCREEN.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 64)
    string_rendered = font.render(f"3 уровень пройден за: {DATA['level_times'][2]} секунд",
                                  True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 300
    intro_rect.x = (WIDTH - intro_rect.width) // 2
    SCREEN.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 64)
    string_rendered = font.render(f"Всего: {sum(DATA['level_times'])} секунд", True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 350
    intro_rect.x = (WIDTH - intro_rect.width) // 2
    SCREEN.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 128)
    string_rendered = font.render(f"Поздравляем", True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 50
    intro_rect.x = (WIDTH - intro_rect.width) // 2
    SCREEN.blit(string_rendered, intro_rect)
    buttons_group.draw(SCREEN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons_group:
                    button.update()
        pygame.display.flip()
        CLOCK.tick(FPS)


FPS = 15
WIDTH, HEIGHT = 1488, 816
CLOCK = pygame.time.Clock()

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

IMAGES = {
    'bg': load_image('background.png', 3),

    'chicken': load_image('pets/Chicken/chicken.png', 3),
    'mini_chicken': load_image('pets/Chicken/MiniChicken.png', 3),
    'seeds': load_image('pets/Chicken/Seeds.png', 3),

    'dog': load_image('pets/Dog/Dog.png', 3),
    'mini_dog': load_image('pets/Dog/MiniDog.png', 3),
    'bone': load_image('pets/Dog/Bone.png', 3),

    'pig': load_image('pets/Pig/pig.png', 3),
    'mini_pig': load_image('pets/Pig/MiniPig.png', 3),
    'acorn': load_image('pets/Pig/Acorn.png', 3),

    'btn_back': load_image('ui/Buttons/Back.png', 5),
    'btn1': load_image('ui/Buttons/btn1.png', 8),
    'btn2': load_image('ui/Buttons/btn2.png', 8),
    'btn3': load_image('ui/Buttons/btn3.png', 8),
    'btn_locked': load_image('ui/Buttons/LockedLevel.png', 8),
    'btn_play': load_image('ui/Buttons/Play.png', 8),

    'top-left': load_image('tiles/top_left.png', 3),
    'top-mid': load_image('tiles/top_mid.png', 3),
    'top_right': load_image('tiles/top_right.png', 3),
    'mid_left': load_image('tiles/mid_left.png', 3),
    'mid_mid': load_image('tiles/mid_mid.png', 3),
    'mid_right': load_image('tiles/mid_right.png', 3),
    'bot_left': load_image('tiles/bot_left.png', 3),
    'bot_mid': load_image('tiles/bot_mid.png', 3),
    'bot_right': load_image('tiles/bot_right.png', 3),
    'box': load_image('tiles/box.png', 3),
    'dirt': load_image('tiles/dirt.png', 3),
    'underdirt': load_image('tiles/underdirt.png', 3),
    'spike': load_image('tiles/spike.png', 3),
    'gun': load_image('tiles/gun.png', 3),
    'fire': load_image('tiles/fire.png', 3),

}

with open('data/data.txt') as f:
    DATA = {}
    f = list(map(str.strip, f.readlines()))
    DATA['open_levels'] = list(map(int, f[0].split()))
    DATA['collected_coins'] = list(map(int, f[1].split()))
    DATA['level_times'] = list(map(float, f[2].split()))

if __name__ == '__main__':
    start_screen()
