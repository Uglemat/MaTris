from __future__ import print_function
from collections import namedtuple

X, O = 'X', None
Tetromino = namedtuple("Tetrimino", "name color shape")

#Creates the list of tetrominos for use in the game
list_of_tetrominoes = [
    Tetromino(name="long",
              color="blue",
              shape=((O,O,O,O),
                     (X,X,X,X),
                     (O,O,O,O),
                     (O,O,O,O))),
    Tetromino(name="square",
              color="yellow",
              shape=((X,X),
                     (X,X))),
    Tetromino(name="hat",
              color="pink",
              shape=((O,X,O),
                     (X,X,X),
                     (O,O,O))),
    Tetromino(name="right_snake",
              color="green",
              shape=((O,X,X),
                     (X,X,O),
                     (O,O,O))),
    Tetromino(name="left_snake",
              color="red",
              shape=((X,X,O),
                     (O,X,X),
                     (O,O,O))),
    Tetromino(name="left_gun",
              color="cyan",
              shape=((X,O,O),
                     (X,X,X),
                     (O,O,O))),
    Tetromino(name="right_gun",
              color="orange",
              shape=((O,O,X),
                     (X,X,X),
                     (O,O,O)))
    ]

def rotate(shape, times=1):
    """ Rotate a shape to the right """
    return shape if times == 0 else rotate(tuple(zip(*shape[::-1])), times-1)


def shape_str(shape):
    """ Return a string of a shape in human readable form """
    return '\n'.join(''.join(map({'X': 'X', None: 'O'}.get, line))
                     for line in shape)

def shape(shape):
    """ Print a shape in human readable form """
    print(shape_str(shape))





def test():
    tetromino_shapes = [t.shape for t in list_of_tetrominoes]
    map(rotate,    tetromino_shapes)
    map(shape,     tetromino_shapes)
    map(shape_str, tetromino_shapes)
    
    #Tests for tetromino shapes
    assert shape_str(tetromino_shapes[4]) == "XXO\nOXX\nOOO"
    
    assert shape_str(tetromino_shapes[1]) == "XX\nXX"
    
    assert shape_str(tetromino_shapes[2]) == "OXO\nXXX\nOOO"
    
    assert shape_str(tetromino_shapes[3]) ==  "OXX\nXXO\nOOO" 
    
    assert rotate(tetromino_shapes[1],4) == ((X,X),(X,X))

    # Rotation Tests
    assert rotate(tetromino_shapes[3], 4) == ((O,X,X),
                                              (X,X,O),
                                              (O,O,O))
    
    
    assert rotate(tetromino_shapes[2], 4) == ((O,X,O),
                                              (X,X,X),
                                              (O,O,O))

    assert rotate(tetromino_shapes[2], 2) == ((O,O,O),
                                      (X,X,X),
                                      (O,X,O))

    print("All tests passed in {}, things seems to be working alright".format(__file__))

if __name__ == '__main__':
    test()
