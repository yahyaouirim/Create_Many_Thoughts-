from flask_app import app
from flask_app.models.Thought import Thought
from flask_app.models.User import User

from flask import request , render_template , session , redirect

@app.route('/thought/add-thought')
def add_thought():
    user = User.get_by_id({'id': session['user_id']})
    return render_template('dashboard.html', logged_user = user)

@app.route('/thought/create' , methods = ['POST'])
def create():
    data = request.form
    if Thought.validate_thought(data):
        Thought.create(data)
    return redirect('/dashboard')

@app.route('/like/<int:id>')
def like(id):
    data = {'id': id}
    thought = Thought.get_by_id(data)
    thought.like_thought()
    return redirect('/dashboard')

@app.route('/unlike/<int:id>')
def unlike(id):
    data = {'id': id}
    thought = Thought.get_by_id(data)
    thought.unlike_thought()
    return redirect("/dashboard")

@app.route('/thought/<int:id>/delete')
def delete(id):
    data = {'id': id}
    thought = Thought.get_by_id(data)
    Thought.delete(data)
    
    return redirect('/dashboard')

@app.route('/thought/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_thoughts.html",user=User.get_by_id(data),logged_user=User.get_by_id(user_data),thoughts=Thought.get_all())
