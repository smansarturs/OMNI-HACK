import tkinter as tk
from tkinter import messagebox
import random
import time
import database


class GameState:
    """Global state to track progress across all games."""
    def __init__(self):
        self.security_level = 1
        self.integrity = 3
        self.credits = 0
        self.completed_games = 0

    def upgrade(self):
        self.completed_games += 1
        if self.completed_games % 3 == 0:
            self.security_level += 1
            self.integrity = 3  # Restore health on level up


state = GameState()


class HackingHub:
    def __init__(self, root):
        self.root = root
        self.root.title("OMNI-HACK v11.0 - PRO EDITION")
        self.root.configure(bg="#050505")
        self.root.geometry("1000x800")

        self.setup_main_layout()
        self.log("SYSTEM INITIALIZED... Welcome, Operator.")
        self.log("SECURITY LEVEL: " + str(state.security_level))
        self.log("STATUS: Connection Stable. Awaiting Target...")

    def setup_main_layout(self):
        # Top Bar: Status
        self.status_frame = tk.Frame(self.root, bg="#111", height=50, highlightbackground="#00FF00", highlightthickness=1)
        self.status_frame.pack(fill=tk.X, padx=5, pady=5)

        self.lbl_sec = tk.Label(self.status_frame, text=f"SEC LEVEL: {state.security_level}", fg="#00FF00", bg="#111", font=("Courier", 12, "bold"))
        self.lbl_sec.pack(side=tk.LEFT, padx=20)

        self.lbl_int = tk.Label(self.status_frame, text=f"INTEGRITY: {'-' * state.integrity}", fg="red", bg="#111", font=("Courier", 12, "bold"))
        self.lbl_int.pack(side=tk.LEFT, padx=20)

        self.lbl_cred = tk.Label(self.status_frame, text=f"CREDITS: {state.credits}", fg="cyan", bg="#111", font=("Courier", 12, "bold"))
        self.lbl_cred.pack(side=tk.RIGHT, padx=20)

        # Main Content Area
        self.content_frame = tk.Frame(self.root, bg="#050505")
        self.content_frame.pack(expand=True, fill=tk.BOTH, padx=20)

        # Bottom Terminal Log
        self.log_frame = tk.Frame(self.root, bg="black", highlightbackground="#333", highlightthickness=1)
        self.log_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

        self.console = tk.Text(self.log_frame, height=8, bg="black", fg="#00FF00", font=("Courier", 10), state=tk.DISABLED, borderwidth=0)
        self.console.pack(fill=tk.X, padx=5, pady=5)

        self.main_menu()

    def log(self, text):
        self.console.config(state=tk.NORMAL)
        timestamp = time.strftime("[%H:%M:%S] ")
        self.console.insert(tk.END, timestamp + text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    def update_status(self):
        self.lbl_sec.config(text=f"SEC LEVEL: {state.security_level}")
        self.lbl_int.config(text=f"INTEGRITY: {'-' * state.integrity}")
        self.lbl_cred.config(text=f"CREDITS: {state.credits}")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_content()
        self.update_status()

        categories = {
            "NETWORK": [
                ("Sequence Breach", SequenceBreach), ("Firewall Breach", FirewallBreach),
                ("Data Stream", DataStream), ("Port Scanner", PortScanner),
                ("Packet Sniffer", PacketSniffer), ("Ping Match", PingMatch)
            ],
            "SYSTEMS": [
                ("Binary Pulse", BinaryPulse), ("Logic Gate", LogicGate),
                ("SQL Injector", SQLInjector), ("Keylogger", Keylogger),
                ("Kernel Panic", KernelPanic), ("BIOS Math", BIOSMath)
            ],
            "HARDWARE": [
                ("Pattern Memory", PatternMemory), ("Fingerprint Scan", FingerprintScan),
                ("Signal Record", SignalRecord), ("RAM Scraper", RAMScraper),
                ("Backdoor Path", BackdoorPath), ("Symbol Mirror", SymbolMirror)
            ],
            "DATA": [
                ("Cipher Cracker", CipherCracker), ("Anagram Crack", AnagramCrack),
                ("Hash Matcher", HashMatcher), ("Metadata Wipe", MetadataWipe)
            ]
        }

        container = tk.Frame(self.content_frame, bg="#050505")
        container.pack(expand=True)

        for cat_name, games in categories.items():
            cat_frame = tk.Frame(container, bg="#050505", highlightbackground="#00FF00", highlightthickness=1)
            cat_frame.pack(side=tk.LEFT, padx=15, pady=15)

            tk.Label(cat_frame, text=cat_name, fg="cyan", bg="#050505", font=("Courier", 14, "bold")).pack(pady=10)

            for game_name, game_class in games:
                btn = tk.Button(cat_frame, text=game_name, bg="#111", fg="#00FF00",
                                font=("Courier", 10), width=22, relief=tk.FLAT,
                                activebackground="#004400",
                                command=lambda gc=game_class, gn=game_name: self.launch_game(gc, gn))
                btn.pack(pady=3, padx=10)

    def launch_game(self, game_class, game_name):
        self.log(f"ATTEMPTING BREACH: {game_name}...")
        self.clear_content()
        # The ABORT button is packed first, at the bottom, so tall games
        # (like Firewall Breach) can never push it out of the window.
        abort_btn = tk.Button(self.content_frame, text="ABORT", fg="red", bg="#050505",
                              command=lambda: game.abort())
        abort_btn.pack(side=tk.BOTTOM, pady=5)
        game = game_class(self.content_frame, self.main_menu, self)


# --- BASE GAME ---
class BaseGame:
    def __init__(self, parent, back_callback, hub):
        self.parent, self.back_callback, self.hub = parent, back_callback, hub
        self.game_running = True
        self.finished = False
        self.difficulty_mod = state.security_level * 0.2  # Increases difficulty

    def abort(self):
        self.game_running = False
        self.back_callback()

    def end_game(self, success, msg_win="BREACH SUCCESSFUL", msg_fail="BREACH FAILED"):
        if self.finished:  # protects against being called twice
            return
        self.finished = True
        self.game_running = False
        if success:
            state.credits += 100 * state.security_level
            state.upgrade()
            self.hub.log("[SUCCESS] Target compromised. Credits awarded.")
            messagebox.showinfo("System", f"{msg_win}\n+ {100 * state.security_level} Credits")
        else:
            state.integrity -= 1
            self.hub.log("[ERROR] Intrusion detected! Integrity damaged.")
            if state.integrity <= 0:
                try:
                    database.reset_progress(state)
                except Exception:
                    pass
                messagebox.showerror("CRITICAL FAILURE", "SYSTEM INTEGRITY ZERO. SESSION TERMINATED.")
                self.hub.root.quit()
                return
            messagebox.showerror("System", msg_fail)
        try:
            database.save_state(state)
        except Exception:
            pass
        self.back_callback()


# ------------------------------------------------------------------ NETWORK

class SequenceBreach(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        self.header = tk.Label(self.parent, text="SEQUENCE BREACH", fg="#00FF00", bg="#050505", font=("Courier", 18, "bold"))
        self.header.pack(pady=20)

        # Difficulty: sequence gets longer as security level rises
        self.seq_len = 4 + (state.security_level // 2)
        self.target = [random.randint(0, 9) for _ in range(self.seq_len)]
        self.progress = 0

        self.lbl = tk.Label(self.parent, text=f"TARGET: {' '.join(map(str, self.target))}", fg="cyan", bg="#050505", font=("Courier", 14))
        self.lbl.pack()

        # The grid always contains every digit of the target, so it can be won
        needed = list(dict.fromkeys(self.target))
        cells = needed + [random.randint(0, 9) for _ in range(16 - len(needed))]
        random.shuffle(cells)

        self.frame = tk.Frame(self.parent, bg="#050505")
        self.frame.pack(pady=20)
        self.btns = []
        for r in range(4):
            row = []
            for c in range(4):
                b = tk.Button(self.frame, text=str(cells[r * 4 + c]), width=5, bg="#111", fg="#00FF00",
                              font=("Courier", 12), command=lambda r=r, c=c: self.click(r, c))
                b.grid(row=r, column=c, padx=2, pady=2)
                row.append(b)
            self.btns.append(row)

    def click(self, r, c):
        if int(self.btns[r][c].cget("text")) == self.target[self.progress]:
            self.btns[r][c].config(bg="#006600", fg="white")
            self.progress += 1
            if self.progress == self.seq_len:
                self.end_game(True)
        else:
            self.btns[r][c].config(bg="#660000")
            self.end_game(False)


class FirewallBreach(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="FIREWALL BREACH: INTERCEPT PACKETS", fg="#00FF00", bg="#050505", font=("Courier", 18, "bold")).pack(pady=20)

        self.target_hits = 10
        self.hits = 0

        self.info_label = tk.Label(self.parent, text=f"INTERCEPTED: 0/{self.target_hits}", fg="cyan", bg="#050505", font=("Courier", 14))
        self.info_label.pack()

        self.warn_label = tk.Label(self.parent, text="CLICK CYAN, AVOID RED TRAPS!", fg="red", bg="#050505", font=("Courier", 12))
        self.warn_label.pack(pady=5)

        self.canvas = tk.Canvas(self.parent, width=600, height=400, bg="#050505", highlightthickness=1, highlightbackground="#00FF00")
        self.canvas.pack(pady=10)

        self.packets = []
        self.spawn_initial_packets()
        self.animate()

    def spawn_initial_packets(self):
        self.create_packet("target")
        self.create_packet("trap")
        self.create_packet("trap")

    def create_packet(self, p_type):
        color = "cyan" if p_type == "target" else "red"
        x, y = random.randint(20, 580), random.randint(20, 380)
        vx = random.choice([-3, -2, 2, 3])
        vy = random.choice([-3, -2, 2, 3])

        pkt_id = self.canvas.create_oval(x, y, x + 20, y + 20, fill=color, outline="white")
        self.canvas.tag_bind(pkt_id, "<Button-1>", lambda e, t=p_type: self.handle_click(t))

        self.packets.append({'id': pkt_id, 'type': p_type, 'x': x, 'y': y, 'vx': vx, 'vy': vy})

    def animate(self):
        if not self.game_running:
            return

        for p in self.packets:
            p['x'] += p['vx']
            p['y'] += p['vy']

            if p['x'] <= 0 or p['x'] >= 580:
                p['vx'] *= -1
            if p['y'] <= 0 or p['y'] >= 380:
                p['vy'] *= -1

            self.canvas.coords(p['id'], p['x'], p['y'], p['x'] + 20, p['y'] + 20)

        self.parent.after(30, self.animate)

    def handle_click(self, p_type):
        if not self.game_running:
            return
        if p_type == "target":
            self.hits += 1
            self.info_label.config(text=f"INTERCEPTED: {self.hits}/{self.target_hits}")
            for p in self.packets:
                if p['type'] == "target":
                    p['x'], p['y'] = random.randint(20, 580), random.randint(20, 380)
                    p['vx'] *= 1.1
                    p['vy'] *= 1.1

            if self.hits >= self.target_hits:
                self.end_game(True)
        else:
            self.end_game(False, "TRAP TRIGGERED: SECURITY ALERT!")

    def end_game(self, success, msg_fail="BREACH FAILED"):
        super().end_game(success, msg_win="FIREWALL BYPASSED", msg_fail=msg_fail)


class DataStream(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="DATA STREAM", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        tk.Label(self.parent, text="STOP THE LINE INSIDE THE GREEN ZONE", fg="yellow", bg="#050505").pack()
        self.canvas = tk.Canvas(self.parent, width=400, height=50, bg="#050505")
        self.canvas.pack(pady=20)
        self.zone = self.canvas.create_rectangle(150, 0, 250, 50, fill="#006600")
        self.line = self.canvas.create_line(0, 0, 0, 50, fill="cyan", width=3)
        self.pos, self.dir = 0, 5 + state.security_level
        self.animate()
        tk.Button(self.parent, text="STOP", command=self.stop).pack()

    def animate(self):
        if self.game_running:
            self.pos += self.dir
            if self.pos >= 400 or self.pos <= 0:
                self.dir *= -1
            self.canvas.coords(self.line, self.pos, 0, self.pos, 50)
            self.parent.after(20, self.animate)

    def stop(self):
        if not self.game_running:
            return
        self.game_running = False
        self.end_game(150 <= self.pos <= 250)


class PortScanner(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="PORT SCANNER", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.target = random.randint(0, 15)
        self.tries = 5
        self.hint = tk.Label(self.parent, text=f"FIND THE OPEN PORT | ATTEMPTS LEFT: {self.tries}", fg="cyan", bg="#050505", font=("Courier", 12))
        self.hint.pack(pady=5)
        self.frame = tk.Frame(self.parent, bg="#050505")
        self.frame.pack()
        self.buttons = {}
        for i in range(16):
            b = tk.Button(self.frame, text=f"Port {8000 + i}", bg="#111", fg="#00FF00", command=lambda x=i: self.check(x))
            b.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.buttons[i] = b

    def check(self, x):
        if x == self.target:
            self.end_game(True)
            return
        self.tries -= 1
        self.buttons[x].config(state=tk.DISABLED)
        if self.tries <= 0:
            self.end_game(False)
            return
        direction = "HIGHER" if self.target > x else "LOWER"
        self.hint.config(text=f"OPEN PORT IS {direction} | ATTEMPTS LEFT: {self.tries}")


class PacketSniffer(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="PACKET SNIFFER", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.target = random.choice(["TCP", "UDP", "HTTP", "FTP", "DNS", "SMTP", "DHCP", "IMAP", "ICMP", "ARP", "BGP"])
        tk.Label(self.parent, text=f"TARGET: {self.target}", fg="yellow", bg="#050505").pack()
        self.lbl = tk.Label(self.parent, text="", fg="cyan", bg="#050505", font=("Courier", 20))
        self.lbl.pack(pady=20)
        tk.Button(self.parent, text="CAPTURE", command=self.cap).pack()
        self.next()

    def next(self):
        if self.game_running:
            self.lbl.config(text=random.choice(["TCP", "UDP", "HTTP", "FTP", "DNS", "SMTP", "DHCP", "IMAP", "ICMP", "ARP", "BGP"]))
            self.parent.after(max(400, 800 - state.security_level * 50), self.next)

    def cap(self):
        if not self.game_running:
            return
        self.end_game(self.lbl.cget("text") == self.target)


class PingMatch(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="PING MATCH", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.n = min(4 + state.security_level // 2, 8)
        self.order = list(range(self.n))
        random.shuffle(self.order)
        self.progress = 0
        tk.Label(self.parent, text="PING THE NODES IN THIS ORDER:", fg="cyan", bg="#050505").pack()
        tk.Label(self.parent, text=" > ".join(str(i) for i in self.order), fg="yellow", bg="#050505", font=("Courier", 18)).pack(pady=10)
        self.frame = tk.Frame(self.parent, bg="#050505")
        self.frame.pack()
        for i in range(self.n):
            tk.Button(self.frame, text=f"Node {i}", bg="#111", fg="#00FF00", command=lambda x=i: self.click(x)).pack(side=tk.LEFT, padx=6)

    def click(self, x):
        if x == self.order[self.progress]:
            self.progress += 1
            if self.progress == self.n:
                self.end_game(True)
        else:
            self.end_game(False)


# ------------------------------------------------------------------ SYSTEMS

class BinaryPulse(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="BINARY PULSE", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.num = random.randint(1, 100)
        tk.Label(self.parent, text=bin(self.num)[2:], fg="yellow", bg="#050505", font=("Courier", 24)).pack(pady=20)
        tk.Label(self.parent, text="IS THIS BINARY NUMBER EVEN OR ODD?", fg="cyan", bg="#050505").pack()
        tk.Button(self.parent, text="EVEN", command=lambda: self.check(True)).pack()
        tk.Button(self.parent, text="ODD", command=lambda: self.check(False)).pack()

    def check(self, even):
        self.end_game((self.num % 2 == 0) == even)


class LogicGate(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        self.gate = random.choice(["AND", "OR", "XOR"])
        self.a, self.b = random.randint(0, 1), random.randint(0, 1)
        tk.Label(self.parent, text=f"GATE: {self.gate}\nIN: {self.a}, {self.b}", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        tk.Button(self.parent, text="0", command=lambda: self.check(0)).pack()
        tk.Button(self.parent, text="1", command=lambda: self.check(1)).pack()

    def check(self, val):
        res = (self.a & self.b) if self.gate == "AND" else (self.a | self.b) if self.gate == "OR" else (self.a ^ self.b)
        self.end_game(val == res)


class SQLInjector(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="SQL INJECTOR", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        tk.Label(self.parent, text="SELECT * FROM users WHERE id = '1' [___]", fg="cyan", bg="#050505").pack(pady=10)
        tk.Label(self.parent, text="HINT: make the condition always true", fg="yellow", bg="#050505").pack()
        self.ent = tk.Entry(self.parent)
        self.ent.pack(pady=5)
        tk.Button(self.parent, text="EXECUTE", command=self.check).pack()

    def check(self):
        value = self.ent.get().strip().upper().replace(" ", "")
        self.end_game(value in ("OR1=1", "OR'1'='1'", "OR'1'='1"))


class Keylogger(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="KEYLOGGER: MEMORIZE THE PASSWORD", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.phrase = random.choice(["AdminPass123", "RootAccess!", "CyberSec2026", "SQLInjection1"])
        self.lbl = tk.Label(self.parent, text=self.phrase, fg="yellow", bg="#050505", font=("Courier", 18))
        self.lbl.pack(pady=20)
        self.ent = tk.Entry(self.parent)
        self.ent.pack()
        tk.Button(self.parent, text="SUBMIT", command=lambda: self.end_game(self.ent.get() == self.phrase)).pack(pady=5)
        self.parent.after(2000, self.hide_phrase)

    def hide_phrase(self):
        if self.game_running:
            self.lbl.config(text="********")


class KernelPanic(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="KERNEL PANIC: CLICK THE ERRORS", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.count = 0
        self.misses = 0
        self.info = tk.Label(self.parent, text="FIXED: 0/5   MISSED: 0/3", fg="cyan", bg="#050505", font=("Courier", 12))
        self.info.pack()
        self.spawn()

    def update_info(self):
        self.info.config(text=f"FIXED: {self.count}/5   MISSED: {self.misses}/3")

    def spawn(self):
        if not self.game_running:
            return
        btn = tk.Button(self.parent, text="ERROR", bg="red", fg="white")
        btn.config(command=lambda b=btn: self.fix(b))
        btn.place(x=random.randint(0, 600), y=random.randint(100, 400))
        self.parent.after(1000, lambda b=btn: self.expire(b))
        self.parent.after(1200, self.spawn)

    def fix(self, btn):
        if not self.game_running:
            return
        btn.destroy()
        self.count += 1
        self.update_info()
        if self.count >= 5:
            self.end_game(True)

    def expire(self, btn):
        if not self.game_running:
            return
        if btn.winfo_exists():
            btn.destroy()
            self.misses += 1
            self.update_info()
            if self.misses >= 3:
                self.end_game(False)


class BIOSMath(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        self.a, self.b = random.randint(10, 50), random.randint(10, 50)
        tk.Label(self.parent, text=f"QUICK MATH: {self.a} + {self.b} = ?", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=30)
        self.ent = tk.Entry(self.parent)
        self.ent.pack()
        tk.Button(self.parent, text="ENTER", command=lambda: self.end_game(self.ent.get().strip() == str(self.a + self.b))).pack(pady=5)


# ----------------------------------------------------------------- HARDWARE

class PatternMemory(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="PATTERN MEMORY", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        tk.Label(self.parent, text="WATCH THE PATTERN, THEN REPEAT IT", fg="yellow", bg="#050505").pack()
        self.pattern = [random.randint(0, 8) for _ in range(3 + (state.security_level // 2))]
        self.progress = 0
        self.input_ready = False
        self.frame = tk.Frame(self.parent, bg="#050505")
        self.frame.pack(pady=10)
        self.btns = []
        for i in range(9):
            b = tk.Button(self.frame, text="", width=5, height=2, bg="#111", command=lambda x=i: self.click(x))
            b.grid(row=i // 3, column=i % 3)
            self.btns.append(b)
        self.show()

    def show(self):
        for i, p in enumerate(self.pattern):
            self.parent.after(500 + i * 600, lambda x=p: self.flash(x))
        # input opens only after the whole pattern has been shown
        self.parent.after(500 + len(self.pattern) * 600, self.enable_input)

    def enable_input(self):
        if self.game_running:
            self.input_ready = True

    def flash(self, p):
        if not self.game_running:
            return
        self.btns[p].config(bg="cyan")
        self.parent.after(300, lambda: self.btns[p].config(bg="#111") if self.game_running else None)

    def click(self, x):
        if not self.input_ready:
            return
        if x == self.pattern[self.progress]:
            self.progress += 1
            if self.progress == len(self.pattern):
                self.end_game(True)
        else:
            self.end_game(False)


class FingerprintScan(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="BIOMETRIC TRACE", fg="#00FF00", bg="#050505", font=("Courier", 18, "bold")).pack(pady=(20, 5))
        tk.Label(self.parent, text="MEMORIZE THE NUMBERS, THEN CLICK THE DOTS IN ORDER", fg="yellow", bg="#050505", font=("Courier", 11)).pack()

        # Complexity increases with level
        self.target = self.make_points(min(4 + state.security_level, 12))
        self.points_count = len(self.target)
        self.progress = 0
        self.dots = []
        self.labels = []

        self.canvas = tk.Canvas(self.parent, width=300, height=300, bg="#050505", highlightthickness=1, highlightbackground="#00FF00")
        self.canvas.pack(pady=10)

        for i, (x, y) in enumerate(self.target):
            dot = self.canvas.create_oval(x - 14, y - 14, x + 14, y + 14, fill="#333", outline="#00FF00")
            num = self.canvas.create_text(x, y, text=str(i + 1), fill="white", font=("Courier", 10, "bold"))
            for item in (dot, num):
                self.canvas.tag_bind(item, "<Button-1>", lambda e, i=i: self.click(i))
            self.dots.append(dot)
            self.labels.append(num)

        self.parent.after(2500, self.hide_numbers)

    def make_points(self, n):
        """Random points that never overlap (at least 40 px apart)."""
        pts = []
        attempts = 0
        while len(pts) < n and attempts < 2000:
            attempts += 1
            p = (random.randint(30, 270), random.randint(30, 270))
            if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 >= 40 ** 2 for q in pts):
                pts.append(p)
        return pts

    def hide_numbers(self):
        if not self.game_running:
            return
        for t in self.labels:
            self.canvas.itemconfig(t, state=tk.HIDDEN)

    def click(self, i):
        if not self.game_running:
            return
        if i == self.progress:
            self.canvas.itemconfig(self.dots[i], fill="#00AA00")
            self.progress += 1
            if self.progress == self.points_count:
                self.end_game(True)
        else:
            self.canvas.itemconfig(self.dots[i], fill="#990000")
            self.end_game(False, msg_fail="BIOMETRIC MISMATCH")


class SignalRecord(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="SIGNAL RECORD", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.target = random.randint(10, 90)
        tk.Label(self.parent, text=f"TARGET: {self.target}Hz", fg="yellow", bg="#050505").pack()
        self.lbl = tk.Label(self.parent, text="CURRENT: 0Hz", fg="cyan", bg="#050505")
        self.lbl.pack()
        self.s = tk.Scale(self.parent, from_=0, to=100, orient=tk.HORIZONTAL, bg="#050505", fg="white",
                          command=lambda v: self.lbl.config(text=f"CURRENT: {v}Hz"))
        self.s.pack(pady=20)
        tk.Button(self.parent, text="LOCK SIGNAL", command=lambda: self.end_game(abs(self.s.get() - self.target) < 3)).pack()


class RAMScraper(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="RAM SCRAPER", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        tk.Label(self.parent, text="FIND THE HIDDEN WORD IN THE MEMORY DUMP AND TYPE IT", fg="yellow", bg="#050505").pack()
        self.key = random.choice(["SECRET", "ACCESS", "TOKEN", "ADMIN", "KERNEL"])
        noise = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(100))
        pos = random.randint(0, len(noise))
        self.grid = noise[:pos] + self.key + noise[pos:]
        self.txt = tk.Text(self.parent, width=40, height=10, bg="#050505", fg="cyan", font=("Courier", 10))
        self.txt.insert(tk.END, self.grid)
        self.txt.pack(pady=5)
        self.ent = tk.Entry(self.parent)
        self.ent.pack()
        tk.Button(self.parent, text="EXTRACT", command=lambda: self.end_game(self.ent.get().strip().upper() == self.key)).pack(pady=5)


class BackdoorPath(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="BACKDOOR PATH", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        tk.Label(self.parent, text="MEMORIZE THE PATH FROM TOP-LEFT TO BOTTOM-RIGHT", fg="yellow", bg="#050505").pack()
        self.path = self.make_path()
        self.pos = 0
        self.input_ready = False
        self.frame = tk.Frame(self.parent, bg="#050505")
        self.frame.pack(pady=10)
        self.btns = []
        for i in range(16):
            b = tk.Button(self.frame, text="?", width=5, bg="#111", fg="#00FF00", command=lambda x=i: self.move(x))
            b.grid(row=i // 4, column=i % 4)
            self.btns.append(b)
        for i in self.path:
            self.btns[i].config(bg="cyan")
        self.parent.after(3000, self.hide_path)

    def make_path(self):
        """Random walk (right/down only) from cell 0 to cell 15."""
        r = c = 0
        path = [0]
        while (r, c) != (3, 3):
            if r == 3:
                c += 1
            elif c == 3:
                r += 1
            elif random.random() < 0.5:
                c += 1
            else:
                r += 1
            path.append(r * 4 + c)
        return path

    def hide_path(self):
        if not self.game_running:
            return
        for b in self.btns:
            b.config(bg="#111")
        self.input_ready = True

    def move(self, x):
        if not self.input_ready:
            return
        if x == self.path[self.pos]:
            self.btns[x].config(bg="#006600")
            self.pos += 1
            if self.pos == len(self.path):
                self.end_game(True)
        else:
            self.btns[x].config(bg="#660000")
            self.end_game(False)


class SymbolMirror(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="SYMBOL MIRROR", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.syms = ["@", "#", "$", "%", "&", "*"]
        self.target = random.choice(self.syms)
        tk.Label(self.parent, text=f"TARGET: {self.target}", fg="yellow", bg="#050505", font=("Courier", 20)).pack(pady=10)
        self.frame = tk.Frame(self.parent, bg="#050505")
        self.frame.pack()
        for s in self.syms:
            tk.Button(self.frame, text=s, width=5, bg="#111", fg="#00FF00", command=lambda x=s: self.end_game(x == self.target)).pack(side=tk.LEFT, padx=5)


# --------------------------------------------------------------------- DATA

class CipherCracker(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="CIPHER CRACKER", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.target = random.choice(["CODE", "HACK", "ROOT", "BYTE", "PING", "LOGS"])
        self.curr = ["A"] * 4
        tk.Label(self.parent, text=f"TARGET: {self.target}", fg="yellow", bg="#050505", font=("Courier", 16)).pack()
        self.lbl = tk.Label(self.parent, text="".join(self.curr), fg="cyan", bg="#050505", font=("Courier", 20))
        self.lbl.pack(pady=20)
        self.frame = tk.Frame(self.parent, bg="#050505")
        self.frame.pack()
        for i in range(4):
            tk.Button(self.frame, text="UP", command=lambda x=i: self.cycle(x)).pack(side=tk.LEFT, padx=5)

    def cycle(self, i):
        self.curr[i] = chr((ord(self.curr[i]) - 65 + 1) % 26 + 65)
        self.lbl.config(text="".join(self.curr))
        if "".join(self.curr) == self.target:
            self.end_game(True)


class AnagramCrack(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        self.word_list = ["FIREWALL", "DATABASE", "PROTOCOL", "ENCRYPTION", "BACKDOOR", "MALWARE", "PHISHING", "KERNEL", "NETWORK", "PASSWORD",
                          "CIPHER", "BITCOIN", "SATELLITE", "MAINBOARD", "FIRMWARE", "SPOOFING", "ROOTKIT", "KEYLOGGER", "PROXY", "METADATA"]
        self.word = random.choice(self.word_list)

        scrambled_list = list(self.word)
        while "".join(scrambled_list) == self.word:
            random.shuffle(scrambled_list)
        self.scrambled = "".join(scrambled_list)

        tk.Label(self.parent, text="ANAGRAM CRACK: UNSCRAMBLE THE KEY", fg="#00FF00", bg="#050505", font=("Courier", 18, "bold")).pack(pady=20)
        tk.Label(self.parent, text=self.scrambled, fg="yellow", bg="#050505", font=("Courier", 30, "bold")).pack(pady=20)
        self.ent = tk.Entry(self.parent, font=("Courier", 14), bg="#111", fg="#00FF00", insertbackground="white", justify="center")
        self.ent.pack(pady=10)
        self.ent.focus_set()
        tk.Button(self.parent, text="SUBMIT", bg="#111", fg="#00FF00", font=("Courier", 12), command=self.check).pack(pady=10)

    def check(self):
        if self.ent.get().strip().upper() == self.word:
            self.end_game(True)
        else:
            messagebox.showerror("Error", "INVALID KEY")


class HashMatcher(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        self.h = "".join(random.choice("0123456789abcdef") for _ in range(8))
        tk.Label(self.parent, text="HASH MATCHER", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        tk.Label(self.parent, text=f"TARGET: {self.h}", fg="yellow", bg="#050505", font=("Courier", 18)).pack(pady=10)
        self.ent = tk.Entry(self.parent)
        self.ent.pack()
        tk.Button(self.parent, text="MATCH", command=lambda: self.end_game(self.ent.get().strip().lower() == self.h)).pack(pady=5)


class MetadataWipe(BaseGame):
    def __init__(self, parent, back_callback, hub):
        super().__init__(parent, back_callback, hub)
        tk.Label(self.parent, text="METADATA WIPE", fg="#00FF00", bg="#050505", font=("Courier", 18)).pack(pady=20)
        self.b1 = tk.BooleanVar()
        self.b2 = tk.BooleanVar()
        tk.Checkbutton(self.parent, text="Wipe EXIF", variable=self.b1, bg="#050505", fg="white", selectcolor="black").pack()
        tk.Checkbutton(self.parent, text="Wipe GPS", variable=self.b2, bg="#050505", fg="white", selectcolor="black").pack()
        tk.Button(self.parent, text="CONFIRM", command=lambda: self.end_game(self.b1.get() and self.b2.get())).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    try:
        database.init_db()
        database.load_state(state)
    except Exception as e:
        messagebox.showwarning("Database", f"Progress saving is off:\n{e}")
    app = HackingHub(root)
    root.mainloop()