from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

#Database Models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)
    

@app.route('/')
def index():
    todo_list = Todo.query.all()
    total_todo = Todo.query.count()
    completed_todo = Todo.query.filter_by(complete=True).count()
    uncompleted = total_todo - completed_todo
    return render_template('dashboard/index.html', **locals())

@app.route('/add_tasks', methods=['POST'])
def add_tasks():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add_tasks(new_todo)
    db.session.commit() 
    return redirect(url_for('index'))

@app.route('/update_tasks/<int:id>')
def update_tasks(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_tasks/<int:id>')
def delete_tasks(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete_tasks(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
