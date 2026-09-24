<!-- ═══════════════════════════════════════════════════════════════ -->
<!--                        🇬🇧 ENGLISH                              -->
<!-- ═══════════════════════════════════════════════════════════════ -->

# 🎮 FNF-MINI-PROJECT — Screen Reader + Auto-Press Bot

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/status-active-success.svg" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/version-8.3-orange.svg" alt="Version">
  <img src="https://img.shields.io/badge/author-ZHBR--228-purple.svg" alt="Author">
</p>

<p align="center">
  <b>Auto-press bot for the Roblox version of Friday Night Funkin'</b><br>
  Reads screen pixels and presses keys in sync with the notes. No memory reading, no injection.
</p>

<p align="center">
  🎵 <a href="https://www.roblox.com/share?code=f31a2c4f820c0548800fbb67545be8f9&type=ExperienceDetails&stamp=1790237557391"><b>▶ Play the game on Roblox</b></a>
</p>

<p align="center">
  Made by <a href="https://github.com/ZHBR-228"><b>ZHBR-228</b></a>
</p>

---

## 📖 Table of Contents

- [What is this](#-what-is-this)
- [Why use it](#-why-use-it)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Default Keys](#-default-keys)
- [Presets](#-presets)
- [Configuration](#-configuration)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Disclaimer](#-disclaimer)
- [License](#-license)
- [Contributing](#-contributing)

---

## 🎯 What is this

**FNF-MINI-PROJECT** is a **standalone bot** for FNF-style rhythm games on Roblox. It:

- 📸 **Reads the screen** via `mss` (screenshots every 8–16 ms)
- 🎨 **Finds notes** by color (HSV) or brightness within configured zones
- ⌨️ **Emulates key presses** via `keyboard` library
- 🎵 **Holds tails** (sustain notes) — reacts not just to note appearance but to its continuation
- 🎚️ **Fully configurable** — coordinates, colors, thresholds, timings, modes
- 🖥️ **Has a GUI** — settings, presets, debug window, calibration picker

**The game it's made for** 👉 [**FNF Roblox — Play**](https://www.roblox.com/share?code=f31a2c4f820c0548800fbb67545be8f9&type=ExperienceDetails&stamp=1790237557391)

---

## 🧠 Why use it

| Reason | Explanation |
|---|---|
| 🎓 **Learn computer vision** | Practice HSV filtering, ROI cropping, threshold tuning, real-time processing |
| 🖥️ **Learn GUI programming** | Tkinter, threading, JSON configs, live settings |
| 🎮 **Enjoy the game** | Watch a song play itself, test skins, analyze patterns |
| 🛠️ **Base for forks** | Rewrite for any skin, any game, any keys — the code is clean and modular |
| 🤖 **Bot development** | Learn the fundamentals of screen-reading bots without touching memory |

> ⚠️ **DO NOT use against real players.** This project is for single-player and educational use. Disrupting other people's matches is bad.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖼️ **Screenshot detection** | No memory reading, no process injection — only pixels |
| 🎯 **ROI cropping** | Processes only the receptor area → FPS doesn't drop |
| 🎨 **HSV tuning** | Separate range for each column, supports red (2 ranges) |
| 🔥 **Tails (sustain)** | Holds the key until the note ends |
| ⚡ **Single taps** | Rising edge + `min_gap` — no sticking during spam |
| 👁️ **Debug window** | See exactly what the bot sees: zones, pixel counts, mode |
| 📁 **Presets** | Save and load configs for different skins |
| 🔘 **Coordinate picker** | Fullscreen overlay: 4 clicks on arrows + 1 on the hit line |
| 💾 **JSON config** | `fnf_bot_config.json` — right next to the script |
| ⌨️ **F8 hotkey** | Instant bot stop at any moment |
| 🌈 **Skins support** | Arrows, circles, dark, bright — any color scheme |
| 🎛️ **Live debugging** | Change settings without restarting the bot |

---

## 📋 Requirements

- **Windows** (tested on 10/11) — Linux/Mac may work with `pynput` instead of `keyboard`
- **Python 3.9+**
- **Roblox** running in **windowed mode** (not fullscreen exclusive)
- Any resolution (coordinates are configurable)

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/ZHBR-228/FNF-MINI-PROJECT.git
cd FNF-MINI-PROJECT

# 2. Install dependencies
pip install mss numpy opencv-python keyboard pillow

# 3. Run
python bot.py
```

### Optional: virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### `requirements.txt`

```
mss>=9.0.0
numpy>=1.24.0
opencv-python>=4.8.0
keyboard>=0.13.5
pillow>=10.0.0
```

---

## 🎮 Quick Start

1. **Launch Roblox** and enter the FNF place
2. **Launch the bot** — the GUI opens
3. Pick a preset in **📁 Preset Manager**:
   - `Standard — Arrows Right`
   - `Standard — Arrows Left`
   - `Monochrome — Circles Right`
   - `Monochrome — Circles Left`
   - `15 Kopeks (kvartira 42) — Arrows Left`
4. If coordinates don't match — click **👁 Picker** and click 4 receptors + the hit line
5. Open **🔍 Debug** — verify the zones match the notes
6. Press **▶ Start** and launch the song
7. **F8** — emergency stop at any moment

---

## ⌨️ Default Keys

```
┌────────┬───────┬──────┬────────┐
│  Left  │ Down  │  Up  │ Right  │
│   A    │   S   │  K   │   L    │
└────────┴───────┴──────┴────────┘
```

**Keys can be changed in the GUI** — just type your letters into the top fields and press **💾 Save**.

> 🎉 **For those who fork the project:** change anything — keys, coordinates, HSV, logic, add features. **Nobody will scold you for it.** Open project, MIT license, do whatever you want.

---

## 🖼️ Presets

All presets are stored in `fnf_bot_presets.json` next to the bot. Manage them via **📁 Preset Manager**:

| Button | Action |
|---|---|
| **📥 Load** | Apply preset to the current fields |
| **💾 Save as…** | Create a new preset from current settings |
| **✏ Overwrite** | Update the selected preset |
| **🗑 Delete** | Remove the preset |
| **↺ Restore built-ins** | Bring back the 5 default presets |
| **Double click** | Fast load |

### Built-in presets

| Name | Skin | Side |
|---|---|---|
| `Standard — Arrows Right` | Colored arrows | Right |
| `Standard — Arrows Left` | Colored arrows | Left |
| `Monochrome — Circles Right` | Grey circles | Right |
| `Monochrome — Circles Left` | Grey circles | Left |
| `15 Kopeks (kvartira 42) — Arrows Left` | Arrows | Left |

---

## 🔧 Configuration

### Zones

| Parameter | Description |
|---|---|
| `head_offset` | How many px **above** the receptor to look for a note (bigger = earlier reaction) |
| `head_half_h` | Half-height of the note detection zone |
| `col_half_w` | Half-width of the column |
| `tail_height` | ROI height upward (how far the bot sees above the receptor) |
| `below_view` | ROI height downward (for tails going under the receptor) |
| `glow_buffer` | Dead zone around the receptor (so the glow on press doesn't trigger) |
| `tail_x_offset` | X-axis offset of the tail zone per column |

### Timings

| Parameter | Description |
|---|---|
| `tap_duration_ms` | Minimum key hold time (ms) |
| `min_gap_ms` | Pause between presses in the same column (ms) |
| `fps` | Screen scan frequency |

### Thresholds

| Parameter | Description |
|---|---|
| `min_head_pixels` | Minimum colored pixels to consider it a note |
| `min_tail_pixels` | Minimum colored pixels for a sustain |

### Modes

| Parameter | Description |
|---|---|
| `use_tail` | Enable/disable sustain tracking |

---

## 🛠️ How It Works

```
┌─────────────────┐
│   mss.grab()    │  ← Screenshot of ROI (receptor area only)
└────────┬────────┘
         ▼
┌─────────────────┐
│  cv2.cvtColor   │  ← BGR → HSV
└────────┬────────┘
         ▼
┌─────────────────┐
│   cv2.inRange   │  ← Mask by HSV range
└────────┬────────┘
         ▼
┌─────────────────────────────────┐
│  Pixel counting in zones        │  ← head (rising edge), tail (sustain)
└────────┬────────────────────────┘
         ▼
┌─────────────────────────────────┐
│  Press state machine (v7.0)     │  ← press → hold min → release
└────────┬────────────────────────┘
         ▼
┌─────────────────┐
│ keyboard.press  │  ← Key emulation
└─────────────────┘
```

### Click logic (v7.0 — fire-and-forget)

```
1. Note enters head zone (rising edge) → press
2. Hold at least `tap_duration_ms`
3. If tail visible → keep holding
4. No tail and min time passed → release
5. Next press allowed only after `min_gap_ms`
```

---

## 🩺 Troubleshooting

| Problem | Solution |
|---|---|
| **Bot doesn't press** | Open Debug — if `hNN = 0`, coordinates or HSV are wrong |
| **Key sticking** | Uncheck "Tails" or increase `glow_buffer` to 25 |
| **Missing fast notes** | `min_gap_ms` ↓ to 8, `tap_duration_ms` ↓ to 15 |
| **FPS dropped** | `tail_height` ↓ to 300, `below_view` ↓ to 200 |
| **Presets file not opening** | Click **📂 Folder** — file lives next to `bot.py` |
| **Keys don't reach the game** | Run bot **as Administrator**, game must be in windowed mode |
| **Zones are off** | Use **👁 Picker** to recalibrate coordinates |
| **Wrong colors detected** | Adjust HSV ranges in the GUI (bottom section) |

---

## ❓ FAQ

**Q: Is this detectable by Roblox anti-cheat?**  
A: The bot doesn't inject into the process, doesn't read memory, and doesn't hook anything. It just takes screenshots and emulates key presses — same as a macro. However, Roblox may flag unusual input patterns if abused. Use at your own risk.

**Q: Can I use this in public games?**  
A: Technically yes, but **please don't**. Only in solo games or private servers. Ruining other players' matches is a bad look.

**Q: Does it work on Mac/Linux?**  
A: The `keyboard` library is Windows-only. On Mac/Linux, replace it with `pynput`.

**Q: How do I add a new skin preset?**  
A: Configure everything in the GUI, then **💾 Save as…** in the Preset Manager.

**Q: The bot reacts too early/late.**  
A: Adjust `head_offset` (bigger = earlier, smaller = later).

**Q: Where are my settings stored?**  
A: `fnf_bot_config.json` and `fnf_bot_presets.json` — right next to `bot.py`. Click **📂 Folder** to open the location.

---

## ⚠️ Disclaimer

- The project is created for **educational purposes** and **single-player use**
- It does **NOT** bypass anti-cheats, does **NOT** inject into the Roblox process
- It is **NOT intended** for playing against real players in multiplayer
- The author is **not responsible** for any account bans
- Respect the Roblox community rules and other players

---

## 📜 License

**MIT License** — do whatever you want: fork, modify, sell, rewrite from scratch. Just don't remove the author attribution.

Copyright (c) 2026 **ZHBR-228**

---

## 🙌 Contributing

Forks are welcome! If you built something cool — open a Pull Request or just share a link to your repository.

**Ideas for improvement:**
- 🎨 Auto HSV picking by clicking on a note
- 🔊 BPM detection from audio (no screen needed)
- 🖼️ Built-in zone editor (drag & drop in a window)
- 🌍 Support for 6-button mode (FNF 6K)
- 📱 Port to other languages (JS, C#)
- 🎮 Controller support
- 🎵 Rhythm-based difficulty scaling

---

<p align="center">
  Made with ♥ by <a href="https://github.com/ZHBR-228"><b>ZHBR-228</b></a> for the FNF community<br>
  <b>Good luck with your runs! 🎵🎮</b>
</p>

---

<!-- ═══════════════════════════════════════════════════════════════ -->
<!--                        🇷🇺 РУССКИЙ                              -->
<!-- ═══════════════════════════════════════════════════════════════ -->

---

# 🎮 FNF-MINI-PROJECT — Чтение экрана + автонажатия

<p align="center">
  <b>Бот для Roblox-версии Friday Night Funkin'</b><br>
  Читает пиксели экрана и нажимает клавиши в такт нотам. Без внедрения в процесс игры.
</p>

<p align="center">
  🎵 <a href="https://www.roblox.com/share?code=f31a2c4f820c0548800fbb67545be8f9&type=ExperienceDetails&stamp=1790237557391"><b>▶ Играть в игру на Roblox</b></a>
</p>

<p align="center">
  Автор — <a href="https://github.com/ZHBR-228"><b>ZHBR-228</b></a>
</p>

---

## 📖 Содержание

- [Что это](#-что-это)
- [Зачем это](#-зачем-это)
- [Возможности](#-возможности)
- [Требования](#-требования)
- [Установка](#-установка)
- [Быстрый старт](#-быстрый-старт)
- [Клавиши по умолчанию](#️-клавиши-по-умолчанию)
- [Пресеты](#-пресеты)
- [Настройки](#-настройки)
- [Как это работает](#️-как-это-работает)
- [Решение проблем](#-решение-проблем)
- [FAQ](#-faq-1)
- [Disclaimer](#️-disclaimer)
- [Лицензия](#-лицензия)
- [Вклад](#-вклад)

---

## 🎯 Что это

**FNF-MINI-PROJECT** — **самостоятельный бот** для FNF-игр на платформе Roblox. Он:

- 📸 **Читает экран** через `mss` (скриншоты каждые 8–16 мс)
- 🎨 **Находит ноты** по цвету (HSV) или яркости в заданных зонах
- ⌨️ **Эмулирует нажатия** клавиш через библиотеку `keyboard`
- 🎵 **Держит хвосты** (sustain) — реагирует не только на появление ноты, но и на её продолжение
- 🎚️ **Полностью настраивается** — координаты, цвета, пороги, тайминги, режимы
- 🖥️ **Имеет GUI** — настройки, пресеты, Debug-окно, пипетка калибровки

**Игра, под которую сделан бот** 👉 [**FNF Roblox — играть**](https://www.roblox.com/share?code=f31a2c4f820c0548800fbb67545be8f9&type=ExperienceDetails&stamp=1790237557391)

---

## 🧠 Зачем это

| Причина | Объяснение |
|---|---|
| 🎓 **Изучить computer vision** | Практика HSV, ROI, порогов, real-time обработки |
| 🖥️ **Изучить GUI** | Tkinter, потоки, JSON-конфиги, live-настройки |
| 🎮 **Играть в своё удовольствие** | Посмотреть, как песня играется сама, потестить скины |
| 🛠️ **База для форков** | Переделать под любой скин, любую игру, любые клавиши |
| 🤖 **Bot development** | Освоить основы скриншот-ботов без работы с памятью |

> ⚠️ **НЕ используй против реальных игроков.** Проект сделан для одиночной игры и обучения. Нарушать правила сообщества и портить матчи другим людям — плохо.

---

## ✨ Возможности

| Фича | Описание |
|---|---|
| 🖼️ **Скриншот-детект** | Не читает память, не внедряется в процесс — только пиксели |
| 🎯 **ROI-кроп** | Обрабатывает только область рецепторов → FPS не падает |
| 🎨 **HSV-настройка** | Отдельный диапазон для каждой колонки, поддержка красного (2 диапазона) |
| 🔥 **Хвосты (sustain)** | Держит клавишу до конца ноты |
| ⚡ **Одиночные тапы** | Rising edge + `min_gap` — не заедает на спаме |
| 👁️ **Debug-окно** | Видишь, что бот видит: зоны, пиксели, режим |
| 📁 **Пресеты** | Сохраняй и загружай конфиги под разные скины |
| 🔘 **Пипетка координат** | Оверлей на весь экран: 4 клика по стрелкам + 1 по линии попадания |
| 💾 **JSON-конфиг** | `fnf_bot_config.json` — рядом со скриптом |
| ⌨️ **Хоткей F8** | Мгновенная остановка бота |
| 🌈 **Поддержка скинов** | Стрелки, круги, тёмные, яркие — любая цветовая схема |
| 🎛️ **Live debugging** | Меняй настройки без перезапуска бота |

---

## 📋 Требования

- **Windows** (протестировано на 10/11) — Linux/Mac могут работать с `pynput` вместо `keyboard`
- **Python 3.9+**
- **Roblox** запущен в **оконном режиме** (не fullscreen exclusive)
- Любое разрешение (координаты настраиваются)

---

## 🚀 Установка

```bash
# 1. Клонируй репозиторий
git clone https://github.com/ZHBR-228/FNF-MINI-PROJECT.git
cd FNF-MINI-PROJECT

# 2. Установи зависимости
pip install mss numpy opencv-python keyboard pillow

# 3. Запусти
python bot.py
```

### Опционально: виртуальное окружение

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### `requirements.txt`

```
mss>=9.0.0
numpy>=1.24.0
opencv-python>=4.8.0
keyboard>=0.13.5
pillow>=10.0.0
```

---

## 🎮 Быстрый старт

1. **Запусти Roblox** и зайди в FNF-плейс
2. **Запусти бота** — откроется меню
3. Выбери пресет в **📁 Preset Manager**:
   - `Standard — Arrows Right`
   - `Standard — Arrows Left`
   - `Monochrome — Circles Right`
   - `Monochrome — Circles Left`
   - `15 Kopeks (kvartira 42) — Arrows Left`
4. Если координаты не совпали — нажми **👁 Picker** и кликни по 4 рецепторам + по линии попадания
5. Открой **🔍 Debug** — проверь, что зоны совпадают с нотами
6. Нажми **▶ Start** и запусти песню
7. **F8** — экстренная остановка в любой момент

---

## ⌨️ Клавиши по умолчанию

```
┌────────┬───────┬──────┬────────┐
│  Left  │ Down  │  Up  │ Right  │
│   A    │   S   │  K   │   L    │
└────────┴───────┴──────┴────────┘
```

**Клавиши можно поменять в меню** — просто впиши свои буквы в поля вверху и нажми **💾 Save**.

> 🎉 **Для тех, кто форкает проект:** меняйте что угодно — клавиши, координаты, HSV, логику, добавляйте фичи. **Никто вас за это не будет ругать.** Проект открытый, MIT-лицензия, делайте что хотите.

---

## 🖼️ Пресеты

Все пресеты хранятся в `fnf_bot_presets.json` рядом с ботом. Управление — через **📁 Preset Manager**:

| Кнопка | Что делает |
|---|---|
| **📥 Load** | Применить пресет к текущим полям |
| **💾 Save as…** | Создать новый пресет из текущих настроек |
| **✏ Overwrite** | Обновить выбранный пресет |
| **🗑 Delete** | Удалить пресет |
| **↺ Restore built-ins** | Вернуть встроенные 5 пресетов |
| **Двойной клик** | Быстрая загрузка |

### Встроенные пресеты

| Название | Скин | Сторона |
|---|---|---|
| `Standard — Arrows Right` | Цветные стрелки | Справа |
| `Standard — Arrows Left` | Цветные стрелки | Слева |
| `Monochrome — Circles Right` | Серые круги | Справа |
| `Monochrome — Circles Left` | Серые круги | Слева |
| `15 Kopeks (kvartira 42) — Arrows Left` | Стрелки | Слева |

---

## 🔧 Настройки

### Зоны

| Параметр | Что делает |
|---|---|
| `head_offset` | На сколько px **выше** рецептора искать ноту (больше = реагирует раньше) |
| `head_half_h` | Половина высоты зоны детекта ноты |
| `col_half_w` | Половина ширины колонки |
| `tail_height` | Высота ROI вверх (сколько видит над рецептором) |
| `below_view` | Высота ROI вниз (для хвостов, уходящих под рецептор) |
| `glow_buffer` | Мёртвая зона вокруг рецептора (чтобы свечение при нажатии не триггерило) |
| `tail_x_offset` | Сдвиг зоны хвоста по X для каждой колонки |

### Тайминги

| Параметр | Что делает |
|---|---|
| `tap_duration_ms` | Минимальное удержание клавиши (мс) |
| `min_gap_ms` | Пауза между нажатиями в одной колонке (мс) |
| `fps` | Частота сканирования экрана |

### Пороги

| Параметр | Что делает |
|---|---|
| `min_head_pixels` | Сколько пикселей цвета нужно, чтобы счесть это нотой |
| `min_tail_pixels` | Сколько пикселей цвета нужно для sustain |

### Режимы

| Параметр | Что делает |
|---|---|
| `use_tail` | Включить/выключить отслеживание sustain |

---

## 🛠️ Как это работает

```
┌─────────────────┐
│   mss.grab()    │  ← Скриншот ROI (только зона рецепторов)
└────────┬────────┘
         ▼
┌─────────────────┐
│  cv2.cvtColor   │  ← BGR → HSV
└────────┬────────┘
         ▼
┌─────────────────┐
│   cv2.inRange   │  ← Маска по HSV-диапазону
└────────┬────────┘
         ▼
┌─────────────────────────────────┐
│  Подсчёт пикселей в зонах       │  ← head (rising edge), tail (sustain)
└────────┬────────────────────────┘
         ▼
┌─────────────────────────────────┐
│  State machine нажатий (v7.0)   │  ← press → hold min → release
└────────┬────────────────────────┘
         ▼
┌─────────────────┐
│ keyboard.press  │  ← Эмуляция клавиш
└─────────────────┘
```

### Логика нажатий (v7.0 — fire-and-forget)

```
1. Нота входит в зону головы (rising edge) → press
2. Держим минимум tap_duration_ms
3. Если виден хвост → продолжаем держать
4. Хвоста нет и минимум прошёл → release
5. Следующее нажатие только через min_gap_ms
```

---

## 🩺 Решение проблем

| Проблема | Решение |
|---|---|
| **Бот не нажимает** | Открой Debug — если `hNN = 0`, координаты или HSV неверные |
| **Заедает клавиша** | Сними галочку «Tails» или увеличь `glow_buffer` до 25 |
| **Пропускает быстрые ноты** | `min_gap_ms` ↓ до 8, `tap_duration_ms` ↓ до 15 |
| **FPS просел** | `tail_height` ↓ до 300, `below_view` ↓ до 200 |
| **Не открывается файл пресетов** | Нажми **📂 Folder** — файл лежит рядом с `bot.py` |
| **Клавиши не проходят в игру** | Запусти бота **от имени администратора**, игра должна быть в оконном режиме |
| **Зоны смещены** | Воспользуйся **👁 Picker** для перекалибровки координат |
| **Ловит не те цвета** | Подстрой HSV-диапазоны в нижней секции меню |

---

## ❓ FAQ

**В: Это детектится античитом Roblox?**  
О: Бот не внедряется в процесс, не читает память и не хукает ничего. Он просто делает скриншоты и эмулирует клавиши — как макрос. Однако Roblox может замечать необычные паттерны ввода, если злоупотреблять. Используй на свой риск.

**В: Можно ли это в публичных играх?**  
О: Технически да, но **пожалуйста, не надо**. Только в соло или на приватных серверах. Порт другие матчи — плохо.

**В: Работает на Mac/Linux?**  
О: Библиотека `keyboard` — Windows-only. На Mac/Linux замени на `pynput`.

**В: Как добавить свой пресет скина?**  
О: Настрой всё в меню, затем **💾 Save as…** в Preset Manager.

**В: Бот реагирует слишком рано/поздно.**  
О: Подкрути `head_offset` (больше = раньше, меньше = позже).

**В: Где хранятся настройки?**  
О: `fnf_bot_config.json` и `fnf_bot_presets.json` — рядом с `bot.py`. Нажми **📂 Folder** чтобы открыть папку.

---

## ⚠️ Disclaimer

- Проект создан **в образовательных целях** и для **одиночной игры**
- **НЕ** обходит античиты, **НЕ** внедряется в процесс Roblox
- **НЕ предназначен** для игры против реальных игроков в мультиплеере
- Автор **не несёт ответственности** за возможные блокировки аккаунта
- Соблюдай правила сообщества Roblox и уважай других игроков

---

## 📜 Лицензия

**MIT License** — делай что хочешь, форкай, изменяй, продавай, переписывай с нуля. Только не удаляй упоминание автора.

Copyright (c) 2026 **ZHBR-228**

---

## 🙌 Вклад

Форки приветствуются! Если сделал что-то крутое — оформи Pull Request или просто поделись ссылкой на свой репозиторий.

**Что можно улучшить:**
- 🎨 Автоподбор HSV по клику на ноту
- 🔊 Детект BPM по звуку (без экрана)
- 🖼️ Встроенный редактор зон (drag & drop в окне)
- 🌍 Поддержка 6-кнопочного режима (FNF 6K)
- 📱 Порт на другие языки (JS, C#)
- 🎮 Поддержка геймпада
- 🎵 Скейлинг сложности по ритму

---

<p align="center">
  Сделано с ♥ от <a href="https://github.com/ZHBR-228"><b>ZHBR-228</b></a> для FNF-сообщества<br>
  <b>Удачи в забегах! 🎵🎮</b>
</p>

---

<!-- ═══════════════════════════════════════════════════════════════ -->
<!--                     FIN / КОНЕЦ                                -->
<!-- ═══════════════════════════════════════════════════════════════ -->