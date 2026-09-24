"""
FNF-бот (Roblox) — v8.3.
- Логика нажатий = v7.0 (fire-and-forget, одиночные тапы)
- ROI УВЕЛИЧЕН: длиннее вверх (tail_height=500) + ниже (below_view=300)
- Отслеживание расширено: head_half_h=12, col_half_w=20
- Пресеты, FPS 60, файл создаётся сразу
"""

import json, os, sys, threading, time, tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import mss
import numpy as np
import cv2
import keyboard

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "fnf_bot_config.json")
PRESETS_FILE = os.path.join(BASE_DIR, "fnf_bot_presets.json")

DEFAULT_CONFIG = {
    "keys": ["a", "s", "k", "l"],
    "col_x": [1270, 1435, 1590, 1750],
    "receptor_y": 155,

    "head_offset": 30,
    "head_half_h": 12,           # ← было 8
    "col_half_w": 20,            # ← было 16
    "tail_height": 500,          # ← было 250
    "below_view": 300,           # ← вернулось, было 0
    "tail_x_offset": [-6, 0, 0, 6],
    "glow_buffer": 15,

    "tap_duration_ms": 20,
    "min_gap_ms": 15,
    "fps": 60,

    "min_head_pixels": 40,
    "min_tail_pixels": 10,

    "use_tail": False,

    "hsv": [
        [[130, 120, 110], [170, 255, 255]],
        [[95, 120, 110],  [125, 255, 255]],
        [[45, 120, 110],  [75, 255, 255]],
        [[[0, 120, 100], [10, 255, 255]],
         [[170, 120, 100], [180, 255, 255]]],
    ],
}


# ==================== ПРЕСЕТЫ ====================

BUILTIN_PRESETS = {
    "Стандарт — Стрелки справа": {
        "keys": ["a", "s", "k", "l"],
        "col_x": [1265, 1435, 1590, 1750],
        "receptor_y": 155,
        "head_offset": 30, "head_half_h": 12, "col_half_w": 20,
        "tail_height": 500, "below_view": 300,
        "tail_x_offset": [-6, 0, 0, 6], "glow_buffer": 15,
        "tap_duration_ms": 20, "min_gap_ms": 15, "fps": 120,
        "min_head_pixels": 40, "min_tail_pixels": 10,
        "use_tail": False,
        "hsv": [
            [[130, 120, 110], [170, 255, 255]],
            [[95, 120, 110],  [125, 255, 255]],
            [[45, 120, 110],  [75, 255, 255]],
            [[[0, 120, 100], [10, 255, 255]],
             [[170, 120, 100], [180, 255, 255]]],
        ],
    },
    "Стандарт — Стрелки слева": {
        "keys": ["a", "s", "k", "l"],
        "col_x": [165, 335, 490, 655],
        "receptor_y": 155,
        "head_offset": 30, "head_half_h": 12, "col_half_w": 20,
        "tail_height": 500, "below_view": 300,
        "tail_x_offset": [-6, 0, 0, 6], "glow_buffer": 15,
        "tap_duration_ms": 20, "min_gap_ms": 15, "fps": 120,
        "min_head_pixels": 40, "min_tail_pixels": 10,
        "use_tail": False,
        "hsv": [
            [[130, 120, 110], [170, 255, 255]],
            [[95, 120, 110],  [125, 255, 255]],
            [[45, 120, 110],  [75, 255, 255]],
            [[[0, 120, 100], [10, 255, 255]],
             [[170, 120, 100], [180, 255, 255]]],
        ],
    },
    "Monochrome — Круги справа": {
        "keys": ["a", "s", "k", "l"],
        "col_x": [1245, 1370, 1500, 1630],
        "receptor_y": 160,
        "head_offset": 35, "head_half_h": 14, "col_half_w": 32,
        "tail_height": 500, "below_view": 250,
        "tail_x_offset": [0, 0, 0, 0], "glow_buffer": 20,
        "tap_duration_ms": 20, "min_gap_ms": 15, "fps": 120,
        "min_head_pixels": 60, "min_tail_pixels": 20,
        "use_tail": False,
        "hsv": [
            [[0, 0, 180], [180, 60, 255]],
            [[0, 0, 180], [180, 60, 255]],
            [[0, 0, 180], [180, 60, 255]],
            [[0, 0, 180], [180, 60, 255]],
        ],
    },
    "Monochrome — Круги слева": {
        "keys": ["a", "s", "k", "l"],
        "col_x": [175, 305, 435, 565],
        "receptor_y": 160,
        "head_offset": 35, "head_half_h": 14, "col_half_w": 32,
        "tail_height": 500, "below_view": 250,
        "tail_x_offset": [0, 0, 0, 0], "glow_buffer": 20,
        "tap_duration_ms": 20, "min_gap_ms": 15, "fps": 120,
        "min_head_pixels": 60, "min_tail_pixels": 20,
        "use_tail": False,
        "hsv": [
            [[0, 0, 180], [180, 60, 255]],
            [[0, 0, 180], [180, 60, 255]],
            [[0, 0, 180], [180, 60, 255]],
            [[0, 0, 180], [180, 60, 255]],
        ],
    },
    "15 Копеек (kvartira 42) — Стрелки справа": {
        "keys": ["a", "s", "k", "l"],
        "col_x": [1265, 1435, 1590, 1750],
        "receptor_y": 155,
        "head_offset": 30, "head_half_h": 12, "col_half_w": 20,
        "tail_height": 500, "below_view": 300,
        "tail_x_offset": [-6, 0, 0, 6], "glow_buffer": 15,
        "tap_duration_ms": 20, "min_gap_ms": 15, "fps": 120,
        "min_head_pixels": 40, "min_tail_pixels": 10,
        "use_tail": False,
        "hsv": [
            [[130, 120, 110], [170, 255, 255]],
            [[95, 120, 110],  [125, 255, 255]],
            [[45, 120, 110],  [75, 255, 255]],
            [[[0, 120, 100], [10, 255, 255]],
             [[170, 120, 100], [180, 255, 255]]],
        ],
    },
}


def load_presets():
    if os.path.exists(PRESETS_FILE):
        try:
            with open(PRESETS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and data:
                for name, p in BUILTIN_PRESETS.items():
                    data.setdefault(name, json.loads(json.dumps(p)))
                return data
        except Exception as e:
            print(f"[presets] ошибка чтения: {e}")
    data = json.loads(json.dumps(BUILTIN_PRESETS))
    save_presets(data)
    return data


def save_presets(presets):
    try:
        with open(PRESETS_FILE, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[presets] ошибка записи: {e}")
        return False


# ==================== WORKER ====================

class BotWorker(threading.Thread):
    def __init__(self, cfg, stop_event, log_cb, status_cb, debug_shared):
        super().__init__(daemon=True)
        self.cfg = cfg
        self.stop_event = stop_event
        self.log = log_cb
        self.status = status_cb
        self.debug_shared = debug_shared

    @staticmethod
    def _in_range_for(col_hsv, rng):
        if isinstance(rng[0][0], list):
            m1 = cv2.inRange(col_hsv, np.array(rng[0][0], np.uint8), np.array(rng[0][1], np.uint8))
            m2 = cv2.inRange(col_hsv, np.array(rng[1][0], np.uint8), np.array(rng[1][1], np.uint8))
            return cv2.bitwise_or(m1, m2)
        return cv2.inRange(col_hsv, np.array(rng[0], np.uint8), np.array(rng[1], np.uint8))

    def _build_masks(self, hsv, rx_local, col_hw):
        masks_head, masks_tail = [], []
        offsets = self.cfg.get("tail_x_offset", [0, 0, 0, 0])

        for i in range(4):
            rng = self.cfg["hsv"][i]

            x1 = max(0, rx_local[i] - col_hw)
            x2 = min(hsv.shape[1], rx_local[i] + col_hw)
            masks_head.append(self._in_range_for(hsv[:, x1:x2], rng))

            cx = rx_local[i] + int(offsets[i])
            x1 = max(0, cx - col_hw)
            x2 = min(hsv.shape[1], cx + col_hw)
            masks_tail.append(self._in_range_for(hsv[:, x1:x2], rng))

        return masks_head, masks_tail

    def run(self):
        sct = mss.mss()
        mon = sct.monitors[1]

        col_x = self.cfg["col_x"]
        rec_y = self.cfg["receptor_y"]
        col_hw = int(self.cfg["col_half_w"])
        head_off = int(self.cfg["head_offset"])
        head_hh = int(self.cfg["head_half_h"])
        tail_h = int(self.cfg["tail_height"])
        below_view = int(self.cfg.get("below_view", 300))
        glow_buf = int(self.cfg.get("glow_buffer", 15))
        use_tail = bool(self.cfg.get("use_tail", True))

        # --- ROI: увеличен по вертикали и по ширине ---
        max_off = max(abs(o) for o in self.cfg.get("tail_x_offset", [0, 0, 0, 0]))
        pad_x = col_hw + 16 + max_off
        roi_x1 = max(0, min(col_x) - pad_x)
        roi_x2 = min(mon["width"], max(col_x) + pad_x)
        roi_y1 = max(0, rec_y - tail_h - head_off - head_hh - 20)
        roi_y2 = min(mon["height"], rec_y + below_view)
        region = {"top": roi_y1, "left": roi_x1,
                  "width": roi_x2 - roi_x1, "height": roi_y2 - roi_y1}

        rx_local = [x - roi_x1 for x in col_x]
        ry_local = rec_y - roi_y1
        rh = region["height"]

        head_y1 = max(0, ry_local - head_off - head_hh)
        head_y2 = min(rh, ry_local - head_off + head_hh)

        sustain_above_end = max(0, ry_local - glow_buf)
        sustain_below_start = min(rh, ry_local + glow_buf)

        mode = "ВКЛ" if use_tail else "ВЫКЛ"
        self.log(f"▶ Старт v8.3. ROI={region['width']}×{rh}, хвосты={mode}")
        self.log(f"   head=[{head_y1}:{head_y2}], хвост выше=[0:{sustain_above_end}], "
                 f"ниже=[{sustain_below_start}:{rh}]")

        keys = self.cfg["keys"]
        pressed = [False] * 4
        prev_head = [False] * 4
        press_started = [0.0] * 4
        next_allowed = [0.0] * 4

        tap_s = self.cfg["tap_duration_ms"] / 1000.0
        gap_s = self.cfg["min_gap_ms"] / 1000.0
        frame_time = 1.0 / max(1, self.cfg["fps"])
        min_head = self.cfg["min_head_pixels"]
        min_tail = self.cfg["min_tail_pixels"]

        self.status("running")
        hits = 0

        try:
            while not self.stop_event.is_set():
                if keyboard.is_pressed("f8"):
                    self.log("⏹ Стоп по F8"); break

                t0 = time.perf_counter()
                frame = np.array(sct.grab(region))
                hsv = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR),
                                   cv2.COLOR_BGR2HSV)
                masks_head, masks_tail = self._build_masks(hsv, rx_local, col_hw)

                now = time.perf_counter()
                debug_states = []

                for i in range(4):
                    # --- Голова: rising edge ---
                    head_px = int(np.count_nonzero(masks_head[i][head_y1:head_y2, :]))
                    has_head = head_px >= min_head

                    # --- Хвост: выше + ниже рецептора ---
                    if use_tail:
                        mt = masks_tail[i]
                        above_px = int(np.count_nonzero(mt[0:sustain_above_end, :])) if sustain_above_end > 0 else 0
                        below_px = int(np.count_nonzero(mt[sustain_below_start:rh, :])) if sustain_below_start < rh else 0
                        sustain_px = above_px + below_px
                        has_sustain = sustain_px >= min_tail
                    else:
                        sustain_px = 0
                        has_sustain = False

                    new_note = has_head and not prev_head[i]
                    debug_states.append((has_head, has_sustain, pressed[i], head_px, sustain_px))

                    # ═══════ ЛОГИКА v7.0 (fire-and-forget) ═══════
                    if not pressed[i]:
                        if new_note and now >= next_allowed[i]:
                            keyboard.press(keys[i])
                            pressed[i] = True
                            press_started[i] = now
                            hits += 1
                    else:
                        hold_min_until = press_started[i] + tap_s
                        if now < hold_min_until:
                            pass
                        elif use_tail and has_sustain:
                            pass
                        else:
                            keyboard.release(keys[i])
                            pressed[i] = False
                            next_allowed[i] = now + gap_s
                    # ═════════════════════════════════════════════

                    prev_head[i] = has_head

                if self.debug_shared is not None and self.debug_shared.get("enabled"):
                    self.debug_shared["frame"] = self._draw(
                        frame[:, :, :3].copy(), rx_local,
                        head_y1, head_y2, sustain_above_end, sustain_below_start, rh,
                        col_hw, debug_states, use_tail, ry_local)

                dt = time.perf_counter() - t0
                if dt < frame_time:
                    time.sleep(frame_time - dt)
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")
        finally:
            for i, k in enumerate(keys):
                if pressed[i]:
                    try: keyboard.release(k)
                    except Exception: pass
            self.log(f"✔ Стоп. Нажатий: {hits}")
            self.status("stopped")

    def _draw(self, img, rx, h_y1, h_y2, s_above_end, s_below_start, rh,
              col_hw, states, use_tail, ry_local):
        offsets = self.cfg.get("tail_x_offset", [0, 0, 0, 0])
        for i, x in enumerate(rx):
            has_head, has_sustain, is_pressed, hp, sp = states[i]

            c = (0, 255, 0) if has_head else (100, 100, 100)
            cv2.rectangle(img, (x - col_hw, h_y1), (x + col_hw, h_y2), c, 1)
            cv2.putText(img, f"h{hp}", (x - col_hw, h_y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, c, 1)

            if use_tail:
                xt = x + int(offsets[i])
                ct = (0, 165, 255) if has_sustain else (60, 60, 60)
                if s_above_end > 0:
                    cv2.rectangle(img, (xt - col_hw, 0), (xt + col_hw, s_above_end), ct, 1)
                if s_below_start < rh:
                    cv2.rectangle(img, (xt - col_hw, s_below_start), (xt + col_hw, rh - 1), ct, 1)
                cv2.putText(img, f"s{sp}", (xt - col_hw, 14),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.35, ct, 1)

            cv2.line(img, (x - 30, ry_local), (x + 30, ry_local), (255, 0, 255), 1)
            gb = int(self.cfg.get("glow_buffer", 15))
            cv2.line(img, (x - 20, ry_local - gb), (x + 20, ry_local - gb), (0, 200, 255), 1)
            cv2.line(img, (x - 20, ry_local + gb), (x + 20, ry_local + gb), (0, 200, 255), 1)

            if is_pressed:
                cv2.circle(img, (x, h_y2 + 8), 4, (0, 0, 255), -1)
        return img


# ==================== DEBUG WINDOW ====================

class DebugWindow:
    def __init__(self, root, shared):
        self.shared = shared
        self.top = tk.Toplevel(root)
        self.top.title("Debug — что видит бот")
        self.top.geometry("900x680")
        self.top.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = tk.Canvas(self.top, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._img_id = None; self._photo = None; self._running = True
        self.top.after(60, self.update)

    def update(self):
        if not self._running: return
        frame = self.shared.get("frame")
        if frame is not None:
            try:
                from PIL import Image, ImageTk
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                if img.width < 800:
                    scale = 800 / img.width
                    img = img.resize((int(img.width * scale), int(img.height * scale)))
                self._photo = ImageTk.PhotoImage(img)
                if self._img_id is None:
                    self._img_id = self.canvas.create_image(0, 0, anchor="nw", image=self._photo)
                else:
                    self.canvas.itemconfigure(self._img_id, image=self._photo)
            except ImportError:
                self.canvas.create_text(20, 20, anchor="nw",
                                        text="pip install pillow", fill="red")
                self._running = False; return
        self.top.after(60, self.update)

    def close(self):
        self._running = False
        self.shared["enabled"] = False
        self.top.destroy()


# ==================== PRESETS ====================

class PresetsWindow:
    def __init__(self, parent, gui):
        self.gui = gui
        self.top = tk.Toplevel(parent)
        self.top.title("Пресеты")
        self.top.geometry("440x540")
        self.top.resizable(False, False)
        self.top.transient(parent); self.top.grab_set()

        pad = {"padx": 6, "pady": 4}

        ttk.Label(self.top, text="Двойной клик — загрузить пресет",
                  foreground="#666").pack(anchor="w", padx=8, pady=(8, 0))

        f_list = ttk.LabelFrame(self.top, text="Список пресетов")
        f_list.pack(fill="both", expand=True, **pad)
        self.listbox = tk.Listbox(f_list, height=12, font=("Consolas", 10))
        self.listbox.pack(fill="both", expand=True, padx=4, pady=4, side="left")
        sb = ttk.Scrollbar(f_list, orient="vertical", command=self.listbox.yview)
        sb.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=sb.set)
        self.listbox.bind("<Double-Button-1>", lambda e: self.load_selected())

        f_btns = ttk.Frame(self.top); f_btns.pack(fill="x", **pad)
        ttk.Button(f_btns, text="📥 Загрузить", command=self.load_selected)\
            .pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(f_btns, text="💾 Сохранить как…", command=self.save_as)\
            .pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(f_btns, text="✏ Перезаписать", command=self.overwrite_selected)\
            .pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(f_btns, text="🗑 Удалить", command=self.delete_selected)\
            .pack(side="left", expand=True, fill="x", padx=2)

        ttk.Button(self.top, text="↺ Восстановить встроенные",
                   command=self.restore_builtin).pack(fill="x", padx=8, pady=(0, 8))

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, "end")
        self.presets = load_presets()
        for name in sorted(self.presets.keys()):
            self.listbox.insert("end", name)

    def _selected_name(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Пресеты", "Выбери пресет.")
            return None
        return self.listbox.get(sel[0])

    def load_selected(self):
        name = self._selected_name()
        if not name: return
        preset = self.presets.get(name)
        if not preset:
            messagebox.showerror("Пресеты", f"Не найден: {name}")
            return
        merged = json.loads(json.dumps(DEFAULT_CONFIG))
        merged.update(preset)
        self.gui.cfg = merged
        self.gui.apply_cfg_to_ui()
        self.gui.log(f"📥 Загружен пресет: {name}")

    def save_as(self):
        name = simpledialog.askstring("Сохранить пресет", "Имя:", parent=self.top)
        if not name: return
        name = name.strip()
        if not name: return
        if name in self.presets and not messagebox.askyesno(
                "Пресеты", f"«{name}» уже есть. Перезаписать?"):
            return
        if not self.gui.collect_cfg_from_ui(): return
        self.presets[name] = json.loads(json.dumps(self.gui.cfg))
        save_presets(self.presets); self.refresh()
        self.gui.log(f"💾 Сохранён пресет: {name}")

    def overwrite_selected(self):
        name = self._selected_name()
        if not name: return
        if not messagebox.askyesno("Пресеты", f"Перезаписать «{name}»?"):
            return
        if not self.gui.collect_cfg_from_ui(): return
        self.presets[name] = json.loads(json.dumps(self.gui.cfg))
        save_presets(self.presets)
        self.gui.log(f"✏ Перезаписан: {name}")

    def delete_selected(self):
        name = self._selected_name()
        if not name: return
        if not messagebox.askyesno("Пресеты", f"Удалить «{name}»?"):
            return
        self.presets.pop(name, None)
        save_presets(self.presets); self.refresh()
        self.gui.log(f"🗑 Удалён: {name}")

    def restore_builtin(self):
        if not messagebox.askyesno("Пресеты",
                "Восстановить встроенные? С такими же именами перезапишутся."):
            return
        for name, p in BUILTIN_PRESETS.items():
            self.presets[name] = json.loads(json.dumps(p))
        save_presets(self.presets); self.refresh()
        self.gui.log("↺ Встроенные восстановлены")


# ==================== GUI ====================

class BotGUI:
    def __init__(self, root):
        self.root = root
        root.title("FNF Bot — Roblox v8.3 (большой ROI, тапы v7.0)")
        root.geometry("760x1100")
        root.resizable(False, False)
        self.cfg = self.load_config()
        self.presets = load_presets()
        self.stop_event = threading.Event()
        self.worker = None
        self.debug_shared = {"enabled": False, "frame": None}
        self.debug_window = None
        self.presets_window = None
        self._build_ui()
        self.apply_cfg_to_ui()
        self.log(f"📂 Папка: {BASE_DIR}")
        self.log(f"📋 Пресетов загружено: {len(self.presets)}")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for k, v in DEFAULT_CONFIG.items():
                    data.setdefault(k, v)
                if not isinstance(data.get("hsv"), list) or len(data["hsv"]) != 4:
                    data["hsv"] = json.loads(json.dumps(DEFAULT_CONFIG["hsv"]))
                return data
            except Exception:
                pass
        return json.loads(json.dumps(DEFAULT_CONFIG))

    def save_config(self):
        if not self.collect_cfg_from_ui(): return
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cfg, f, indent=2)
        self.log("💾 Сохранено")

    def _build_ui(self):
        pad = {"padx": 6, "pady": 4}

        f_keys = ttk.LabelFrame(self.root, text="Клавиши")
        f_keys.pack(fill="x", **pad)
        self.entries_keys = []
        for i, name in enumerate(["Left", "Down", "Up", "Right"]):
            ttk.Label(f_keys, text=name, width=6).grid(row=0, column=i * 2, **pad)
            e = ttk.Entry(f_keys, width=6, justify="center")
            e.grid(row=0, column=i * 2 + 1, **pad)
            self.entries_keys.append(e)

        f_coords = ttk.LabelFrame(self.root, text="Координаты")
        f_coords.pack(fill="x", **pad)
        self.entries_x = []
        for i, name in enumerate(["L", "D", "U", "R"]):
            ttk.Label(f_coords, text=f"X {name}", width=5).grid(row=0, column=i * 2, **pad)
            e = ttk.Entry(f_coords, width=7, justify="center")
            e.grid(row=0, column=i * 2 + 1, **pad)
            self.entries_x.append(e)
        ttk.Label(f_coords, text="Receptor Y").grid(row=1, column=0, columnspan=2, **pad)
        self.entry_y = ttk.Entry(f_coords, width=7, justify="center")
        self.entry_y.grid(row=1, column=2, **pad)
        ttk.Button(f_coords, text="👁 Пипетка",
                   command=self.pick_coords).grid(row=1, column=4, columnspan=4, **pad)

        f_preset = ttk.LabelFrame(self.root, text="Пресеты")
        f_preset.pack(fill="x", **pad)
        ttk.Button(f_preset, text="📁 Менеджер пресетов",
                   command=self.open_presets).pack(side="left", expand=True,
                                                   fill="x", padx=4, pady=4)
        ttk.Button(f_preset, text="📂 Папка",
                   command=self.open_folder).pack(side="left", padx=4, pady=4)

        f_mode = ttk.LabelFrame(self.root, text="Режимы")
        f_mode.pack(fill="x", **pad)
        self.var_use_tail = tk.BooleanVar()
        ttk.Checkbutton(f_mode, text="Хвосты (sustain)",
                        variable=self.var_use_tail).pack(side="left", padx=8, pady=4)
        ttk.Label(f_mode, text="(выкл = чистые одиночные тапы)",
                  foreground="#666").pack(side="left", padx=6)

        f_geo = ttk.LabelFrame(self.root, text="Геометрия зон")
        f_geo.pack(fill="x", **pad)
        self._field(f_geo, "head_offset", "head_offset (px выше рецептора)", 0, 0)
        self._field(f_geo, "head_half_h", "head_half_h", 0, 2)
        self._field(f_geo, "col_half_w", "col_half_w", 1, 0)
        self._field(f_geo, "tail_height", "tail_height (ROI вверх)", 1, 2)
        self._field(f_geo, "below_view", "below_view (ROI вниз)", 2, 0)
        self._field(f_geo, "glow_buffer", "glow_buffer", 2, 2)

        f_tx = ttk.LabelFrame(self.root, text="Сдвиг зоны хвоста по X")
        f_tx.pack(fill="x", **pad)
        for i, name in enumerate(["Left", "Down", "Up", "Right"]):
            ttk.Label(f_tx, text=name, width=6).grid(row=0, column=i * 2, **pad)
            e = ttk.Entry(f_tx, width=6, justify="center")
            e.grid(row=0, column=i * 2 + 1, **pad)
            setattr(self, f"entry_txo_{i}", e)

        f_time = ttk.LabelFrame(self.root, text="Тайминги")
        f_time.pack(fill="x", **pad)
        self._field(f_time, "tap_duration_ms", "tap_duration_ms", 0, 0)
        self._field(f_time, "min_gap_ms", "min_gap_ms", 0, 2)
        self._field(f_time, "fps", "FPS", 1, 0)

        f_pix = ttk.LabelFrame(self.root, text="Пороги пикселей")
        f_pix.pack(fill="x", **pad)
        self._field(f_pix, "min_head_pixels", "min_head_pixels", 0, 0)
        self._field(f_pix, "min_tail_pixels", "min_tail_pixels", 0, 2)

        f_hsv = ttk.LabelFrame(self.root, text="HSV (низ — верх)")
        f_hsv.pack(fill="x", **pad)
        self.entries_hsv = []
        for i, name in enumerate(["Left", "Down", "Up", "Right"]):
            ttk.Label(f_hsv, text=name, width=6).grid(row=i, column=0, **pad)
            e1 = ttk.Entry(f_hsv, width=18, justify="center"); e1.grid(row=i, column=1, **pad)
            ttk.Label(f_hsv, text="—").grid(row=i, column=2)
            e2 = ttk.Entry(f_hsv, width=18, justify="center"); e2.grid(row=i, column=3, **pad)
            self.entries_hsv.append((e1, e2))
        ttk.Label(f_hsv, text="Красный — 2 диапазона через ';'",
                  wraplength=650, foreground="#555").grid(row=4, column=0, columnspan=4, pady=(2, 6))

        f_ctrl = ttk.Frame(self.root); f_ctrl.pack(fill="x", **pad)
        self.btn_start = ttk.Button(f_ctrl, text="▶ Старт", command=self.start_bot)
        self.btn_start.pack(side="left", expand=True, fill="x", padx=2)
        self.btn_stop = ttk.Button(f_ctrl, text="⏹ Стоп", command=self.stop_bot, state="disabled")
        self.btn_stop.pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(f_ctrl, text="🔍 Debug", command=self.open_debug)\
            .pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(f_ctrl, text="💾 Save", command=self.save_config)\
            .pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(f_ctrl, text="↺ Reset", command=self.reset_cfg)\
            .pack(side="left", expand=True, fill="x", padx=2)

        f_log = ttk.LabelFrame(self.root, text="Лог"); f_log.pack(fill="both", expand=True, **pad)
        self.log_box = tk.Text(f_log, height=5, state="disabled", bg="#111", fg="#0f0",
                               font=("Consolas", 9))
        self.log_box.pack(fill="both", expand=True, padx=4, pady=4)

        self.status_var = tk.StringVar(value="● Остановлен")
        self.status_lbl = ttk.Label(self.root, textvariable=self.status_var, anchor="w")
        self.status_lbl.pack(fill="x", padx=8, pady=(0, 6))

    def _field(self, parent, key, label, row, col):
        ttk.Label(parent, text=label).grid(row=row, column=col, sticky="w", padx=6, pady=4)
        e = ttk.Entry(parent, width=8, justify="center")
        e.grid(row=row, column=col + 1, padx=6, pady=4)
        setattr(self, f"entry_{key}", e)

    def log(self, msg): self.root.after(0, lambda: self._log(msg))

    def _log(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end"); self.log_box.configure(state="disabled")

    def set_status(self, state):
        def upd():
            if state == "running":
                self.status_var.set("● Работает"); self.status_lbl.configure(foreground="#0a0")
            else:
                self.status_var.set("● Остановлен"); self.status_lbl.configure(foreground="#a00")
        self.root.after(0, upd)

    def apply_cfg_to_ui(self):
        for i, e in enumerate(self.entries_keys):
            e.delete(0, "end"); e.insert(0, self.cfg["keys"][i])
        for i, e in enumerate(self.entries_x):
            e.delete(0, "end"); e.insert(0, str(self.cfg["col_x"][i]))
        self.entry_y.delete(0, "end"); self.entry_y.insert(0, str(self.cfg["receptor_y"]))

        for key in ["head_offset", "head_half_h", "col_half_w", "tail_height", "below_view",
                    "glow_buffer", "tap_duration_ms", "min_gap_ms", "fps",
                    "min_head_pixels", "min_tail_pixels"]:
            e = getattr(self, f"entry_{key}")
            e.delete(0, "end"); e.insert(0, str(self.cfg[key]))

        offs = self.cfg.get("tail_x_offset", [0, 0, 0, 0])
        for i in range(4):
            e = getattr(self, f"entry_txo_{i}")
            e.delete(0, "end"); e.insert(0, str(offs[i]))

        self.var_use_tail.set(bool(self.cfg.get("use_tail", True)))

        for i, (e1, e2) in enumerate(self.entries_hsv):
            rng = self.cfg["hsv"][i]
            if isinstance(rng[0][0], list):
                parts = [f"{r[0][0]},{r[0][1]},{r[0][2]}-{r[1][0]},{r[1][1]},{r[1][2]}" for r in rng]
                e1.delete(0, "end"); e1.insert(0, ";".join(parts))
                e2.delete(0, "end"); e2.insert(0, "")
            else:
                e1.delete(0, "end"); e1.insert(0, f"{rng[0][0]},{rng[0][1]},{rng[0][2]}")
                e2.delete(0, "end"); e2.insert(0, f"{rng[1][0]},{rng[1][1]},{rng[1][2]}")

    def collect_cfg_from_ui(self):
        try:
            self.cfg["keys"] = [e.get().strip().lower() for e in self.entries_keys]
            self.cfg["col_x"] = [int(e.get()) for e in self.entries_x]
            self.cfg["receptor_y"] = int(self.entry_y.get())

            for key in ["head_offset", "head_half_h", "col_half_w", "tail_height", "below_view",
                        "glow_buffer", "tap_duration_ms", "min_gap_ms", "fps",
                        "min_head_pixels", "min_tail_pixels"]:
                self.cfg[key] = int(getattr(self, f"entry_{key}").get())

            self.cfg["tail_x_offset"] = [
                int(getattr(self, f"entry_txo_{i}").get()) for i in range(4)
            ]
            self.cfg["use_tail"] = bool(self.var_use_tail.get())

            new_hsv = []
            for e1, e2 in self.entries_hsv:
                t1 = e1.get().strip(); t2 = e2.get().strip()
                if ";" in t1:
                    ranges = []
                    for p in t1.split(";"):
                        lo, hi = p.split("-")
                        ranges.append([list(map(int, lo.split(","))),
                                       list(map(int, hi.split(",")))])
                    new_hsv.append(ranges)
                else:
                    new_hsv.append([list(map(int, t1.split(","))),
                                    list(map(int, t2.split(",")))])
            if len(new_hsv) != 4:
                raise ValueError(f"HSV должен содержать 4 колонки, получено {len(new_hsv)}")
            self.cfg["hsv"] = new_hsv
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверь поля:\n{e}")
            return False

    def start_bot(self):
        if self.worker and self.worker.is_alive(): return
        if not self.collect_cfg_from_ui(): return
        self.stop_event.clear()
        self.worker = BotWorker(self.cfg, self.stop_event, self.log, self.set_status,
                                self.debug_shared)
        self.worker.start()
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")

    def stop_bot(self):
        self.stop_event.set(); self._poll_stop()

    def _poll_stop(self):
        if self.worker and self.worker.is_alive():
            self.root.after(150, self._poll_stop)
        else:
            self.btn_start.configure(state="normal")
            self.btn_stop.configure(state="disabled")

    def reset_cfg(self):
        if messagebox.askyesno("Сброс", "Вернуть настройки по умолчанию?"):
            self.cfg = json.loads(json.dumps(DEFAULT_CONFIG))
            self.apply_cfg_to_ui()
            self.log("↺ Сброшено")

    def pick_coords(self): OverlayPicker(self.root, self._apply_picked)

    def _apply_picked(self, xs, y):
        for i, e in enumerate(self.entries_x):
            e.delete(0, "end"); e.insert(0, str(xs[i]))
        self.entry_y.delete(0, "end"); self.entry_y.insert(0, str(y))
        self.log(f"✔ Координаты: X={xs}, Y={y}")

    def open_debug(self):
        if self.debug_window is None or not self.debug_window.top.winfo_exists():
            self.debug_shared["enabled"] = True
            self.debug_window = DebugWindow(self.root, self.debug_shared)
            self.log("🔍 Debug открыт")
        else:
            self.debug_window.close(); self.debug_window = None

    def open_presets(self):
        if self.presets_window is None or not self.presets_window.top.winfo_exists():
            self.presets_window = PresetsWindow(self.root, self)
            self.log("📁 Менеджер пресетов открыт")
        else:
            self.presets_window.top.lift()

    def open_folder(self):
        try:
            if os.name == "nt":
                os.startfile(BASE_DIR)
            elif sys.platform == "darwin":
                os.system(f'open "{BASE_DIR}"')
            else:
                os.system(f'xdg-open "{BASE_DIR}"')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть папку:\n{e}")


class OverlayPicker:
    def __init__(self, parent, on_done):
        self.on_done = on_done; self.xs = []; self.stage = 0
        self.labels = ["Left", "Down", "Up", "Right"]
        self.top = tk.Toplevel(parent)
        self.top.attributes("-fullscreen", True, "-alpha", 0.25, "-topmost", True)
        self.top.configure(bg="#000"); self.top.overrideredirect(True)
        self.canvas = tk.Canvas(self.top, bg="#000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.hint = self.canvas.create_text(200, 40, anchor="nw",
            text=f"Клик по центру стрелки: {self.labels[0]}",
            fill="#0ff", font=("Segoe UI", 16, "bold"))
        self.canvas.bind("<Button-1>", self.on_left)
        self.canvas.bind("<Button-3>", lambda e: self.cancel())
        self.top.bind("<Escape>", lambda e: self.cancel())
        self.top.grab_set(); self.top.focus_force()

    def on_left(self, ev):
        if self.stage < 4:
            self.xs.append(ev.x)
            self.canvas.create_oval(ev.x-10, ev.y-10, ev.x+10, ev.y+10, outline="#0f0", width=3)
            self.canvas.create_text(ev.x+14, ev.y, anchor="w",
                                    text=self.labels[self.stage], fill="#0f0",
                                    font=("Segoe UI", 11, "bold"))
            self.stage += 1
            if self.stage < 4:
                self.canvas.itemconfigure(self.hint,
                    text=f"Клик по центру стрелки: {self.labels[self.stage]}")
            else:
                self.canvas.itemconfigure(self.hint, text="Клик по ЛИНИИ попадания (Y)")
        else:
            self.on_done(self.xs, ev.y); self.top.destroy()

    def cancel(self): self.top.destroy()


def main():
    root = tk.Tk()
    try: ttk.Style().theme_use("clam")
    except Exception: pass
    BotGUI(root); root.mainloop()


if __name__ == "__main__":
    main()