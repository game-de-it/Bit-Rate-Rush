"""敵定義。r は当たり判定半径、sprite は core.sprites の矩形。

雑魚は全員 16x16 / r=8 (人間が弾を当てやすいサイズに揃える)。
ボス: shots = 一度に撃つ弾数 (放射状)、shoot_cd = 発射間隔 (frame)、
      summon = 召喚する敵種リスト、summon_n = 一度の召喚数、summon_cd = 召喚間隔。
"""
from core import sprites as S

ENEMIES = {
    "bat":    dict(name=("コウモリ", "bats"), hp=4,   spd=0.55, dmg=4,  xp=1,   r=8,  sprite=S.BAT),
    "zombie": dict(name=("ゾンビ", "zombies"), hp=12,  spd=0.3,  dmg=8,  xp=2,   r=8,  sprite=S.ZOMBIE),
    "ghost":  dict(name=("ゴースト", "ghosts"), hp=8,   spd=0.75, dmg=6,  xp=2,   r=8,  sprite=S.GHOST, phase=True),
    "skull":  dict(name=("スカル", "skulls"), hp=30,  spd=0.65, dmg=12, xp=5,   r=8,  sprite=S.SKULL),
    "brute":  dict(name=("ブルート", "brutes"), hp=90,  spd=0.25, dmg=18, xp=15,  r=8,  sprite=S.BRUTE),
    "forest_lord": dict(name=("森の主", "Lord of the Forest"), hp=700, spd=0.35, dmg=22, xp=100, r=12, sprite=S.BRUTE, boss=True,
                        summon=["bat", "ghost"], summon_n=6, summon_cd=300, shots=6, shoot_cd=200, shot_spd=1.0),
    "boss1":  dict(name=("魔城の門番", "Gatekeeper"), hp=1200, spd=0.35, dmg=25, xp=150, r=15, sprite=S.BOSS, boss=True,
                   summon=["bat"], summon_n=8, summon_cd=240,
                   shots=8, shoot_cd=180, shot_spd=1.2),
    "boss2":  dict(name=("魔王", "Demon Lord"), hp=3000, spd=0.4, dmg=35, xp=400, r=15, sprite=S.BOSS, boss=True, final=True,
                   summon=["skull", "ghost", "bat"], summon_n=10, summon_cd=200,
                   shots=12, shoot_cd=150, shot_spd=1.5, aimed=True),
}
