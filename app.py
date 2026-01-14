from flask import Flask, render_template, request, redirect, url_for, session
from questions import questions

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session storage

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    username = request.form.get('username')
    if username:
        session['username'] = username
        session['score'] = 0
        return redirect(url_for('quiz'))
    return redirect(url_for('index'))

@app.route('/quiz')
def quiz():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    score = 0
    # Loop through questions to check answers
    for q in questions:
        # User answer key format: q-1, q-2, etc.
        user_answer = request.form.get(f"q-{q['id']}")
        if user_answer and user_answer.lower() == q['answer'].lower():
            score += 10 # 10 points per correct answer
    
    session['score'] = score
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('result.html', username=session['username'], score=session['score'], total_score=len(questions)*10)

if __name__ == '__main__':
    app.run(debug=True)
