import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []

        # Поля ввода
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Combobox(root, values=["Бег", "Плавание", "Силовая", "Йога", "Велоспорт"])
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Дата", "Тип", "Длительность"), show="headings")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Длительность", text="Длительность (мин)")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(root, values=["Все"] + ["Бег", "Плавание", "Силовая", "Йога", "Велоспорт"])
        self.filter_type.set("Все")
        self.filter_type.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтры", command=self.apply_filters).grid(row=7, column=0, columnspan=2, pady=10)

        # Кнопки сохранения/загрузки
        tk.Button(root, text="Сохранить в JSON", command=self.save_to_json).grid(row=8, column=0, pady=5)
        tk.Button(root, text="Загрузить из JSON", command=self.load_from_json).grid(row=8, column=1, pady=5)

    def add_training(self):
        date_str = self.date_entry.get()
        training_type = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Проверка корректности ввода
        if not self.validate_input(date_str, duration_str):
            return

        try:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
            duration = int(duration_str)
            self.trainings.append({"date": str(date), "type": training_type, "duration": duration})
            self.update_table()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты или длительности.")

    def validate_input(self, date_str, duration_str):
        # Проверка формата даты
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ДД.ММ.ГГГГ.")
            return False

        # Проверка длительности
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return False
        return True

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.set("")
        self.duration_entry.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for training in self.trainings:
            self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))

    def apply_filters(self):
        filtered = self.trainings
        filter_type = self.filter_type.get()
        filter_date = self.filter_date.get()

        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]
        if filter_date:
            try:
                filter_date_obj = datetime.strptime(filter_date, "%d.%m.%Y").date()
                filtered = [t for t in filtered if datetime.strptime(t["date"], "%Y-%m-%d").date() == filter_date_obj]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты для фильтра.")
                return
        self.update_filtered_table(filtered)

    def update_filtered_table(self, filtered_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for training in filtered_list:
            self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))

    def save_to_json(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Успех", "Данные сохранены в trainings.json.")

    def load_from_json(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
            self.update_table()
            messagebox.showinfo("Успех", "Данные загружены из trainings.json.")
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл trainings.json не найден.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
