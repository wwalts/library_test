# test_e2e_critical_path.py
# Наскрізний тест критичного шляху бібліотечної системи
# Запуск: python -m pytest test_e2e_critical_path.py -v

import logging
import pytest
from datetime import date

from api.library import Library

# ─── Налаштування логування (відображається в --live-log) ────────────────────
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# ─── Фасад: емулює "інтерфейс" бібліотечної програми ────────────────────────

class LibraryApp:
    """
    Емулює запуск головного вікна програми.
    Надає селектори та поля виводу — аналог UI-компонентів.
    """

    def __init__(self):
        self._lib = Library()
        self._current_book = None
        self._current_reader = None
        self._last_rental = None
        self._last_return = None
        self._report = None

        # Наповнюємо фонд книг (аналог початкового стану БД)
        self._lib.add_book("Кобзар", "Тарас Шевченко", "Poetry", 1840)
        self._lib.add_book("1984", "George Orwell", "Dystopia", 1949)
        self._lib.add_book("Dune", "Frank Herbert", "Sci-Fi", 1965)

    # ── Селектори (аналог UI-елементів вводу) ────────────────────────────────

    class _BookSelector:
        def __init__(self, app): self._app = app

        def set(self, title: str):
            results = self._app._lib.catalog.search_by_title(title)
            if not results:
                raise ValueError(f"Книгу '{title}' не знайдено в каталозі")
            self._app._current_book = results[0]

    class _ReaderSelector:
        def __init__(self, app): self._app = app

        def set(self, name: str, email: str):
            self._app._current_reader = self._app._lib.register_reader(name, email)

    # ── Поля виводу (аналог UI-лейблів) ──────────────────────────────────────

    class _BookStatusOutput:
        def __init__(self, app): self._app = app

        def text(self) -> str:
            book = self._app._current_book
            if book is None:
                return ""
            return "доступна" if book.is_available else "видана"

    class _RentalStatusOutput:
        def __init__(self, app): self._app = app

        def text(self) -> str:
            rental = self._app._last_rental
            if rental is None:
                return ""
            return f"оренда #{rental.rental_id} активна"

    class _ReturnStatusOutput:
        def __init__(self, app): self._app = app

        def text(self) -> str:
            record = self._app._last_return
            if record is None:
                return ""
            return "книга повернута" if record.is_returned else "не повернута"

    class _ReportOutput:
        def __init__(self, app): self._app = app

        def value(self, key: str):
            if self._app._report is None:
                return None
            return self._app._report.get(key)

    # ── Ініціалізація компонентів ─────────────────────────────────────────────

    @property
    def book_selector(self):       return self._BookSelector(self)

    @property
    def reader_selector(self):     return self._ReaderSelector(self)

    @property
    def book_status_output(self):  return self._BookStatusOutput(self)

    @property
    def rental_status_output(self): return self._RentalStatusOutput(self)

    @property
    def return_status_output(self): return self._ReturnStatusOutput(self)

    @property
    def report_output(self):       return self._ReportOutput(self)

    # ── Дії (аналог кнопок у UI) ──────────────────────────────────────────────

    def press_rent(self):
        self._last_rental = self._lib.rent_book(
            self._current_book.book_id,
            self._current_reader.reader_id
        )

    def press_return(self):
        self._last_return = self._lib.return_book(self._current_book.book_id)

    def press_refresh_report(self):
        self._report = self._lib.get_status_report()


# ═══════════════════════════════════════════════════════════════════════════════
# ТЕСТ КРИТИЧНОГО ШЛЯХУ
# ═══════════════════════════════════════════════════════════════════════════════

def test_e2e_critical_path():
    # Емуляція запуску головного вікна програми
    app = LibraryApp()

    # Крок 1: Вибір книги та читача
    app.book_selector.set("Кобзар")
    logger.info("Крок 1: app.book_selector.set('Кобзар')                    OK")

    app.reader_selector.set("Іван", "ivan@lib.ua")
    logger.info("Крок 2: app.reader_selector.set('Іван', 'ivan@lib.ua')     OK")

    # Крок 2: Видача книги та перевірка статусу через інтерфейс
    app.press_rent()
    assert app.book_status_output.text() == "видана"
    logger.info("Крок 3: assert app.book_status_output.text() == 'видана'   OK")

    assert app.rental_status_output.text() == "оренда #1 активна"
    logger.info("Крок 4: assert app.rental_status_output.text()             OK  ->  'оренда #1 активна'")

    # Крок 3: Повернення книги та перевірка статусу
    app.press_return()
    assert app.return_status_output.text() == "книга повернута"
    logger.info("Крок 5: assert app.return_status_output.text()             OK  ->  'книга повернута'")

    assert app.book_status_output.text() == "доступна"
    logger.info("Крок 6: assert app.book_status_output.text() == 'доступна' OK")

    # Крок 4: Перевірка звіту через інтерфейс
    app.press_refresh_report()
    assert app.report_output.value("total_books") == 3
    logger.info("Крок 7: assert app.report_output.value('total_books') == 3 OK")

    assert app.report_output.value("available_books") == 3
    logger.info("Крок 8: assert app.report_output.value('available_books')  OK  ->  3")