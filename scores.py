
scorefile = ".highscores"

def load_score():
    try:
        with open(scorefile) as file:
            scores = sorted([int(score.strip())
                             for score in file.readlines()
                             if score.strip().isdigit()], reverse=True)
            topscore = scores[0] if scores else 0
    except IOError:
        scores = []
        topscore = 0

    return topscore

def write_score(score):
    assert str(score).isdigit()
    with open(scorefile, 'a') as file:
        file.write("{}\n".format(score))

if __name__ == "__main__":
    write_score("1233333")
    print load_score()
