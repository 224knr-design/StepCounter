# =============================================================
# КРАЧКОМЕР (STEP COUNTER) - Python 
# =============================================================

import tkinter as tk        # Главната библиотека за GUI
import math                 # За математически функции
import random               # За симулация на акселерометър
import time                 # За работа с времето

# =============================================================
# КЛАС: КРАЧКОМЕР
# =============================================================
class StepCounter:
    """
    Главният клас на приложението.
    Съдържа целия UI и логиката за броене на крачки.
    """

    def __init__(self, root):
        """
        Конструктор - извиква се при стартиране.
        root = главният прозорец на Tkinter
        """
        self.root = root
        self.root.title("👣 Крачкомер")           
        self.root.geometry("360x640")             
        self.root.configure(bg="#1a1a2e")         
        self.root.resizable(False, False)          

        # --- Променливи за броене ---
        self.step_count = 0             # Брой крачки
        self.last_magnitude = 0.0       # Предишна стойност на ускорението
        self.threshold = 1.2            # Праг за крачка (в g-сила)
        self.step_detected = False      # Флаг - засечена ли е крачка?
        self.is_running = True          # Дали симулацията върви?

        # --- Изграждане на интерфейса ---
        self._build_ui()

        # --- Стартиране на симулацията ---
        self._update()

    # ----------------------------------------------------------
    # ИЗГРАЖДАНЕ НА ИНТЕРФЕЙСА
    # ----------------------------------------------------------
    def _build_ui(self):
        """Създава всички елементи на екрана."""

        # Заглавие
        tk.Label(
            self.root,
            text="👣 Крачкомер",
            font=("Arial", 26, "bold"),
            bg="#1a1a2e",
            fg="#4fc3f7"                 
        ).pack(pady=30)

        # Рамка за голямото число
        frame = tk.Frame(self.root, bg="#16213e", bd=2, relief="solid")
        frame.pack(pady=10, padx=40, fill="both")

        # Голям дисплей за броя крачки
        self.steps_var = tk.StringVar(value="0")  
        tk.Label(
            frame,
            textvariable=self.steps_var,           
            font=("Arial", 90, "bold"),
            bg="#16213e",
            fg="#ffffff"
        ).pack(pady=10)

        # Подпис "крачки"
        tk.Label(
            frame,
            text="крачки",
            font=("Arial", 18),
            bg="#16213e",
            fg="#90a4ae"
        ).pack(pady=(0, 15))

        # Информация за сензора (X, Y, Z стойности)
        self.accel_var = tk.StringVar(value="Сензор: стартиране...")
        tk.Label(
            self.root,
            textvariable=self.accel_var,
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="#66bb6a"                 
        ).pack(pady=15)

        # Статус лента
        self.status_var = tk.StringVar(value="⚡ Режим: Симулация")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 11),
            bg="#1a1a2e",
            fg="#ffa726"                 
        ).pack(pady=5)

        # Разделителна линия
        tk.Frame(
            self.root,
            height=2,
            bg="#4fc3f7"
        ).pack(fill="x", padx=40, pady=20)

        # Бутон НУЛИРАНЕ
        tk.Button(
            self.root,
            text="🔄  НУЛИРАНЕ",
            font=("Arial", 16, "bold"),
            bg="#e53935",               
            fg="white",
            activebackground="#b71c1c", 
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",             
            command=self._reset_steps   
        ).pack(pady=10)



    # ----------------------------------------------------------
    # СИМУЛАЦИЯ НА АКСЕЛЕРОМЕТЪР
    # ----------------------------------------------------------
    def _get_acceleration(self):
        """
        Симулира акселерометър с синусоидна вълна.
        На реален телефон тук би се четял хардуерният сензор.

        При ходене акселерометърът показва повтарящи се пикове.
        Симулираме около 1.5 крачки в секунда.
        """
        t = time.time()

        # Синусоидна вълна симулира ритъма на ходене
        # sin() се движи между -1 и 1, умножаваме по 3.5 за амплитуда
        simulated_z = 9.8 + math.sin(t * 3.0) * 3.5

        # Малък случаен шум в X и Y оси (реалистично)
        simulated_x = random.uniform(-0.5, 0.5)
        simulated_y = random.uniform(-0.3, 0.3)

        return (simulated_x, simulated_y, simulated_z)

    # ----------------------------------------------------------
    # АЛГОРИТЪМ ЗА ЗАСИЧАНЕ НА КРАЧКИ
    # ----------------------------------------------------------
    def _detect_step(self, x, y, z):
        """
        Peak Detection алгоритъм.

        Логика:
        - Изчисляваме общото ускорение (magnitude)
        - Нормализираме спрямо 9.8 (земно ускорение)
        - Крачка = преход от стойност > праг към стойност < праг
        """
        # Обща сила на ускорението: sqrt(x² + y² + z²)
        magnitude = math.sqrt(x**2 + y**2 + z**2)

        # Нормализиране: 1.0 = покой, >1 = движение
        normalized = magnitude / 9.8

        # Засичане на слизане от пик = 1 крачка
        if self.last_magnitude > self.threshold and normalized < self.threshold:
            if not self.step_detected:
                self.step_count += 1        
                self.step_detected = True
        else:
            self.step_detected = False      

        self.last_magnitude = normalized

    # ----------------------------------------------------------
    # ГЛАВЕН ЦИКЪЛ НА ОБНОВЯВАНЕ
    # ----------------------------------------------------------
    def _update(self):
        """
        Обновява показанията на всеки 50ms (20 пъти/сек).
        Tkinter версията на Clock.schedule_interval от Kivy.
        """
        if self.is_running:
            # 1. Вземаме данни от (симулирания) акселерометър
            x, y, z = self._get_acceleration()

            # 2. Проверяваме за крачка
            self._detect_step(x, y, z)

            # 3. Обновяваме UI
            self.steps_var.set(str(self.step_count))
            self.accel_var.set(f"X: {x:.2f}  Y: {y:.2f}  Z: {z:.2f}")

        # 4. Планираме следващото обновяване след 50ms
        self.root.after(50, self._update)

    # ----------------------------------------------------------
    # НУЛИРАНЕ
    # ----------------------------------------------------------
    def _reset_steps(self):
        """Нулира брояча при натискане на бутона."""
        self.step_count = 0
        self.steps_var.set("0")
        self.status_var.set("✅ Нулирано!")
        # След 2 секунди връщаме статуса
        self.root.after(2000, lambda: self.status_var.set("⚡ Режим: Симулация"))


# =============================================================
# СТАРТИРАНЕ НА ПРИЛОЖЕНИЕТО
# =============================================================
if __name__ == "__main__":
    root = tk.Tk()                  
    app = StepCounter(root)         
    root.mainloop()                 
