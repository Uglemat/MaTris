import pygame
from pygame import Rect, Surface
import random
import kezmenu

from tetrominoes import (T_long, 
                         T_square, 
                         T_hat,
                         T_right_snake,
                         T_left_snake,
                         T_left_gun,
                         T_right_gun)
from tetrominoes import list_of_tetrominoes
from tetrominoes import rotate

class BrokenMatrixException(Exception):
    pass

class Matris(object):
    def __init__(self, size=(10, 22), blocksize=30):
        self.size = {'width': size[0], 'height': size[1]}
        self.blocksize = blocksize
        self.surface = Surface((self.size['width']  * self.blocksize,
                                (self.size['height']-2) * self.blocksize))
        self.matrix = dict()
        for y in range(self.size['height']):
            for x in range(self.size['width']):
                self.matrix[(y,x)] = None


        self.next_tetromino = random.choice(list_of_tetrominoes)
        self.set_tetrominoes()
        self.tetromino_rotation = 0
        self.down_key_timer = 0
        self.down_key_speed = 0.3

        self.movement_keys = {'left': 0, 'right': 0}
        self.movement_keys_speed = 0.05
        self.movement_keys_timer = (-self.movement_keys_speed)*2

    def set_tetrominoes(self):
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = random.choice(list_of_tetrominoes)
        self.surface_of_next_tetromino = self.construct_surface_of_next_tetromino()
        self.tetromino_position = (0,4) if len(self.current_tetromino.shape) == 2 else (0, 3)
        self.tetromino_rotation = 0
        self.tetromino_block = self.block(self.current_tetromino.color)
        self.shadow_block = self.block(self.current_tetromino.color, shadow=True)

    
    def hard_drop(self):
        while self.request_movement('down'):
            pass

        self.lock_tetromino()

    def update(self, timepassed, events):
        pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key
        unpressed = lambda key: event.type == pygame.KEYUP and event.key == key
        for event in events:
            if pressed(pygame.K_SPACE):
                self.hard_drop()
            elif pressed(pygame.K_UP):
                self.request_rotation()

            elif pressed(pygame.K_LEFT) or pressed(pygame.K_a):
                self.request_movement('left')
                self.movement_keys['left'] = 1
            elif pressed(pygame.K_RIGHT) or pressed(pygame.K_d):
                self.request_movement('right')
                self.movement_keys['right'] = 1

            elif unpressed(pygame.K_LEFT) or unpressed(pygame.K_a):
                self.movement_keys['left'] = 0
                self.movement_keys_timer = (-self.movement_keys_speed)*2
            elif unpressed(pygame.K_RIGHT) or unpressed(pygame.K_d):
                self.movement_keys['right'] = 0
                self.movement_keys_timer = (-self.movement_keys_speed)*2

            elif pressed(pygame.K_w):
                self.request_movement('up')
            elif pressed(pygame.K_s):
                self.request_movement('down')
            elif pressed(pygame.K_l):
                self.lock_tetromino()

        self.down_key_timer += timepassed
        down_key_speed = self.down_key_speed*0.10 if pygame.key.get_pressed()[pygame.K_DOWN] else self.down_key_speed
        if self.down_key_timer > down_key_speed:
            result = self.request_movement('down')
            if not result:
                self.lock_tetromino()
            self.down_key_timer %= down_key_speed


        if any(self.movement_keys.values()):
            self.movement_keys_timer += timepassed
        if self.movement_keys_timer > self.movement_keys_speed:
            result = self.request_movement('right' if self.movement_keys['right'] else 'left')
            self.movement_keys_timer %= self.movement_keys_speed

        with_shadow = self.place_shadow()
        with_tetromino = self.blend(self.rotated(), allow_failure=False, matrix=with_shadow)

        self.remove_lines()
        
        for y in range(self.size['height']):
            for x in range(self.size['width']):

                #                                       I hide the 2 first rows by drawing them outside of the surface
                block_location = Rect(x*self.blocksize, (y*self.blocksize - 2*self.blocksize), self.blocksize, self.blocksize)
                if with_tetromino[(y,x)] is None:
                    self.surface.fill((30,30,30), block_location)
                else:
                    self.surface.fill((30,30,30), block_location)
                    self.surface.blit(with_tetromino[(y,x)][1], block_location)

    def place_shadow(self):
        posY, posX = self.tetromino_position
        while self.blend(position=(posY, posX)):
            posY += 1

        position = (posY-1, posX)

        return self.blend(position=position, block=self.shadow_block, shadow=True) or self.matrix
        # If the blend isn't successful just return the old matrix. The blend will fail later in self.update, it's game over.

    def request_rotation(self):
        rotation = (self.tetromino_rotation + 1) % 4
        shape = self.rotated(rotation)
        if self.blend(shape):
            self.tetromino_rotation = rotation
            return self.tetromino_rotation
        else:
            return False
            
    def request_movement(self, direction):
        posY, posX = self.tetromino_position
        if direction == 'left' and self.blend(position=(posY, posX-1)):
            self.tetromino_position = (posY, posX-1)
            return self.tetromino_position
        elif direction == 'right' and self.blend(position=(posY, posX+1)):
            self.tetromino_position = (posY, posX+1)
            return self.tetromino_position
        elif direction == 'up' and self.blend(position=(posY-1, posX)):
            self.tetromino_position = (posY-1, posX)
            return self.tetromino_position
        elif direction == 'down' and self.blend(position=(posY+1, posX)):
            self.tetromino_position = (posY+1, posX)
            return self.tetromino_position
        else:
            return False

    def rotated(self, rotation=None):
        if rotation is None:
            rotation = self.tetromino_rotation
        return rotate(self.current_tetromino.shape, rotation)

    def block(self, color, shadow=False):
        colors = {'blue':   (27, 34, 224),
                  'yellow': (225, 242, 41),
                  'pink':   (242, 41, 195),
                  'green':  (22, 181, 64),
                  'red':    (204, 22, 22),
                  'orange': (245, 144, 12),
                  'cyan':   (10, 255, 226)}


        if shadow:
            end = [40] # end is the alpha value
        else:
            end = [] # Adding this to the end will not change the array, thus no alpha value

        border = Surface((self.blocksize, self.blocksize), pygame.SRCALPHA, 32)
        border.fill(map(lambda c: c*0.5, colors[color]) + end)

        borderwidth = 2

        box = Surface((self.blocksize-borderwidth*2, self.blocksize-borderwidth*2), pygame.SRCALPHA, 32)
        boxarr = pygame.PixelArray(box)
        for x in range(len(boxarr)):
            for y in range(len(boxarr)):
                boxarr[x][y] = tuple(map(lambda c: min(255, int(c*random.uniform(0.8, 1.2))), colors[color]) + end) 

        del boxarr # deleting boxarr or else the box surface will be 'locked' or something like that and won't blit.
        border.blit(box, Rect(borderwidth, borderwidth, 0, 0))


        return border

    def lock_tetromino(self):
        self.matrix = self.blend()
        self.set_tetrominoes()

    def remove_lines(self):
        lines = []
        for y in range(self.size['height']):
            line = (y, [])
            for x in range(self.size['width']):
                if self.matrix[(y,x)]:
                    line[1].append(x)
            if len(line[1]) == self.size['width']:
                lines.append(y)

        for line in sorted(lines):
            for x in range(self.size['width']):
                self.matrix[(line,x)] = None
            for y in range(0, line+1)[::-1]:
                for x in range(self.size['width']):
                    self.matrix[(y,x)] = self.matrix.get((y-1,x), None)


    def blend(self, shape=None, position=None, matrix=None, block=None, allow_failure=True, shadow=False):
        if shape is None:
            shape = self.rotated()
        if position is None:
            position = self.tetromino_position

        copy = dict(self.matrix if matrix is None else matrix)
        posY, posX = position
        for x in range(posX, posX+len(shape)):
            for y in range(posY, posY+len(shape)):
                if (copy.get((y, x), False) is False and shape[y-posY][x-posX] # shape is outside the matrix
                    or # coordinate is occupied by something else which isn't a shadow
                    copy.get((y,x)) and shape[y-posY][x-posX] and copy[(y,x)][0] != 'shadow'): 
                    if allow_failure:
                        return False
                    else:
                        print copy[(y,x)]
                        raise BrokenMatrixException("Tried to blend a broken matrix. This should mean game over, if you see this it is certainly a bug. (or you are developing)")
                elif shape[y-posY][x-posX] and not shadow:
                    copy[(y,x)] = ('block', self.tetromino_block if block is None else block)
                elif shape[y-posY][x-posX] and shadow:
                    copy[(y,x)] = ('shadow', block)

        return copy

    def construct_surface_of_next_tetromino(self):
        shape = self.next_tetromino.shape
        surf = Surface((len(shape)*self.blocksize, len(shape)*self.blocksize), pygame.SRCALPHA, 32)

        for y in range(len(shape)):
            for x in range(len(shape)):
                if shape[y][x]:
                    surf.blit(self.block(self.next_tetromino.color), (x*self.blocksize, y*self.blocksize))
        return surf

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()
        background = Surface(screen.get_size())
        background.fill((200,0,0))
        matris = Matris()
        matris_border = Surface((10*30+20, 20*30+20))
        matris_border.fill((80,80,80))

        while 1:
            dt = clock.tick(45)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            matris.update(dt / 1000., events)

            background.blit(matris_border, (0,0))
            background.blit(matris.surface, (10,10))
            background.blit(self.next_tetromino_surf(matris.surface_of_next_tetromino), (400, 30))

            screen.blit(background, (0, 0))
            pygame.display.flip()

    def next_tetromino_surf(self, tetromino_surf):
        area = Surface((30*5, 30*5))
        area.fill((80,80,80))
        area.fill((30,30,30), Rect(10, 10, 30*5-20, 30*5-20))

        areasize = area.get_size()[0]
        tetromino_surf_size = tetromino_surf.get_size()[0]
        # ^^ I'm assuming width and height are the same

        center = areasize/2 - tetromino_surf_size/2
        area.blit(tetromino_surf, (center, center))

        return area

class Menu(object):
    running = True
    def main(self, screen):
        clock = pygame.time.Clock()
        menu = kezmenu.KezMenu(
            ['Play!', lambda: Game().main(screen)],
            ['Quit', lambda: setattr(self, 'running', False)],
        )
        menu.x = 50
        menu.y = 50
        menu.enableEffect('raise-col-padding-on-focus', enlarge_time=0.1)

        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            menu.update(events, clock.tick(30)/1000.)
            screen.fill((0,200,0))
            menu.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 880))
    Menu().main(screen)
