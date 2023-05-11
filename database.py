import sqlite3

def database_call(native, automate, professional, score, abbreviation):
    # Підключення до бази даних (якщо база даних не існує, вона буде створена)
    conn = sqlite3.connect('mydatabase.db')

    # Cтворення курсора
    cursor = conn.cursor()

    # Виконання SQL-запиту для створення таблиці
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS translator (id INTEGER PRIMARY KEY, native_text TEXT,automate_translation ,'
        'professional_translation TEXT, quality_score REAL, abbreviation TEXT)')

    # Виконання SQL-запиту для вставки даних
    cursor.execute(
        'INSERT INTO translator (native_text, automate_translation, professional_translation, quality_score, abbreviation) '
        'VALUES (?, ?, ?, ?, ?)', (native, automate, professional, score, abbreviation))

    # Застосування змін до бази даних
    conn.commit()

    # Закриття з'єднання
    conn.close()

def get_data(key):
    # Підключення до бази даних
    conn = sqlite3.connect('mydatabase.db')

    # Створення курсора
    cursor = conn.cursor()

    # Виконання SQL-запиту для читання даних за PRIMARY KEY
    cursor.execute('SELECT * FROM translator WHERE id = ?', (key,))

    # Отримання одного запису з результату запиту
    row = cursor.fetchone()

    # Перевірка, чи знайдено запис
    if row:
        # Закриття з'єднання
        conn.close()
        return row
    else:
        # Закриття з'єднання
        conn.close()
        return "Error."
