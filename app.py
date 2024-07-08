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




def get_max_score():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(score) FROM results')
    max_score = cursor.fetchone()[0]
    conn.close()
    return max_score if max_score is not None else 0

@app.route('/')
def index():
    max_score = get_max_score()
    return render_template('index.html', max_score=max_score)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        answers = {
            'first': request.form.get('first'),
            'second': request.form.get('second'),
            'third': request.form.get('third')
        }

        correct_answers = {
            'first': '1',
            'second': '2',
            'third': '3'
        }

        # Calculate the score
        score = sum(1 for key in answers if answers[key] == correct_answers[key])

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
    best_score = get_max_score()
    return render_template('result.html', name=name, score=score, best_score=best_score)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)