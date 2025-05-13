import wtforms
from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.secret_key = 'some secret string'
bootstrap = Bootstrap5(app)

def my_length_check(form, field):
    if len(field.data) < 5:
        raise ValidationError('Field must more than 5 characters')

class MyForm(FlaskForm):
    email = StringField(label='email', validators=[
        wtforms.validators.Email(message='this field must contains "@" and . (must me an email address)'),
        DataRequired(), ])
    password = PasswordField(label='password', validators=[DataRequired(), my_length_check])
    submit = SubmitField(label='Log in')


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()

    if form.validate_on_submit():
        if form.email.data == "admin@admin.com" and form.password.data =="12345678":
            return redirect('/success')
        else:
            return redirect('/denied')

    return render_template('login.html', form=form)

@app.route('/denied')
def denied():
    return render_template('denied.html')

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
