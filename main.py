import pyxel

from config import W, H, FPS
from game import Game


def main():
    pyxel.init(W, H, title="Bit-Rate-Rush", fps=FPS, quit_key=pyxel.KEY_NONE)
    game = Game()
    pyxel.run(game.update, game.draw)


if __name__ == "__main__":
    main()
