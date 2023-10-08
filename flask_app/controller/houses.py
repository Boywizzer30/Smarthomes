from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models.user import Users

from flask_app.models.house import Houses

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/welcomepage')
def all_users_houses():
    print(session)
    if 'user_id' not in session:
        flash("you need to log in to access that page")
        return redirect('/')
    user = Users.get_one(session['user_id'])
    house = Houses.get_all_houses()
    return render_template("welcome.html", user = user, house = house, smart= Users.get_all(), homes= Houses.get_all_houses())


@app.route('/create_house')
def house():
    return render_template('new.html')

@app.route('/create_house', methods=['POST'])
def create():
    print(session)
    if not Houses.houses_validator(request.form):
        return redirect('/create_house')
    data = {
        'house_type' : request.form ['house_type'],
        'price' : request.form ['price'],
        'address' : request.form ['address'],
        'square_foot' : request.form ['square_foot'],
        'bed' : request.form['bed'],
        'bath' : request.form ['bath'],
        'year_built' : request.form ['year_built'],
        'listing_date' : request.form  ['listing_date'],
        'smartdevice' : request.form['smartdevice'],
        'user_id' : session['user_id'],
    }
    Houses.create_homes(data)
    return redirect('/welcomepage')

@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        flash("you need to log in to access that page")
        return redirect('/')
    home = Houses.get_one_house(id)
    print(id)
    return render_template('show.html', home = home, houses=Users.get_one(id))

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        flash("you need to log in to access that page")
        return redirect('/')
    home = Houses.get_one_house(id)
    print(id)
    return render_template('edit.html', home = home, homes=Users.get_one(id))

@app.route('/edit/<int:id>',methods=['POST'])
def update(id):
    if not Houses.houses_validator(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'house_type' : request.form ['house_type'],
        'price' : request.form ['price'],
        'address' : request.form ['address'],
        'square_foot' : request.form ['square_foot'],
        'bed' : request.form['bed'],
        'bath' : request.form ['bath'],
        'year_built' : request.form ['year_built'],
        'listing_date' : request.form  ['listing_date'],
        'smartdevice' : request.form['smartdevice'],
        'id':id
    }
    Houses.update_house(data)
    return redirect('/welcomepage')

@app.route('/delete/<int:id>')
def delete(id):
    Houses.delete_house(id)
    return redirect ('/welcomepage')

@app.route('/purchase/<int:id>')
def purchase(id):
    Houses.purchase_house(id)
    return redirect ('/welcomepage')