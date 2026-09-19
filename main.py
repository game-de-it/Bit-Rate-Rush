import pyxel

import config
from config import W, H, FPS


def main():
    pyxel.init(W, H, title="Bit-Rate-Rush", fps=FPS, quit_key=pyxel.KEY_NONE)
    config.refresh_debug()   # user_data_dir は init 後でないと使えない環境がある
    from game import Game    # デバッグ設定が確定してから各シーンを読み込む
    game = Game()
    pyxel.run(game.update, game.draw)


if __name__ == "__main__":
    main()
