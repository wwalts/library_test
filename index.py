import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from library import Library

lib = Library()
_b1 = lib.catalog.add_book("1984", "George Orwell", "Dystopia", 1949)
_b2 = lib.catalog.add_book("Dune", "Frank Herbert", "Sci-Fi", 1965)
_b3 = lib.catalog.add_book("Кобзар", "Тарас Шевченко", "Поезія", 1840)
lib.register_reader("Ivan Franko", "ivan@lib.ua")


def handler(request):
    report = lib.get_status_report()
    books = lib.catalog.get_all_books()
    readers = lib.readers.get_all_readers()

    books_html = ""
    for b in books:
        status = "✅ доступна" if b.is_available else "📤 видана"
        books_html += f"<tr><td>{b.book_id}</td><td><b>{b.title}</b></td><td>{b.author}</td><td>{b.genre}</td><td>{b.year}</td><td>{status}</td></tr>"

    readers_html = ""
    for r in readers:
        blocked = "🔴 заблок." if r.is_blocked else "🟢 активний"
        readers_html += f"<tr><td>{r.reader_id}</td><td><b>{r.name}</b></td><td>{r.email}</td><td>{len(r.rented_book_ids)}</td><td>{blocked}</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📚 Library System</title>
<style>
  body {{ font-family: Georgia, serif; background: #f5f0e8; color: #1a1208; margin: 0; }}
  header {{ background: #1a1208; color: #f5f0e8; padding: 1.5rem 2rem; border-bottom: 4px solid #b8860b; }}
  header h1 {{ margin: 0; font-size: 1.8rem; }} header h1 span {{ color: #b8860b; }}
  .stats {{ background: #ede8db; padding: 1rem 2rem; display: flex; gap: 2rem; border-bottom: 1px solid #ccc; }}
  .stat {{ text-align: center; }}
  .stat-num {{ font-size: 2rem; font-weight: bold; color: #c0392b; }}
  .stat-label {{ font-size: 0.7rem; text-transform: uppercase; opacity: 0.6; }}
  .content {{ padding: 2rem; }}
  h2 {{ font-size: 1.2rem; border-bottom: 2px solid #1a1208; padding-bottom: 0.5rem; margin-top: 2rem; }}
  table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }}
  th {{ background: #1a1208; color: #f5f0e8; padding: 0.6rem 1rem; text-align: left; font-size: 0.8rem; text-transform: uppercase; }}
  td {{ padding: 0.6rem 1rem; border-bottom: 1px solid #eee; font-size: 0.9rem; }}
  tr:hover {{ background: #fafafa; }}
</style>
</head>
<body>
<header><h1>📚 <span>Library</span> System</h1></header>
<div class="stats">
  <div class="stat"><div class="stat-num">{report['total_books']}</div><div class="stat-label">Книг</div></div>
  <div class="stat"><div class="stat-num">{report['available_books']}</div><div class="stat-label">Доступних</div></div>
  <div class="stat"><div class="stat-num">{report['total_readers']}</div><div class="stat-label">Читачів</div></div>
  <div class="stat"><div class="stat-num">{report['active_rentals']}</div><div class="stat-label">Оренд</div></div>
</div>
<div class="content">
  <h2>📖 Каталог книг</h2>
  <table><tr><th>#</th><th>Назва</th><th>Автор</th><th>Жанр</th><th>Рік</th><th>Статус</th></tr>
  {books_html}</table>
  <h2>👤 Читачі</h2>
  <table><tr><th>#</th><th>Ім'я</th><th>Email</th><th>Книг на руках</th><th>Статус</th></tr>
  {readers_html}</table>
</div>
</body></html>"""

    return html