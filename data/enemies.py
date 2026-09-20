"""敵定義。r は当たり判定半径、sprite は core.sprites の矩形。

雑魚は全員 16x16 / r=8 (人間が弾を当てやすいサイズに揃える)。
ボス: shots = 一度に撃つ弾数 (放射状)、shoot_cd = 発射間隔 (frame)、
      summon = 召喚する敵種リスト、summon_n = 一度の召喚数、summon_cd = 召喚間隔。

後編で追加した挙動 (scenes/play.update_enemies):
  zigzag=(振幅 px, 周期 frame)  進行方向に対して左右に蛇行する
  keep=距離                     その距離まで近づいたら止まり、shoot_cd ごとにプレイヤー狙いの弾を 1 発撃つ (shot_spd)
  dash=(休み frame, 突進 frame, 倍率)  周期的に突進する (ボスの突進と同じ仕組み)
  midboss=True                  ボス扱い (押されない・HP バー) だが召喚しない。spiral=True で放射弾が回転する
"""
from core import sprites as S

ENEMIES = {
    "bat":    dict(name=("コウモリ", "bats"), hp=4,   spd=0.55, dmg=4,  xp=1,   r=8,  sprite=S.BAT),
    "zombie": dict(name=("ゾンビ", "zombies"), hp=12,  spd=0.3,  dmg=8,  xp=2,   r=8,  sprite=S.ZOMBIE),
    "ghost":  dict(name=("ゴースト", "ghosts"), hp=8,   spd=0.75, dmg=6,  xp=2,   r=8,  sprite=S.GHOST, phase=True),
    "skull":  dict(name=("スカル", "skulls"), hp=30,  spd=0.65, dmg=12, xp=5,   r=8,  sprite=S.SKULL),
    "brute":  dict(name=("ブルート", "brutes"), hp=90,  spd=0.25, dmg=18, xp=15,  r=8,  sprite=S.BRUTE),
    # ---- 後編 ----
    "wisp":   dict(name=("鬼火", "wisps"), hp=6, spd=0.9, dmg=5, xp=2, r=8, sprite=S.WISP, phase=True, zigzag=(2.2, 40)),
    "archer": dict(name=("骸骨の射手", "skeleton archers"), hp=20, spd=0.5, dmg=8, xp=4, r=8, sprite=S.ARCHER,
                   keep=110, shoot_cd=150, shot_spd=1.4),
    "boar":   dict(name=("魔猪", "boars"), hp=40, spd=0.4, dmg=14, xp=6, r=8, sprite=S.BOAR, dash=(150, 22, 4.0)),
    "knight": dict(name=("亡霊騎士", "Phantom Knight"), hp=500, spd=0.45, dmg=24, xp=80, r=11, sprite=S.KNIGHT, boss=True, midboss=True,
                   shots=10, shoot_cd=120, shot_spd=1.3, spiral=True, dash=(150, 24, 3.5)),
    "forest_lord": dict(name=("森の主", "Lord of the Forest"), hp=700, spd=0.35, dmg=22, xp=100, r=12, sprite=S.BRUTE, boss=True,
                        summon=["bat", "ghost"], summon_n=6, summon_cd=300, shots=6, shoot_cd=200, shot_spd=1.0),
    "boss1":  dict(name=("魔城の門番", "Gatekeeper"), hp=1200, spd=0.35, dmg=25, xp=150, r=15, sprite=S.BOSS, boss=True,
                   summon=["bat"], summon_n=8, summon_cd=240,
                   shots=8, shoot_cd=180, shot_spd=1.2),
    "boss2":  dict(name=("魔王", "Demon Lord"), hp=3000, spd=0.4, dmg=35, xp=400, r=15, sprite=S.BOSS, boss=True, final=True,
                   summon=["skull", "ghost", "bat"], summon_n=10, summon_cd=200,
                   shots=12, shoot_cd=150, shot_spd=1.5, aimed=True),
}
