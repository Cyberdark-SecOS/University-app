from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'clave_secreta'  # Asegúrate de cambiar esto por una clave segura en un entorno de producción
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('citas_medicas.html')

# ...

@app.route('/citas_medicas')
def citas_medicas():
    # Verificar si el usuario está autenticado antes de mostrar la página de citas
    if 'user_id' in session:
        return render_template('citas_medicas.html', username=session.get('username'))
    else:
        return redirect(url_for('login'))

# ...



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['contrasena']

        try:
            user = User.query.filter(or_(User.username == email, User.email == email),
                                      User.password == password).one()

            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        except NoResultFound:
            flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Verificar si el usuario está autenticado antes de mostrar el panel de control
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Eliminar la información del usuario de la sesión
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Agrega esta línea para imprimir información sobre el nuevo usuario
        print(f'Nuevo usuario registrado: {username}, {email}, {password}')

        return redirect(url_for('index'))

    return render_template('signup.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
