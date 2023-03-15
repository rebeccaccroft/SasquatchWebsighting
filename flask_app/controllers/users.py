
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask import flash
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


#RENDERED ROUTES
@app.route('/')
def main():
    return render_template('login_reg.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html',logged_in_user = User.get_single_id(data),  all_sightings = Sighting.all_sightings_of_user())

# #REDIRECTED ROUTES


#REGISTER
@app.route('/register_user', methods=['POST'])
def register_user():
    if not User.validate_register(request.form):
        return redirect('/')
        
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email_register'],
        'password' : bcrypt.generate_password_hash(request.form['password_register']).decode('utf-8')
    }
    User.create_user(data)

    flash('You are now registered. Please log in.')
        # pick one login for
    return redirect('/')

#LOGIN
@app.route('/login', methods=['POST'])
def login():
    
    if not User.validate_login(request.form):
        return redirect ('/')

    data = {
        'email': request.form['email']
    }

    user = User.get_single_email(data)
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect ('/dashboard')
    
#LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 
