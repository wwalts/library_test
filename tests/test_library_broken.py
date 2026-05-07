# test_library_broken.py
# Версія тестів із навмисною помилкою (для демонстрації роботи системи тестування)
# Студент: [Ваше ім'я], група ПП-33

import pytest
from unittest.mock import MagicMock
from datetime import date, timedelta

from catalog import Book, Catalog
from reader import Reader, ReaderRegistry
from rental import RentalRecord, RentalManager
from library import Library


# ═══════════════════════════════════════════════════════
# БЛОК 1: Тести модуля catalog.py (тести 1–12)
# ═══════════════════════════════════════════════════════

class TestBook:

    def test_01_book_default_available(self):
        book = Book(1, "Кобзар", "Тарас Шевченко", "Поезія", 1840)
        assert book.is_available is True

    def test_02_book_repr_contains_title(self):
        book = Book(2, "Тіні забутих предків", "М. Коцюбинський", "Проза", 1911)
        assert "Тіні забутих предків" in repr(book)

    def test_03_book_repr_shows_status_available(self):
        book = Book(3, "Тест", "Автор", "Жанр", 2020)
        assert "доступна" in repr(book)

    def test_04_book_repr_shows_status_rented(self):
        book = Book(4, "Тест", "Автор", "Жанр", 2020)
        book.is_available = False
        assert "видана" in repr(book)


class TestCatalog:

    def setup_method(self):
        self.catalog = Catalog()

    def test_05_add_book_returns_book_object(self):
        book = self.catalog.add_book("1984", "Джордж Орвелл", "Антиутопія", 1949)
        assert isinstance(book, Book)
        assert book.title == "1984"

    def test_06_add_book_increments_total_count(self):
        self.catalog.add_book("Книга 1", "Автор 1", "Жанр", 2000)
        self.catalog.add_book("Книга 2", "Автор 2", "Жанр", 2001)
        assert self.catalog.total_count == 2

    def test_07_add_book_empty_title_raises_error(self):
        with pytest.raises(ValueError):
            self.catalog.add_book("", "Автор", "Жанр", 2000)

    def test_08_add_book_invalid_year_raises_error(self):
        with pytest.raises(ValueError):
            self.catalog.add_book("Книга", "Автор", "Жанр", -5)

    def test_09_get_book_returns_correct_book(self):
        book = self.catalog.add_book("Гаррі Поттер", "Роулінг", "Фентезі", 1997)
        fetched = self.catalog.get_book(book.book_id)
        assert fetched.title == "Гаррі Поттер"

    def test_10_get_book_nonexistent_raises_error(self):
        with pytest.raises(KeyError):
            self.catalog.get_book(999)

    def test_11_search_by_title_partial_match(self):
        self.catalog.add_book("Майстер і Маргарита", "Булгаков", "Проза", 1967)
        self.catalog.add_book("Майстер класу", "Автор", "Проза", 2010)
        results = self.catalog.search_by_title("Майстер")
        assert len(results) == 2

    def test_12_get_available_books_filters_correctly(self):
        b1 = self.catalog.add_book("Доступна", "Автор", "Жанр", 2000)
        b2 = self.catalog.add_book("Видана", "Автор", "Жанр", 2001)
        b2.is_available = False
        available = self.catalog.get_available_books()
        assert len(available) == 1


# ═══════════════════════════════════════════════════════
# БЛОК 2: Тести модуля reader.py (тести 13–20)
# ═══════════════════════════════════════════════════════

class TestReader:

    def test_13_new_reader_can_rent(self):
        reader = Reader(1, "Іван Іванов", "ivan@test.com")
        assert reader.can_rent() is True

    def test_14_blocked_reader_cannot_rent(self):
        reader = Reader(2, "Петро Петров", "petro@test.com")
        reader.is_blocked = True
        assert reader.can_rent() is False

    def test_15_reader_at_max_books_cannot_rent(self):
        reader = Reader(3, "Оля Олійник", "olya@test.com")
        reader.rented_book_ids = [1, 2, 3]
        assert reader.can_rent() is False

    def test_16_reader_repr_shows_name(self):
        reader = Reader(4, "Марія Коваль", "maria@test.com")
        assert "Марія Коваль" in repr(reader)


class TestReaderRegistry:

    def setup_method(self):
        self.registry = ReaderRegistry()

    def test_17_register_reader_returns_reader(self):
        reader = self.registry.register("Тарас Шевченко", "taras@example.com")
        assert isinstance(reader, Reader)
        assert reader.name == "Тарас Шевченко"

    def test_18_register_duplicate_email_raises_error(self):
        self.registry.register("Перший Користувач", "test@example.com")
        with pytest.raises(ValueError):
            self.registry.register("Другий Користувач", "test@example.com")

    def test_19_register_invalid_email_raises_error(self):
        with pytest.raises(ValueError):
            self.registry.register("Користувач", "not-an-email")

    def test_20_block_and_unblock_reader(self):
        reader = self.registry.register("Василь Василенко", "vasyl@test.com")
        self.registry.block_reader(reader.reader_id)
        assert reader.is_blocked is True
        self.registry.unblock_reader(reader.reader_id)
        assert reader.is_blocked is False


# ═══════════════════════════════════════════════════════
# БЛОК 3: Тести модуля rental.py (тести 21–26)
# ═══════════════════════════════════════════════════════

class TestRentalRecord:

    def test_21_new_rental_is_not_returned(self):
        record = RentalRecord(1, 10, 20, date.today())
        assert record.is_returned is False

    def test_22_due_date_is_14_days_from_rent(self):
        rent_date = date(2026, 1, 1)
        record = RentalRecord(2, 10, 20, rent_date)
        assert record.due_date == date(2026, 1, 15)

    def test_23_overdue_rental_detected(self):
        old_date = date.today() - timedelta(days=20)
        record = RentalRecord(3, 10, 20, old_date)
        assert record.is_overdue is True

    def test_24_returned_rental_not_overdue_if_on_time(self):
        rent_date = date.today()
        record = RentalRecord(4, 10, 20, rent_date)
        record.return_date = date.today()
        assert record.is_overdue is False


class TestRentalManager:

    def setup_method(self):
        self.manager = RentalManager()

    def test_25_create_rental_returns_record(self):
        record = self.manager.create_rental(1, 1)
        assert isinstance(record, RentalRecord)

    def test_26_close_rental_sets_return_date(self):
        record = self.manager.create_rental(2, 2)
        closed = self.manager.close_rental(record.rental_id)
        assert closed.is_returned is True


# ═══════════════════════════════════════════════════════
# БЛОК 4: Інтеграційні тести через Library (тести 27–30)
# ═══════════════════════════════════════════════════════

class TestLibraryIntegration:

    def setup_method(self):
        self.lib = Library()

    def test_27_rent_and_return_full_cycle(self):
        book = self.lib.add_book("Дюна", "Герберт", "Фантастика", 1965)
        reader = self.lib.register_reader("Олег Олегов", "oleg@test.com")
        self.lib.rent_book(book.book_id, reader.reader_id)
        self.lib.return_book(book.book_id)
        assert book.is_available

    def test_28_rent_unavailable_book_raises_error(self):
        book = self.lib.add_book("Книга", "Автор", "Жанр", 2000)
        reader1 = self.lib.register_reader("Читач 1", "r1@test.com")
        reader2 = self.lib.register_reader("Читач 2", "r2@test.com")
        self.lib.rent_book(book.book_id, reader1.reader_id)
        with pytest.raises(ValueError):
            self.lib.rent_book(book.book_id, reader2.reader_id)

    def test_29_status_report_reflects_state(self):
        self.lib.add_book("Книга А", "Автор", "Жанр", 2000)
        book_b = self.lib.add_book("Книга Б", "Автор", "Жанр", 2001)
        reader = self.lib.register_reader("Читач", "reader@test.com")
        self.lib.rent_book(book_b.book_id, reader.reader_id)

        report = self.lib.get_status_report()
        assert report["total_books"] == 2
        assert report["available_books"] == 1
        assert report["active_rentals"] == 1

    # ──────────────────────────────────────────────────
    # НАВМИСНА ПОМИЛКА (тест 30):
    # Очікуємо 14 днів терміну оренди, але перевіряємо 7 —
    # це призведе до AssertionError: 14 != 7
    # ──────────────────────────────────────────────────
 