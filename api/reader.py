# reader.py
# Модуль для управління читачами бібліотеки
# Відповідає за реєстрацію читачів та їх абонементи


class Reader:
    """Представляє зареєстрованого читача бібліотеки."""

    MAX_BOOKS = 3  # Максимальна кількість книг на руках одночасно

    def __init__(self, reader_id: int, name: str, email: str):
        self.reader_id = reader_id
        self.name = name
        self.email = email
        self.rented_book_ids: list[int] = []  # ID книг, що зараз на руках
        self.is_blocked = False  # Чи заблокований читач

    def can_rent(self) -> bool:
        """Перевіряє, чи може читач взяти ще одну книгу."""
        return not self.is_blocked and len(self.rented_book_ids) < self.MAX_BOOKS

    def __repr__(self):
        return f"Reader({self.reader_id}, '{self.name}', books={len(self.rented_book_ids)})"


class ReaderRegistry:
    """
    Реєстр читачів бібліотеки.
    Відповідає за реєстрацію нових читачів та пошук існуючих.
    """

    def __init__(self):
        self._readers: dict[int, Reader] = {}
        self._next_id = 1

    def register(self, name: str, email: str) -> Reader:
        """Реєструє нового читача. Повертає створеного читача."""
        name = name.strip()
        email = email.strip().lower()

        if not name:
            raise ValueError("Ім'я читача не може бути порожнім")
        if "@" not in email or "." not in email:
            raise ValueError(f"Некоректна email-адреса: {email}")
        if self._find_by_email(email):
            raise ValueError(f"Читач з email {email} вже зареєстрований")

        reader = Reader(self._next_id, name, email)
        self._readers[self._next_id] = reader
        self._next_id += 1
        return reader

    def get_reader(self, reader_id: int) -> Reader:
        """Повертає читача за ID."""
        if reader_id not in self._readers:
            raise KeyError(f"Читач з ID {reader_id} не знайдений")
        return self._readers[reader_id]

    def block_reader(self, reader_id: int) -> None:
        """Блокує читача (наприклад, за затримку повернення)."""
        reader = self.get_reader(reader_id)
        reader.is_blocked = True

    def unblock_reader(self, reader_id: int) -> None:
        """Розблоковує читача."""
        reader = self.get_reader(reader_id)
        reader.is_blocked = False

    def _find_by_email(self, email: str) -> Reader | None:
        """Внутрішній метод: пошук читача за email."""
        for reader in self._readers.values():
            if reader.email == email:
                return reader
        return None

    def find_by_name(self, name: str) -> list[Reader]:
        """Шукає читачів за ім'ям (часткове співпадіння)."""
        name = name.lower().strip()
        return [r for r in self._readers.values() if name in r.name.lower()]

    def get_all_readers(self) -> list[Reader]:
        """Повертає список усіх зареєстрованих читачів."""
        return list(self._readers.values())