import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from sqlalchemy.sql import func

#  Application Initialization 
app = Flask(__name__)

#  Configuration 
# Using SQLite for simplicity
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'a_very_simple_secret_key_for_this_example' # Replace with a real key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Database Initialization 
db = SQLAlchemy(app)

#  Database Model 
class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), index=True, nullable=False)
    term_in_months = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<WorkExperience {self.company} - {self.term_in_months} months>'

#  Form Definition 
class WorkExperienceForm(FlaskForm):
    company = StringField('Наименование места работы', validators=[DataRequired()])
    term_in_months = IntegerField('Срок работы в месяцах', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Добавить запись')

#  Routes 
@app.route('/', methods=['GET', 'POST'])
def index():
    form = WorkExperienceForm()
    if form.validate_on_submit():
        new_entry = WorkExperience(
            company=form.company.data,
            term_in_months=form.term_in_months.data
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))

    all_entries = WorkExperience.query.all()
    total_experience = db.session.query(func.sum(WorkExperience.term_in_months)).scalar() or 0

    return render_template('index.html', form=form, all_entries=all_entries, total_experience=total_experience)

#  Running the Application 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)