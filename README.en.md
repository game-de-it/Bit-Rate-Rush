# Bit-Rate-Rush

![Bit-Rate-Rush](docs/shots/title.png)

[日本語](README.md) ・ English ・ **[Official site](https://game-de-it.github.io/bit-rate-rush-web/index.en.html)**

> **Survive a battlefield flooded with monsters, armed with nothing but a knife. Back in town, the next job and the next chapter of the story are waiting.**

A 2D pixel-art survival action RPG that combines a town, jobs and a story with "move-to-fight" action.
Built with [Pyxel](https://github.com/kitao/pyxel). 320×240, 64 colours, Japanese / English.

---

## Screens

| | |
|---|---|
| ![Town](docs/shots/town.png) | ![Tavern](docs/shots/tavern.png) |
| **Castle town** — tavern, weaponsmith, store, inn, castle | **Tavern** — take jobs from the master |
| ![Battle](docs/shots/battle.png) | ![Level up](docs/shots/levelup.png) |
| **Battle** — just move; weapons fire themselves | **Level up** — pick one of three upgrades |
| ![Chapter](docs/shots/chapter.png) | ![Story](docs/shots/vn.png) |
| **A chapter begins** | **Story scenes** |

---

## What is it?

On the battlefield you do one thing: **keep moving**. Weapons throw themselves, magic burns on its own. All you choose is where to run and what to grow next.

Survive a few minutes, return to town, spend the coins you found on weapons, rest at the inn, and pick the next job at the tavern. Step by step you grow stronger — and closer to what is really happening in this world.

### The world — when the rate rises, the Rush comes

Every living thing carries **bits**, tiny motes of light. Slay a monster and its bits scatter on the wind. No human can gather them.

The world also has a **rate** — the speed of its flow — and when someone raises it, sleeping monsters wake without end and pour toward the town in a **Rush**. People have feared the word so long they no longer say it aloud.

Now bats are darkening the sky over the castle town of Lumen.
— Since the day a young man walked through its gate.

---

## How to play

### In town
| Place | What you do |
|---|---|
| **Tavern** | Pick a job from the board (survive / hunt). Hear the master's rumours |
| **Weaponsmith** | Buy weapons with coin and raise their rank |
| **General store** | Herbs, bombs, charms. Carry up to three |
| **Inn** | Rest to recover (for a fee). Keeping the journal saves the game |
| **Castle** | The King's special requests, rewarded with royal **relics** (magic). Opens once every tavern job of the chapter is done |
| **Depart** | Check your starting weapon and items, then head out |

### In the field
- **Move only.** Everything else is automatic
- Defeat monsters, gather bits, and pick one of **three** upgrades on every level up
- Items: L / R to select, Y to use
- Clear the job and go home with **START → Return** — or keep fighting for coin until time runs out. A knockout halves what you bring back
- Wounds follow you into town; healing costs coin
- Survival jobs end with a one-minute **Rush** (double spawns). Hunt jobs grant a bonus minute for every multiple of the target you clear

### Story
Five chapters. You start with one weapon; slots grow as the chapters advance, and the castle unlocks magic. A run through takes about 60–90 minutes. After the ending, a glimpse of part two plays.

---

## Controls

| | Gamepad | Keyboard |
|---|---|---|
| Move | D-pad / left stick | WASD / arrows |
| Confirm | A | Z / Enter / Space |
| Cancel | B | X |
| Pause / return | START | Esc |
| Items | L / R select, Y use | Q / E select, C use |
| Language, volume | Title → Options (in battle: START → Options) | |

The game starts in English. Japanese can be selected under Options → Language (the setting is saved).

---

## Running it

### Requirements
- Python 3.10+
- [Pyxel](https://github.com/kitao/pyxel) 2.9+ (`pip install pyxel`)

### Run
```bash
python3 main.py
```
or the packaged build (`Bit-Rate-Rush.pyxapp`, from [Releases](../../releases)):
```bash
pyxel play Bit-Rate-Rush.pyxapp
```

### Tested on
- macOS (Pyxel 2.9.9)
- Anbernic handhelds running plumOS-Bubble (RK3566, Pyxel 2.9.3) — drop the `.pyxapp` into Pyxel's ROM folder

### Save data
`save.json` and `settings.json` are written to Pyxel's user data directory (`pyxel.user_data_dir("kroot", "Bit-Rate-Rush")`).

---

## Status

- **v1.0.0** — Part one (the Lumen arc): the core loop and the first half of the story
- **v1.0.1** — Fixed a crash at startup on Pyxel Web (browser / PWF)
- **v1.1.0 (planned)** — Part two (the Aria arc)

Bugs and impressions are welcome in [Issues](../../issues). Balance will be tuned from feedback.

---

## License

| | |
|---|---|
| **Source code** | [PolyForm Noncommercial License 1.0.0](LICENSE) — free to use, modify and redistribute **for noncommercial purposes** |
| **Assets** (music, art, portraits, icons, story text) | [All rights reserved](LICENSE-assets.md) — usable only as part of this game |
| **Third-party components** (the bundled font) | see [THIRD-PARTY.md](THIRD-PARTY.md) |

For commercial use, please contact the author.

**Pull requests are not being accepted at this time.** If that changes, the terms for contributions will be stated here.

Copyright (c) 2026 game-de-it
