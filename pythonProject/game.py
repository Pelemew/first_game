import pygame

clock = pygame.time.Clock()

# запуск проекта
pygame.init()
# размер игрового экрана
screen = pygame.display.set_mode((600,360))

# форматирование картинок под андроид
# image_path = '/data/data/org.test.myapp/files/app/'

# установка иконки игры
pygame.display.set_caption('Dota 2')
icon = pygame.image.load('images/dota2.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('images/bg.jpg').convert()

walk_left = [
    pygame.image.load( 'images/hero_left1.png').convert_alpha(),
    pygame.image.load('images/hero_left2.png').convert_alpha(),
    pygame.image.load('images/hero_left3.png').convert_alpha(),
    pygame.image.load('images/hero_left4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/hero_right1.png').convert_alpha(),
    pygame.image.load('images/hero_right2.png').convert_alpha(),
    pygame.image.load('images/hero_right3.png').convert_alpha(),
    pygame.image.load('images/hero_right4.png').convert_alpha(),
]

# создание врага
enemy = pygame.image.load('images/enemy.png').convert_alpha()
enemy_list_in_game = []

hero_anim_count = 0
bg_x = 0

bg_sound = pygame.mixer.Sound('sounds/bg.mp3')
bg_sound.play()

# создание персонажа
player_speed = 8
player_x = 100
player_y = 210

is_jump = False
jump_count = 8

label = pygame.font.Font('Fonts/Roboto-Black.ttf', 40)
restart_label = label.render('Играть заново', False,(115, 132,148 ))
lose_label = label.render('Вы проиграли!', False,(193, 196,199))
restart_label_rect = restart_label.get_rect(topleft =(170,200))

# создание патрона и дальнейшей стрельбы
bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []

gameplay = True

running = True

# спавнер врагов
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 2500)

while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 600, 0))

    if gameplay == True:

        # хитбоксы юнитов
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if enemy_list_in_game:
            for (i,el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 10

                # удаление пробежавщих врагов
                if el.x < -10:
                    enemy_list_in_game.pop(i)

                # соприкосновение персонажа
                if player_rect.colliderect(el):
                    gameplay = False

        # ходьба персонажа
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[hero_anim_count], (player_x, player_y))

        else:
            screen.blit(walk_right[hero_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 300:
            player_x += player_speed

        # прыжок персонажа
        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2)/2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8


        # анимация ходьбы персонажа
        if hero_anim_count == 3:
            hero_anim_count = 0
        else:
            hero_anim_count += 1

        # передвижение заднего фона
        bg_x -= 3
        if bg_x == -600:
            bg_x = 0

        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 15

                if el.x > 615:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for (index, enemy_el) in enumerate (enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (170, 130))
        screen.blit(restart_label, restart_label_rect)

        # collidepoint - проверка соприкосновения хитбокса с мышкой
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            enemy_list_in_game.clear()
            player_x = 100
            bullets.clear()
            bullets_left = 5
            gameplay = True



    # обновление экрана
    pygame.display.update()

    clock.tick(10)

    # цикл перебора всех возможных событий
    for event in pygame.event.get():
        # отключение проекта
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # создание евента спавнера мобов
        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(620,220)))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 25, player_y + 20)))
            bullets_left -= 1


