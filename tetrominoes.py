from __future__ import print_function
from collections import namedtuple

X, O = 'X', None
Tetromino = namedtuple("Tetrimino", "name color shape")

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

    assert shape_str(T_left_snake.shape) == "XXO\nOXX\nOOO"

    assert rotate(T_square.shape) == T_square.shape

    assert rotate(T_right_snake.shape, 4) == T_right_snake.shape

    assert rotate(T_hat.shape)    == ((O,X,O),
                                      (O,X,X),
                                      (O,X,O))

    assert rotate(T_hat.shape, 2) == ((O,O,O),
                                      (X,X,X),
                                      (O,X,O))
    print("All tests passed in {}, things seems to be working alright".format(__file__))

if __name__ == '__main__':
    test()
