# rental.py
from datetime import date, timedelta
from posthog import Posthog

posthog = Posthog(project_api_key="phc_kiafjm2VjjcX4XJEHZST6LL4sGXvxYw5TUVeKEVEzkiJ", host="https://eu.i.posthog.com")


class RentalRecord:
    RENTAL_DAYS = 14

    def __init__(self, rental_id: int, book_id: int, reader_id: int, rent_date: date):
        self.rental_id = rental_id
        self.book_id = book_id
        self.reader_id = reader_id
        self.rent_date = rent_date
        self.due_date = rent_date + timedelta(days=self.RENTAL_DAYS)
        self.return_date: date | None = None

    @property
    def is_returned(self) -> bool:
        return self.return_date is not None

    @property
    def is_overdue(self) -> bool:
        if self.is_returned:
            return self.return_date > self.due_date
        return date.today() > self.due_date

    def __repr__(self):
        status = "повернута" if self.is_returned else "активна"
        return f"Rental({self.rental_id}, book={self.book_id}, reader={self.reader_id}, {status})"


class RentalManager:

    def __init__(self):
        self._records: dict[int, RentalRecord] = {}
        self._next_id = 1

    def create_rental(self, book_id: int, reader_id: int,
                      rent_date: date | None = None) -> RentalRecord:
        if rent_date is None:
            rent_date = date.today()

        record = RentalRecord(self._next_id, book_id, reader_id, rent_date)
        self._records[self._next_id] = record
        self._next_id += 1

        posthog.capture("book_rented", distinct_id=f"reader_{reader_id}", properties={
            "book_id": book_id,
            "reader_id": reader_id,
            "rent_date": str(rent_date),
            "due_date": str(record.due_date),
        })

        return record

    def close_rental(self, rental_id: int,
                     return_date: date | None = None) -> RentalRecord:
        if rental_id not in self._records:
            raise KeyError(f"Запис про оренду {rental_id} не знайдено")

        record = self._records[rental_id]
        if record.is_returned:
            raise ValueError(f"Книгу за орендою {rental_id} вже було повернено")

        record.return_date = return_date or date.today()

        posthog.capture("book_returned", distinct_id=f"reader_{record.reader_id}", properties={
            "book_id": record.book_id,
            "rental_id": rental_id,
            "is_overdue": record.is_overdue,
            "return_date": str(record.return_date),
        })

        return record

    def get_active_rentals_by_reader(self, reader_id: int) -> list[RentalRecord]:
        return [
            r for r in self._records.values()
            if r.reader_id == reader_id and not r.is_returned
        ]

    def get_overdue_rentals(self) -> list[RentalRecord]:
        return [r for r in self._records.values() if r.is_overdue]

    def get_rental_by_book(self, book_id: int) -> RentalRecord | None:
        for record in self._records.values():
            if record.book_id == book_id and not record.is_returned:
                return record
        return None

    def get_all_records(self) -> list[RentalRecord]:
        return list(self._records.values())