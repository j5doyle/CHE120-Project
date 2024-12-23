import pygame
import random

pygame.init()

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

# colours
red = (255, 0, 0)
light_red = (255, 100, 100)
gray = (50, 50, 50)
light_gray = (100, 100, 100)
white = (255, 255, 255)
black = (0, 0, 0)


shots_left = 50
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

hidden_grid = [[0 for i in range(grid_size)] for i in range(grid_size)]  #computer's ships (the hidden board)
visible_grid = [[0 for i in range(grid_size)] for i in range(grid_size)]  #player's hits/misses (the visible board)

menu_running = True #defines the variable and starts the game with the menu starts running

def place_ships(grid): #randomly place's the computer's ships on the grid 
    ships = [5, 4, 3, 3, 2]  #ship lengths
    for ship_length in ships:
        placed = False
        while not placed:
            direction = random.choice(["horizontal", "vertical"])
            if direction == "horizontal":
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - ship_length)
                if all(grid[row][col + i] == 0 for i in range(ship_length)):  #check space
                    for i in range(ship_length):
                        grid[row][col + i] = 1  #place ship
                    placed = True
            else:  # vertical placement
                row = random.randint(0, grid_size - ship_length)
                col = random.randint(0, grid_size - 1)
                if all(grid[row + i][col] == 0 for i in range(ship_length)):  #check space
                    for i in range(ship_length):
                        grid[row + i][col] = 1  #place ship
                    placed = True
    
place_ships(hidden_grid) #places ships immediately as the game is opened for the first game
    
def main_menu():
    menu_running = True
    
    while menu_running:
        screen.blit(menu_bg, (0, 0))

        title_text = title_font.render("BATTLESHIP", True, black)
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 40))

        subtitle_text = subtitle_font.render("CHE 120 EDITION", True, black)
        screen.blit(subtitle_text, (width // 2 - subtitle_text.get_width() // 2, 140))

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
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos): #start btn
                    menu_running = False  #exit menu loop
                if quit_button.collidepoint(event.pos): #quit btn
                    pygame.quit()
                    exit()


def draw_grid_and_labels():
    screen.blit(game_bg, (0, 0))
    
   
    
    title_text = title_font.render("BATTLESHIP", True, black)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 0))
    
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
                
                #^tbh i didnt comment at the time i forget exactly wtf this means

def check_game_over():
    total_ship_cells = sum(sum(1 for cell in row if cell == 1) for row in hidden_grid) #count total ship cells on the hidden grid

    total_hits = sum(sum(1 for cell in row if cell == 1) for row in visible_grid) #count hits on the visible grid
    
    if total_hits == total_ship_cells:
        return True  # game over
    
    return False  # game continues

def draw_game_over():
    game_over_text = "YOU SUNK ALL THE SHIPS!"
    text = button_font.render(game_over_text, True, white)
    pygame.draw.rect(screen, black, (width // 2 - 200, height // 2 - 50, 600, 100))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    play_again_text = "PLAY AGAIN?"
    again_text = button_font.render(play_again_text, True, white)
    pygame.draw.rect(screen, black, again_button)
    screen.blit(again_text, (again_button.x + (again_button.width - again_text.get_width()) // 2,
                             again_button.y + (again_button.height - again_text.get_height()) // 2))

def draw_shots_game_over():
    game_over_text = "GAME OVER"
    text = button_font.render(game_over_text, True, white)
    pygame.draw.rect(screen, black, (width // 2 - 200, height // 2 - 50, 600, 100))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    play_again_text = "PLAY AGAIN?"
    again_text = button_font.render(play_again_text, True, white)
    pygame.draw.rect(screen, black, again_button)
    screen.blit(again_text, (again_button.x + (again_button.width - again_text.get_width()) // 2,
                             again_button.y + (again_button.height - again_text.get_height()) // 2))

def reset_grids():
    for row in range(grid_size):
        for col in range(grid_size):
            hidden_grid[row][col] = 0
            visible_grid[row][col] = 0 #clears ships
            
    place_ships(hidden_grid) #places new ships

def run_game():
    global menu_running
    game_over = False
    shots_game_over = False
    shots_left = 10
    while not menu_running:  #loop while in the game
        draw_grid_and_labels()
        
        
        shots_remaining_text = shorter_font.render(f"SHOTS REMAINING: {shots_left}", True, black)
        screen.blit(shots_remaining_text, (width // 2 - shots_remaining_text.get_width() // 2 - 133, 635))
        
        if game_over:
            draw_game_over()
            
        if shots_game_over:
            draw_shots_game_over()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN: #if there is a left click

                if home_button.collidepoint(event.pos): #if that left click is on the home button
                    menu_running = True  #transition back to the main menu
                    reset_grids()
                    return  #exit the game loop

                #check if the game is over and Play Again button is clicked
                if game_over and again_button.collidepoint(event.pos):
                    reset_grids()

                #check if a grid cell is clicked
                if not game_over:
                    mouse_x, mouse_y = event.pos
                    if grid_x_offset <= mouse_x < grid_x_offset + grid_size * cell_size and \
                       grid_y_offset <= mouse_y < grid_y_offset + grid_size * cell_size:
                        col = (mouse_x - grid_x_offset) // cell_size
                        row = (mouse_y - grid_y_offset) // cell_size

                        #mark hit or miss on player's grid
                        if visible_grid[row][col] == 0:  #if not already clicked (1 would mean already clicked)
                            shots_left -= 1
                            if shots_left <= 0:
                                shots_game_over = True
                            print(shots_left)
                            if hidden_grid[row][col] == 1:  #indeed a ship on cell hit
                                visible_grid[row][col] = 1 #show hit
                            else:  # miss
                                visible_grid[row][col] = -1 #show miss

                        #check win condition
                        if check_game_over():
                            game_over = True

        pygame.display.update()

while True:
    if menu_running:
        main_menu()  #show the main menu initially
        menu_running = False #set to False when exiting the menu (i forget why this works tbh)
    else:
        run_game()  #enter the game loop
