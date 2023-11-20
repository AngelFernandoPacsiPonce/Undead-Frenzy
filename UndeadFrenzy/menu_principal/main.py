import pygame
import sys
import pygame.mixer
import subprocess
from button import Button

pygame.init()
# PANTALLA
SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Undead Frenzy")
# FONDO DE PANTALLA
BG = pygame.image.load("Background.jpg")

# Declarar las variables de botones como globales
PLAY_BUTTON = None
OPTIONS_BUTTON = None
QUIT_BUTTON = None

def get_font(size):
    return pygame.font.Font("imagenes/font.ttf", size)
#PARTE DE SELECCION DE NIVELES
def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("The Bridge Abyss:", True, "Yellow")
        PLAY_RECT = PLAY_TEXT.get_rect(topleft=(20, 20))

        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        LEVEL_FONT_SIZE = 35
        LEVEL_FONT_COLOR = "White"
        LEVEL_FONT = get_font(LEVEL_FONT_SIZE)

        LEVEL_1_TEXT = LEVEL_FONT.render("1. Comisaría", True, LEVEL_FONT_COLOR)
        LEVEL_1_RECT = LEVEL_1_TEXT.get_rect(topleft=(40, 150))

        LEVEL_2_TEXT = LEVEL_FONT.render("2. Parque", True, LEVEL_FONT_COLOR)
        LEVEL_2_RECT = LEVEL_2_TEXT.get_rect(topleft=(40, 250))

        LEVEL_3_TEXT = LEVEL_FONT.render("3. Puente", True, LEVEL_FONT_COLOR)
        LEVEL_3_RECT = LEVEL_3_TEXT.get_rect(topleft=(40, 350))
#COMISARI COLORCITO
        if LEVEL_1_RECT.collidepoint(PLAY_MOUSE_POS):
            LEVEL_1_COLOR = "Cyan"
        else:
            LEVEL_1_COLOR = "White"

        LEVEL_1_TEXT = LEVEL_FONT.render("1. Comisaría", True, LEVEL_1_COLOR)
#PARQUE COLORCITO
        if LEVEL_2_RECT.collidepoint(PLAY_MOUSE_POS):
            LEVEL_2_COLOR = "Cyan"
        else:
            LEVEL_2_COLOR = "White"

        LEVEL_2_TEXT = LEVEL_FONT.render("2. Parque", True, LEVEL_2_COLOR)


#PUENTE COLORCITO
        if LEVEL_3_RECT.collidepoint(PLAY_MOUSE_POS):
            LEVEL_3_COLOR = "Cyan"
        else:
            LEVEL_3_COLOR = "White"

        LEVEL_3_TEXT = LEVEL_FONT.render("3. Puente", True, LEVEL_3_COLOR)



        SCREEN.blit(LEVEL_1_TEXT, LEVEL_1_RECT)
        SCREEN.blit(LEVEL_2_TEXT, LEVEL_2_RECT)
        SCREEN.blit(LEVEL_3_TEXT, LEVEL_3_RECT)

   

        PLAY_BACK = Button(image=None, pos=(1000, 600), text_input="Retroceder", font=get_font(35),
                           base_color="White", hovering_color="Cyan")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                elif LEVEL_1_RECT.collidepoint(PLAY_MOUSE_POS):
                    subprocess.Popen(["python", "game.py"])
                    pygame.quit()
                    sys.exit()
                elif LEVEL_2_RECT.collidepoint(PLAY_MOUSE_POS):
                    level_selected(2)
                elif LEVEL_3_RECT.collidepoint(PLAY_MOUSE_POS):
                    level_selected(3)

        pygame.display.update()

def level_selected(level):
    print("Nivel seleccionado:", level)
VOLUME = 0.5
#MENU OPCIONES
def options():
    global VOLUME

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("Black")

        OPTIONS_TEXT = get_font(45).render("Opciones", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(topleft=(20, 20))

        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(1000, 600),
                              text_input="Retroceder", font=get_font(25), base_color="White", hovering_color="Cyan")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        VOLUME_TEXT = get_font(35).render(f"Volumen: {int(VOLUME * 100)}", True, "White")
        VOLUME_RECT = VOLUME_TEXT.get_rect(topleft=(40, 150))
        SCREEN.blit(VOLUME_TEXT, VOLUME_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    VOLUME = min(1.0, VOLUME + 0.1)  # Aumentar el volumen en 0.1 (máximo 1.0)
                    pygame.mixer.music.set_volume(VOLUME)  # Aplicar el nuevo volumen al sonido
                elif event.key == pygame.K_DOWN:
                    VOLUME = max(0.0, VOLUME - 0.1)  # Disminuir el volumen en 0.1 (mínimo 0.0)
                    pygame.mixer.music.set_volume(VOLUME)  # Aplicar el nuevo volumen al sonido

        pygame.display.update()

def main_menu():
    global PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, COMISARIA_BUTTON	 # Declarar las variables como globales

    PLAY_BUTTON = Button(image=pygame.image.load("imagenes/Play Rect.png"), pos=(200, 400),
                         text_input="Jugar", font=get_font(35), base_color="#ffffff", hovering_color="Cyan")
    OPTIONS_BUTTON = Button(image=pygame.image.load("imagenes/Options Rect.png"), pos=(200, 500),
                             text_input="Opciones", font=get_font(35), base_color="#ffffff",
                             hovering_color="Cyan")
    QUIT_BUTTON = Button(image=pygame.image.load("imagenes/Quit Rect.png"), pos=(200, 600),
                         text_input="Salir", font=get_font(35), base_color="#ffffff", hovering_color="Cyan")
    COMISARIA_BUTTON = Button(image=None, pos=(500, 250), text_input="Comisaría", font=get_font(30),
                                  base_color="Black", hovering_color="Yellow")
   


    background_images = [
        pygame.image.load("C:/Users/Fernando Ponce/Documents/UndeadFrenzy/menu_principal/fondos/background1.png"),
        pygame.image.load("C:/Users/Fernando Ponce/Documents/UndeadFrenzy/menu_principal/fondos/background2.png"),
        pygame.image.load("C:/Users/Fernando Ponce/Documents/UndeadFrenzy/menu_principal/fondos/background3.png"),
        pygame.image.load("C:/Users/Fernando Ponce/Documents/UndeadFrenzy/menu_principal/fondos/background4.png"),
        pygame.image.load("C:/Users/Fernando Ponce/Documents/UndeadFrenzy/menu_principal/fondos/background5.png"),
        pygame.image.load("C:/Users/Fernando Ponce/Documents/UndeadFrenzy/menu_principal/fondos/background6.png"),
        pygame.image.load("C:/Users/Fernando Ponce/Documents/UndeadFrenzy/menu_principal/fondos/background7.png")
    ]
    background_index = 0

    fade_duration = 20000  # Duración del fade en milisegundos (15 segundos)
    fade_start_time = pygame.time.get_ticks()

    def change_background():
        nonlocal background_index, fade_start_time
        background_index = (background_index + 1) % len(background_images)
        fade_start_time = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        if current_time - fade_start_time >= fade_duration:
            change_background()

        # Superponer los fondos
        for i in range(len(background_images)):
            alpha = max(0, min(255, int((current_time - fade_start_time) / fade_duration * 255)))
            background = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
            background.blit(background_images[i], (0, 0))
            background.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
            SCREEN.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        TITLE_FONT_SIZE = 100
        TITLE_FONT_COLOR = "#FFFF00"
        TITLE_FONT = get_font(TITLE_FONT_SIZE)

        MENU_FONT_SIZE = 40
        MENU_FONT_COLOR = "#ffffff"
        MENU_FONT = get_font(MENU_FONT_SIZE)

        TITLE_TEXT = TITLE_FONT.render("Undead", True, TITLE_FONT_COLOR)
        TITLE_RECT = TITLE_TEXT.get_rect(center=(SCREEN.get_width() // 2, 100))

        FRENZY_TEXT = TITLE_FONT.render("Frenzy", True, TITLE_FONT_COLOR)
        FRENZY_RECT = FRENZY_TEXT.get_rect(center=(SCREEN.get_width() // 2, 100 + TITLE_FONT_SIZE + 10))

        SCREEN.blit(TITLE_TEXT, TITLE_RECT)
        SCREEN.blit(FRENZY_TEXT, FRENZY_RECT)

        PLAY_BUTTON.changeColor(MENU_MOUSE_POS)
        PLAY_BUTTON.update(SCREEN)

        OPTIONS_BUTTON.changeColor(MENU_MOUSE_POS)
        OPTIONS_BUTTON.update(SCREEN)

        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.update(SCREEN)


        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


"""pygame.mixer.music.load("sonidodemenu/menusong.ogg")
pygame.mixer.music.play(-1)  # El argumento -1 hace que la canción se reproduzca en un bucle infinito
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()"""

# Ejecutar el menú principal
main_menu()