
import tkinter as tk
from tkinter import ttk, messagebox
import time


class TimerStopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Таймер — секундомер")
        self.root.geometry("430x330")
        self.root.minsize(360, 280)
        self.root.resizable(True, True)

        self.timer_running = False
        self.timer_remaining = 0
        self.timer_deadline = 0
        self.timer_job = None

        self.watch_running = False
        self.watch_elapsed = 0
        self.watch_started = 0
        self.watch_job = None

        self.create_menu()
        self.create_interface()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def create_menu(self):
        menu = tk.Menu(self.root)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Выход", command=self.close)
        menu.add_cascade(label="Файл", menu=file_menu)

        mode_menu = tk.Menu(menu, tearoff=0)
        mode_menu.add_command(
            label="Таймер",
            command=lambda: self.tabs.select(self.timer_tab)
        )
        mode_menu.add_command(
            label="Секундомер",
            command=lambda: self.tabs.select(self.watch_tab)
        )
        menu.add_cascade(label="Режим", menu=mode_menu)

        settings_menu = tk.Menu(menu, tearoff=0)
        settings_menu.add_command(
            label="Маленькое окно",
            command=lambda: self.root.geometry("360x280")
        )
        settings_menu.add_command(
            label="Стандартное окно",
            command=lambda: self.root.geometry("430x330")
        )
        settings_menu.add_command(
            label="Большое окно",
            command=lambda: self.root.geometry("600x420")
        )
        menu.add_cascade(label="Настройки", menu=settings_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="О программе", command=self.about)
        menu.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menu)

    def create_interface(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        self.tabs = ttk.Notebook(frame)
        self.tabs.pack(fill="both", expand=True)

        self.timer_tab = ttk.Frame(self.tabs, padding=12)
        self.watch_tab = ttk.Frame(self.tabs, padding=12)

        self.tabs.add(self.timer_tab, text="Таймер")
        self.tabs.add(self.watch_tab, text="Секундомер")

        self.create_timer()
        self.create_watch()

    def create_timer(self):
        ttk.Label(
            self.timer_tab,
            text="Введите время:"
        ).pack(pady=5)

        fields = ttk.Frame(self.timer_tab)
        fields.pack()

        self.minutes = tk.StringVar(value="0")
        self.seconds = tk.StringVar(value="30")

        ttk.Label(fields, text="Минуты").grid(row=0, column=0, padx=5)
        ttk.Entry(
            fields,
            textvariable=self.minutes,
            width=6
        ).grid(row=0, column=1, padx=5)

        ttk.Label(fields, text="Секунды").grid(row=0, column=2, padx=5)
        ttk.Entry(
            fields,
            textvariable=self.seconds,
            width=6
        ).grid(row=0, column=3, padx=5)

        self.timer_label = ttk.Label(
            self.timer_tab,
            text="00:30",
            font=("Arial", 30, "bold")
        )
        self.timer_label.pack(pady=15)

        buttons = ttk.Frame(self.timer_tab)
        buttons.pack()

        ttk.Button(
            buttons, text="Старт", command=self.start_timer
        ).grid(row=0, column=0, padx=4)

        ttk.Button(
            buttons, text="Пауза", command=self.pause_timer
        ).grid(row=0, column=1, padx=4)

        ttk.Button(
            buttons, text="Сброс", command=self.reset_timer
        ).grid(row=0, column=2, padx=4)

    def create_watch(self):
        ttk.Label(
            self.watch_tab,
            text="Измерение времени"
        ).pack(pady=5)

        self.watch_label = ttk.Label(
            self.watch_tab,
            text="00:00:00",
            font=("Arial", 30, "bold")
        )
        self.watch_label.pack(pady=20)

        buttons = ttk.Frame(self.watch_tab)
        buttons.pack()

        ttk.Button(
            buttons, text="Старт", command=self.start_watch
        ).grid(row=0, column=0, padx=3)

        ttk.Button(
            buttons, text="Пауза", command=self.pause_watch
        ).grid(row=0, column=1, padx=3)

        ttk.Button(
            buttons, text="Продолжить", command=self.start_watch
        ).grid(row=0, column=2, padx=3)

        ttk.Button(
            buttons, text="Сброс", command=self.reset_watch
        ).grid(row=0, column=3, padx=3)

    @staticmethod
    def format_time(seconds):
        total = max(0, int(seconds + 0.999))
        minutes, secs = divmod(total, 60)
        return f"{minutes:02d}:{secs:02d}"

    @staticmethod
    def format_watch(seconds):
        total = int(seconds)
        hours, remainder = divmod(total, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def start_timer(self):
        if self.timer_running:
            return

        try:
            if self.timer_remaining <= 0:
                minutes = int(self.minutes.get())
                seconds = int(self.seconds.get())

                if minutes < 0 or seconds < 0 or seconds > 59:
                    raise ValueError

                self.timer_remaining = minutes * 60 + seconds

                if self.timer_remaining <= 0:
                    raise ValueError

            self.timer_deadline = time.monotonic() + self.timer_remaining
            self.timer_running = True
            self.update_timer()

        except ValueError:
            messagebox.showerror(
                "Ошибка",
                "Введите корректное время. Минуты должны быть неотрицательными, секунды — от 0 до 59, общее время — больше нуля."
            )

    def update_timer(self):
        if not self.timer_running:
            return

        self.timer_remaining = max(
            0, self.timer_deadline - time.monotonic()
        )

        self.timer_label.config(
            text=self.format_time(self.timer_remaining)
        )

        if self.timer_remaining <= 0:
            self.timer_running = False
            self.timer_job = None
            messagebox.showinfo("Таймер", "Время вышло!")
            return

        self.timer_job = self.root.after(100, self.update_timer)

    def pause_timer(self):
        if self.timer_running:
            self.timer_remaining = max(
                0, self.timer_deadline - time.monotonic()
            )
            self.timer_running = False
            self.cancel_timer_job()
            self.timer_label.config(
                text=self.format_time(self.timer_remaining)
            )

    def reset_timer(self):
        self.timer_running = False
        self.cancel_timer_job()
        self.timer_remaining = 0

        try:
            minutes = int(self.minutes.get())
            seconds = int(self.seconds.get())

            if minutes < 0 or seconds < 0 or seconds > 59:
                raise ValueError

            self.timer_label.config(
                text=self.format_time(minutes * 60 + seconds)
            )
        except ValueError:
            self.timer_label.config(text="00:00")

    def cancel_timer_job(self):
        if self.timer_job is not None:
            try:
                self.root.after_cancel(self.timer_job)
            except tk.TclError:
                pass
            self.timer_job = None

    def start_watch(self):
        if self.watch_running:
            return

        self.watch_started = time.monotonic() - self.watch_elapsed
        self.watch_running = True
        self.update_watch()

    def update_watch(self):
        if not self.watch_running:
            return

        self.watch_elapsed = time.monotonic() - self.watch_started

        self.watch_label.config(
            text=self.format_watch(self.watch_elapsed)
        )

        self.watch_job = self.root.after(100, self.update_watch)

    def pause_watch(self):
        if self.watch_running:
            self.watch_elapsed = time.monotonic() - self.watch_started
            self.watch_running = False
            self.cancel_watch_job()

            self.watch_label.config(
                text=self.format_watch(self.watch_elapsed)
            )

    def reset_watch(self):
        self.watch_running = False
        self.cancel_watch_job()
        self.watch_elapsed = 0
        self.watch_label.config(text="00:00:00")

    def cancel_watch_job(self):
        if self.watch_job is not None:
            try:
                self.root.after_cancel(self.watch_job)
            except tk.TclError:
                pass
            self.watch_job = None

    def about(self):
        messagebox.showinfo(
            "О программе",
            "Таймер — секундомер\n"
            "Лабораторная работа № 3\n"
            "Разработано на Python с Tkinter"
        )

    def close(self):
        self.timer_running = False
        self.watch_running = False
        self.cancel_timer_job()
        self.cancel_watch_job()
        self.root.destroy()


def main():
    try:
        root = tk.Tk()
        app = TimerStopwatch(root)
        root.mainloop()
    except tk.TclError as error:
        print("Ошибка запуска приложения:", error)
    except Exception as error:
        print("Непредвиденная ошибка:", error)


if __name__ == "__main__":
    main()
