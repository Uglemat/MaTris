import os

scorefile = os.path.join(os.path.dirname(__file__), ".highscores")

def load_score():
    """ Returns the highest score, or 0 if no one has scored yet """
    try:
        with open(scorefile) as file:
            scores = sorted([int(score.strip())
                             for score in file.readlines()
                             if score.strip().isdigit()], reverse=True)
    except IOError:
        scores = []

    return scores[0] if scores else 0

def write_score(score):
    assert str(score).isdigit()
    with open(scorefile, 'a') as file:
        file.write("{}\n".format(score))
