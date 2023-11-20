#Sin esto no funca el juego
import pygame
import sys
import pytmx
from pygame.locals import *
import os
import subprocess
import pygame.sprite

#PARA LOS ZOMBIS
class Enemy:
    def __init__(self, sprite):
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.pos = pygame.Vector2(0, 0)
        self.speed = 1
        self.health = 1
    def set_position(self, x, y):
        self.pos.x = x
        self.pos.y = y
    def get_rect(self):             #COLISIÓN SUPUESTAMENTE
        return self.rect

    def update(self, player_pos):             #PARA QUE PERSIGA AL JUGADOR      
        direction = (player_pos - self.pos).normalize()
        self.pos += direction * self.speed

    def draw(self, screen, camera_x, camera_y):  #PARA QUE SALGA EL SPRITE
        screen.blit(self.sprite, (self.pos.x - camera_x, self.pos.y - camera_y))
    

#ARMAS
class Weapon:        
    def __init__(self):
        self.ammo = 60
        self.sprite = pygame.image.load('piupiu.png').convert_alpha()
        self.sprite_shot = pygame.image.load('piupiu_shot.png').convert_alpha()

    def fire(self):
        if self.ammo > 0:
            print("¡Disparo!")
            self.ammo -= 1
        else:
            print("Sin munición")
            

#ACA SE MUESTRA EL MAPA
class IsoGame:

    def __init__(self, title='Undead Frenzy'):
        pygame.init()



        self.fpsClk = pygame.time.Clock()

        self.WSurf = pygame.display.set_mode((1200, 720), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.scrW = 1200
        self.scrH = 720

        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont(u'arial', 24)

        self.bg = (0, 0, 0)

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 5

        self.buffLvl('mapa1.tmx')

        self.player_pos = pygame.Vector2(1510, 1410)
        self.player_speed = 1.2

        # Cargar spritesheet del jugador
        self.player_frames_idle = []
        self.player_frames_walk_right = []
        self.player_frames_walk_left = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 210  # Delay entre frames de la animación

        self.extract_player_frames()  # Extraer los frames de los sprites

        self.moving_left = False
        self.moving_right = False

        # Variables del menú de pausa
        self.is_paused = False
        self.pause_menu_options = ['Continuar', 'Salir al menú']
        self.current_pause_option = 0

        self.weapon = Weapon()  # Crear una instancia de la clase Weapon

        # Agregar variables para los proyectiles
        self.projectiles = []
        self.projectile_image = pygame.image.load('projectile.png').convert_alpha()
        #CAPTURAR POSICION DEL MOUSE
        self.mouse_pos = pygame.mouse.get_pos()
        self.player_pos = pygame.Vector2(1510, 1410)
        self.enemies = []
        self.enemy_sprite = pygame.image.load('zombie.png').convert_alpha()

        for enemy in self.enemies:
            enemy.update(self.player_pos)
            
        
        self.health = 100
        self.weapon_name = "Fusil"
        self.consumable_name = "Botiquín"
        self.health_image = pygame.image.load('vida100.png').convert_alpha()
    def create_enemy(self):
        enemy = Enemy(self.enemy_sprite)
        self.enemies.append(enemy)
           
        enemy.set_position(2332, 1264) #CORDENADA DE SPAWN DE LOS ZOMBIS.
        self.enemies.append(enemy)

    def buffLvl(self, lvl='mapa1.tmx'):
        self.tmx = pytmx.load_pygame(lvl, pixelalpha=True)

        self.tile_width = self.tmx.tilewidth
        self.tile_height = self.tmx.tileheight

        self.lvlSurf = pygame.Surface((self.tile_width * self.tmx.width, self.tile_height * self.tmx.height + self.tile_height))
        self.lvlSurf.fill(self.bg)

        for layer in self.tmx.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)
                    if tile:
                        tile_rect = tile.get_rect()
                        tile_rect.x = (x - y) * self.tile_width / 2 + self.tile_width * self.tmx.width / 2 - self.tile_width
                        tile_rect.y = (x + y) * self.tile_height / 2
                        self.lvlSurf.blit(tile, (int(tile_rect.x), int(tile_rect.y)))

    def extract_player_frames(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Cargar sprites de idle
        idle_path = os.path.join(current_dir, 'sprites', 'idle')
        for filename in sorted(os.listdir(idle_path)):
            image_path = os.path.join(idle_path, filename)
            frame = pygame.image.load(image_path).convert_alpha()
            self.player_frames_idle.append(frame)

        # Cargar sprites de walk hacia la derecha
        walk_right_path = os.path.join(current_dir, 'sprites', 'walk', 'walk_right')
        for filename in sorted(os.listdir(walk_right_path)):
            image_path = os.path.join(walk_right_path, filename)
            frame = pygame.image.load(image_path).convert_alpha()
            self.player_frames_walk_right.append(frame)

        # Cargar sprites de walk hacia la izquierda
        walk_left_path = os.path.join(current_dir, 'sprites', 'walk', 'walk_left')
        for filename in sorted(os.listdir(walk_left_path)):
            image_path = os.path.join(walk_left_path, filename)
            frame = pygame.image.load(image_path).convert_alpha()
            self.player_frames_walk_left.append(frame)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            self.camera_y -= self.camera_speed
        if keys[K_DOWN]:
            self.camera_y += self.camera_speed
        if keys[K_LEFT]:
            self.camera_x -= self.camera_speed
        if keys[K_RIGHT]:
            self.camera_x += self.camera_speed

        if keys[K_w]:
            self.player_speed = 1.2  # Idle
            self.moving_left = False
            self.moving_right = False
        elif keys[K_LSHIFT] and (keys[K_w] or keys[K_a] or keys[K_s] or keys[K_d]):
            self.player_speed = 5  # Run
        else:
            self.player_speed = 1.2  # Walk

        if keys[K_a]:
            self.moving_left = True
            self.moving_right = False
        elif keys[K_d]:
            self.moving_left = False
            self.moving_right = True
        else:
            self.moving_left = False
            self.moving_right = False

        if keys[K_w]:
            self.player_pos.y -= self.player_speed
        if keys[K_s]:
            self.player_pos.y += self.player_speed
        if keys[K_a]:
            self.player_pos.x -= self.player_speed
        if keys[K_d]:
            self.player_pos.x += self.player_speed
        #################
        if keys[K_e]:
            self.create_enemy()
        # Manejo de la pausa
        if keys[K_ESCAPE]:
            self.is_paused = not self.is_paused

        # Manejo de la acción de disparo
        if pygame.mouse.get_pressed()[0]:  # Botón izquierdo del mouse presionado
            self.weapon.fire()
            self.create_projectile(pygame.mouse.get_pos() + pygame.Vector2(self.camera_x, self.camera_y))


    def create_projectile(self, mouse_pos):
        projectiles_to_remove = []
        projectile_pos = pygame.Vector2(self.player_pos.x + self.player_frames_idle[0].get_width() // 2, self.player_pos.y + self.player_frames_idle[0].get_height() // 2 + 5)
        direction = (mouse_pos - self.player_pos).normalize()
        mouse_pos = pygame.mouse.get_pos() - pygame.Vector2(self.camera_x, self.camera_y)
        
        projectile = {'rect': pygame.Rect(projectile_pos.x, projectile_pos.y, self.projectile_image.get_width(), self.projectile_image.get_height()), 'direction': direction, 'damage': 50, 'pos': projectile_pos}

        self.projectiles.append(projectile)
    
        self.weapon.sprite = self.weapon.sprite_shot
        
        projectiles_to_remove = []
        enemies_to_remove = []
        projectile_rect = self.projectile_image.get_rect()
        projectile_rect.center = projectile_pos

        projectile = {
            'rect': projectile_rect,
            'direction': direction,
            'damage': 50,
            'pos': projectile_pos
}
        for projectile in self.projectiles:
            for enemy in self.enemies:
                if projectile['rect'].colliderect(enemy.get_rect()):
                    # Reduce la salud del enemigo según el daño del proyectil
                    enemy.health -= projectile['damage']
                    projectiles_to_remove.append(projectile)
                    
                    if enemy.health <= 0:
                        enemies_to_remove.append(enemy)
                    break
        # Eliminar proyectiles que colisionaron
        for projectile in projectiles_to_remove:
            if projectile in self.projectiles:
                self.projectiles.remove(projectile)
        # Eliminar enemigos eliminados
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
        # Se itera sobre los enemigos para verificar colisiones con los proyectiles
        for index, enemy in enumerate(self.enemies):
            if projectile['rect'].colliderect(enemy.rect):
                enemy.health -= projectile['damage']
                projectiles_to_remove.append(index)
                break
        
    # Eliminar proyectiles que colisionaron
        for index in reversed(projectiles_to_remove):
            del self.projectiles[index]

        self.weapon.sprite = pygame.image.load('piupiu_shot.png').convert_alpha()


    def update_projectiles(self):
        projectiles_to_remove = []
        enemies_to_remove = []

        for index, projectile in enumerate(self.projectiles):
            projectile['pos'] += projectile['direction'] * 20 #velocidad del proyectilaaaaaaaaaaaaa

            if projectile['pos'].x > self.player_pos.x + self.scrW:
                projectiles_to_remove.append(index)

            for enemy in self.enemies:
                if projectile['rect'].colliderect(enemy.get_rect()):
                    enemy.health -= projectile['damage']
                    projectiles_to_remove.append(index)
                    if enemy.health <= 0:
                        enemies_to_remove.append(enemy)
                    break

        for index in reversed(projectiles_to_remove):
            del self.projectiles[index]

        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)

    def draw_projectiles(self):
        for projectile in self.projectiles:
            projectile_rect = projectile['rect']
            projectile_rect.center = (projectile['pos'].x - self.camera_x, projectile['pos'].y - self.camera_y)
            self.WSurf.blit(self.projectile_image, projectile_rect)

        for enemy in self.enemies:
            enemy_rect = enemy.rect
            enemy_rect.center = (enemy.pos.x - self.camera_x, enemy.pos.y - self.camera_y)
            self.WSurf.blit(enemy.sprite, enemy_rect)

        self.weapon.sprite = pygame.image.load('piupiu.png').convert_alpha()


    def check_collision(self):
        projectiles_to_remove = []
        enemies_to_remove = []

        for projectile in self.projectiles:
            for enemy in self.enemies:
                if projectile['rect'].colliderect(enemy.get_rect()):
                    projectiles_to_remove.append(projectile)
                    enemies_to_remove.append(enemy)

        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)

        for enemy in enemies_to_remove:
            self.enemies.remove(enemy)
        

    def draw_pause_menu(self):
        menu_width = 200
        menu_height = len(self.pause_menu_options) * 40 + 10
        menu_x = self.scrW // 2 - menu_width // 2
        menu_y = self.scrH // 2 - menu_height // 2

        pygame.draw.rect(self.WSurf, (255, 255, 255), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(self.WSurf, (0, 0, 0), (menu_x, menu_y, menu_width, menu_height), 3)

        for i, option in enumerate(self.pause_menu_options):
            text_surface = self.font.render(option, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.scrW // 2, menu_y + 20 + i * 40))
            self.WSurf.blit(text_surface, text_rect)

            if i == self.current_pause_option:
                pygame.draw.rect(self.WSurf, (255, 0, 0), (text_rect.left - 10, text_rect.top, text_rect.width + 20, text_rect.height), 3)

    def handle_pause_menu_input(self):
        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            self.current_pause_option = (self.current_pause_option - 1) % len(self.pause_menu_options)
        if keys[K_DOWN]:
            self.current_pause_option = (self.current_pause_option + 1) % len(self.pause_menu_options)
        if keys[K_RETURN]:
            if self.current_pause_option == 0:  # Continuar
                self.is_paused = False
            elif self.current_pause_option == 1:  # Salir al menú
                pygame.quit()
                subprocess.call(["python", "main.py"])
                sys.exit()

    def update(self):
        if self.is_paused:
            self.handle_pause_menu_input()
        else:
            self.handle_input()

        if self.moving_left:
            self.current_frame += 1
            if self.current_frame >= len(self.player_frames_walk_left):
                self.current_frame = 0
            self.player_pos.x -= int(self.player_speed)
        elif self.moving_right:
            self.current_frame += 1
            if self.current_frame >= len(self.player_frames_walk_right):
                self.current_frame = 0
            self.player_pos.x += int(self.player_speed)
        else:
            self.current_frame += 1
            if self.current_frame >= len(self.player_frames_idle):
                self.current_frame = 0

        # Actualizar la posición de la cámara para que siga al jugador
        self.camera_x = self.player_pos.x - self.scrW // 2
        self.camera_y = self.player_pos.y - self.scrH // 2

        # Limitar la posición de la cámara para que no se salga de los límites del nivel
        self.camera_x = max(0, min(self.camera_x, self.lvlSurf.get_width() - self.scrW))
        self.camera_y = max(0, min(self.camera_y, self.lvlSurf.get_height() - self.scrH))
#CORDENADAS ACTUALES
        self.display_player_coordinates()
              
        self.check_game_over()
        

        self.update_projectiles()

        for enemy in self.enemies:
            enemy.update(self.player_pos)

        self.update_health_image(self.health)
        self.check_collision()
    def display_player_coordinates(self):
        text_surface = self.font.render(f"Player Coordinates: ({int(self.player_pos.x)}, {int(self.player_pos.y)})", True, (255, 255, 255))
        self.WSurf.blit(text_surface, (10, 10))    
    def draw(self):
        self.WSurf.fill(self.bg)
        self.WSurf.blit(self.lvlSurf, (0 - self.camera_x, 0 - self.camera_y))

        self.draw_projectiles()
        
        if self.is_paused:
            self.draw_pause_menu()
        else:
            if self.moving_left:
                self.WSurf.blit(self.player_frames_walk_left[self.current_frame], (self.player_pos.x - self.camera_x, self.player_pos.y - self.camera_y))
            elif self.moving_right:
                self.WSurf.blit(self.player_frames_walk_right[self.current_frame], (self.player_pos.x - self.camera_x, self.player_pos.y - self.camera_y))
            else:
                self.WSurf.blit(self.player_frames_idle[self.current_frame], (self.player_pos.x - self.camera_x, self.player_pos.y - self.camera_y))

        for enemy in self.enemies:
            enemy.draw(self.WSurf, self.camera_x, self.camera_y)

        self.WSurf.blit(self.health_image, (10, self.scrH - self.health_image.get_height() - 10))

#IMGANE DE LA VIDA
    def update_health_image(self, health):
        health_image_name = "vida{}.png".format(health)
        self.health_image = pygame.image.load(health_image_name).convert_alpha()
        scale_factor = 5  # Factor de escala, puedes ajustarlo según tus necesidades
        scaled_width = int(self.health_image.get_width() * scale_factor)
        scaled_height = int(self.health_image.get_height() * scale_factor)
        self.health_image = pygame.transform.scale(self.health_image, (scaled_width, scaled_height))

        

        pygame.display.update()
        self.fpsClk.tick(30)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    self.WSurf = pygame.display.set_mode((event.w, event.h), HWSURFACE | DOUBLEBUF | RESIZABLE)
                    self.scrW = event.w
                    self.scrH = event.h

            self.update()
            self.draw()

    def check_game_over(self):
        if self.player_pos.x <= 2477 and self.player_pos.y <= 989:
            pygame.quit()
            sys.exit()
            

if __name__ == '__main__':
    game = IsoGame()
    game.run()


