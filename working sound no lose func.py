import pygame
import random
import time

pygame.init()       #initializes pygame
pygame.mixer.init() #initializes the sound mixer

#window dimensions
height = 740
width = 640

#opens & names game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battleship - CHE 120 Edition")

cell_size = 50
grid_size = 10
grid_x_offset = 75  # x-offset of the grid (from left of window)
grid_y_offset = 125  # y-offset of the grid (from top of window)

# colours1
red = (255, 0, 0)
light_red = (255, 100, 100)
gray = (50, 50, 50)
light_gray = (100, 100, 100)
white = (255, 255, 255)
black = (0, 0, 0)

#sound variables 
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
destroy_sound = pygame.mixer.Sound("sounds/destroy.wav")
hit_special = pygame.mixer.Sound("sounds/hit_special.wav")
destroy_special = pygame.mixer.Sound("sounds/destroy_special.wav")
meow = pygame.mixer.Sound("sounds/meow.wav")
seeya = pygame.mixer.Sound("sounds/seeya.mp3")
last_one = pygame.mixer.Sound("sounds/enemy_remaining.mp3")
outro = pygame.mixer.Sound("sounds/outro_song.mp3")
play_again = pygame.mixer.Sound("sounds/one_more.mp3")
home_button_sound = pygame.mixer.Sound("sounds/running.mp3")
epic = pygame.mixer.Sound("sounds/pirates.mp3")
main_sound = pygame.mixer.Sound("sounds/cat.mp3")

#intializing sound channels
channel1 = pygame.mixer.Channel(1) #these allow us to control certain parts of the audio
channel2 = pygame.mixer.Channel(2)

#font variables
font_path = "fonts/ByteBounce.ttf"

title_font = pygame.font.Font(font_path, 120)
button_font = pygame.font.Font(font_path, 50)
subtitle_font = pygame.font.Font(font_path, 40)
shorter_font = pygame.font.Font(font_path, 30)

#images
game_bg = pygame.image.load("images/game bg.png")
menu_bg = pygame.image.load("images/ocean.png")
awesome_cat = pygame.image.load("images/awesome cat.jpg")

#buttons
start_button = pygame.Rect((width - 300) // 2, height // 2 + 80, 300, 80)
quit_button = pygame.Rect((width - 300)// 2, height // 2 + 200, 300, 80)
home_button = pygame.Rect((width - 150)//2, height // 2 + 300, 150, 60)
again_button = pygame.Rect((width - 150)//2, height // 2 + 300, 300, 60)
awesome_cat_click = pygame.Rect(210, 200, 230, 220)

# New: Ship class to track individual ship hits
class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hits = set()
    
    def hit(self, coordinate):
        if coordinate in self.coordinates:
            self.hits.add(coordinate)
            return True
        return False
    
    def is_sunk(self):
        return len(self.hits) == len(self.coordinates)

# Modified ship placement to create Ship objects
def place_ships(grid):
    ships = [5, 4, 3, 3, 2]  # ship lengths
    ship_list = []
    for ship_length in ships:
        placed = False
        while not placed:
            direction = random.choice(["horizontal", "vertical"])
            if direction == "horizontal":
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - ship_length)
                if all(grid[row][col + i] == 0 for i in range(ship_length)):  # check space
                    ship_coords = [(row, col + i) for i in range(ship_length)]
                    ship = Ship(ship_coords)
                    for x, y in ship_coords:
                        grid[x][y] = 1
                    ship_list.append(ship)
                    placed = True
            else:  # vertical placement
                row = random.randint(0, grid_size - ship_length)
                col = random.randint(0, grid_size - 1)
                if all(grid[row + i][col] == 0 for i in range(ship_length)):  # check space
                    ship_coords = [(row + i, col) for i in range(ship_length)]
                    ship = Ship(ship_coords)
                    for x, y in ship_coords:
                        grid[x][y] = 1
                    ship_list.append(ship)
                    placed = True
    return ship_list

hidden_grid = [[0 for i in range(grid_size)] for i in range(grid_size)]  # computer's ships (the hidden board)
visible_grid = [[0 for i in range(grid_size)] for i in range(grid_size)]  # player's hits/misses (the visible board)

menu_running = True  # defines the variable and starts the game with the menu starts running

# Modified to track ships instead of just a hit count
ships = place_ships(hidden_grid)
total_ships = len(ships)  # Store the total number of ships at the start

def main_menu():
    menu_running = True
    channel2.set_volume(0.25)   # this turns on the background music for the main menu
    channel2.play(main_sound,-1)
    
    while menu_running:
        screen.blit(menu_bg, (0, 0))

        title_text = title_font.render("BATTLESHIP", True, black)
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 40))

        subtitle_text = subtitle_font.render("CHE 120 EDITION", True, black)
        screen.blit(subtitle_text, (width // 2 - subtitle_text.get_width() // 2, 140))

        
        pygame.draw.rect(screen, black, awesome_cat_click)
        screen.blit(awesome_cat, (210, 200))

        pygame.draw.rect(screen, black, start_button)
        start_text = button_font.render("START GAME", True, white)
        screen.blit(start_text, (start_button.x + 50, start_button.y + 15))

        pygame.draw.rect(screen, black, quit_button)
        quit_text = button_font.render("QUIT", True, white)
        screen.blit(quit_text, (quit_button.x + 100, quit_button.y + 15))

        credit_text = subtitle_font.render("BY: JOHN, NIK, VIKTOR AND NATHAN", True, black)
        screen.blit(credit_text, (width // 2 - credit_text.get_width() // 2, 680))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                goodbye() #Plays the seeya sound
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if awesome_cat_click.collidepoint(event.pos): #Awesome Easter egg, try to find it!
                    meow.set_volume(1)
                    meow.play()
                if start_button.collidepoint(event.pos): #start btn
                    menu_running = False  #exit menu loop
                if quit_button.collidepoint(event.pos): #quit btn
                    goodbye() #Goodbye sound
                    pygame.quit()
                    exit()

def draw_grid_and_labels():
    screen.blit(game_bg, (0, 0))
    
    title_text = title_font.render("BATTLESHIP", True, black)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 0))
    
    sunken_ships_text = shorter_font.render("Remaining ships:", True, black)
    screen.blit(sunken_ships_text, (width // 2 - sunken_ships_text.get_width() // 2 + 155, 635))
    
    # Count remaining ships (total ships minus sunk ships)
    remaining_ships = total_ships - sum(1 for ship in ships if ship.is_sunk())
    number_ships = shorter_font.render(f"{remaining_ships}", True, black)
    screen.blit(number_ships, (width // 2 - number_ships.get_width() // 2 + 252, 635))
    total_ships - sum(1 for ship in ships if ship.is_sunk())
    pygame.draw.rect(screen, black, home_button)
    home_text = button_font.render("HOME", True, white)
    screen.blit(home_text, (width // 2 - home_text.get_width() // 2, 680))

    for x in range(grid_size + 1):
        pygame.draw.line(screen, black,(grid_x_offset + x * cell_size, grid_y_offset),
            (grid_x_offset + x * cell_size, grid_y_offset + grid_size * cell_size), 4)
    
    for y in range(grid_size + 1):
        pygame.draw.line(screen, black,(grid_x_offset, grid_y_offset + y * cell_size),
            (grid_x_offset + grid_size * cell_size, grid_y_offset + y * cell_size), 4)

    font = pygame.font.Font(font_path, 40)
    for col in range(grid_size):
        label = font.render(chr(65 + col), True, black)
        x = grid_x_offset + col * cell_size + (cell_size // 2 - label.get_width() // 2)
        y = grid_y_offset - 30
        screen.blit(label, (x, y))

    for row in range(grid_size):
        label = font.render(str(row + 1), True, black)
        x = grid_x_offset - 32
        y = grid_y_offset + row * cell_size + (cell_size // 2 - label.get_height() // 2)
        screen.blit(label, (x, y))

    for row in range(grid_size):
        for col in range(grid_size):
            if visible_grid[row][col] == 1:
                pygame.draw.circle(screen, red, (grid_x_offset + col * cell_size + cell_size // 2,
                     grid_y_offset + row * cell_size + cell_size // 2), cell_size // 3)
                pygame.draw.circle(screen, light_red, (grid_x_offset + col * cell_size + cell_size // 2,
                     grid_y_offset + row * cell_size + cell_size // 2), cell_size // 6)
                
            if visible_grid[row][col] == -1:
                pygame.draw.circle(screen, gray, (grid_x_offset + col * cell_size + cell_size // 2,
                                    grid_y_offset + row * cell_size + cell_size // 2), cell_size // 3)
                pygame.draw.circle(screen, light_gray, (grid_x_offset + col * cell_size + cell_size // 2,
                     grid_y_offset + row * cell_size + cell_size // 2), cell_size // 6)

def goodbye(): #the goodbye function plays the seeya track for 1.1 seconds
    seeya.play()
    time.sleep(1.1)

def check_game_over():
    return all(ship.is_sunk() for ship in ships)

def draw_game_over():
    game_over_text = "YOU SUNK ALL THE SHIPS!"
    text = button_font.render(game_over_text, True, white)
    pygame.draw.rect(screen, black, (width // 2 - (text.get_width() + 40) // 2, height // 2 - (text.get_height() + 20) // 2, text.get_width() + 40, text.get_height() + 20))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    play_again_text = "PLAY AGAIN?"
    again_text = button_font.render(play_again_text, True, white)
    pygame.draw.rect(screen, black, again_button)
    screen.blit(again_text, (again_button.x + (again_button.width - again_text.get_width()) // 2,
                             again_button.y + (again_button.height - again_text.get_height()) // 2))

def reset_grids():
    global ships, hidden_grid, visible_grid, total_ships
    for row in range(grid_size):
        for col in range(grid_size):
            hidden_grid[row][col] = 0
            visible_grid[row][col] = 0
    
    hidden_grid = [[0 for i in range(grid_size)] for i in range(grid_size)]
    visible_grid = [[0 for i in range(grid_size)] for i in range(grid_size)]
    ships = place_ships(hidden_grid)
    total_ships = len(ships)  # Reset total ships count

def run_game():
    global menu_running
    game_over = False
    channel2.stop()
    channel1.set_volume(0.35) #Stops the background music for the main menu and begins the intense gameplay music
    channel1.play(epic,-1)
    while not menu_running:  #loop while in the game
        draw_grid_and_labels()
        
        if game_over:
            draw_game_over()
            channel1.stop() #Stops the game background music
            if not pygame.mixer.get_busy(): #Only plays if the outro isnt already playing
                outro.set_volume(0.5)
                outro.play()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Quit function
                channel1.stop()
                channel2.stop()
                goodbye()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN: #if there is a left click

                if home_button.collidepoint(event.pos): #if that left click is on the home button
                    channel1.stop()
                    home_button_sound.play() #Plays a sound when you return to home
                    menu_running = True  #transition back to the main menu
                    reset_grids()
                    return  #exit the game loop

                #check if the game is over and Play Again button is clicked
                if game_over and again_button.collidepoint(event.pos):
                    pygame.mixer.stop()
                    channel1.stop()
                    play_again.play() #Plays a sound when you rpess play again
                    channel1.play(epic)
                    reset_grids()
                    game_over = False

                #check if a grid cell is clicked
                if not game_over:
                    mouse_x, mouse_y = event.pos
                    if grid_x_offset <= mouse_x < grid_x_offset + grid_size * cell_size and \
                       grid_y_offset <= mouse_y < grid_y_offset + grid_size * cell_size:
                        col = (mouse_x - grid_x_offset) // cell_size
                        row = (mouse_y - grid_y_offset) // cell_size
                        
                        #mark hit or miss on player's grid
                        if visible_grid[row][col] == 0:  #if not already clicked
                            # Check if this hit sinks a ship
                            ship_hit = False
                            for ship in ships:
                                temp_random = random.randint(0,100)
                                if (row, col) in ship.coordinates:
                                    ship.hit((row, col))
                                    visible_grid[row][col] = 1  # mark as hit
                                    ship_hit = True
                                    
                                    if temp_random == 69: #Another easter egg :P
                                        hit_special.play()
                                    else:
                                        hit_sound.play() #Plays a sound everytime a ship is hit
                                    
                                    # If ship is sunk, you might want to do something special
                                    if ship.is_sunk():
                                        print("Ship Sunk!")
                                        if temp_random == 69:
                                            destroy_special.play()
                                        else:
                                            destroy_sound.play() #Plays a different sound if a ship is destroyed
                                            
                                        if total_ships - sum(1 for ship in ships if ship.is_sunk()) == 1:
                                            time.sleep(0.4)
                                            last_one.play()
                                    break
                            
                            if not ship_hit:
                                visible_grid[row][col] = -1  # mark as miss

                        #check win condition
                        if check_game_over():
                            game_over = True

        pygame.display.update()

while True:
    if menu_running:
        main_menu()  #show the main menu initially
        menu_running = False #set to False when exiting the menu
    else:
        run_game()  #enter the game loop
