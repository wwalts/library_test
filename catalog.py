# catalog.py
# Модуль для управління каталогом книг
# Відповідає за зберігання та пошук книг у бібліотеці


class Book:
    """Представляє окрему книгу в каталозі."""

    def __init__(self, book_id: int, title: str, author: str, genre: str, year: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year
        self.is_available = True  # Книга вільна за замовчуванням

    def __repr__(self):
        status = "доступна" if self.is_available else "видана"
        return f"Book({self.book_id}, '{self.title}', {self.author}, {status})"


class Catalog:
    """
    Каталог книг бібліотеки.
    Відповідає за додавання, видалення та пошук книг.
    """

    def __init__(self):
        self._books: dict[int, Book] = {}  # Словник: book_id -> Book
        self._next_id = 1  # Автоінкремент ID

    def add_book(self, title: str, author: str, genre: str, year: int) -> Book:
        """Додає нову книгу до каталогу та повертає її."""
        if not title or not author:
            raise ValueError("Назва та автор книги не можуть бути порожніми")
        if year < 0 or year > 2100:
            raise ValueError(f"Некоректний рік видання: {year}")

        book = Book(self._next_id, title, author, genre, year)
        self._books[self._next_id] = book
        self._next_id += 1
        return book

    def remove_book(self, book_id: int) -> bool:
        """Видаляє книгу з каталогу. Повертає True якщо успішно."""
        if book_id not in self._books:
            raise KeyError(f"Книга з ID {book_id} не знайдена")
        if not self._books[book_id].is_available:
            raise ValueError("Не можна видалити книгу, яка зараз видана читачу")
        del self._books[book_id]
        return True

    def get_book(self, book_id: int) -> Book:
        """Повертає книгу за її ID."""
        if book_id not in self._books:
            raise KeyError(f"Книга з ID {book_id} не знайдена")
        return self._books[book_id]

    def search_by_title(self, query: str) -> list[Book]:
        """Шукає книги за назвою (часткове співпадіння, без урахування регістру)."""
        query = query.lower().strip()
        return [b for b in self._books.values() if query in b.title.lower()]

    def search_by_author(self, author: str) -> list[Book]:
        """Шукає книги за автором."""
        author = author.lower().strip()
        return [b for b in self._books.values() if author in b.author.lower()]

    def get_available_books(self) -> list[Book]:
        """Повертає список всіх доступних для видачі книг."""
        return [b for b in self._books.values() if b.is_available]

    def get_all_books(self) -> list[Book]:
        """Повертає список усіх книг каталогу."""
        return list(self._books.values())

    @property
    def total_count(self) -> int:
        """Загальна кількість книг у каталозі."""
        return len(self._books)