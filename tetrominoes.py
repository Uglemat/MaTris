from __future__ import print_function
from collections import namedtuple

X, O = 'X', None
Tetromino = namedtuple("Tetrimino", "color shape")

tetrominoes = {
    "long": Tetromino(color="blue",
                      shape=((O,O,O,O),
                             (X,X,X,X),
                             (O,O,O,O),
                             (O,O,O,O))),
    "square": Tetromino(color="yellow",
                        shape=((X,X),
                               (X,X))),
    "hat": Tetromino(color="pink",
                     shape=((O,X,O),
                            (X,X,X),
                            (O,O,O))),
    "right_snake": Tetromino(color="green",
                             shape=((O,X,X),
                                    (X,X,O),
                                    (O,O,O))),
    "left_snake": Tetromino(color="red",
                            shape=((X,X,O),
                                   (O,X,X),
                                   (O,O,O))),
    "left_gun": Tetromino(color="cyan",
                          shape=((X,O,O),
                                 (X,X,X),
                                 (O,O,O))),
    "right_gun": Tetromino(color="orange",
                           shape=((O,O,X),
                                  (X,X,X),
                                  (O,O,O)))
}
list_of_tetrominoes = list(tetrominoes.values())

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

    assert shape_str(tetrominoes["left_snake"].shape) == "XXO\nOXX\nOOO"

    assert rotate(tetrominoes["square"].shape) == tetrominoes["square"].shape

    assert rotate(tetrominoes["right_snake"].shape, 4) == tetrominoes["right_snake"].shape

    assert rotate(tetrominoes["hat"].shape)    == ((O,X,O),
                                                   (O,X,X),
                                                   (O,X,O))

    assert rotate(tetrominoes["hat"].shape, 2) == ((O,O,O),
                                                   (X,X,X),
                                                   (O,X,O))
    print("All tests passed in {}, things seems to be working alright".format(__file__))

if __name__ == '__main__':
    test()
