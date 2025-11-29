# main.py
from database import create_table, add_series, list_series, search_series, update_rating, delete_series, search_series_filtered

def print_series_list(series_list):
    if not series_list:
        print("Список пуст.")
        return
    print(f"\n{'ID':<4} {'Название':<25} {'Жанр':<15} {'Год':<6} {'Сезонов':<8} {'Рейтинг':<6}")
    print("-" * 70)
    for s in series_list:
        print(f"{s[0]:<4} {s[1]:<25} {s[2]:<15} {s[3]:<6} {s[4]:<8} {s[5]:<6}")

def menu():
    create_table()
    while True:
        print("\n--- EpisodeVault ---")
        print("1. Добавить сериал")
        print("2. Показать все сериалы")
        print("3. Поиск с фильтрами")
        print("4. Изменить рейтинг")
        print("5. Удалить сериал")
        print("0. Выход")
        choice = input("Выбери действие: ").strip()

        if choice == '1':
            title = input("Название: ").strip()
            genre = input("Жанр: ").strip()
            year = input("Год выхода: ").strip()
            seasons = input("Количество сезонов: ").strip()
            rating = input("Рейтинг (0-10): ").strip()

            try:
                year = int(year)
                seasons = int(seasons)
                rating = float(rating)
                add_series(title, genre, year, seasons, rating)
                print("Сериал добавлен.")
            except ValueError:
                print("Ошибка: год, сезоны и рейтинг должны быть числами.")

        elif choice == '2':
            series_list = list_series()
            print_series_list(series_list)


        elif choice == '3':

            print("\n--- Поиск с фильтрами ---")

            keyword = input("Ключевое слово (название/жанр) (Enter чтобы пропустить): ").strip()

            genre = input("Жанр (Enter чтобы пропустить): ").strip()

            year_min = input("Минимальный год (Enter чтобы пропустить): ").strip()

            year_max = input("Максимальный год (Enter чтобы пропустить): ").strip()

            rating_min = input("Минимальный рейтинг (Enter чтобы пропустить): ").strip()

            year_min = int(year_min) if year_min.isdigit() else None

            year_max = int(year_max) if year_max.isdigit() else None

            try:

                rating_min = float(rating_min)

            except ValueError:

                rating_min = None

            results = search_series_filtered(

                keyword=keyword if keyword else None,

                genre=genre if genre else None,

                year_min=year_min,

                year_max=year_max,

                rating_min=rating_min

            )

            print_series_list(results)



        elif choice == '4':

            series_id = input("ID сериала для изменения рейтинга: ").strip()

            new_rating = input("Новый рейтинг (0-10): ").strip()

            try:

                series_id = int(series_id)

                new_rating = float(new_rating)

                update_rating(series_id, new_rating)

                print("Рейтинг обновлён.")

            except ValueError:

                print("Ошибка: ID должен быть целым числом, рейтинг — числом с точкой.")


        elif choice == '5':

            series_id = input("ID сериала для удаления: ").strip()

            try:

                series_id = int(series_id)

                delete_series(series_id)

                print("Сериал удалён.")

            except ValueError:

                print("Ошибка: ID должен быть целым числом.")

        elif choice == '0':
            print("Выход. Удачи!")
            break

        else:
            print("Неверный выбор. Попробуйте ещё раз.")


if __name__ == '__main__':
    menu()
