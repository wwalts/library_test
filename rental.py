# rental.py
# Модуль для управління записами про видачу книг
# Відповідає за фіксацію та відстеження всіх оренд

from datetime import date, timedelta


class RentalRecord:
    """Запис про одну конкретну видачу книги читачу."""

    RENTAL_DAYS = 14  # Стандартний термін оренди — 14 днів

    def __init__(self, rental_id: int, book_id: int, reader_id: int, rent_date: date):
        self.rental_id = rental_id
        self.book_id = book_id
        self.reader_id = reader_id
        self.rent_date = rent_date
        self.due_date = rent_date + timedelta(days=self.RENTAL_DAYS)
        self.return_date: date | None = None  # None = ще не повернута

    @property
    def is_returned(self) -> bool:
        """Перевіряє, чи книгу вже повернули."""
        return self.return_date is not None

    @property
    def is_overdue(self) -> bool:
        """Перевіряє, чи прострочено термін повернення."""
        if self.is_returned:
            return self.return_date > self.due_date
        return date.today() > self.due_date

    def __repr__(self):
        status = "повернута" if self.is_returned else "активна"
        return f"Rental({self.rental_id}, book={self.book_id}, reader={self.reader_id}, {status})"


class RentalManager:
    """
    Менеджер оренди книг.
    Відповідає за видачу та повернення книг,
    а також ведення журналу всіх операцій.
    """

    def __init__(self):
        self._records: dict[int, RentalRecord] = {}
        self._next_id = 1

    def create_rental(self, book_id: int, reader_id: int,
                      rent_date: date | None = None) -> RentalRecord:
        """
        Створює новий запис про видачу книги.
        Якщо дата не вказана — використовується сьогоднішня.
        """
        if rent_date is None:
            rent_date = date.today()

        record = RentalRecord(self._next_id, book_id, reader_id, rent_date)
        self._records[self._next_id] = record
        self._next_id += 1
        return record

    def close_rental(self, rental_id: int,
                     return_date: date | None = None) -> RentalRecord:
        """Фіксує повернення книги. Повертає оновлений запис."""
        if rental_id not in self._records:
            raise KeyError(f"Запис про оренду {rental_id} не знайдено")

        record = self._records[rental_id]
        if record.is_returned:
            raise ValueError(f"Книгу за орендою {rental_id} вже було повернено")

        record.return_date = return_date or date.today()
        return record

    def get_active_rentals_by_reader(self, reader_id: int) -> list[RentalRecord]:
        """Повертає всі активні (не повернуті) оренди конкретного читача."""
        return [
            r for r in self._records.values()
            if r.reader_id == reader_id and not r.is_returned
        ]

    def get_overdue_rentals(self) -> list[RentalRecord]:
        """Повертає всі прострочені оренди (не повернуті в термін)."""
        return [r for r in self._records.values() if r.is_overdue]

    def get_rental_by_book(self, book_id: int) -> RentalRecord | None:
        """Знаходить активну оренду для конкретної книги."""
        for record in self._records.values():
            if record.book_id == book_id and not record.is_returned:
                return record
        return None

    def get_all_records(self) -> list[RentalRecord]:
        """Повертає всі записи про оренди (і активні, і завершені)."""
        return list(self._records.values())