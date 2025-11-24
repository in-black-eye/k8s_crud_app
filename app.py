from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'notes.db'

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Получить все заметки
def get_notes():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Позволяет обращаться по имени столбца
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    conn.close()
    return notes

# Получить заметку по ID
def get_note(note_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()
    return note

# Добавить новую заметку
def add_note(title, content):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

# Обновить заметку
def update_note(note_id, title, content):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))
    conn.commit()
    conn.close()

# Удалить заметку
def delete_note(note_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

# Главная страница — список заметок
@app.route('/')
def index():
    notes = get_notes()
    return render_template('index.html', notes=notes)

# Страница создания новой заметки
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        add_note(title, content)
        return redirect(url_for('index'))
    return render_template('edit.html', note=None)

# Страница редактирования заметки
@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit(note_id):
    note = get_note(note_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        update_note(note_id, title, content)
        return redirect(url_for('index'))
    return render_template('edit.html', note=note)

# Удаление заметки
@app.route('/delete/<int:note_id>')
def delete(note_id):
    delete_note(note_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)