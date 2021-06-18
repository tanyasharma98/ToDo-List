from enum import unique
from flask import Flask , render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.sqltypes import DateTime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///tanya.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Todo(db.Model):
    Sno = db.Column(db.Integer,unique=False, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    desc = db.Column(db.String(120), unique=False, nullable=False)
    date_set =db.Column(db.DateTime, default= datetime.utcnow)
   

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title= request.form['title']
        desc= request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    # Error Fixed
    """sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: todo.Sno
    [SQL: INSERT INTO todo ("Sno", title, "desc", date_set) VALUES (?, ?, ?, ?)]
    [parameters: (1, 'First Title', 'Do some work', '2021-06-17 19:48:58.695901')]
    (Background on this error at: http://sqlalche.me/e/14/gkpj)"""
    # todo.query.delete()
    
    allTodo = Todo.query.all()
    #you'll attempt to create the new user even though it already exists. you will just remove everything from User table.
    #Error Fixed
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'Checker'

@app.route('/delete/<int:Sno>',)
def delete(Sno):
    todo = Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
@app.route('/update/<int:Sno>', methods=['GET','POST'])
def update(Sno):
    if request.method=='POST':
        title= request.form['title']
        desc= request.form['desc']
        todo = Todo.query.filter_by(Sno=Sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(Sno=Sno).first()
    return render_template('update.html', todo=todo)


if __name__=="__main__":
    # app.run(debug=True, port=9000)
    app.run(debug=True)