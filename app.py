"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory
from forms import Search, AddPet, EditPet
from models import db, connect_db, Pet



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

# app.config['UPLOADED_IMAGES_DEST'] = 'static/images'
# images = UploadSet('images', IMAGES)
# configure_uploads(app,images)
# from flask_uploads import configure_uploads, IMAGES, UploadSet
# from werkzeug.utils import secure_filename, FileStorage

db.create_all()

@app.route('/')
def home():
    """homepage, displays a list of all the pets in \d pets"""
    form = Search()
    pets = Pet.query.order_by(Pet.id.desc()).all()
    return render_template('home.html', pets=pets, form=form)


@app.route('/pets', methods=("POST","GET"))
def search():
    """ The search by name return page the lists pets with the searched name """
    form = Search()

    if form.validate_on_submit():
        search = form.name.data
        pets = Pet.query.filter(Pet.name.like('%'+search+'%'))
        return render_template('search_results.html', pets=pets, form=form)
    else:
        pets = Pet.query.all()
        return redirect('/')

@app.route('/pets/<int:pet_id>', methods=("POST","GET"))
def pet_details(pet_id):
    """get  details on a particular pet"""
    pet = Pet.query.get(pet_id)
    editForm = EditPet()
    form=Search()
    if form.validate_on_submit():
        if editForm.photo_url.data != None and editForm.photo_url.data != '':
            pet.photo_url = editForm.photo_url.data
        if editForm.notes.data != None and editForm.notes.data != '':
            pet.notes = editForm.notes.data
        if editForm.available.data != None and editForm.available.data != '':
            pet.available = editForm.available.data
            if pet.available == False:
                flash(f'{pet.name} has been adopted!')
        db.session.commit()
        return redirect(f'/pets/{pet_id}')
    else:
        return render_template('pet_details.html', pet=pet, form=form, editForm=editForm)

@app.route('/add_pet', methods=("POST","GET"))
def add_pet():
    """the add a pet to the database form"""
    form = AddPet()

    if form.validate_on_submit():
        # if form.photo.data != None:
        #     pic = form.photo.data

        #     filename = images.save(pic)
        # else:
        #     pic = photo_url.field.data
        new_pet = Pet(name=form.name.data,species=form.species.data,photo_url=form.photo_url.data,age=form.age.data,notes=form.notes.data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f'{new_pet.name} has been added!')
        return redirect('/')

    else:
        return render_template('add_pet.html', form=form)

@app.route('/delete/<int:pet_id>', methods=["POST","GET"])
def delete(pet_id):
    """delete route"""
    pet = Pet.query.get(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return redirect('/')