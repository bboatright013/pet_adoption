from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, FileField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange

class Search(FlaskForm):
    """Form for navbar Search"""
    name = StringField("Pet Name",render_kw={"placeholder": "Pet's Name"})

class AddPet(FlaskForm):
    """add pet to the database"""

    name = StringField("Pet Name",validators=[InputRequired()], render_kw={"placeholder": "Pet Name"})
    species = StringField("Species",validators=[InputRequired(),AnyOf(['dog','cat','porcupine'])],render_kw={"placeholder": "Species"})
    photo_url = StringField("Pet Pic",validators=[Optional(),URL(False,'Please Enter A Valid URL')],render_kw={"placeholder": "URL path"})
    # photo = FileField("Photo", validators=[Optional()])
    age = IntegerField("Age",validators=[Optional(),NumberRange(min=0,max=30)],render_kw={"placeholder": "Age as a whole number"})
    notes = StringField("Notes",validators=[Optional()],render_kw={"placeholder": "add notes"})


class EditPet(FlaskForm):
    """edit pet in the database"""
    photo_url = StringField("Pet Pic",validators=[Optional(),URL(False,'Please Enter A Valid URL')],render_kw={"placeholder": "URL path"})
    notes = StringField("Notes",validators=[Optional()],render_kw={"placeholder": "add notes"})
    available = BooleanField("Availability",validators=[Optional()],default="checked" )