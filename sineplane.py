"""cos/sin graph surfer
   Caelan Thomas, 2/09/2016

   The main file for the program.

   A 'Level' is broken up into 'Chunks' - a ten second block of
   obstacles. Each level contains a few chunks, and each chunk
   contains a dictionary with 250 entries - one for each of 25
   ticks per second for 10 seconds - when the current tick matches
   one in the chunk dictionary, the specified obstacle in the chunk
   dictionary is created on screen.

   For the level title screens, the tick number is set to -50 ->
   allowing 2 seconds for the title to be displayed. The rest of
   the code runs when the tick counter reaches 0.

   Eventually, an endless mode will be implemented by taking a
   random selection of the level chunks and simply putting them
   together.
"""
from tkinter import *
from sineplane_constants import *
import math
import time
import random
from PIL import Image, ImageTk
import pygame


class LevelChunk:
    """250 ticks long (10 seconds), holds all obstacle creation code"""
    def __init__(self):
        self.tick_signals = {}


class Plane:
    """The player piece"""
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        self.color = PLANE_COLOR
        
        
class Obstacle:
    """An obstacle that will kill the player on collision"""
    def __init__(self, x_pos, y_pos, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        
        self.color = OBSTACLE_COLOR
        
    def intersects_with(self, plane):
        """
        Checks if the obstacle intersects with the player
        Keyword Arguments:
            plane -- The instance of plane to check if the obstacle intersects
        """
        if self.x_pos < plane.x_pos + PLANE_WIDTH / 2 and \
        self.x_pos + self.width > plane.x_pos - PLANE_WIDTH / 2 and \
        self.y_pos < plane.y_pos + PLANE_HEIGHT / 2 and \
        self.y_pos + self.height > plane.y_pos - PLANE_HEIGHT / 2:
            return True
        return False
    
    
class SinWave:
    """The sin wave showing trajectory"""
    def __init__(self):
        self.angle = 0
        self.period = SIN_STARTING_PERIOD
        
        
class Level:
    """A collection of chunks that make up a level in the game"""
    def __init__(self, chunks, title):
        self.chunks = chunks

        self.title = title
        
        self.index = -1
        
    def chunks_left(self):
        """
        Returns the number of chunks left in the level
        """
        if self.index >= len(self.chunks) - 1:
            return False
        return True
    
    def next_chunk(self):
        """
        Moves the level onto the next level chunk
        """
        self.index += 1
        return self.chunks[self.index]
    
    
class LevelSelectButton:
    """The buttons in the classic menu screen for selecting level"""
    def __init__(self, level_number, unlocked, x_pos, y_pos, width, height, bg, fg, font, canvas):
        self.level_number = level_number
        self.unlocked = unlocked
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.bg = bg
        self.fg = fg
        self.font = font
        
        self.canvas = canvas
        
        self.create_self_as_button()
        
    def create_self_as_button(self):
        """
        Sets the button as a tkinter button and gives it an id number for easy reference later
        """
        self.button = Label(self.canvas, font=self.font, fg=self.fg, bg=self.bg, text=self.level_number)
        self.button.id_no = self.level_number
        

class GUI:
    """Graphics class"""
    def __init__(self, parent, easy_chunks, medium_chunks, hard_chunks, levels):
        self.parent = parent
        
        # Overriding the X press
        self.parent.protocol('WM_DELETE_WINDOW', self.exit_button_press)
        
        self.easy_chunks = easy_chunks
        self.medium_chunks = medium_chunks
        self.hard_chunks = hard_chunks
        
        self.levels = levels
             
        # Logo image
        log("Loading logo")
        t = time.time()
        self.pil_logo = Image.open("assets\images\sine_surfer_logo.png")
        self.logo_image = ImageTk.PhotoImage(self.pil_logo)
        log("Successfully loaded logo")
        log("Time taken: {}s".format(time.time() - t))
        
        # Music
        log("Loading music")
        t = time.time()
        pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
        pygame.init() #turn all of pygame on.        
        self.music = pygame.mixer.Sound(file="assets\music\sine_surfer_music.wav")
        self.music.play(loops=-1)
        log("Successfully loaded music")
        log("Time taken: {}s".format(time.time() - t))        
        
        self.setup()
        
        
    def setup(self):
        """Sets up the starting variables for the game"""
        self.parent.title(WINDOW_TITLE)
        
        # Game variables
        self.run_mode = None
        self.current_level = -1
        self.dead = False
        
        # Setting up the player
        self.plane = Plane(PLANE_STARTING_X, WINDOW_HEIGHT / 2)
        
        # Setting up obstacles
        self.obstacles = []
        
        # Setting up sin wave
        self.sin = SinWave()
        
        # Setting up the drawing canvas
        self.canvas = Canvas(self.parent, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=CANVAS_BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.pack(padx=0, pady=0, ipadx=0, ipady=0)
        
        # Binding key presses
        self.right = False
        self.left = False
        self.parent.bind("<a>", self.left_press)
        self.parent.bind("<d>", self.right_press)
        self.parent.bind("<KeyRelease-a>", self.left_release)
        self.parent.bind("<KeyRelease-d>", self.right_release)
        self.parent.bind("<Left>", self.left_press)
        self.parent.bind("<Right>", self.right_press)
        self.parent.bind("<KeyRelease-Left>", self.left_release)
        self.parent.bind("<KeyRelease-Right>", self.right_release)  
        self.parent.bind("<Escape>", self.escape)
        
        # Setting up chunk ticks
        self.chunk_tick = 0
        self.chunk = None
        
        # Setting up level select buttons
        self.create_level_buttons()
        self.current_level = -1
        self.complete = False
        self.finished_game = False
        
        self.back_to_main_menu_button = Label(self.canvas, bg=START_MENU_BUTTON_BACKGROUND_COLOR, font=START_MENU_BUTTON_FONT, fg=START_MENU_BUTTON_TEXT_COLOR, text="BACK TO MAIN MENU")
        
        # Logo
        self.logo = Label(self.canvas, image=self.logo_image, highlightthickness=0, bd=0)
        
        # Loads the main screen
        self.main_screen()
        
    def main_screen(self, event=None):
        """Sets up the starting screen for the game"""
        self.canvas.delete("all")
        
        # Logo
        self.canvas.create_window((WINDOW_WIDTH) / 2, LOGO_Y, window=self.logo)
        
        # Classic button
        self.play_classic_button = Label(self.canvas, bg=START_MENU_BUTTON_BACKGROUND_COLOR, font=START_MENU_BUTTON_FONT, fg=START_MENU_BUTTON_TEXT_COLOR, text="PLAY")
        self.play_classic_button.bind("<Button-1>", self.play_classic_button_press)

        self.canvas.create_window((WINDOW_WIDTH) / 2, START_MENU_BUTTON_STARTING_Y_POS + START_MENU_BUTTON_SPACING, window=self.play_classic_button, width=START_MENU_BUTTON_WIDTH, height=START_MENU_BUTTON_HEIGHT)

        # How to play button
        self.how_to_play_button = Label(self.canvas, bg=START_MENU_BUTTON_BACKGROUND_COLOR, font=START_MENU_BUTTON_FONT, fg=START_MENU_BUTTON_TEXT_COLOR, text="HOW TO PLAY")
        self.how_to_play_button.bind("<Button-1>", self.how_to_play_button_press)
        
        self.canvas.create_window((WINDOW_WIDTH) / 2, START_MENU_BUTTON_STARTING_Y_POS + 2 * START_MENU_BUTTON_SPACING, window=self.how_to_play_button, width=START_MENU_BUTTON_WIDTH, height=START_MENU_BUTTON_HEIGHT)         
        
        # Exit button
        self.exit_button = Label(self.canvas, bg=START_MENU_BUTTON_BACKGROUND_COLOR, font=START_MENU_BUTTON_FONT, fg=START_MENU_BUTTON_TEXT_COLOR, text="EXIT")
        self.exit_button.bind("<Button-1>", self.exit_button_press)
        
        self.canvas.create_window((WINDOW_WIDTH) / 2, START_MENU_BUTTON_STARTING_Y_POS + 3 * START_MENU_BUTTON_SPACING, window=self.exit_button, width=START_MENU_BUTTON_WIDTH, height=START_MENU_BUTTON_HEIGHT)            


    def options_button_press(self, event=None):
        """Sets up the options menu screen"""
        log("Options Press")
        # Music on/off, sound on/off etc.

        # Note: Does not exist anymore
        # TO BE IMPLEMENTED LATER
        
        
    def exit_button_press(self, event=None):
        """Quits the game"""
        self.music.stop()
        self.parent.destroy()
        
        
    def how_to_play_button_press(self, event=None):
        """Displays the help menu"""
        # Sets up the screen
        self.canvas.delete("all")   
        
        # Logo
        self.canvas.create_window((WINDOW_WIDTH) / 2, LOGO_CLASSIC_Y, window=self.logo)  
        
        # Help Menu Label
        self.help_label = Label(self.canvas, font=HELP_LABEL_FONT, bg=HELP_LABEL_BG, fg=HELP_LABEL_FG, highlightthickness=0, bd=0, text="Use the left/right arrow keys, or a/d keys to adjust your trajectory to make sure you don't collide with any of the white obstacles. \n\n\nPressing the Escape key while in a level will take you back to the level select screen.\n\n\nGood Luck!", wraplength = WINDOW_WIDTH-100, justify=LEFT)
        self.canvas.create_window((WINDOW_WIDTH) / 2, HELP_LABEL_Y, window=self.help_label, width=WINDOW_WIDTH-100)
        
        # Back to main menu button
        self.back_to_main_menu_button.bind("<Button-1>", self.main_screen)
        self.canvas.create_window(BACK_X, BACK_Y, width=BACK_WIDTH, height=BACK_HEIGHT, window = self.back_to_main_menu_button)        
        

    def play_classic_button_press(self, event=None):
        """Sets up the classic menu screen"""
        self.run_mode = "Classic"
        
        # Sets up the screen
        self.canvas.delete("all")
        
        # Logo
        self.canvas.create_window((WINDOW_WIDTH) / 2, LOGO_CLASSIC_Y, window=self.logo)        
        
        for button in self.level_buttons:
            if self.finished_game:
                button.button.config(fg=CLASSIC_MENU_FINISHED_FG, bg=CLASSIC_MENU_FINISHED_BG)
            elif not button.unlocked:
                button.button.config(fg=CLASSIC_MENU_LOCKED_FG, bg=CLASSIC_MENU_LOCKED_BG)
            else:
                button.button.config(fg=CLASSIC_MENU_BUTTON_FG, bg=CLASSIC_MENU_BUTTON_BG)
                
            self.canvas.create_window(button.x_pos,
                                      button.y_pos,
                                      width=button.width,
                                      height=button.height,
                                      window=button.button)
                
            
        # Back to main menu button
        self.back_to_main_menu_button.bind("<Button-1>", self.main_screen)
        self.canvas.create_window(BACK_X, BACK_Y, width=BACK_WIDTH, height=BACK_HEIGHT, window = self.back_to_main_menu_button)
        

    def play_endless_button_press(self, event=None):
        """
        Runs the game in endless mode
        Keyword Arguments:
            event -- the tkinter event parameter automatically passed for some callbacks, creates error safety
        """
        self.run_mode = "Endless"
        self.run_game()
    
        
    def left_press(self, event=None):
        """
        Runs when the left key is pressed
        Keyword Arguments:
            event -- the tkinter event parameter automatically passed for some callbacks, creates error safety
        """
        if not self.right:
            self.left = True
            
    
    def right_press(self, event=None):
        """
        Runs when the right key is pressed
        Keyword Arguments:
            event -- the tkinter event parameter automatically passed for some callbacks, creates error safety
        """
        if not self.left:
            self.right = True
            
            
    def left_release(self, event=None):
        """
        Runs when the left key is released
        Keyword Arguments:
            event -- the tkinter event parameter automatically passed for some callbacks, creates error safety
        """
        self.left = False
        
        
    def right_release(self, event=None):
        """
        Runs when the right key is released
        Keyword Arguments:
            event -- the tkinter event parameter automatically passed for some callbacks, creates error safety
        """
        self.right = False
        
        
    def escape(self, event=None):
        """
        Runs when the escape key is pressed
        Keyword Arguments:
            event -- the tkinter event parameter automatically passed for some callbacks, creates error safety
        """
        self.dead = True
        
        
    def create_level_buttons(self):
        """
        Creates the level select buttons on the screen and unlocks the correct ones.
        """
        # self, level_number, x_pos, y__pos, width, height, bg, fg, font, canvas):
        self.level_buttons = []
        for i in range(NUMBER_OF_LEVELS):
            self.level_buttons.append(LevelSelectButton(i + 1, 
                                                        False, 
                                                        CLASSIC_MENU_BUTTON_X + (i % 10) * CLASSIC_MENU_BUTTON_SPACING,
                                                        CLASSIC_MENU_BUTTON_Y + (int(i/10)) * CLASSIC_MENU_BUTTON_SPACING,
                                                        CLASSIC_MENU_BUTTON_WIDTH,
                                                        CLASSIC_MENU_BUTTON_HEIGHT,
                                                        CLASSIC_MENU_BUTTON_BG,
                                                        CLASSIC_MENU_BUTTON_FG,
                                                        CLASSIC_MENU_BUTTON_FONT,
                                                        self.canvas))
            self.level_buttons[i].button.bind("<Button-1>", self.level_select_press)
            
        # Unlocking first level
        self.level_buttons[0].unlocked = True
        
        # Unlocking all the levels for testing purposes, will not be in the release version
        if CHEAT:
            for button in self.level_buttons:
                button.unlocked = True
        
 
        
    def level_select_press(self, event=None, level=None):
        """Callback for when a classic level is selected"""
        if not event is None:
            level = event.widget.id_no

        if self.level_buttons[level - 1].unlocked:
            # Resetting obstacles
            self.obstacles = []
                
            self.levels[self.current_level].index = -1
                
            self.current_level = level - 1
            self.dead = False
            self.complete = False
            self.sin.period = 800
            self.chunk_tick = -50 # Gives 2 seconds to display text
            self.run_game()
            
        if self.complete and self.current_level < 19:
            self.level_select_press(level=self.current_level + 2)
        if self.dead:
            self.play_classic_button_press()
    
    
    def run_game(self, event=None):
        """Main run loop"""
        self.sin.period = SIN_STARTING_PERIOD

        # A workaround to get the sin wave starting correctly
        self.left_press()
        self.calculate_sin()
        self.left_release()

        # The main run loop
        while not self.dead and not self.complete and not self.finished_game:
            #print(self.chunk_tick)
            t = time.time()
            self.tick()
            # Making sure that each tick is only 0.04 seconds (25 fps)
            t2 = (time.time() - t)
            if t2 < 0.04:
                time.sleep(0.04 - t2)
                
        if self.run_mode == "Endless":
            # Has died in survival mode, handle it here
            self.main_screen()
                
        
            
            
    def tick(self):
        """Runs every tick, updates canvas, does calculations, detects collisions etc"""
        self.canvas.delete("all")
        
        # Create new obstacles
            
        # Using chunks
        if self.run_mode == "Classic":
            if self.chunk_tick < 0:
                # Print level title
                self.canvas.create_window(WINDOW_WIDTH/2,
                                          WINDOW_HEIGHT/2,
                                          width=WINDOW_WIDTH,
                                          height=TITLE_HEIGHT,
                                          window=Label(self.canvas, 
                                                       fg=TITLE_FG,
                                                       bg=TITLE_BG,
                                                       font=TITLE_FONT,
                                                       text=self.levels[self.current_level].title))
            if self.chunk_tick == 0:
                if self.levels[self.current_level].chunks_left():
                    self.chunk = self.levels[self.current_level].next_chunk()
                else:
                    # Level is complete when all obstacles are off screen
                    if len(self.obstacles) > 0:
                        self.chunk_tick = -1
                    else:
                        # FINISHED!!
                        
                        # Unlocking next level
                        if self.current_level == 19:
                            self.complete = True
                            self.finished_game = True
                            # Finished whole game
                            return self.main_screen()
                        else:
                            self.level_buttons[self.current_level + 1].unlocked = True
                            self.complete = True
                            
                
            if self.chunk_tick > 0 and self.chunk_tick in self.chunk.tick_signals.keys():
                x_pos, y_pos, width, height = self.chunk.tick_signals[self.chunk_tick]
                self.obstacles.append(Obstacle(x_pos, y_pos, width, height))
            
            # Allowing for title screen => not mod 250 if the chink tick is below zero
            if self.chunk_tick >= 0:    
                self.chunk_tick = (self.chunk_tick + 1) % 250
            else:
                self.chunk_tick += 1
            
        elif self.run_mode == "Endless":
            if self.chunk_tick == 0:
                self.chunk = self.easy_chunks[1]
                
            if self.chunk_tick in self.chunk.tick_signals.keys():
                y_pos, width, height = self.chunk.tick_signals[self.chunk_tick]
                self.obstacles.append(Obstacle(y_pos, width, height))
                
            self.chunk_tick = (self.chunk_tick + 1) % 250            
        
        
        # If chunk_tick is below zero then the title is being displayed, don't draw everything
        if self.chunk_tick >=0:
            
            # Move obstacles (left/right)
            obstacles_to_delete = []
            for obstacle in self.obstacles:
                obstacle.x_pos -= MOVESPEED
                if obstacle.x_pos + obstacle.width < 0:
                    obstacles_to_delete.append(obstacle)
                self.canvas.create_rectangle(obstacle.x_pos, obstacle.y_pos, obstacle.x_pos + obstacle.width, obstacle.y_pos + obstacle.height, fill=obstacle.color, width=0)
                
            for obstacle in obstacles_to_delete:
                self.obstacles.remove(obstacle)
            
            # Set plane position to starting sin curve height 
            # (sin curve calculation is correct, saves doing all the maths twice,
            # and eliminates any mathematical errors/rounding errors etc.)
            self.plane.y_pos = WINDOW_HEIGHT/2 + SIN_AMPLITUDE*math.sin(self.sin.angle)
            
            
            # Detect collisions
            for obstacle in self.obstacles:
                if obstacle.intersects_with(self.plane):
                    self.collision_handler()
                    return
            
            # Recalcculate sin line
            self.calculate_sin()
                
            # Drawing the sin curve (after obstacles so it can be seen over the obstacles)
            if self.current_level < 18: # Do not draw the sin wave for the last 2 levels
                self.draw_sin()
                
            # Draw plane last so it is always on the top
            self.canvas.create_rectangle(self.plane.x_pos - PLANE_WIDTH / 2, self.plane.y_pos - PLANE_WIDTH / 2, self.plane.x_pos + PLANE_WIDTH / 2, self.plane.y_pos + PLANE_WIDTH / 2, fill=self.plane.color)
            
        # Updates the canvas after everything has been calculated/moved    
        self.canvas.update()
        
        
    def calculate_sin(self):
        """Calculates the positions of the sin curve"""
        # Recalcculate sin line
        if self.right:
            self.sin.period = self.sin.period * SIN_CHANGE_RATE
        if self.left:
            self.sin.period = self.sin.period / SIN_CHANGE_RATE

       # Update sin angle
        self.sin.angle = self.sin.angle + 2*math.pi*(MOVESPEED/self.sin.period)
        if self.sin.angle > 2*math.pi:
            self.sin.angle = self.sin.angle - 2*math.pi        
        
        
    def draw_sin(self):
        """Draws the sin curve, used for modularising the code"""
        
        # Max number of arguments in a function call is 255
        # So splitting the line up into 4 parts to be drawn
        # Actually 4 create line function calls, all having less than 255 arguments
        
        xcoord = PLANE_STARTING_X
        iterations = 1      
            
        for i in range(4):
            temp_string = "self.canvas.create_line(PLANE_STARTING_X + {0} * SIN_PLOT_POINT_DISTANCE, WINDOW_HEIGHT/2 + SIN_AMPLITUDE*math.sin(self.sin.angle + {0} * SIN_PLOT_POINT_DISTANCE/self.sin.period*2*math.pi), ".format(iterations - 1)
            
            while xcoord < WINDOW_WIDTH/4 * (i + 1):
                temp_string = temp_string + "PLANE_STARTING_X + {0} * SIN_PLOT_POINT_DISTANCE, WINDOW_HEIGHT/2 + SIN_AMPLITUDE*math.sin(self.sin.angle + {0} * SIN_PLOT_POINT_DISTANCE/self.sin.period*2*math.pi), ".format(iterations)
                iterations += 1
                xcoord += SIN_PLOT_POINT_DISTANCE
                
            temp_string = temp_string + "fill = SIN_COLOR)"
            
            eval(temp_string)         
        
        
    def collision_handler(self):
        """Handles collisions between plane and obstacle"""
        self.canvas.delete("all")
        self.dead = True
    
    
    
def log(s):
    """Logs into console"""
    if LOGGING:
        print(s)
        
        
def create_chunks():
    """Creates all the level chunks"""
    easy_chunks = []
    medium_chunks = []
    hard_chunks = []
    
    # Create chunks
    # Of the form: temp_chunk.tick_signals[tick] = (x_pos, y_pos, width, height)
    
    # Note that a chunk which will create no obstacles for 250 ticks (10 seconds)
    #  can simply be created by chunk = LevelChunk().
    
    # Predictable
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH, 300, 50, 300)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 300, 50, 300)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[126] = (WINDOW_WIDTH, 300, 50, 300)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH, 300, 50, 300)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 300, 50, 300)
    easy_chunks.append(temp_chunk)
    
    # Unpredictable
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH,   0, 50, 400)
    easy_chunks.append(temp_chunk)    
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH,   0, 50, 400)    
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 200, 50, 400)
    easy_chunks.append(temp_chunk)     
    
    # Short and tall
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH,   0, 50, 200)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH,   0, 50, 200)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH, 400, 50, 200)
    temp_chunk.tick_signals[126] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH, 400, 50, 200)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 200, 50, 400)
    easy_chunks.append(temp_chunk)       

    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH,   0, 50, 100)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH,   0, 50, 400)    
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH, 500, 50, 100)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 400, 50, 200)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH,   0, 50, 200)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH,   0, 50, 200)
    easy_chunks.append(temp_chunk) 
    
    # And off the wall
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 200, 50, 200)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 250, 50, 100)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH, 200, 50, 200)
    temp_chunk.tick_signals[126] = (WINDOW_WIDTH, 150, 50, 300)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH, 250, 50, 100)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH, 250, 50, 100)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 250, 50, 100)
    easy_chunks.append(temp_chunk)
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 250, 50, 100)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH, 200, 50, 200)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 200, 50, 200)
    temp_chunk.tick_signals[126] = (WINDOW_WIDTH, 250, 50, 200)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 100, 50, 250)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH, 300, 50, 150)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 100, 50, 200)
    easy_chunks.append(temp_chunk)    
    
    # Fat and thin
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 250,200, 100)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 250,200, 100)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH, 100,200, 100)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 400,200, 100)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH, 100,200, 100)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 400,200, 100)
    easy_chunks.append(temp_chunk)    

    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 200, 100, 10)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH, 250, 100, 10)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 300, 100, 10)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 350, 100, 10)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH, 400, 100, 10)
    temp_chunk.tick_signals[126] = (WINDOW_WIDTH, 450, 100, 10)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 200, 100, 10)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH, 450, 100, 10)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH, 500, 100, 10)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 150, 100, 10)
    easy_chunks.append(temp_chunk)    
    
    # Heartbeat
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH,   0, 30, 320)
    temp_chunk.tick_signals[61]  = (WINDOW_WIDTH, 280, 30, 320)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH,   0, 30, 320)
    temp_chunk.tick_signals[161] = (WINDOW_WIDTH, 280, 30, 320)
    easy_chunks.append(temp_chunk)    
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 280, 30, 320)
    temp_chunk.tick_signals[61]  = (WINDOW_WIDTH,   0, 30, 320)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 280, 30, 320)
    temp_chunk.tick_signals[161] = (WINDOW_WIDTH,   0, 30, 320)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH, 280, 30, 320)
    temp_chunk.tick_signals[211] = (WINDOW_WIDTH,   0, 30, 320)
    easy_chunks.append(temp_chunk)  
    
    #Combo
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 280, 30, 320)
    temp_chunk.tick_signals[161] = (WINDOW_WIDTH,   0, 30, 320)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH,   0, 50, 200)
    easy_chunks.append(temp_chunk)    

    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 200, 100, 10)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH, 500, 100, 10)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 300, 100,100)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 400, 100, 10)
    temp_chunk.tick_signals[126] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 300, 50, 300)
    easy_chunks.append(temp_chunk) 
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 300, 50, 300)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 300, 50, 300)    
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH, 300, 50, 300)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH,   0, 30, 320)
    temp_chunk.tick_signals[161] = (WINDOW_WIDTH, 280, 30, 320)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH,   0, 30, 320)
    temp_chunk.tick_signals[211] = (WINDOW_WIDTH, 280, 30, 320)
    easy_chunks.append(temp_chunk)     
    
    # The aim of the game
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 300, 50, 300)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 300, 50, 300)
    easy_chunks.append(temp_chunk)    
    
    # Faster
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[16]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[31]  = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[46]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[61]  = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[91]  = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[106] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[121] = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[136] = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[166] = (WINDOW_WIDTH, 200, 50, 400)  
    temp_chunk.tick_signals[181] = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[196] = (WINDOW_WIDTH, 200, 50, 400)    
    temp_chunk.tick_signals[211] = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 200, 50, 400)
    medium_chunks.append(temp_chunk) 
    
    # Morse Code
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 290, 200, 30)
    temp_chunk.tick_signals[31]  = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[46]  = (WINDOW_WIDTH, 290, 200, 30)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[91]  = (WINDOW_WIDTH, 290, 200, 30)
    temp_chunk.tick_signals[121] = (WINDOW_WIDTH, 290, 200, 30)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[166] = (WINDOW_WIDTH, 290, 200, 30)  
    temp_chunk.tick_signals[196] = (WINDOW_WIDTH, 290, 200, 30)   
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 290, 200, 30) 
    medium_chunks.append(temp_chunk)  
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[5 + 1]   = (WINDOW_WIDTH, 290, 200, 30) 
    temp_chunk.tick_signals[5 + 31]  = (WINDOW_WIDTH, 290, 200, 30) 
    temp_chunk.tick_signals[5 + 61]  = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[5 + 76]  = (WINDOW_WIDTH, 290, 200, 30) 
    temp_chunk.tick_signals[5 + 106] = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[5 + 121] = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[5 + 136] = (WINDOW_WIDTH, 290, 200, 30)
    temp_chunk.tick_signals[5 + 166] = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[5 + 181] = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[5 + 196] = (WINDOW_WIDTH, 290, 80, 30)    
    temp_chunk.tick_signals[5 + 211] = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[5 + 226] = (WINDOW_WIDTH, 290, 80, 30)
    temp_chunk.tick_signals[5 + 241] = (WINDOW_WIDTH, 290, 80, 30)    
    medium_chunks.append(temp_chunk)      
    
    # Flappy Bird?
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH + 10,   0, 50, 200)
    temp_chunk.tick_signals[2]   = (WINDOW_WIDTH,      400, 50, 200)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH + 10,   0, 50, 100)
    temp_chunk.tick_signals[52]  = (WINDOW_WIDTH,      300, 50, 300)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH + 10,   0, 50, 300)
    temp_chunk.tick_signals[102] = (WINDOW_WIDTH,      500, 50, 100)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH + 10,   0, 50, 200)
    temp_chunk.tick_signals[152] = (WINDOW_WIDTH,      400, 50, 200)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH + 10,   0, 50, 300)
    temp_chunk.tick_signals[202] = (WINDOW_WIDTH,      500, 50, 100)
    medium_chunks.append(temp_chunk) 
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH + 10,   0, 50,  50)
    temp_chunk.tick_signals[2]   = (WINDOW_WIDTH,      250, 50, 350)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH + 10,   0, 50, 200)
    temp_chunk.tick_signals[52]  = (WINDOW_WIDTH,      400, 50, 200)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH + 10,   0, 50, 350)
    temp_chunk.tick_signals[102] = (WINDOW_WIDTH,      550, 50,  50)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH + 10,   0, 50, 200)
    temp_chunk.tick_signals[152] = (WINDOW_WIDTH,      400, 50, 200)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH + 10,   0, 50, 200)
    temp_chunk.tick_signals[202] = (WINDOW_WIDTH,      400, 50, 200)
    medium_chunks.append(temp_chunk)   
    
    # Choices
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH + 20,   0, 50,  50)
    temp_chunk.tick_signals[2]   = (WINDOW_WIDTH + 10, 150, 50, 100)
    temp_chunk.tick_signals[3]   = (WINDOW_WIDTH,      420, 50, 180)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH + 20,   0, 50,  50)
    temp_chunk.tick_signals[52]  = (WINDOW_WIDTH + 10, 100, 50, 200)
    temp_chunk.tick_signals[53]  = (WINDOW_WIDTH,      480, 50, 120)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH + 20,   0, 50, 200)
    temp_chunk.tick_signals[102] = (WINDOW_WIDTH + 10, 380, 50,  50)
    temp_chunk.tick_signals[103] = (WINDOW_WIDTH,      500, 50, 100)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH + 20,   0, 50, 100)
    temp_chunk.tick_signals[177] = (WINDOW_WIDTH + 10, 280, 50, 200)
    temp_chunk.tick_signals[178] = (WINDOW_WIDTH,      580, 50,  20)
    medium_chunks.append(temp_chunk)  
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH + 30,   0, 50,  30)
    temp_chunk.tick_signals[2]   = (WINDOW_WIDTH + 20, 100, 50, 100)
    temp_chunk.tick_signals[3]   = (WINDOW_WIDTH + 10, 250, 50, 100)
    temp_chunk.tick_signals[4]   = (WINDOW_WIDTH,      530, 50,  70)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH + 10,   0, 50, 200)
    temp_chunk.tick_signals[52]  = (WINDOW_WIDTH,      400, 50, 200)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH + 20,   0, 50, 250)
    temp_chunk.tick_signals[102] = (WINDOW_WIDTH + 10, 350, 50,  50)
    temp_chunk.tick_signals[103] = (WINDOW_WIDTH,      570, 50,  30)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH + 20,   0, 50,  50)
    temp_chunk.tick_signals[152] = (WINDOW_WIDTH + 10, 300, 50,  50)
    temp_chunk.tick_signals[153] = (WINDOW_WIDTH,      530, 50,  70)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH + 20,   0, 50, 200)
    temp_chunk.tick_signals[202] = (WINDOW_WIDTH + 10, 400, 50,  50)
    temp_chunk.tick_signals[203] = (WINDOW_WIDTH,      500, 50, 100)
    medium_chunks.append(temp_chunk)   

    # Split down the middle
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[26] = (WINDOW_WIDTH, 270, 1700, 60) 
    medium_chunks.append(temp_chunk)   
    
    # Asteroids
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,  50, 25, 25)
    temp_chunk.tick_signals[6]   = (WINDOW_WIDTH, 450, 25, 25)
    temp_chunk.tick_signals[16]  = (WINDOW_WIDTH, 125, 25, 25)
    temp_chunk.tick_signals[21]  = (WINDOW_WIDTH,  40, 25, 25)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH, 300, 25, 25)
    temp_chunk.tick_signals[31]  = (WINDOW_WIDTH, 200, 25, 25)
    temp_chunk.tick_signals[36]  = (WINDOW_WIDTH, 410, 25, 25)
    temp_chunk.tick_signals[41]  = (WINDOW_WIDTH, 500, 25, 25)
    temp_chunk.tick_signals[46]  = (WINDOW_WIDTH, 190, 25, 25)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 280, 25, 25)
    temp_chunk.tick_signals[56]  = (WINDOW_WIDTH, 100, 25, 25)
    temp_chunk.tick_signals[61]  = (WINDOW_WIDTH, 550, 25, 25)
    temp_chunk.tick_signals[66]  = (WINDOW_WIDTH, 150, 25, 25)
    temp_chunk.tick_signals[71]  = (WINDOW_WIDTH, 180, 25, 25)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 420, 25, 25)
    temp_chunk.tick_signals[81]  = (WINDOW_WIDTH, 360, 25, 25)
    temp_chunk.tick_signals[86]  = (WINDOW_WIDTH, 170, 25, 25)
    temp_chunk.tick_signals[91]  = (WINDOW_WIDTH, 530, 25, 25)
    temp_chunk.tick_signals[96]  = (WINDOW_WIDTH, 220, 25, 25) 
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH,  10, 25, 25)
    temp_chunk.tick_signals[106] = (WINDOW_WIDTH, 210, 25, 25)
    temp_chunk.tick_signals[116] = (WINDOW_WIDTH, 380, 25, 25)
    temp_chunk.tick_signals[121] = (WINDOW_WIDTH, 440, 25, 25)
    temp_chunk.tick_signals[126] = (WINDOW_WIDTH, 130, 25, 25)
    temp_chunk.tick_signals[131] = (WINDOW_WIDTH, 470, 25, 25)
    temp_chunk.tick_signals[136] = (WINDOW_WIDTH, 390, 25, 25)
    temp_chunk.tick_signals[141] = (WINDOW_WIDTH, 500, 25, 25)
    temp_chunk.tick_signals[146] = (WINDOW_WIDTH,  20, 25, 25)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 295, 25, 25)
    temp_chunk.tick_signals[156] = (WINDOW_WIDTH, 150, 25, 25)
    temp_chunk.tick_signals[161] = (WINDOW_WIDTH, 450, 25, 25)
    temp_chunk.tick_signals[166] = (WINDOW_WIDTH, 390, 25, 25)
    temp_chunk.tick_signals[171] = (WINDOW_WIDTH, 540, 25, 25)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH, 140, 25, 25)
    temp_chunk.tick_signals[181] = (WINDOW_WIDTH, 300, 25, 25)
    temp_chunk.tick_signals[186] = (WINDOW_WIDTH, 320, 25, 25)
    temp_chunk.tick_signals[191] = (WINDOW_WIDTH, 180, 25, 25)
    temp_chunk.tick_signals[196] = (WINDOW_WIDTH, 430, 25, 25) 
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH,  10, 25, 25)
    temp_chunk.tick_signals[206] = (WINDOW_WIDTH, 130, 25, 25)
    temp_chunk.tick_signals[216] = (WINDOW_WIDTH, 400, 25, 25)
    temp_chunk.tick_signals[221] = (WINDOW_WIDTH, 320, 25, 25)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 550, 25, 25)
    temp_chunk.tick_signals[231] = (WINDOW_WIDTH, 180, 25, 25)
    temp_chunk.tick_signals[236] = (WINDOW_WIDTH, 420, 25, 25)
    temp_chunk.tick_signals[241] = (WINDOW_WIDTH, 500, 25, 25)
    temp_chunk.tick_signals[246] = (WINDOW_WIDTH,  50, 25, 25)    
    medium_chunks.append(temp_chunk)   
    
    # Good Aim
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH,      270, 1000,  60)
    temp_chunk.tick_signals[141] = (WINDOW_WIDTH + 10,   0,   50, 250)
    temp_chunk.tick_signals[142] = (WINDOW_WIDTH,      350,   50, 250)
    temp_chunk.tick_signals[163] = (WINDOW_WIDTH,      270,  780,  60)    
    temp_chunk.tick_signals[246] = (WINDOW_WIDTH + 10,   0,   50, 255)
    temp_chunk.tick_signals[247] = (WINDOW_WIDTH,      345,   50, 255)
    medium_chunks.append(temp_chunk)     
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[8]   = (WINDOW_WIDTH,      270, 1930,  60)   
    temp_chunk.tick_signals[211] = (WINDOW_WIDTH + 10,   0,   50, 270)
    temp_chunk.tick_signals[212] = (WINDOW_WIDTH,      330,   50, 270)
    medium_chunks.append(temp_chunk)     
    
    # Fasterer!
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[11]  = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[21]  = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[31]  = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[41]  = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[61]  = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[71]  = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[81]  = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[91]  = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[101] = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[111] = (WINDOW_WIDTH, 200, 30, 400)  
    temp_chunk.tick_signals[121] = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[131] = (WINDOW_WIDTH, 200, 30, 400)    
    temp_chunk.tick_signals[141] = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[161] = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[171] = (WINDOW_WIDTH, 200, 30, 400)   
    temp_chunk.tick_signals[181] = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[191] = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[211] = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[221] = (WINDOW_WIDTH,   0, 30, 400)
    temp_chunk.tick_signals[231] = (WINDOW_WIDTH, 200, 30, 400)
    temp_chunk.tick_signals[241] = (WINDOW_WIDTH,   0, 30, 400)
    hard_chunks.append(temp_chunk)
    
    # Outta Nowhere
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0,   10,  10)
    temp_chunk.tick_signals[66]  = (WINDOW_WIDTH - 650,   0, 50, 400)
    temp_chunk.tick_signals[31]  = (WINDOW_WIDTH,  590,  10,  10)
    temp_chunk.tick_signals[96]  = (WINDOW_WIDTH - 650, 200, 50, 400)  
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH,  590,  10,  10)
    temp_chunk.tick_signals[116] = (WINDOW_WIDTH - 650, 200, 50, 400)     
    temp_chunk.tick_signals[71]  = (WINDOW_WIDTH,    0,  10,  10)
    temp_chunk.tick_signals[136] = (WINDOW_WIDTH - 650,   0, 50, 400) 
    temp_chunk.tick_signals[121] = (WINDOW_WIDTH,    0,  10,  10)
    temp_chunk.tick_signals[186] = (WINDOW_WIDTH - 650,   0, 50, 400)   
    temp_chunk.tick_signals[141] = (WINDOW_WIDTH,    0,  10,  10)
    temp_chunk.tick_signals[206] = (WINDOW_WIDTH - 650,   0, 50, 400) 
    temp_chunk.tick_signals[161] = (WINDOW_WIDTH,  590,  10,  10)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH - 650, 200, 50, 400)
    temp_chunk.tick_signals[191] = (WINDOW_WIDTH,    0,  10,  10)
    temp_chunk.tick_signals[241] = (WINDOW_WIDTH,    0,  10,  10)
    hard_chunks.append(temp_chunk)
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[6]   = (WINDOW_WIDTH - 650,   0,  50,  400)
    temp_chunk.tick_signals[56]  = (WINDOW_WIDTH - 650,   0,  50,  400)
    
    temp_chunk.tick_signals[11]  = (WINDOW_WIDTH,    0,  10,  10)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH - 650,   0,  50,  400)
    temp_chunk.tick_signals[31]  = (WINDOW_WIDTH,    0,  10,  10)
    temp_chunk.tick_signals[96]  = (WINDOW_WIDTH - 650,   0,  50,  400)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH,    0,  10,  10)
    temp_chunk.tick_signals[116] = (WINDOW_WIDTH - 650,   0,  50,  400)    
    temp_chunk.tick_signals[86]  = (WINDOW_WIDTH,  590,  10,  10)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH - 650, 200,  50,  400)
    temp_chunk.tick_signals[106] = (WINDOW_WIDTH,  590,  10,  10)
    temp_chunk.tick_signals[171] = (WINDOW_WIDTH - 650, 200,  50,  400)  
    temp_chunk.tick_signals[156] = (WINDOW_WIDTH,    0,  10,  10)
    temp_chunk.tick_signals[221] = (WINDOW_WIDTH - 650,   0,  50,  400)    
    hard_chunks.append(temp_chunk)    
    
    # Tetris
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH, 200, 30, 120)
    temp_chunk.tick_signals[16]  = (WINDOW_WIDTH, 400, 60,  30)
    temp_chunk.tick_signals[19]  = (WINDOW_WIDTH, 430, 60,  30)
    temp_chunk.tick_signals[31]  = (WINDOW_WIDTH, 180, 30,  90)
    temp_chunk.tick_signals[34]  = (WINDOW_WIDTH, 210, 30,  30)
    temp_chunk.tick_signals[46]  = (WINDOW_WIDTH, 100,120,  30)
    temp_chunk.tick_signals[61]  = (WINDOW_WIDTH, 500, 30,  60)
    temp_chunk.tick_signals[64]  = (WINDOW_WIDTH, 530, 30,  60)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 300, 60,  30)
    temp_chunk.tick_signals[79]  = (WINDOW_WIDTH, 270, 60,  30)
    temp_chunk.tick_signals[91]  = (WINDOW_WIDTH, 480, 90,  30)
    temp_chunk.tick_signals[94]  = (WINDOW_WIDTH, 510, 30,  30)
    temp_chunk.tick_signals[106] = (WINDOW_WIDTH,  50, 60,  30)
    temp_chunk.tick_signals[109] = (WINDOW_WIDTH,  80, 60,  30)
    temp_chunk.tick_signals[121] = (WINDOW_WIDTH, 300, 30, 120)
    temp_chunk.tick_signals[136] = (WINDOW_WIDTH, 500,120,  30)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 160, 30,  60)
    temp_chunk.tick_signals[154] = (WINDOW_WIDTH, 190, 30,  60)
    temp_chunk.tick_signals[166] = (WINDOW_WIDTH, 200, 30,  30) 
    temp_chunk.tick_signals[169] = (WINDOW_WIDTH, 170, 30,  90)
    temp_chunk.tick_signals[181] = (WINDOW_WIDTH, 300, 30, 120)
    temp_chunk.tick_signals[196] = (WINDOW_WIDTH, 500, 60,  30)
    temp_chunk.tick_signals[199] = (WINDOW_WIDTH, 470, 60,  30) 
    temp_chunk.tick_signals[211] = (WINDOW_WIDTH, 300, 60,  30)
    temp_chunk.tick_signals[214] = (WINDOW_WIDTH, 270, 60,  30)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH,  80, 90,  30)
    temp_chunk.tick_signals[229] = (WINDOW_WIDTH, 110, 30,  30)
    temp_chunk.tick_signals[241] = (WINDOW_WIDTH, 500, 60,  30)
    temp_chunk.tick_signals[244] = (WINDOW_WIDTH, 530, 60,  30)
    hard_chunks.append(temp_chunk)     
    
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[5 + 1]   = (WINDOW_WIDTH, 100, 30, 120)
    temp_chunk.tick_signals[5 + 16]  = (WINDOW_WIDTH, 200, 60,  30)
    temp_chunk.tick_signals[5 + 19]  = (WINDOW_WIDTH, 230, 60,  30)
    temp_chunk.tick_signals[5 + 31]  = (WINDOW_WIDTH, 400, 30,  90)
    temp_chunk.tick_signals[5 + 34]  = (WINDOW_WIDTH, 430, 30,  30)
    temp_chunk.tick_signals[5 + 46]  = (WINDOW_WIDTH, 380,120,  30)
    temp_chunk.tick_signals[5 + 61]  = (WINDOW_WIDTH,  50, 30,  60)
    temp_chunk.tick_signals[5 + 64]  = (WINDOW_WIDTH,  80, 30,  60)
    temp_chunk.tick_signals[5 + 76]  = (WINDOW_WIDTH, 300, 60,  30)
    temp_chunk.tick_signals[5 + 79]  = (WINDOW_WIDTH, 270, 60,  30)
    temp_chunk.tick_signals[5 + 91]  = (WINDOW_WIDTH, 480, 90,  30)
    temp_chunk.tick_signals[5 + 94]  = (WINDOW_WIDTH, 510, 30,  30)
    temp_chunk.tick_signals[5 + 106] = (WINDOW_WIDTH, 250, 60,  30)
    temp_chunk.tick_signals[5 + 109] = (WINDOW_WIDTH, 280, 60,  30)
    temp_chunk.tick_signals[5 + 121] = (WINDOW_WIDTH,  80, 30, 120)
    temp_chunk.tick_signals[5 + 136] = (WINDOW_WIDTH, 450,120,  30)
    temp_chunk.tick_signals[5 + 151] = (WINDOW_WIDTH, 260, 30,  60)
    temp_chunk.tick_signals[5 + 154] = (WINDOW_WIDTH, 290, 30,  60)
    temp_chunk.tick_signals[5 + 166] = (WINDOW_WIDTH, 400, 30,  30) 
    temp_chunk.tick_signals[5 + 169] = (WINDOW_WIDTH, 370, 30,  90)
    temp_chunk.tick_signals[5 + 181] = (WINDOW_WIDTH,  40, 30, 120)
    temp_chunk.tick_signals[5 + 196] = (WINDOW_WIDTH, 450, 60,  30)
    temp_chunk.tick_signals[5 + 199] = (WINDOW_WIDTH, 420, 60,  30) 
    temp_chunk.tick_signals[5 + 211] = (WINDOW_WIDTH, 300, 60,  30)
    temp_chunk.tick_signals[5 + 214] = (WINDOW_WIDTH, 270, 60,  30)
    temp_chunk.tick_signals[5 + 226] = (WINDOW_WIDTH, 100, 90,  30)
    temp_chunk.tick_signals[5 + 229] = (WINDOW_WIDTH, 130, 30,  30)
    hard_chunks.append(temp_chunk)  
    
    # The Grand Finale
    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[1]   = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[26]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[51]  = (WINDOW_WIDTH,   0, 50, 400)
    temp_chunk.tick_signals[76]  = (WINDOW_WIDTH, 200, 50, 400)
    temp_chunk.tick_signals[106] = (WINDOW_WIDTH,  50, 60,  30)
    temp_chunk.tick_signals[109] = (WINDOW_WIDTH,  80, 60,  30)
    temp_chunk.tick_signals[136] = (WINDOW_WIDTH, 500,120,  30)
    temp_chunk.tick_signals[151] = (WINDOW_WIDTH, 160, 30,  60)
    temp_chunk.tick_signals[154] = (WINDOW_WIDTH, 190, 30,  60)
    temp_chunk.tick_signals[166] = (WINDOW_WIDTH, 200, 30,  30) 
    temp_chunk.tick_signals[169] = (WINDOW_WIDTH, 170, 30,  90)
    temp_chunk.tick_signals[181] = (WINDOW_WIDTH, 300, 30, 120)
    temp_chunk.tick_signals[196] = (WINDOW_WIDTH, 500, 60,  30)
    temp_chunk.tick_signals[199] = (WINDOW_WIDTH, 470, 60,  30) 
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH,  10, 25, 25)
    temp_chunk.tick_signals[216] = (WINDOW_WIDTH, 400, 25, 25)
    temp_chunk.tick_signals[221] = (WINDOW_WIDTH, 320, 25, 25)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 550, 25, 25)
    temp_chunk.tick_signals[231] = (WINDOW_WIDTH, 180, 25, 25)
    temp_chunk.tick_signals[236] = (WINDOW_WIDTH, 420, 25, 25)
    temp_chunk.tick_signals[241] = (WINDOW_WIDTH, 500, 25, 25)
    temp_chunk.tick_signals[246] = (WINDOW_WIDTH,  50, 25, 25)   
    easy_chunks.append(temp_chunk)    

    temp_chunk = LevelChunk()
    temp_chunk.tick_signals[21]   = (WINDOW_WIDTH,   0,   10,  10)
    temp_chunk.tick_signals[86]  = (WINDOW_WIDTH - 650,   0, 50, 400) 
    temp_chunk.tick_signals[71]  = (WINDOW_WIDTH,  590,  10,  10)
    temp_chunk.tick_signals[136] = (WINDOW_WIDTH - 650, 200, 50, 400)
    temp_chunk.tick_signals[176] = (WINDOW_WIDTH + 20,   0, 50, 100)
    temp_chunk.tick_signals[177] = (WINDOW_WIDTH + 10, 280, 50, 200)
    temp_chunk.tick_signals[178] = (WINDOW_WIDTH,      580, 50,  20)    
    temp_chunk.tick_signals[201] = (WINDOW_WIDTH,   0, 50, 300)
    temp_chunk.tick_signals[226] = (WINDOW_WIDTH, 300, 50, 300)
    easy_chunks.append(temp_chunk) 
            
    return easy_chunks, medium_chunks, hard_chunks


def create_levels(easy_chunks, medium_chunks, hard_chunks):
    """Creates all levels"""
    levels = []
    
    # Easy levels (using the easy chunks)
    # 1-8
    levels.append(Level([easy_chunks[14]], "The aim of the game"))
    levels.append(Level([easy_chunks[0]], "Predictable"))
    levels.append(Level([easy_chunks[1], easy_chunks[2]], "Unpredictable"))
    levels.append(Level([easy_chunks[3], easy_chunks[4]], "Short and Tall"))
    levels.append(Level([easy_chunks[5], easy_chunks[6]], "And off the Wall"))
    levels.append(Level([easy_chunks[7], easy_chunks[8]], "Fat and Thin"))
    levels.append(Level([easy_chunks[9], easy_chunks[10]], "Heartbeat"))
    levels.append(Level([easy_chunks[11], easy_chunks[12], easy_chunks[13]], "Combo")) # TO DO
    
    # Medium levels (chunks are out of order, as I wanted to balance the levels
    # and did not do that exactly in order as for the easy levels).
    # 9-14
    levels.append(Level([medium_chunks[0]], "Faster!"))
    levels.append(Level([medium_chunks[7]], "Split down the middle"))
    levels.append(Level([medium_chunks[3], medium_chunks[4]], "Flappy Bird?"))
    levels.append(Level([medium_chunks[5], medium_chunks[6]], "Choices"))
    levels.append(Level([medium_chunks[1], medium_chunks[2]], "Morse Code"))
    levels.append(Level([medium_chunks[9], medium_chunks[10]], "Good Aim"))
    levels.append(Level([medium_chunks[8]], "Asteroids"))
    
    # Hard levels
    # 16-18
    levels.append(Level([hard_chunks[0]], "Fasterer!"))
    levels.append(Level([hard_chunks[3], hard_chunks[4]], "Tetris"))
    
    # Quite hard, maybe level 18
    levels.append(Level([hard_chunks[1], hard_chunks[2]], "Outta Nowhere"))
    
    # Blind levels
    # 19-20
    levels.append(Level([easy_chunks[0]], "Driving Blind"))
    
    # And one here (finale)
    levels.append(Level([easy_chunks[15], easy_chunks[16]], "The Grand Finale"))

    return levels
    

if __name__ == "__main__":
    """Run the program"""
    # Initially create the level chunks and overall levels
    log("Loading chunks")
    t = time.time()
    try:
        easy, medium, hard = create_chunks()
        log("Chunks loaded successfully")
        log("Time taken: {}s".format(time.time() - t))
    except e:
        log("Error loading chunks: {}".format(e))
    
    log("Creating levels")
    t = time.time()
    try:
        levels = create_levels(easy, medium, hard)
        log("Levels created successfully")
        log("Time taken: {}s".format(time.time() - t))
    except e:
        log("Error creating levels: {}".format(e))
    
    # Initialize the Tk window
    log("Initializing window")
    root = Tk()
    root.geometry("{}x{}+50+50".format(WINDOW_WIDTH, WINDOW_HEIGHT))
    
    gui = GUI(root, easy, medium, hard, levels)
        
    root.mainloop()    