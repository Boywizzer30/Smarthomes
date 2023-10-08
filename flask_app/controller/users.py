from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models.user import Users

from flask_app.models import house

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def splash():
    return render_template("splashpage.html")



@app.route('/register_user', methods=['POST'])
def register_user():
    print(session)
    if not Users.user_validator(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user = Users.create_users(data)
    session['user_id'] = user
    return redirect('/login')

@app.route('/login')
def display_users():
    print(session)
    if 'user_id' not in session:
        flash("you need to log in to access that page")
        return redirect('/')
    user = Users.get_one(session['user_id'])
    print(user.first_name)
    return render_template("login.html", user = user, house= house.Houses.get_all_houses())

@app.route('/login1')
def work():
    return render_template('login.html')

@app.route('/register_user')
def register():
    return render_template("registration.html")

@app.route('/login', methods=['POST'])
def login_users():
    user_in_DB = Users.get_user_by_email(request.form['email'])
    if not user_in_DB:
        flash("Invalid email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_DB.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_DB.id
    return redirect('/welcomepage')


@app.route("/clear_session")
def clear_session():
    session.clear()
    return redirect('/')