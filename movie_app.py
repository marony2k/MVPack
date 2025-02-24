import customtkinter as ctk
import json
import os
import math
import tkinter.messagebox as tk_messagebox

ctk.set_appearance_mode("System")  # Системная тема по умолчанию
ctk.set_default_color_theme("blue")  # Синяя цветовая схема

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Фильмотека")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Загрузка фильмов из файла при старте
        self.file_name = "movies.json"
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as file:
                self.movies = json.load(file)
        else:
            self.movies = []

        # Создание основного интерфейса
        self.create_main_window()

        # Переменная для хранения ссылки на окно просмотра фильмов
        self.view_window = None
        self.filtered_movies = self.movies  # Фильтрованный список фильмов
        self.movie_frames = []  # Храним ссылки на созданные фреймы для оптимизации

    def create_main_window(self):
        # Фрейм для ввода данных
        input_frame = ctk.CTkFrame(self.root, fg_color="#242424" if ctk.get_appearance_mode() == "Dark" else "#f9f9fa", corner_radius=10)
        input_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Название фильма
        ctk.CTkLabel(input_frame, text="Название фильма:", font=("SF Pro Display", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.title_entry = ctk.CTkEntry(input_frame, width=300, font=("SF Pro Display", 14))
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Рейтинг
        ctk.CTkLabel(input_frame, text="Рейтинг (1-10):", font=("SF Pro Display", 14)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.rating_entry = ctk.CTkEntry(input_frame, width=300, font=("SF Pro Display", 14))
        self.rating_entry.grid(row=1, column=1, padx=10, pady=5)

        # Продолжительность
        ctk.CTkLabel(input_frame, text="Продолжительность (минуты):", font=("SF Pro Display", 14)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.duration_entry = ctk.CTkEntry(input_frame, width=300, font=("SF Pro Display", 14))
        self.duration_entry.grid(row=2, column=1, padx=10, pady=5)

        # Жанр
        ctk.CTkLabel(input_frame, text="Жанр:", font=("SF Pro Display", 14)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.genre_entry = ctk.CTkEntry(input_frame, width=300, font=("SF Pro Display", 14))
        self.genre_entry.grid(row=3, column=1, padx=10, pady=5)

        # Комментарии
        ctk.CTkLabel(input_frame, text="Комментарии:", font=("SF Pro Display", 14)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.comments_entry = ctk.CTkTextbox(input_frame, height=80, width=300, font=("SF Pro Display", 14))
        self.comments_entry.grid(row=4, column=1, padx=10, pady=5)

        # Кнопка "Добавить фильм" той же ширины, что и поля ввода
        add_button = ctk.CTkButton(
            input_frame, text="Добавить фильм",
            command=self.add_movie, font=("SF Pro Display", 16), corner_radius=10,
            fg_color="#007aff", hover_color="#005caa", width=300, height=40
        )
        add_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Кнопка "Просмотреть фильмы" внизу справа
        view_button = ctk.CTkButton(
            self.root, text="Просмотреть фильмы",
            command=self.view_movies, font=("SF Pro Display", 14), corner_radius=10,
            fg_color="#007aff", hover_color="#005caa"
        )
        view_button.pack(side="right", anchor="se", padx=20, pady=20)

        # Меню настроек
        settings_button = ctk.CTkButton(
            self.root, text="⚙️ Настройки",
            command=self.open_settings, font=("SF Pro Display", 14), corner_radius=10,
            fg_color="#007aff", hover_color="#005caa", width=120, height=40
        )
        settings_button.pack(side="left", anchor="nw", padx=20, pady=20)

    def open_settings(self):
        # Создание окна настроек
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("300x250")
        settings_window.resizable(False, False)

        # Смена темы
        theme_label = ctk.CTkLabel(settings_window, text="Тема:", font=("SF Pro Display", 14))
        theme_label.pack(pady=10)

        theme_switch = ctk.CTkSwitch(
            settings_window, text="Тёмная тема", command=self.toggle_theme,
            font=("SF Pro Display", 14), switch_height=20, switch_width=40
        )
        theme_switch.pack(pady=5)
        theme_switch.select() if ctk.get_appearance_mode() == "Dark" else theme_switch.deselect()

        # Добавляем надпись "made.by qwen/marony"
        made_by_label = ctk.CTkLabel(
            settings_window, text="made.by qwen/marony",
            font=("SF Pro Display", 12), text_color="#a9a9a9"
        )
        made_by_label.pack(side="bottom", pady=10)

    def toggle_theme(self):
        # Переключение между темами
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)

        # Обновляем цвета виджетов
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color="#242424" if new_mode == "Dark" else "#f9f9fa")

    def add_movie(self):
        title = self.title_entry.get().strip()
        rating = self.rating_entry.get().strip()
        duration = self.duration_entry.get().strip()
        genre = self.genre_entry.get().strip()
        comments = self.comments_entry.get("1.0", "end").strip()

        if not all([title, rating, duration, genre]):
            tk_messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        try:
            rating = int(rating)
            duration = int(duration)
            if rating < 1 or rating > 10:
                raise ValueError("Рейтинг должен быть от 1 до 10.")
        except ValueError as e:
            tk_messagebox.showwarning("Ошибка", f"Неверный формат данных: {e}")
            return

        movie = {
            "title": title,
            "rating": rating,
            "duration": duration,
            "genre": genre,
            "comments": comments
        }
        self.movies.append(movie)
        self.save_movies()
        self.clear_entries()

        # Анимация уведомления
        self.animate_message("Успех", "Фильм успешно добавлен!")

    def clear_entries(self):
        self.title_entry.delete(0, "end")
        self.rating_entry.delete(0, "end")
        self.duration_entry.delete(0, "end")
        self.genre_entry.delete(0, "end")
        self.comments_entry.delete("1.0", "end")

    def save_movies(self):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(self.movies, file, ensure_ascii=False, indent=4)

    def view_movies(self):
        if not self.movies:
            tk_messagebox.showinfo("Информация", "Список фильмов пуст.")
            return

        if self.view_window and self.view_window.winfo_exists():
            self.update_view_window()
            return

        # Создание нового окна для просмотра фильмов
        self.view_window = ctk.CTkToplevel(self.root)
        self.view_window.title("Список фильмов")
        self.view_window.geometry("800x600")
        self.view_window.resizable(True, True)

        # Поиск по названию
        search_frame = ctk.CTkFrame(self.view_window, fg_color="#242424" if ctk.get_appearance_mode() == "Dark" else "#f9f9fa", corner_radius=10)
        search_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(search_frame, text="Поиск по названию:", font=("SF Pro Display", 14)).pack(side="left", padx=10)
        self.search_entry = ctk.CTkEntry(search_frame, width=300, font=("SF Pro Display", 14))
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", self.filter_movies)

        # Общее время просмотра
        total_duration_minutes = sum(movie["duration"] for movie in self.movies)
        total_duration_hours = math.ceil(total_duration_minutes / 60)

        total_time_label = ctk.CTkLabel(
            self.view_window,
            text=f"В сумме просмотрено часов: {total_duration_hours}",
            font=("SF Pro Display", 16), anchor="center"
        )
        total_time_label.pack(pady=10)

        # Таблица фильмов
        self.tree = ctk.CTkScrollableFrame(self.view_window, fg_color="#242424" if ctk.get_appearance_mode() == "Dark" else "#f9f9fa", corner_radius=10)
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Создаем фильмы только один раз
        self.display_movies(self.movies)

        # Кнопки сортировки
        sort_frame = ctk.CTkFrame(self.view_window, fg_color="#242424" if ctk.get_appearance_mode() == "Dark" else "#f9f9fa", corner_radius=10)
        sort_frame.pack(pady=10, padx=10, fill="x")

        rating_button = ctk.CTkButton(
            sort_frame, text="По рейтингу",
            command=lambda: self.sort_and_update("rating"),
            font=("SF Pro Display", 14), corner_radius=10,
            fg_color="#007aff", hover_color="#005caa"
        )
        rating_button.pack(side="left", padx=5)

        duration_button = ctk.CTkButton(
            sort_frame, text="По продолжительности",
            command=lambda: self.sort_and_update("duration"),
            font=("SF Pro Display", 14), corner_radius=10,
            fg_color="#007aff", hover_color="#005caa"
        )
        duration_button.pack(side="left", padx=5)

        genre_button = ctk.CTkButton(
            sort_frame, text="По жанру",
            command=lambda: self.sort_and_update("genre"),
            font=("SF Pro Display", 14), corner_radius=10,
            fg_color="#007aff", hover_color="#005caa"
        )
        genre_button.pack(side="left", padx=5)

    def display_movies(self, movies_list):
        # Очистка текущих фреймов
        for frame in self.movie_frames:
            frame.destroy()
        self.movie_frames = []

        # Отображение фильмов
        for idx, movie in enumerate(movies_list):
            movie_frame = ctk.CTkFrame(self.tree, fg_color="#333333" if ctk.get_appearance_mode() == "Dark" else "#e5e5ea", corner_radius=10)
            movie_frame.pack(pady=5, padx=10, fill="x", expand=True)
            self.movie_frames.append(movie_frame)

            ctk.CTkLabel(movie_frame, text=f"{idx + 1}. {movie['title']}", font=("SF Pro Display", 14), anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(movie_frame, text=f"Рейтинг: {movie['rating']}", font=("SF Pro Display", 12), anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(movie_frame, text=f"Продолжительность: {movie['duration']} мин.", font=("SF Pro Display", 12), anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(movie_frame, text=f"Жанр: {movie['genre']}", font=("SF Pro Display", 12), anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            ctk.CTkLabel(movie_frame, text=f"Комментарии: {movie['comments']}", font=("SF Pro Display", 12), anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")

            # Кнопки редактирования и удаления
            edit_button = ctk.CTkButton(
                movie_frame, text="Редактировать",
                command=lambda m=movie, i=idx: self.edit_movie(m, i),
                font=("SF Pro Display", 12), corner_radius=10, width=100,
                fg_color="#007aff", hover_color="#005caa"
            )
            edit_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")

            delete_button = ctk.CTkButton(
                movie_frame, text="Удалить",
                command=lambda i=idx: self.delete_movie(i),
                font=("SF Pro Display", 12), corner_radius=10, width=100,
                fg_color="#ff3b30", hover_color="#dd1c11"
            )
            delete_button.grid(row=5, column=1, padx=10, pady=5, sticky="e")

    def filter_movies(self, event=None):
        query = self.search_entry.get().strip().lower()
        if query:
            self.filtered_movies = [movie for movie in self.movies if query in movie["title"].lower()]
        else:
            self.filtered_movies = self.movies
        self.display_movies(self.filtered_movies)

    def edit_movie(self, movie, index):
        new_title = ctk.CTkInputDialog(text=f"Текущее название: {movie['title']}\nВведите новое название:", title="Редактирование").get_input()
        if not new_title:
            return

        new_rating = ctk.CTkInputDialog(text=f"Текущий рейтинг: {movie['rating']}\nВведите новый рейтинг (1-10):", title="Редактирование").get_input()
        if not new_rating.isdigit() or not (1 <= int(new_rating) <= 10):
            tk_messagebox.showwarning("Ошибка", "Неверный рейтинг.")
            return

        new_duration = ctk.CTkInputDialog(text=f"Текущая продолжительность: {movie['duration']} мин.\nВведите новую продолжительность (минуты):", title="Редактирование").get_input()
        if not new_duration.isdigit():
            tk_messagebox.showwarning("Ошибка", "Неверная продолжительность.")
            return

        new_genre = ctk.CTkInputDialog(text=f"Текущий жанр: {movie['genre']}\nВведите новый жанр:", title="Редактирование").get_input()
        if not new_genre:
            return

        new_comments = ctk.CTkInputDialog(text=f"Текущие комментарии: {movie['comments']}\nВведите новые комментарии:", title="Редактирование").get_input()

        # Обновление фильма
        self.movies[index] = {
            "title": new_title,
            "rating": int(new_rating),
            "duration": int(new_duration),
            "genre": new_genre,
            "comments": new_comments
        }

        self.save_movies()
        self.update_view_window()

    def delete_movie(self, index):
        del self.movies[index]
        self.save_movies()
        self.update_view_window()

    def sort_and_update(self, criteria):
        if criteria == "rating":
            self.movies.sort(key=lambda x: x["rating"], reverse=True)
        elif criteria == "duration":
            self.movies.sort(key=lambda x: int(x["duration"]))
        elif criteria == "genre":
            self.movies.sort(key=lambda x: x["genre"])
        self.save_movies()
        self.update_view_window()

    def update_view_window(self):
        if self.view_window and self.view_window.winfo_exists():
            self.filter_movies()

    def animate_message(self, title, message):
        # Создаем временное окно с сообщением
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("300x100")
        popup.attributes("-topmost", True)

        label = ctk.CTkLabel(popup, text=message, font=("SF Pro Display", 14))
        label.pack(pady=20)

        # Закрываем окно через 2 секунды
        popup.after(2000, popup.destroy)


if __name__ == "__main__":
    root = ctk.CTk()
    app = MovieApp(root)
    root.mainloop()
