from library import Library


def main():
    print("INSIDE MAIN")

    lib = Library()

    # 📚 Додаємо книги
    book1 = lib.catalog.add_book("1984", "George Orwell", "Dystopia", 1949)
    book2 = lib.catalog.add_book("Dune", "Frank Herbert", "Sci-Fi", 1965)

    print("Books added")

    # 👤 Реєстрація читача (ПРАВИЛЬНО)
    reader = lib.register_reader("Ivan", "ivan@gmail.com")

    print("Reader registered")

    # 📦 Оренда (ВАЖЛИВО: book_id, reader_id)
    lib.rent_book(book1.book_id, reader.reader_id)

    print("Book rented")

    # 📊 Вивід
    print("\n=== КНИГИ ===")
    print(lib.catalog.get_all_books())

    print("\n=== ЧИТАЧІ ===")
    print(lib.readers.get_all_readers())

    print("\n=== ОРЕНДИ ===")
    print(lib.rentals.get_all_records())

    print("\n=== ЗВІТ ===")
    print(lib.get_status_report())


if __name__ == "__main__":
    main()