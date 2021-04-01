from flask import Flask, request, make_response, redirect, render_template,session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import  FlaskForm
from wtforms.fields import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired
import unittest

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY']= '123115515'

listado = ['manzana', 'pera', 'naranja', 'banano']

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('enviar')

@app.cli.command()
def test ():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error= error)


@app.errorhandler(500)
def server_fail(error):
    return render_template('500.html', error= error)    

@app.route('/')
def index():
    dato = request.remote_addr

    response = make_response(redirect('/bienvenido'))
    session['user_ip']= dato
    return response

@app.route('/bienvenido', methods=['GET', 'POST'])
def hola():
    dato = session.get('user_ip')
    loginform = LoginForm() 
    username = session.get('username')
    info = {
        'user_ip':dato,
        'listado':listado,
        'login_form':loginform,
        'username':username
    }

    if loginform.validate_on_submit():
        username = loginform.username.data
        session['username'] = username
        flash('Usuario registrado exitosamente')
        return redirect(url_for('index'))    

    return render_template('hello.html',**info)


if __name__ == '__main__':
    app.run(debug=True)