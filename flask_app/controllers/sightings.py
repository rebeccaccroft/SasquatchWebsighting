
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

#RENDERED
@app.route('/add_new_sighting')
def add_new_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_sighting.html')

@app.route('/view_sighting/<int:id>/')
def view_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id

    }
    return render_template('view_sighting.html', one_sighting = Sighting.view_sighting(data), user = User.get_single_id)

@app.route('/edit_sighting/<int:id>/')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    return render_template("edit_sighting.html", one_sighting = Sighting.view_sighting(data))



#REDIRECTED
@app.route('/process_new_sighting', methods=['POST'])
def process_new_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'date_seen': request.form['date_seen'],
        'num_sasquatches':request.form['num_sasquatches'],
        'user_id':session['user_id']
    }
    Sighting.new_sighting(data)
    return redirect('/add_new_sighting')

@app.route('/process_edit/<int:id>', methods=['POST'])
def process_edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'location': request.form['location'],
        'what_happened': request.form['what_happened'],
        'date_seen': request.form['date_seen'],
        'num_sasquatches':request.form['num_sasquatches'],
        'id':  id
    }
    Sighting.edit_sighting(data)
    return redirect('/dashboard')


@app.route('/delete_sighting/<int:id>')
def delete_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id':  id
    }
    Sighting.delete_sighting(data)
    return redirect('/dashboard')
