import random
import pygame
import enemies
import player
import explosion
import colors as c
from os import path

def play_again(max_pkt):
    import random
    import pygame
    import enemies
    import player
    import explosion
    import colors as c
    from os import path

    img_dir = path.join(path.dirname(__file__), 'images')
    snd_dir = path.join(path.dirname(__file__), 'sounds')

    laser_img = pygame.image.load(path.join(img_dir, "EnemyProjectile1.png"))

    WIDTH = 1024
    HEIGHT = 600
    FPS = 60
    SPAWN = 3

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space tide")
    clock = pygame.time.Clock()

    # tło
    background = pygame.image.load(path.join(img_dir, "2762074.jpg")).convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background_rect = background.get_rect()

    # dźwięki
    pygame.mixer.music.load(path.join(snd_dir, 'Empire of War.mp3'))
    pygame.mixer.music.set_volume(0.3)


    expl_sounds = []
    for snd in ['explosion01.wav', 'explosion02.wav', 'explosion03.wav']:
        expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

    # ładowanie gracza i przeciwnikow
    player_img = pygame.image.load(path.join(img_dir, "LargeBlueShip-removebg-preview.png")).convert()
    basic_mob = pygame.image.load(path.join(img_dir, "warrior1.png")).convert()
    bouncing_mob = pygame.image.load(path.join(img_dir, "warrior2.png")).convert()
    shooting_mob = pygame.image.load(path.join(img_dir, "shooting_ship-removebg-preview.png")).convert()

    # wybuchy
    explosion_anim = {}
    explosion_anim['basic'] = []

    for i in range(1, 13):
        filename = 'explosion{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(c.BLACK)
        img_lg = pygame.transform.scale(img, (200, 200))
        explosion_anim['basic'].append(img_lg)

    def newmob():
        m1 = enemies.Mob(basic_mob, WIDTH, HEIGHT, 80, 40)
        m2 = enemies.BouncingMob(bouncing_mob, WIDTH, HEIGHT, 80, 40)
        m3 = enemies.ShootingMob(shooting_mob, WIDTH, HEIGHT, 80, 80, pygame.time.get_ticks())
        # trohę prymitywnie, ale wybiera to przeciwnika z "wagą"
        spawn_choice = random.choice((m1, m1, m1, m1, m1, m2, m2, m3, m3, m3))
        all_sprites.add(spawn_choice)
        mobs.add(spawn_choice)

    font_name = pygame.font.match_font('arial')

    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, c.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    all_sprites = pygame.sprite.Group()
    player = player.Player(player_img, WIDTH, HEIGHT, 80, 40, 0.5, pygame.time.get_ticks())
    all_sprites.add(player)
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemyBullets = pygame.sprite.Group()
    all_sprites.add(player)
    for i in range(SPAWN):
        newmob()

    score = 0
    stopSpown = 0
    upSpawn = 500
    pygame.mixer.music.play(loops=-1)

    running = True
    player_lives = True

    while running:
        # keep loop running at the right speed
        clock.tick(FPS)

        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot(all_sprites, bullets, pygame.time.get_ticks())
                if event.key == pygame.K_q and player.quantum_bombs > 0:
                    player.quantum_bombs -= 1
                    for mob in mobs:
                        random.choice(expl_sounds).play()
                        expl = explosion.Explosion(mob.rect.center, 'basic', explosion_anim)
                        all_sprites.add(expl)
                        mob.kill()

        # duszenie strzału
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot(all_sprites, bullets, pygame.time.get_ticks())

        for mob in mobs:
            mob.shoot(all_sprites, enemyBullets, pygame.time.get_ticks(), laser_img)

        all_sprites.update()

        hitsPlayer = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hitsPlayer:
            score += hit.score
            random.choice(expl_sounds).play()
            expl = explosion.Explosion(hit.rect.center, 'basic', explosion_anim)
            all_sprites.add(expl)
            if len(mobs) < SPAWN:
                newmob()

        hitsEnemy = pygame.sprite.spritecollide(player, enemyBullets, True, pygame.sprite.collide_circle)
        for hit in hitsEnemy:
            random.choice(expl_sounds).play()
            expl = explosion.Explosion(hit.rect.center, 'basic', explosion_anim)
            player.kill()
            all_sprites.add(expl)
            player_lives = False

        collide = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for cols in collide:
            random.choice(expl_sounds).play()
            expl = explosion.Explosion(cols.rect.center, 'basic', explosion_anim)
            player.kill()
            all_sprites.add(expl)
            player_lives = False

        if player_lives == False and not expl.alive():
            if max_pkt < score:
                max_pkt = score
                with open("maxscore.txt", "w") as f:
                    f.write(str(max_pkt))

            play_again(max_pkt)

        screen.fill(c.BLACK)
        screen.blit(background, background_rect)

        all_sprites.draw(screen)
        score_text = str(score) + " TOP: " + str(max_pkt)
        if score>max_pkt:
            score_text+=" NEW RECORD!"

        draw_text(screen, score_text, 18, WIDTH / 2, 10)
        text_powreup = "Number of quantum bombs: " + str(player.quantum_bombs)
        draw_text(screen, text_powreup, 18, WIDTH / 2, 30)
        text_control = "keys to move ship, SPACE to FIRE, Q to drop quantum bomb"
        draw_text(screen, text_control, 18, WIDTH / 2, 50)


        if (len(mobs)) < SPAWN:  # dev only
            newmob()

        if score != 0 and score >= upSpawn and score != stopSpown:
            SPAWN += 1
            upSpawn += 500
            stopSpown = score

        pygame.display.flip()

    pygame.quit()


max_pkt = 0
try:
    with open("maxscore.txt", "r") as f:
        tmp = []
        tmp.append(f.readlines())
        print(tmp)
        max_pkt = tmp[0][0]
except:
    pass

if __name__ == "__main__":
    play_again(int(max_pkt))
