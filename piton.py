from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'  # Изменили имя базы данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):  # Изменили имя класса
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)  # Изменили поле на "name"
    location = db.Column(db.String(100), nullable=False)  # Добавили поле "location"
    description = db.Column(db.Text, nullable=False)  # Изменили поле на "description"
    organizer = db.Column(db.String(100), nullable=False)  # Поле осталось, но теперь для организатора
    contact_phone = db.Column(db.String(20), nullable=False)  # Поле осталось, но теперь для контактного номера
    status = db.Column(db.String(50), default='Планируется')  # Изменили на "Планируется"

@app.route('/')
def index():
    events = Event.query.all()  # Изменили имя переменной на "events"
    return render_template('index.html', events=events)  # Изменили имя переменной в шаблоне

@app.route('/add', methods=['GET', 'POST'])
def add_events():  # Изменили имя функции
    if request.method == 'POST':
        new_event = Event(  # Изменили имя переменной на "new_event"
            name=request.form['name'],
            location=request.form['location'],
            description=request.form['description'],
            organizer=request.form['organizer'],
            contact_phone=request.form['contact_phone'],
            status=request.form['status']
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_events.html')  # Изменили имя шаблона

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)