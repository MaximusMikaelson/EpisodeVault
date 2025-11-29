# database.py
import sqlite3

DB_NAME = 'episodevault.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre TEXT,
        year INTEGER,
        seasons INTEGER,
        rating REAL
    )
    ''')
    conn.commit()
    conn.close()

def add_series(title, genre, year, seasons, rating):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO series (title, genre, year, seasons, rating)
    VALUES (?, ?, ?, ?, ?)
    ''', (title, genre, year, seasons, rating))
    conn.commit()
    conn.close()

def list_series():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM series')
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_series(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    keyword = f'%{keyword}%'
    cursor.execute('''
    SELECT * FROM series
    WHERE title LIKE ? OR genre LIKE ?
    ''', (keyword, keyword))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_rating(series_id, new_rating):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE series SET rating = ? WHERE id = ?
    ''', (new_rating, series_id))
    conn.commit()
    conn.close()

def delete_series(series_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM series WHERE id = ?', (series_id,))
    conn.commit()
    conn.close()

def search_series_filtered_python(keyword=None, genre=None, year_min=None, year_max=None, rating_min=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM series")
    rows = cursor.fetchall()
    conn.close()

    def match(s, pattern):
        return pattern in s.lower()

    results = []

    kw = keyword.lower() if keyword else None
    gen = genre.lower() if genre else None

    for row in rows:
        _id, title, g, year, seasons, rating = row
        if kw and not (kw in title.lower() or kw in g.lower()):
            continue
        if gen and gen != g.lower():
            continue
        if year_min and year < year_min:
            continue
        if year_max and year > year_max:
            continue
        if rating_min and rating < rating_min:
            continue
        results.append(row)

    return results
