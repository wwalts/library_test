# library.py
# Головний модуль бібліотеки
# Клас Library об'єднує Catalog, ReaderRegistry та RentalManager

from api.catalog import Catalog
from api.reader import ReaderRegistry
from api.rental import RentalManager


class Library:
    """
    Головний клас бібліотечної системи.
    Координує взаємодію між каталогом, реєстром читачів та менеджером оренди.
    Реалізує основні сценарії використання бібліотеки.
    """

    def __init__(self):
        self.catalog = Catalog()
        self.readers = ReaderRegistry()
        self.rentals = RentalManager()

    # ── Робота з книгами ──────────────────────────────────────────────────

    def add_book(self, title: str, author: str, genre: str, year: int):
        """Додає книгу до бібліотечного фонду."""
        return self.catalog.add_book(title, author, genre, year)

    # ── Робота з читачами ─────────────────────────────────────────────────

    def register_reader(self, name: str, email: str):
        """Реєструє нового читача."""
        return self.readers.register(name, email)

    # ── Оренда ───────────────────────────────────────────────────────────

    def rent_book(self, book_id: int, reader_id: int):
        """
        Основна операція: видає книгу читачу.
        Перевіряє всі необхідні умови перед видачею.
        """
        # 1. Отримуємо книгу та читача (піднімуть KeyError якщо не існують)
        book = self.catalog.get_book(book_id)
        reader = self.readers.get_reader(reader_id)

        # 2. Перевіряємо, чи книга доступна
        if not book.is_available:
            raise ValueError(f"Книга '{book.title}' зараз недоступна — вона видана іншому читачу")

        # 3. Перевіряємо, чи читач може взяти ще одну книгу
        if not reader.can_rent():
            if reader.is_blocked:
                raise PermissionError(f"Читач {reader.name} заблокований і не може брати книги")
            raise ValueError(
                f"Читач {reader.name} вже має максимальну кількість книг ({reader.MAX_BOOKS})"
            )

        # 4. Створюємо запис оренди
        record = self.rentals.create_rental(book_id, reader_id)

        # 5. Оновлюємо стан книги та список читача
        book.is_available = False
        reader.rented_book_ids.append(book_id)

        return record

    def return_book(self, book_id: int):
        """
        Приймає повернення книги.
        Знаходить активну оренду та закриває її.
        """
        # 1. Перевіряємо, що книга існує
        book = self.catalog.get_book(book_id)

        # 2. Знаходимо активну оренду для цієї книги
        record = self.rentals.get_rental_by_book(book_id)
        if record is None:
            raise ValueError(f"Книга '{book.title}' не рахується виданою")

        # 3. Закриваємо оренду
        self.rentals.close_rental(record.rental_id)

        # 4. Оновлюємо стан книги та список читача
        book.is_available = True
        reader = self.readers.get_reader(record.reader_id)
        reader.rented_book_ids.remove(book_id)

        return record

    # ── Звіти ────────────────────────────────────────────────────────────

    def get_status_report(self) -> dict:
        """Повертає загальний звіт про стан бібліотеки."""
        return {
            "total_books": self.catalog.total_count,
            "available_books": len(self.catalog.get_available_books()),
            "total_readers": len(self.readers.get_all_readers()),
            "active_rentals": len([
                r for r in self.rentals.get_all_records() if not r.is_returned
            ]),
            "overdue_rentals": len(self.rentals.get_overdue_rentals()),
        }