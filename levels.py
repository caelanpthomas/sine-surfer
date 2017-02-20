"""
Creates all the level instances to be used in the main program
"""

from sineplane_constants import *

class LevelChunk:
    """250 ticks long (10 seconds), holds all obstacle creation code"""
    def __init__(self):
        self.tick_signals = {}
        
        
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