"""
index.py — веб-інтерфейс для Бібліотечної системи з PostHog аналітикою
Запуск: python index.py
Відкрий браузер: http://localhost:5000
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template_string, request, redirect, url_for, flash
from library import Library
from posthog import Posthog

app = Flask(__name__)
app.secret_key = "library-secret-key-2026"

# PostHog аналітика
posthog = Posthog(
    api_key='phc_wNnVRHx5Y588NMtQEsP2evJaPKKuRtRfBbfEki4jzrdL',
    host='https://us.i.posthog.com'
)

lib = Library()
_book1 = lib.catalog.add_book("1984", "George Orwell", "Dystopia", 1949)
_book2 = lib.catalog.add_book("Dune", "Frank Herbert", "Sci-Fi", 1965)
_book3 = lib.catalog.add_book("Кобзар", "Тарас Шевченко", "Поезія", 1840)
lib.register_reader("Ivan Franko", "ivan@lib.ua")

HTML = """
<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>📚 Library System</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<script>
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]);t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+" (stub)"},o="init push capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    posthog.init('phc_wNnVRHx5Y588NMtQEsP2evJaPKKuRtRfBbfEki4jzrdL', {
        api_host: 'https://us.i.posthog.com',
        person_profiles: 'identified_only',
        session_recording: { maskAllInputs: false },
    })
</script>
<style>
  :root {
    --ink: #1a1208; --paper: #f5f0e8; --cream: #ede8db;
    --accent: #c0392b; --gold: #b8860b; --sage: #5a7a5a;
    --shadow: rgba(26,18,8,0.12);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: var(--paper); color: var(--ink); font-family: 'DM Sans', sans-serif; min-height: 100vh; }
  header { background: var(--ink); color: var(--paper); padding: 2rem 3rem; display: flex; align-items: center; justify-content: space-between; border-bottom: 4px solid var(--gold); }
  header h1 { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 900; letter-spacing: -0.5px; }
  header h1 span { color: var(--gold); }
  .header-sub { font-size: 0.8rem; opacity: 0.6; letter-spacing: 2px; text-transform: uppercase; margin-top: 0.2rem; }
  .stats-bar { background: var(--cream); border-bottom: 1px solid rgba(26,18,8,0.15); padding: 1rem 3rem; display: flex; gap: 2.5rem; align-items: center; }
  .stat { display: flex; align-items: baseline; gap: 0.5rem; }
  .stat-num { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 700; color: var(--accent); }
  .stat-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.6; }
  .stat-divider { width: 1px; height: 2rem; background: rgba(26,18,8,0.2); }
  .main { display: grid; grid-template-columns: 1fr 1fr 340px; gap: 0; min-height: calc(100vh - 140px); }
  .panel { padding: 2rem; border-right: 1px solid rgba(26,18,8,0.1); }
  .panel:last-child { border-right: none; }
  .panel-title { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; margin-bottom: 1.5rem; padding-bottom: 0.75rem; border-bottom: 2px solid var(--ink); display: flex; align-items: center; gap: 0.5rem; }
  .book-card { background: white; border: 1px solid rgba(26,18,8,0.1); border-radius: 4px; padding: 1rem 1.2rem; margin-bottom: 0.75rem; display: flex; align-items: center; justify-content: space-between; transition: box-shadow 0.2s; box-shadow: 0 1px 3px var(--shadow); }
  .book-card:hover { box-shadow: 0 4px 12px var(--shadow); }
  .book-info { flex: 1; }
  .book-title { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 0.95rem; }
  .book-meta { font-size: 0.75rem; opacity: 0.55; margin-top: 0.2rem; }
  .badge { font-size: 0.65rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; padding: 0.25rem 0.6rem; border-radius: 2px; white-space: nowrap; }
  .badge-available { background: #e8f5e9; color: var(--sage); border: 1px solid #a5d6a7; }
  .badge-rented { background: #fdecea; color: var(--accent); border: 1px solid #f5c6c6; }
  .reader-card { background: white; border: 1px solid rgba(26,18,8,0.1); border-radius: 4px; padding: 0.9rem 1.2rem; margin-bottom: 0.75rem; box-shadow: 0 1px 3px var(--shadow); }
  .reader-name { font-weight: 500; font-size: 0.9rem; }
  .reader-meta { font-size: 0.75rem; opacity: 0.5; margin-top: 0.15rem; }
  .reader-books { margin-top: 0.4rem; font-size: 0.75rem; color: var(--accent); }
  .form-section { background: white; border: 1px solid rgba(26,18,8,0.1); border-radius: 4px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 1px 3px var(--shadow); }
  .form-section h3 { font-family: 'Playfair Display', serif; font-size: 0.95rem; font-weight: 700; margin-bottom: 0.9rem; color: var(--ink); }
  .form-row { margin-bottom: 0.6rem; }
  label { display: block; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.6; margin-bottom: 0.25rem; }
  input, select { width: 100%; padding: 0.5rem 0.7rem; border: 1px solid rgba(26,18,8,0.2); border-radius: 3px; font-family: 'DM Sans', sans-serif; font-size: 0.85rem; background: var(--paper); color: var(--ink); transition: border-color 0.2s; }
  input:focus, select:focus { outline: none; border-color: var(--gold); }
  .btn { width: 100%; padding: 0.6rem; border: none; border-radius: 3px; font-family: 'DM Sans', sans-serif; font-size: 0.8rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; cursor: pointer; margin-top: 0.5rem; transition: all 0.2s; }
  .btn-primary { background: var(--ink); color: var(--paper); }
  .btn-primary:hover { background: #2d2010; }
  .btn-danger { background: var(--accent); color: white; }
  .btn-danger:hover { background: #a93226; }
  .btn-success { background: var(--sage); color: white; }
  .btn-success:hover { background: #4a6a4a; }
  .alerts { padding: 0 3rem; margin-top: 1rem; }
  .alert { padding: 0.75rem 1rem; border-radius: 3px; font-size: 0.85rem; margin-bottom: 0.5rem; border-left: 4px solid; }
  .alert-success { background: #e8f5e9; border-color: var(--sage); color: #2d5a2d; }
  .alert-error { background: #fdecea; border-color: var(--accent); color: #7b1c1c; }
  .rental-item { font-size: 0.8rem; padding: 0.6rem 0; border-bottom: 1px dashed rgba(26,18,8,0.12); display: flex; justify-content: space-between; align-items: center; }
  .rental-item:last-child { border-bottom: none; }
  .overdue { color: var(--accent); font-weight: 500; }
  .empty-state { font-size: 0.8rem; opacity: 0.4; text-align: center; padding: 2rem 0; font-style: italic; }
</style>
</head>
<body>
<header>
  <div>
    <h1>📚 <span>Library</span> System</h1>
    <div class="header-sub">Система управління бібліотекою</div>
  </div>
</header>

{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
  <div class="alerts">
    {% for cat, msg in messages %}
    <div class="alert alert-{{ cat }}">{{ msg }}</div>
    {% endfor %}
  </div>
  {% endif %}
{% endwith %}

<div class="stats-bar">
  <div class="stat"><div class="stat-num">{{ report.total_books }}</div><div class="stat-label">Книг всього</div></div>
  <div class="stat-divider"></div>
  <div class="stat"><div class="stat-num">{{ report.available_books }}</div><div class="stat-label">Доступних</div></div>
  <div class="stat-divider"></div>
  <div class="stat"><div class="stat-num">{{ report.total_readers }}</div><div class="stat-label">Читачів</div></div>
  <div class="stat-divider"></div>
  <div class="stat"><div class="stat-num">{{ report.active_rentals }}</div><div class="stat-label">Активних оренд</div></div>
  {% if report.overdue_rentals > 0 %}
  <div class="stat-divider"></div>
  <div class="stat"><div class="stat-num overdue">{{ report.overdue_rentals }}</div><div class="stat-label overdue">Прострочених</div></div>
  {% endif %}
</div>

<div class="main">
  <div class="panel">
    <div class="panel-title">📖 Каталог книг</div>
    {% for book in books %}
    <div class="book-card">
      <div class="book-info">
        <div class="book-title">{{ book.title }}</div>
        <div class="book-meta">{{ book.author }} · {{ book.genre }} · {{ book.year }}</div>
      </div>
      <div style="display:flex; flex-direction:column; align-items:flex-end; gap:0.4rem; margin-left:1rem;">
        {% if book.is_available %}
          <span class="badge badge-available">доступна</span>
          <form method="POST" action="/rent">
            <input type="hidden" name="book_id" value="{{ book.book_id }}">
            <select name="reader_id" style="width:auto; font-size:0.72rem; padding:0.2rem 0.4rem; margin-bottom:0.3rem;">
              {% for r in readers %}<option value="{{ r.reader_id }}">{{ r.name }}</option>{% endfor %}
            </select>
            <button type="submit" class="btn btn-primary" style="padding:0.25rem 0.6rem; font-size:0.65rem;">Видати</button>
          </form>
        {% else %}
          <span class="badge badge-rented">видана</span>
          <form method="POST" action="/return">
            <input type="hidden" name="book_id" value="{{ book.book_id }}">
            <button type="submit" class="btn btn-success" style="padding:0.25rem 0.6rem; font-size:0.65rem;">Повернути</button>
          </form>
        {% endif %}
      </div>
    </div>
    {% else %}
    <div class="empty-state">Книг ще немає</div>
    {% endfor %}
    <div class="form-section" style="margin-top:1.5rem;">
      <h3>＋ Додати книгу</h3>
      <form method="POST" action="/add_book">
        <div class="form-row"><label>Назва</label><input type="text" name="title" required placeholder="Назва книги"></div>
        <div class="form-row"><label>Автор</label><input type="text" name="author" required placeholder="Прізвище Імя"></div>
        <div class="form-row" style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
          <div><label>Жанр</label><input type="text" name="genre" placeholder="Жанр"></div>
          <div><label>Рік</label><input type="number" name="year" placeholder="2024" min="0" max="2100"></div>
        </div>
        <button type="submit" class="btn btn-primary">Додати до каталогу</button>
      </form>
    </div>
  </div>

  <div class="panel">
    <div class="panel-title">👤 Читачі</div>
    {% for reader in readers %}
    <div class="reader-card">
      <div style="display:flex; justify-content:space-between; align-items:start;">
        <div>
          <div class="reader-name">{{ reader.name }}</div>
          <div class="reader-meta">{{ reader.email }}</div>
          {% if reader.rented_book_ids %}<div class="reader-books">📚 {{ reader.rented_book_ids | length }} книг(и) на руках</div>{% endif %}
        </div>
        <div style="display:flex; gap:0.4rem; align-items:center;">
          {% if reader.is_blocked %}
            <span class="badge badge-rented">заблок.</span>
            <form method="POST" action="/unblock">
              <input type="hidden" name="reader_id" value="{{ reader.reader_id }}">
              <button class="btn btn-success" style="padding:0.2rem 0.5rem; font-size:0.65rem; margin:0;">Розблок.</button>
            </form>
          {% else %}
            <span class="badge badge-available">активний</span>
            <form method="POST" action="/block">
              <input type="hidden" name="reader_id" value="{{ reader.reader_id }}">
              <button class="btn btn-danger" style="padding:0.2rem 0.5rem; font-size:0.65rem; margin:0;">Блок.</button>
            </form>
          {% endif %}
        </div>
      </div>
    </div>
    {% else %}
    <div class="empty-state">Читачів ще немає</div>
    {% endfor %}
    <div class="form-section" style="margin-top:1.5rem;">
      <h3>＋ Зареєструвати читача</h3>
      <form method="POST" action="/add_reader">
        <div class="form-row"><label>Імя</label><input type="text" name="name" required placeholder="Повне імя"></div>
        <div class="form-row"><label>Email</label><input type="email" name="email" required placeholder="reader@example.com"></div>
        <button type="submit" class="btn btn-primary">Зареєструвати</button>
      </form>
    </div>
  </div>

  <div class="panel">
    <div class="panel-title">📋 Активні оренди</div>
    {% set has_active = false %}
    {% for record in rentals %}
      {% if not record.is_returned %}
        {% set has_active = true %}
        <div class="rental-item {% if record.is_overdue %}overdue{% endif %}">
          <div>
            <div style="font-weight:500; font-size:0.82rem;">{{ book_map.get(record.book_id, '?') }}</div>
            <div style="opacity:0.55; font-size:0.72rem; margin-top:0.1rem;">{{ reader_map.get(record.reader_id, '?') }}</div>
            <div style="opacity:0.45; font-size:0.7rem;">до {{ record.due_date.strftime('%d.%m.%Y') }}</div>
          </div>
          {% if record.is_overdue %}<span class="badge badge-rented">прострочено</span>{% endif %}
        </div>
      {% endif %}
    {% endfor %}
    {% if not has_active %}<div class="empty-state">Активних оренд немає</div>{% endif %}
    {% set completed = rentals | selectattr('is_returned') | list %}
    {% if completed %}
    <div class="panel-title" style="margin-top:1.5rem; font-size:1rem;">✅ Повернені</div>
    {% for record in completed %}
    <div class="rental-item" style="opacity:0.5;">
      <div>
        <div style="font-size:0.8rem;">{{ book_map.get(record.book_id, '?') }}</div>
        <div style="font-size:0.7rem;">{{ reader_map.get(record.reader_id, '?') }}</div>
      </div>
      <div style="font-size:0.7rem;">{{ record.return_date.strftime('%d.%m.%Y') if record.return_date else '' }}</div>
    </div>
    {% endfor %}
    {% endif %}
  </div>
</div>
</body>
</html>
"""


@app.route("/")
def index():
    books = lib.catalog.get_all_books()
    readers = lib.readers.get_all_readers()
    rentals = lib.rentals.get_all_records()
    report = lib.get_status_report()
    book_map = {b.book_id: b.title for b in books}
    reader_map = {r.reader_id: r.name for r in readers}
    return render_template_string(HTML, books=books, readers=readers,
                                  rentals=rentals, report=report,
                                  book_map=book_map, reader_map=reader_map)


@app.route("/add_book", methods=["POST"])
def add_book():
    try:
        lib.catalog.add_book(
            title=request.form["title"],
            author=request.form["author"],
            genre=request.form.get("genre", ""),
            year=int(request.form.get("year") or 0),
        )
        posthog.capture(
            distinct_id="library_admin",
            event="book_added",
            properties={"book_title": request.form["title"],
                        "book_author": request.form["author"],
                        "book_genre": request.form.get("genre", "")})
        flash(f"Книгу «{request.form['title']}» додано до каталогу!", "success")
    except Exception as e:
        flash(f"Помилка: {e}", "error")
    return redirect(url_for("index"))


@app.route("/add_reader", methods=["POST"])
def add_reader():
    try:
        reader = lib.register_reader(
            name=request.form["name"],
            email=request.form["email"],
        )
        posthog.capture(
            distinct_id=f"reader_{reader.reader_id}",
            event="reader_registered",
            properties={"reader_name": reader.name, "reader_email": reader.email})
        flash(f"Читача «{request.form['name']}» зареєстровано!", "success")
    except Exception as e:
        flash(f"Помилка: {e}", "error")
    return redirect(url_for("index"))


@app.route("/rent", methods=["POST"])
def rent():
    try:
        book_id = int(request.form["book_id"])
        reader_id = int(request.form["reader_id"])
        book = lib.catalog.get_book(book_id)
        lib.rent_book(book_id, reader_id)
        posthog.capture(
            distinct_id=f"reader_{reader_id}",
            event="book_rented",
            properties={"book_title": book.title, "book_genre": book.genre,
                        "book_year": book.year, "book_id": book_id})
        flash(f"Книгу «{book.title}» видано читачу!", "success")
    except Exception as e:
        flash(f"Помилка: {e}", "error")
    return redirect(url_for("index"))


@app.route("/return", methods=["POST"])
def return_book():
    try:
        book_id = int(request.form["book_id"])
        book = lib.catalog.get_book(book_id)
        lib.return_book(book_id)
        posthog.capture(
            distinct_id="library_admin",
            event="book_returned",
            properties={"book_title": book.title, "book_id": book_id})
        flash(f"Книгу «{book.title}» повернено!", "success")
    except Exception as e:
        flash(f"Помилка: {e}", "error")
    return redirect(url_for("index"))


@app.route("/block", methods=["POST"])
def block():
    try:
        reader_id = int(request.form["reader_id"])
        reader = lib.readers.get_reader(reader_id)
        lib.readers.block_reader(reader_id)
        posthog.capture(distinct_id="library_admin", event="reader_blocked",
                        properties={"reader_name": reader.name})
        flash(f"Читача «{reader.name}» заблоковано.", "success")
    except Exception as e:
        flash(f"Помилка: {e}", "error")
    return redirect(url_for("index"))


@app.route("/unblock", methods=["POST"])
def unblock():
    try:
        reader_id = int(request.form["reader_id"])
        reader = lib.readers.get_reader(reader_id)
        lib.readers.unblock_reader(reader_id)
        posthog.capture(distinct_id="library_admin", event="reader_unblocked",
                        properties={"reader_name": reader.name})
        flash(f"Читача «{reader.name}» розблоковано.", "success")
    except Exception as e:
        flash(f"Помилка: {e}", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    print("🚀 Сервер запущено: http://localhost:5000")
    app.run(debug=True, port=5000)