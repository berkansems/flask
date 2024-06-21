from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Veritabanı bağlantısı ve tablo oluşturma
def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                            name TEXT,
                            score INTEGER
                        )''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        animal = request.form['animal']
        hobbies = request.form['hobbies']

        # Skor hesaplama (örneğin)
        score = 0
        if color == 'Blue':
            score += 1
        if animal == 'Cat':
            score += 1

        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO results (name, score) VALUES (?, ?)", (name, score))
        conn.commit()
        conn.close()

        session['name'] = name
        session['score'] = score

        return redirect(url_for('result'))


@app.route('/result')
def result():
    name = session.get('name', None)
    score = session.get('score', None)
    return render_template('result.html', name=name, score=score)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)