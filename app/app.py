from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField,RadioField,widgets,SelectMultipleField
from wtforms.validators import InputRequired, Length, EqualTo
import hashlib
import bleach
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import os

app = Flask(__name__,template_folder='/opt/fantacc/templates')
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Database setup with SQLAlchemy (example with MariaDB)
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Define ORM class for players table
class Sede(Base):
    __tablename__ = 'sedi'
    id_sede = Column(Integer, primary_key=True)
    tag_sede = Column(String(20), nullable=False)
    full_name_sede = Column(String(100), nullable=False)
    logo_sede = Column(String(50))

class Bonus(Base):
    __tablename__ = 'bonus'
    id_bonus = Column(Integer, primary_key=True)
    description_bonus = Column(String(255), nullable=False)
    value_bonus = Column(Integer, nullable=False)

class Player(Base):
    __tablename__ = 'players'
    id_player = Column(Integer, primary_key=True)
    name_player = Column(String(100), nullable=False)
    sede_player = Column(Integer, ForeignKey('sedi.id_sede'))
    password_player = Column(String(64), nullable=False)
    team_player = Column(Integer, ForeignKey('teams.id_team'))
    
    sede = relationship("Sede")
    team = relationship("Team")

class Team(Base):
    __tablename__ = 'teams'
    id_team = Column(Integer, primary_key=True)
    name_team = Column(String(100), nullable=False)
    captain_team = Column(Integer, ForeignKey('sedi.id_sede'))
    uni2_team = Column(Integer, ForeignKey('sedi.id_sede'))
    uni3_team = Column(Integer, ForeignKey('sedi.id_sede'))
    uni4_team = Column(Integer, ForeignKey('sedi.id_sede'))
    uni5_team = Column(Integer, ForeignKey('sedi.id_sede'))

    captain = relationship("Sede", foreign_keys=[captain_team])
    uni2 = relationship("Sede", foreign_keys=[uni2_team])
    uni3 = relationship("Sede", foreign_keys=[uni3_team])
    uni4 = relationship("Sede", foreign_keys=[uni4_team])
    uni5 = relationship("Sede", foreign_keys=[uni5_team])

class Point(Base):
    __tablename__ = 'points'
    id_point = Column(Integer, primary_key=True)
    bonus_id_point = Column(Integer, ForeignKey('bonus.id_bonus'))
    sede_id_point = Column(Integer, ForeignKey('sedi.id_sede'))
    multiplier_point = Column(DECIMAL(5,2))

    bonus = relationship("Bonus")
    sede = relationship("Sede")

# WTForm for login
class LoginForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

# Filter function for Jinja to determine row color based on value
@app.template_filter('color_class')
def color_class(value):
    if value > 0:
        return 'table-success'
    elif value < 0:
        return 'table-danger'
    else:
        return ''

# WTForm for registration
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=6, message='Password must be at least 6 characters long'),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()])
    sede = RadioField('Scegli la tua sede', validators=[InputRequired()])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        session_db = Session()
        # Dynamically populate sede choices from database session_db.query(Sede).all()
        self.sede.choices = [(str(sede.id_sede), sede.full_name_sede,sede.logo_sede) for sede in session_db.query(Sede).all()]

class NewTeamForm(FlaskForm):
    name_team = StringField('Team Name', validators=[InputRequired(), Length(max=100)])
    universities = SelectMultipleField('Scegli le tue università',option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False),coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(NewTeamForm, self).__init__(*args, **kwargs)
        session_db = Session()
        # Dynamically populate sede choices from database session_db.query(Sede).all()
        sedi_list = session_db.query(Sede).all()
        self.universities.choices = [(str(sede.id_sede), sede.full_name_sede,sede.logo_sede) for sede in sedi_list if sede.id_sede != session['user_sede']]

class CaptainForm(FlaskForm):
    capitano = RadioField('Scegli il tuo capitano', validators=[InputRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(CaptainForm, self).__init__(*args, **kwargs)
        session_db = Session()
        # Dynamically populate sede choices from database session_db.query(Sede).all()
        sedi_list = session_db.query(Sede).all()
        self.capitano.choices = [(str(sede.id_sede), sede.full_name_sede,sede.logo_sede) for sede in sedi_list if sede.id_sede != session['user_sede']]

class MyForm(FlaskForm):
    options = SelectMultipleField('Choose Options', choices=[
        ('value1', 'Option 1'),
        ('value2', 'Option 2'),
        ('value3', 'Option 3'),
        ('value4', 'Option 4'),
        ('value5', 'Option 5'),
        ('value6', 'Option 6'),
        ('value7', 'Option 7'),
        ('value8', 'Option 8')
    ], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Submit')



# Sanitization function using bleach
def sanitize_input(input_str):
    # Allow only specific HTML tags and attributes as needed
    # Example: Allow <b> and <i> tags
    cleaned_input = bleach.clean(input_str, tags=[], attributes={})
    return cleaned_input.strip()

# Hashing function using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Hashing function using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Sanitize inputs
        name = sanitize_input(form.name.data)
        sede_id = int(form.sede.data)  # Convert selected sede to integer (assuming it's stored as str)
        
        # Hash password
        hashed_password = hash_password(form.password.data)
        
        # Save to database using SQLAlchemy
        try:
            session = Session()
            
            # Insert into players table
            insert_query = text("INSERT INTO players (name_player, sede_player, password_player) VALUES (:name, :sede_id, :hashed_password)")
            session.execute(insert_query, {'name': name, 'sede_id': sede_id, 'hashed_password': hashed_password})
            session.commit()
            
            flash(f'Registration successful for {name} at {form.sede.choices[int(form.sede.data)-1][1]}!', 'success')
            return redirect(url_for('register'))  # Redirect to registration page after successful registration
        
        except Exception as e:
            session.rollback()
            flash('Error occurred while registering. Please try again.', 'error')
            print(e)
        
        finally:
            session.close()
    
    return render_template('register.html', form=form)

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        
        try:
            session_db = Session()
            # Querying the database to find the user by name and password
            user = session_db.query(Player).filter_by(name_player=name, password_player=hash_password(password)).first()

            if user:
                # If user exists, store user information in session
                session['user_id'] = user.id_player
                session['user_name'] = user.name_player
                session['user_sede'] = user.sede_player
                flash('Login successful!', 'success')
                return redirect(url_for('index'))  # Redirect to index or dashboard page after login
            else:
                flash('Invalid username or password. Please try again.', 'error')

        except Exception as e:
            session_db.rollback()
            flash('Error occurred while logging in. Please try again.', 'error')
            print(e)

        finally:
            session_db.close()

    return render_template('login.html', form=form)

# Example route for index or dashboard page (to be added to app.py)
@app.route('/index')
def index():
    if 'user_id' in session:
        user_name = session['user_name']
        user_sede = session['user_sede']
        form = MyForm()
        if form.validate_on_submit():
            selected_options = form.options.data
            print(f'Selected options: {selected_options}')
        
        return render_template('index.html', user_name=user_name, user_sede=user_sede,form=form)
    else:
        return redirect(url_for('scoreboard'))  # Redirect to login page if user not logged in

# Example route for the scoreboard page (to be added to app.py)
@app.route('/scoreboard')
def scoreboard():
    if 'user_id' in session:
        user_name = session['user_name']
        user_sede = session['user_sede']
        return render_template('scoreboard.html', user_name=user_name, user_sede=user_sede)
    else:
        return redirect(url_for('login'))  # Redirect to login page if user not logged in

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Redirect to login page after logout

# Route for Team Management page
@app.route('/team', methods=['GET', 'POST'])
def team():
    try:
        session_db = Session()
        # Fetch current player's details
        player_id = session['user_id']
        player = session_db.query(Player).filter_by(id_player=player_id).first()
        # If player already has a team, redirect to team view page
        if player.team_player:
            team_id = player.team_player
            flash(team_id,"warning")
            session_db.close()
            return redirect(url_for('team_view', team_id=team_id))
        # Get list of sedi (venues) for team members selection
        # Populate choices for SelectFields in TeamForm
        form = NewTeamForm()
        if session.get('temp_set'):
            session['temp_set'] = False
            session['temp_name'] = None
            session['temp_team'] = None

        if form.validate_on_submit():
            if len(form.universities.data) != 5:
                flash('Il team deve essere composto da 5 università!', 'danger')
                session_db.close()
                return render_template('teams.html', form=form)
            
            if session["user_sede"] in form.universities.data:
                flash('Non puoi scegliere la tua sede!', 'danger')
                session_db.close()
                return render_template('teams.html', form=form)
            
            name = sanitize_input(form.name_team.data)
            if len(name.strip()) < 1:
                flash('Nome team non valido!', 'danger')
                session_db.close()
                return render_template('teams.html', form=form)\
            
            session['temp_set'] = True
            session['temp_name'] = form.name_team.data
            session['temp_team'] = form.universities.data
            return redirect(url_for('cap'))
    
        session_db.close()
        return render_template('teams.html', form=form)

    except Exception as e:
        flash('Error occurred while managing teams.', 'error')
        print(e.__str__())
        session['temp_set'] = False
        session['temp_name'] = None
        session['temp_team'] = None
        return redirect(url_for('index'))

@app.route('/cap', methods=['GET', 'POST'])
def cap():
    try:
        session_db = Session()
        player_id = session.get('user_id')
        player = session_db.query(Player).filter_by(id_player=player_id).first()

        if player.team_player:
            flash('Player already has a team', 'danger')
            team_id = player.team_player
            session_db.close()
            return redirect(url_for('team_view', team_id=team_id))

        captain_form = CaptainForm()

        if not session.get('temp_set'):
            return redirect(url_for('team'))

        if captain_form.validate_on_submit():
            session['temp_team'] = [x for x in session['temp_team'] if x !=captain_form.capitano.data]
            new_team = Team(
                name_team=session['temp_name'],
                captain_team=captain_form.capitano.data,
                uni2_team=session['temp_team'][0],
                uni3_team=session['temp_team'][1],
                uni4_team=session['temp_team'][2],
                uni5_team=session['temp_team'][3]
            )
            session_db.add(new_team)
            session_db.flush()
            player.team_player = new_team.id_team
            session_db.commit()
            new_team = session_db.merge(new_team)
            flash('Team created successfully', 'success')
            
            session_db.close()
            session['temp_set'] = False
            session['temp_name'] = None
            session['temp_team'] = None
            return redirect(url_for('team_view', team_id=new_team.id_team))

        # Add validation error messages
        if captain_form.errors:
            for field, errors in captain_form.errors.items():
                for error in errors:
                    flash(f"Error in {getattr(captain_form, field).label.text}: {error}", 'danger')

        sedi_list = session_db.query(Sede).all()

        if not session.get('temp_team'):
            return redirect(url_for('team'))

        captain_form.capitano.choices = [
            (str(sede.id_sede), sede.full_name_sede, sede.logo_sede)
            for sede in sedi_list if sede.id_sede in session['temp_team']
        ]

        return render_template('captain.html', form=captain_form)

    except Exception as e:
        flash('Error occurred while managing teams.', 'error')
        print(str(e), 'error')
        session['temp_set'] = False
        session['temp_name'] = None
        session['temp_team'] = None
        return redirect(url_for('index'))
    finally:
        session_db.close()

# Route for Team View page
@app.route('/teams/<int:team_id>')
def team_view(team_id):
    try:
        session_db = Session()
        flash(team_id)
        # Fetch team details
        team = session_db.query(Team).filter_by(id_team=team_id).first()
        flash(team,"secondary")
        return render_template('team_view.html', team=team)

    except Exception as e:
        flash('Error occurred while fetching team details.', 'error')
        print(e)
        return redirect(url_for('index'))
    finally:
        session_db.close()

# Route for Bonus page
@app.route('/bonus')
def bonus():
    try:
        session_db = Session()
        bonuses = session_db.query(Bonus).all()
        session_db.close()
        return render_template('bonus.html', bonuses=bonuses)

    except Exception as e:
        flash('Error occurred while fetching bonus data.', 'error')
        print(e)
        return redirect(url_for('index'))

# Route for Venues page
@app.route('/venues')
def venues():
    try:
        session_db = Session()
        # Query all sedi (venues)
        sedi = session_db.query(Sede).all()
        # Prepare data structure to store bonus details per sede
        venues_data = []
        # Iterate over each sede and find associated bonuses with calculated values
        for sede in sedi:
            bonuses = session_db.query(Point).filter_by(sede_id_point=sede.id_sede).all()
            bonuses_data = []

            for point in bonuses:
                calculated_value = point.bonus.value_bonus * point.multiplier_point
                bonuses_data.append({
                    'description': point.bonus.description_bonus,
                    'value': calculated_value
                })

            venues_data.append({
                'sede': sede,
                'bonuses': bonuses_data
            })
        return render_template('venues.html', venues_data=venues_data)

    except Exception as e:
        flash('Error occurred while fetching venues data.', 'error')
        print(e)
        return redirect(url_for('scoreboard'))
    finally:
        session_db.close()

if __name__ == '__main__':
    Base.metadata.create_all(engine)  # Create database tables based on Base metadata
    app.run(debug=True)
