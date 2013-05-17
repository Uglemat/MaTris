from collections import namedtuple

X, O = 'X', None
Tetromino = namedtuple("Tetrimino", "name color shape")

T_long = Tetromino(name="long",
                   color="blue",
                   shape=((O,O,O,O),
                          (X,X,X,X),
                          (O,O,O,O),
                          (O,O,O,O)))

T_square = Tetromino(name="square",
                     color="yellow",
                     shape=((X,X),
                            (X,X)))

T_hat = Tetromino(name="hat",
                  color="pink",
                  shape=((O,X,O),
                         (X,X,X),
                         (O,O,O)))

T_right_snake = Tetromino(name="right_snake",
                          color="green",
                          shape=((O,X,X),
                                 (X,X,O),
                                 (O,O,O)))

T_left_snake = Tetromino(name="left_snake",
                         color="red",
                         shape=((X,X,O),
                                (O,X,X),
                                (O,O,O)))

T_left_gun = Tetromino(name="left_gun",
                       color="cyan",
                       shape=((X,O,O),
                              (X,X,X),
                              (O,O,O)))

T_right_gun = Tetromino(name="right_gun",
                        color="orange",
                        shape=((O,O,X),
                               (X,X,X),
                               (O,O,O)))

list_of_tetrominoes = [T_long, T_square, T_hat,
                       T_right_snake, T_left_snake, 
                       T_left_gun, T_right_gun]

def rotate(shape, times=1):
    """ Rotate a shape to the right """
    if times == 0:
        return shape

    rotated = [[] for _ in range(len(shape))]

    # Rotate one time to the right
    for line in shape:
        for index, atom in enumerate(line):
            rotated[index].insert(0, atom)

    return tuple(map(tuple, rotated)) if times <= 1 else rotate(rotated, times-1)

def rotate_left(shape, times=1):
    """ Rotate a shape to the left """
    return rotate(shape, 3) if times <= 1 else rotate_left(rotate(shape, 3), times-1)

def shape_str(shape):
    """ Return a string of a shape in human readable form """
    return '\n'.join(''.join(line) for line in shape)

def shape(shape):
    """ Print a shape in human readable form """
    print shape_str(shape)





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
    print "All tests passed in {}, things seems to be working alright".format(__file__)

if __name__ == '__main__':
    test()
