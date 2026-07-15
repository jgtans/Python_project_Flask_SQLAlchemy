#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилитный скрипт для просмотра SQLite БД в браузере.
Читает var/flask.db, генерирует HTML с Bootstrap-таблицами.

Запуск:
  python view_db_tables.py
"""
from pathlib import Path
import sqlite3
import html
import webbrowser


def get_db_path():
    base = Path(__file__).parent
    db = base / 'var' / 'flask.db'
    return db


def fetch_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    return [r[0] for r in cur.fetchall()]


def fetch_table_data(conn, table, limit=500):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM '{table}' LIMIT {limit}")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    return cols, rows


def fetch_table_schema(conn, table):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info('{table}')")
    return cur.fetchall()


def render_html(db_path, tables_data):
    title = f"DB Viewer — {db_path.name}"
    parts = []
    parts.append("<!doctype html>")
    parts.append('<html lang="ru">')
    parts.append("<head>")
    parts.append('<meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    parts.append(f"<title>{html.escape(title)}</title>")
    parts.append('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">')
    parts.append("<style>body { background-color: #f8f9fa; } table { font-size: 0.9rem; }</style>")
    parts.append("</head>")
    parts.append("<body class=\"p-4\">")
    parts.append(f"<div class=\"container-fluid\">\n<h1 class=\"mb-4\">{html.escape(title)}</h1>")
    parts.append("<p class=\"text-muted\">Автоматически сгенерированный просмотр таблиц БД (максимум 500 строк на таблицу)</p>")

    for table, meta in tables_data.items():
        schema = meta['schema']
        cols = meta['columns']
        rows = meta['rows']

        parts.append(f"<section class=\"mb-5 card\">")
        parts.append(f"<div class=\"card-header bg-primary text-white\"><h3 class=\"mb-0\">📊 {html.escape(table)}</h3></div>")
        parts.append(f"<div class=\"card-body\">")

        # Schema
        parts.append("<h5 class=\"mt-3\">📋 Схема таблицы</h5>")
        parts.append('<div class="table-responsive">')
        parts.append('<table class="table table-sm table-bordered table-hover">')
        parts.append('<thead class="table-light"><tr><th>#</th><th>Поле</th><th>Тип</th><th>Not Null</th><th>Значение по умолчанию</th><th>PK</th></tr></thead>')
        parts.append('<tbody>')
        for col in schema:
            cid, name, ctype, notnull, dflt_value, pk = col
            parts.append(f"<tr><td>{cid}</td><td><code>{html.escape(str(name))}</code></td><td>{html.escape(str(ctype))}</td><td>{'✓' if notnull else ''}</td><td>{html.escape(str(dflt_value) if dflt_value is not None else '')}</td><td>{'✓' if pk else ''}</td></tr>")
        parts.append('</tbody></table></div>')

        # Data
        row_count = len(rows)
        parts.append(f'<h5 class="mt-4">📊 Данные ({row_count} строк)</h5>')
        parts.append('<div class="table-responsive">')
        parts.append('<table class="table table-sm table-striped table-bordered">')
        parts.append('<thead class="table-dark"><tr>')
        for c in cols:
            parts.append(f"<th>{html.escape(str(c))}</th>")
        parts.append('</tr></thead>')
        parts.append('<tbody>')
        if rows:
            for r in rows:
                parts.append('<tr>')
                for cell in r:
                    txt = '' if cell is None else str(cell)
                    if len(txt) > 100:
                        txt = txt[:100] + '...'
                    parts.append(f"<td>{html.escape(txt)}</td>")
                parts.append('</tr>')
        else:
            parts.append(f'<tr><td colspan="{len(cols)}" class="text-center text-muted"><em>Нет данных</em></td></tr>')
        parts.append('</tbody></table></div>')

        parts.append('</div></section>')

    parts.append('</div></body></html>')
    return '\n'.join(parts)


def main():
    db_path = get_db_path()
    if not db_path.exists():
        print(f"❌ Файл БД не найден: {db_path}")
        return

    try:
        conn = sqlite3.connect(str(db_path))
        tables = fetch_tables(conn)

        if not tables:
            print("⚠️  В БД нет таблиц.")
            conn.close()
            return

        print(f"✓ Найдено таблиц: {len(tables)} — {', '.join(tables)}")

        tables_data = {}
        for t in tables:
            schema = fetch_table_schema(conn, t)
            cols, rows = fetch_table_data(conn, t, limit=500)
            tables_data[t] = {'schema': schema, 'columns': cols, 'rows': rows}
            print(f"  — {t}: {len(rows)} строк, {len(cols)} колонок")

        html_text = render_html(db_path, tables_data)
        out = db_path.parent / 'db_view.html'
        out.write_text(html_text, encoding='utf-8')
        print(f"\n✓ HTML сохранён: {out}")

        try:
            webbrowser.open(f'file:///{out.resolve()}')
            print("✓ Открыли в браузере")
        except Exception as e:
            print(f"⚠️  Не удалось открыть браузер: {e}")
            print(f"   Откройте вручную: {out}")

        conn.close()
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == '__main__':
    main()

