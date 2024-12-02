import pygame
import random
import sys
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

# colours
red = (255, 0, 0)
light_red = (255, 100, 100)
gray = (50, 50, 50)
light_gray = (100, 100, 100)
white = (255, 255, 255)
black = (0, 0, 0)

#font variables
font_path = "fonts/ByteBounce.ttf"

#some preset font sizes for consistency later
title_font = pygame.font.Font(font_path, 120)
button_font = pygame.font.Font(font_path, 50)
subtitle_font = pygame.font.Font(font_path, 38)
tiny_font = pygame.font.Font(font_path, 32)

#images
game_bg = pygame.image.load("images/game bg.png")
menu_bg = pygame.image.load("images/ocean.png")
awesome_cat = pygame.image.load("images/awesome cat.jpg")

#sound variables 
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
destroy_sound = pygame.mixer.Sound("sounds/destroy.wav")
meow = pygame.mixer.Sound("sounds/meow.wav")
seeya = pygame.mixer.Sound("sounds/seeya.mp3")
last_one = pygame.mixer.Sound("sounds/enemy_remaining.mp3")
outro = pygame.mixer.Sound("sounds/outro_song.mp3")
play_again = pygame.mixer.Sound("sounds/one_more.mp3")
home_button_sound = pygame.mixer.Sound("sounds/running.mp3")
epic = pygame.mixer.Sound("sounds/pirates.mp3")
main_sound = pygame.mixer.Sound("sounds/cat.mp3")
losing_sound = pygame.mixer.Sound("sounds/losing_music.mp3")

#intializing sound channels
channel1 = pygame.mixer.Channel(1) #these allow us to control certain parts of the audio
channel2 = pygame.mixer.Channel(2)
channel3 = pygame.mixer.Channel(3)

#buttons
start_button = pygame.Rect((width - 300) // 2, height // 2 + 80, 300, 80)
quit_button = pygame.Rect((width - 300)// 2, height // 2 + 200, 300, 80)
home_button = pygame.Rect((width - 150)//2, height // 2 + 300, 150, 60)
again_button = pygame.Rect((width - 300) // 2, height // 2 + 60, 300, 60)
awesome_cat_click = pygame.Rect(210, 200, 230, 220) #this gives the dimensions of the box containg the cat

hidden_grid = [[0 for i in range(grid_size)] for i in range(grid_size)]  #computer's ships (the hidden board)
visible_grid = [[0 for i in range(grid_size)] for i in range(grid_size)]  #player's hits/misses (the visible board)

menu_running = True #defines the variable and starts the game with the menu starts running
shots_left = 30

def goodbye(): #the goodbye function plays the seeya track for 1.1 seconds
    seeya.play()
    time.sleep(1.1)

def place_ships(grid):  #randomly places the computer's ships on the grid
    ships = [5, 4, 3, 3, 2]  #ship lengths
    ship_id = 2  #start from 2 to differentiate ships
    for ship_length in ships:
        placed = False
        while not placed:
            direction = random.choice(["horizontal", "vertical"])
            if direction == "horizontal":
                row = random.randint(0, grid_size - 1)
                col = random.randint(0, grid_size - ship_length)
                if all(grid[row][col + i] == 0 for i in range(ship_length)):  #check space
                    for i in range(ship_length):
                        grid[row][col + i] = ship_id  #place ship with unique ID
                    placed = True
            else:  #vertical placement
                row = random.randint(0, grid_size - ship_length)
                col = random.randint(0, grid_size - 1)
                if all(grid[row + i][col] == 0 for i in range(ship_length)):  #check space
                    for i in range(ship_length):
                        grid[row + i][col] = ship_id  #place ship with unique ID
                    placed = True
        ship_id += 1  #increment ship_id for the next ship

place_ships(hidden_grid)  #places ships immediately for the first game


def count_remaining_ships(grid):  #counts remaining ships
    remaining_ships = set()
    for row in grid:
        for cell in row: #checking all the positions of the grid
            if cell > 1:  #ship_ids start from 2
                remaining_ships.add(cell)
    return len(remaining_ships)

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

        
        pygame.draw.rect(screen, black, awesome_cat_click) #This creates a button under the cat
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
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if awesome_cat_click.collidepoint(event.pos): #Awesome Easter egg, try to find it!
                    meow.set_volume(1)
                    meow.play()
                if start_button.collidepoint(event.pos): #start btn
                    menu_running = False  #exit menu loop
                if quit_button.collidepoint(event.pos): #quit btn
                    goodbye() #Goodbye sound
                    pygame.quit()
                    sys.exit()


def draw_grid_and_labels():
    screen.blit(game_bg, (0, 0))

    title_text = title_font.render("BATTLESHIP", True, black)
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 0))

    pygame.draw.rect(screen, black, home_button)

    home_text = button_font.render("HOME", True, white)
    screen.blit(home_text, (width // 2 - home_text.get_width() // 2, 680))
    
    shots_remaining_text = subtitle_font.render(f"SHOTS REMAINING: {shots_left}", True, black)
    screen.blit(shots_remaining_text, (10, 635))

    remaining = count_remaining_ships(hidden_grid) #effectively remaining = sum of all unique IDs
    remaining_text = subtitle_font.render("SHIPS REMAINING: " + str(remaining), True, black)
    screen.blit(remaining_text, (350, 635)) #position

    #draw vertical grid lines to divide the columns
    for x in range(grid_size + 1):  #draw one extra line for the right boundary
        pygame.draw.line(screen, black, 
                         (grid_x_offset + x * cell_size, grid_y_offset),  #line start point
                         (grid_x_offset + x * cell_size, grid_y_offset + grid_size * cell_size), 4)  #line end point

    #draw horizontal grid lines to divide the rows
    for y in range(grid_size + 1):  #draw one extra line for the bottom boundary
        pygame.draw.line(screen, black, 
                         (grid_x_offset, grid_y_offset + y * cell_size),  #line start point
                         (grid_x_offset + grid_size * cell_size, grid_y_offset + y * cell_size), 4)  #line end point

    #set the font for the grid labels (letters and numbers)
    font = pygame.font.Font(font_path, 40)

    #draw column labels (A-J) above the grid
    for col in range(grid_size):
        #render the letter corresponding to the current column index
        label = font.render(chr(65 + col), True, black)  #ASCII conversion: 65 is 'A'
        #calculate the label position (centered above the column)
        x = grid_x_offset + col * cell_size + (cell_size // 2 - label.get_width() // 2)
        y = grid_y_offset - 30  #place above the grid
        screen.blit(label, (x, y))  #draw the label on the screen

    #draw row labels (1-10) to the left of the grid
    for row in range(grid_size):
        #render the number corresponding to the current row index
        label = font.render(str(row + 1), True, black)
        #calculate the label position (centered next to the row)
        x = grid_x_offset - 32  #place to the left of the grid
        y = grid_y_offset + row * cell_size + (cell_size // 2 - label.get_height() // 2)
        screen.blit(label, (x, y))  #draw the label on the screen

    #loop through each cell of the grid to draw hits and misses
    for row in range(grid_size):
        for col in range(grid_size):
            if visible_grid[row][col] == 1:  #if the player hit a ship
                #draw a red circle if a hit, (wth a smaller light red circle inside)
                pygame.draw.circle(screen, red, 
                                   (grid_x_offset + col * cell_size + cell_size // 2, 
                                    grid_y_offset + row * cell_size + cell_size // 2), 
                                   cell_size // 3)  #outer circle for the hit
                #draw a smaller, lighter red circle inside the hit for effect
                pygame.draw.circle(screen, light_red, 
                                   (grid_x_offset + col * cell_size + cell_size // 2, 
                                    grid_y_offset + row * cell_size + cell_size // 2), 
                                   cell_size // 6)

            if visible_grid[row][col] == -1:  #if the player missed
                #draw a gray circle if a miss (with a smaller light grey circle inside)
                pygame.draw.circle(screen, gray, 
                                   (grid_x_offset + col * cell_size + cell_size // 2, 
                                    grid_y_offset + row * cell_size + cell_size // 2), 
                                   cell_size // 3)  # Outer circle for the miss
                pygame.draw.circle(screen, light_gray, 
                                   (grid_x_offset + col * cell_size + cell_size // 2, 
                                    grid_y_offset + row * cell_size + cell_size // 2), 
                                   cell_size // 6)

                

def check_game_over():
    #check if all ship parts are hit (no IDs > 1 remain in the hidden grid)
    for row in hidden_grid:
        for cell in row:
            if cell > 1:  #any part of any ship still hasn't been hit
                return False
    return True  #all ships are sunk, game over


def draw_game_over():
    channel2.stop()
    channel1.stop()
    channel3.play(losing_sound)
    text = button_font.render("YOU SUNK ALL THE SHIPS!", True, white)
    pygame.draw.rect(screen, black, (width // 2 - (text.get_width() + 40) // 2, height // 2 - (text.get_height() + 20) // 2, text.get_width() + 40, text.get_height() + 20))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    
    again_text = button_font.render("PLAY AGAIN?", True, white)
    pygame.draw.rect(screen, black, again_button)
    screen.blit(again_text, (again_button.x + (again_button.width - again_text.get_width()) // 2,
                                 again_button.y + (again_button.height - again_text.get_height()) // 2))

def draw_shots_game_over():
    text = button_font.render("YOU RAN OUT OF SHOTS!", True, white)
    pygame.draw.rect(screen, black, (width // 2 - (text.get_width() + 40) // 2, height // 2 - (text.get_height() + 20) // 2, text.get_width() + 40, text.get_height() + 20))
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))


    again_text = button_font.render("PLAY AGAIN?", True, white)
    pygame.draw.rect(screen, black, again_button)
    screen.blit(again_text, (again_button.x + (again_button.width - again_text.get_width()) // 2,
                             again_button.y + (again_button.height - again_text.get_height()) // 2))


def reset_grids():
    global shots_left
    for row in range(grid_size):
        for col in range(grid_size):
            hidden_grid[row][col] = 0 
            visible_grid[row][col] = 0 #clears ships
            
    place_ships(hidden_grid) #places new ships
    shots_left = 30 #resets your shots

def run_game():
    global menu_running
    global shots_left
    game_over = False
    shots_game_over = False
    list = []
    
    channel3.stop()
    channel2.stop()
    channel1.set_volume(0.35) #Stops the background music for the main menu and begins the intense gameplay music
    channel1.play(epic,-1)

    while not menu_running:  #loop while in the game
        draw_grid_and_labels() #display game

        if game_over:
            draw_game_over()
            channel1.stop() #Stops the game background music
            if not pygame.mixer.get_busy(): #Only plays if the outro isnt already playing
                outro.set_volume(0.5)
                outro.play()
            
        if shots_game_over:
            draw_shots_game_over()
            channel1.stop() #Stops the game background music
            if not pygame.mixer.get_busy(): #Only plays if the outro isnt already playing
                losing_sound.set_volume(0.5)
                losing_sound.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                channel1.stop()
                channel2.stop()
                goodbye()
                
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  #if there is a left click
                if home_button.collidepoint(event.pos):  #if click is on the home button
                    pygame.mixer.stop()
                    channel1.stop()

                    home_button_sound.play() #plays a sound when you return to home                
                
                    menu_running = True  #transition back to the main menu
                    reset_grids()
                    return  #exit the game loop

                if game_over or shots_game_over and again_button.collidepoint(event.pos):  #play again button
                    pygame.mixer.stop()
                    channel1.stop()
                    play_again.play() #Plays a sound when you rpess play again
                    channel1.play(epic)
                
                    reset_grids()
                    game_over = False  #reset game state 
                    shots_game_over = False 
                    
                    continue  #restart game loop

                #check if a grid cell is clicked
                if not game_over:
                    mouse_x, mouse_y = event.pos
                    if grid_x_offset <= mouse_x < grid_x_offset + grid_size * cell_size and \
                            grid_y_offset <= mouse_y < grid_y_offset + grid_size * cell_size:
                        col = (mouse_x - grid_x_offset) // cell_size
                        row = (mouse_y - grid_y_offset) // cell_size

                        #mark hit or miss on player's grid
                        if visible_grid[row][col] == 0:  #if not already clicked
                            if hidden_grid[row][col] > 1:  #if it's a ship part
                                visible_grid[row][col] = 1  #show hit
                                hidden_grid[row][col] = 0  #mark as hit on hidden grid
                                hit_sound.play() #BOOOOOOOOM
                                
                                list.append(count_remaining_ships(hidden_grid))
                                if len(list) > 1:
                                    if list[-1] < list[-2]:  #compare the last and second-to-last entries
                                        destroy_sound.play()        
                                    
                                        if list[-1] == 1:
                                            last_one.play()                                       
                                    else:
                                        continue
                            
                            else:  #miss
                                visible_grid[row][col] = -1  #show miss
                                
                                shots_left -= 1 #you lose a shot if you miss
                                print(shots_left)
                                if shots_left <= 0: #if you run out of shots, the game ends
                                    shots_game_over = True

                        #check win condition after each click
                        if check_game_over():
                            game_over = True

        pygame.display.update()


while True:
    if menu_running:
        main_menu()  #show the main menu initially
        menu_running = False #set to False when exiting the menu
    else:
        run_game()  #enter the game loop