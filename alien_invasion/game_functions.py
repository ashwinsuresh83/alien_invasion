import pygame
import sys
from bullet import Bullet
from aliens import Alien
from time import sleep
def key_down_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key==pygame.K_SPACE:
        fire_bullets(ai_settings,screen,ship,bullets)
    elif event.key==pygame.K_q:
        sys.exit()
def fire_bullets(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.allowed_bullets:
        # create a new bulllet and add it to bullets group
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
def key_up_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            key_down_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            key_up_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active=True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    # get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens)==0:
        bullets.empty()
        stats.level+=1
        sb.prep_level()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens)
def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliensx = int(available_space_x / (2 * alien_width))
    return number_aliensx
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+(2*alien_number*alien_width)
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height+alien.rect.height*row_number
    aliens.add(alien)
def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=ai_settings.screen_height-ship_height-(4*alien_height)
    number_rows=int(available_space_y/(alien_height))
    return number_rows
def create_fleet(ai_settings,screen,ship,aliens):
    '''createsa full fleet of aliens'''
    #create an alien and find the number of aliens in the row
    #spacing between each alien is one alien width
    alien = Alien(ai_settings, screen)
    number_aliensx=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    #create rows of aliens
    for row_no in range(number_rows):
        for alien_number in range(number_aliensx):
            create_alien(ai_settings,screen,aliens,alien_number,row_no)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
    stats.ships_left-=1
    if stats.ships_left<1:
        stats.game_active=False
        pygame.mouse.set_visible(True)
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()
    sleep(0.5)
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()