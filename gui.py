# gui.py
import tkinter as tk
from tkinter import ttk, messagebox # simpledialog
from database import create_table, add_series, list_series, search_series_filtered_python, update_rating, delete_series

class EpisodeVaultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EpisodeVault")
        self.geometry("700x400")
        create_table()

        # Кнопки
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Показать все", command=self.show_all).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Добавить сериал", command=self.add_series_window).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Поиск", command=self.search_window).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Изменить рейтинг", command=self.update_rating_window).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Удалить сериал", command=self.delete_series_window).grid(row=0, column=4, padx=5)

        # Таблица
        columns = ("id", "title", "genre", "year", "seasons", "rating")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, minwidth=30, width=100)
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.show_all()

    def show_all(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for series in list_series():
            self.tree.insert("", tk.END, values=series)

    def add_series_window(self):
        def save():
            try:
                title = entry_title.get().strip()
                genre = entry_genre.get().strip()
                year = int(entry_year.get())
                seasons = int(entry_seasons.get())
                rating = float(entry_rating.get())

                if not title:
                    messagebox.showwarning("Ошибка", "Название обязательно")
                    return

                add_series(title, genre, year, seasons, rating)
                messagebox.showinfo("Успех", "Сериал добавлен")
                add_win.destroy()
                self.show_all()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте корректность введённых данных")

        add_win = tk.Toplevel(self)
        add_win.title("Добавить сериал")

        tk.Label(add_win, text="Название:").grid(row=0, column=0, sticky=tk.W, pady=2)
        entry_title = tk.Entry(add_win, width=30)
        entry_title.grid(row=0, column=1, pady=2)

        tk.Label(add_win, text="Жанр:").grid(row=1, column=0, sticky=tk.W, pady=2)
        entry_genre = tk.Entry(add_win, width=30)
        entry_genre.grid(row=1, column=1, pady=2)

        tk.Label(add_win, text="Год выхода:").grid(row=2, column=0, sticky=tk.W, pady=2)
        entry_year = tk.Entry(add_win, width=30)
        entry_year.grid(row=2, column=1, pady=2)

        tk.Label(add_win, text="Сезонов:").grid(row=3, column=0, sticky=tk.W, pady=2)
        entry_seasons = tk.Entry(add_win, width=30)
        entry_seasons.grid(row=3, column=1, pady=2)

        tk.Label(add_win, text="Рейтинг (0-10):").grid(row=4, column=0, sticky=tk.W, pady=2)
        entry_rating = tk.Entry(add_win, width=30)
        entry_rating.grid(row=4, column=1, pady=2)

        tk.Button(add_win, text="Сохранить", command=save).grid(row=5, column=0, columnspan=2, pady=10)

    def search_window(self):
        def do_search():
            keyword = entry_keyword.get().strip() or None
            genre = entry_genre.get().strip() or None

            try:
                year_min = int(entry_year_min.get()) if entry_year_min.get().strip() else None
            except ValueError:
                messagebox.showerror("Ошибка", "Минимальный год должен быть числом")
                return

            try:
                year_max = int(entry_year_max.get()) if entry_year_max.get().strip() else None
            except ValueError:
                messagebox.showerror("Ошибка", "Максимальный год должен быть числом")
                return

            try:
                rating_min = float(entry_rating_min.get()) if entry_rating_min.get().strip() else None
            except ValueError:
                messagebox.showerror("Ошибка", "Минимальный рейтинг должен быть числом")
                return

            results = search_series_filtered_python(
                keyword=keyword,
                genre=genre,
                year_min=year_min,
                year_max=year_max,
                rating_min=rating_min
            )

            for row in self.tree.get_children():
                self.tree.delete(row)
            for series in results:
                self.tree.insert("", tk.END, values=series)
            search_win.destroy()

        search_win = tk.Toplevel(self)
        search_win.title("Поиск с фильтрами")

        tk.Label(search_win, text="Ключевое слово (название/жанр):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        entry_keyword = tk.Entry(search_win, width=30)
        entry_keyword.grid(row=0, column=1, pady=2)

        tk.Label(search_win, text="Жанр:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        entry_genre = tk.Entry(search_win, width=30)
        entry_genre.grid(row=1, column=1, pady=2)

        tk.Label(search_win, text="Минимальный год:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        entry_year_min = tk.Entry(search_win, width=30)
        entry_year_min.grid(row=2, column=1, pady=2)

        tk.Label(search_win, text="Максимальный год:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        entry_year_max = tk.Entry(search_win, width=30)
        entry_year_max.grid(row=3, column=1, pady=2)

        tk.Label(search_win, text="Минимальный рейтинг:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        entry_rating_min = tk.Entry(search_win, width=30)
        entry_rating_min.grid(row=4, column=1, pady=2)

        tk.Button(search_win, text="Искать", command=do_search).grid(row=5, column=0, columnspan=2, pady=10)

    def update_rating_window(self):
        def do_update():
            try:
                series_id = int(entry_id.get())
                new_rating = float(entry_rating.get())
                update_rating(series_id, new_rating)
                messagebox.showinfo("Успех", "Рейтинг обновлён")
                update_win.destroy()
                self.show_all()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте корректность введённых данных")

        update_win = tk.Toplevel(self)
        update_win.title("Изменить рейтинг")

        tk.Label(update_win, text="ID сериала:").grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_id = tk.Entry(update_win, width=30)
        entry_id.grid(row=0, column=1, pady=5)

        tk.Label(update_win, text="Новый рейтинг (0-10):").grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_rating = tk.Entry(update_win, width=30)
        entry_rating.grid(row=1, column=1, pady=5)

        tk.Button(update_win, text="Обновить", command=do_update).grid(row=2, column=0, columnspan=2, pady=10)

    def delete_series_window(self):
        def do_delete():
            try:
                series_id = int(entry_id.get())
                delete_series(series_id)
                messagebox.showinfo("Успех", "Сериал удалён")
                delete_win.destroy()
                self.show_all()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректный ID")

        delete_win = tk.Toplevel(self)
        delete_win.title("Удалить сериал")

        tk.Label(delete_win, text="ID сериала:").pack(pady=5)
        entry_id = tk.Entry(delete_win, width=30)
        entry_id.pack(pady=5)

        tk.Button(delete_win, text="Удалить", command=do_delete).pack(pady=10)

if __name__ == '__main__':
    app = EpisodeVaultApp()
    app.mainloop()
