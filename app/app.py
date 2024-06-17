from flask import Flask, render_template, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField
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
    sede = SelectField('Sede', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=6, message='Password must be at least 6 characters long'),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        session_db = Session()
        # Dynamically populate sede choices from database session_db.query(Sede).all()
        self.sede.choices = [(str(sede.id_sede), sede.full_name_sede) for sede in session_db.query(Sede).all()]

# Form for team creation
class TeamForm(FlaskForm):
    name_team = StringField('Team Name', validators=[InputRequired(), Length(max=100)])
    captain_team = SelectField('Captain', coerce=int)
    uni2_team = SelectField('Member 2', coerce=int)
    uni3_team = SelectField('Member 3', coerce=int)
    uni4_team = SelectField('Member 4', coerce=int)
    uni5_team = SelectField('Member 5', coerce=int)
    submit = SubmitField('Create Team')

# Sanitization function using bleach
def sanitize_input(input_str):
    # Allow only specific HTML tags and attributes as needed
    # Example: Allow <b> and <i> tags
    cleaned_input = bleach.clean(input_str, tags=['b', 'i'], attributes={})
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
            
            flash(f'Registration successful for {name} at {form.sede.choices[int(form.sede.data)][1]}!', 'success')
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
        return render_template('index.html', user_name=user_name, user_sede=user_sede)
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
@app.route('/teams', methods=['GET', 'POST'])
def teams():
    try:
        session_db = Session()

        # Fetch current player's details
        player_id = session['user_id']
        player = session_db.query(Player).filter_by(id_player=player_id).first()

        # If player already has a team, redirect to team view page
        if player.team_player:
            team_id = player.team_player
            session_db.close()
            return redirect(url_for('team_view', team_id=team_id))

        # Get list of sedi (venues) for team members selection
        sedi_list = session_db.query(Sede).all()

        # Populate choices for SelectFields in TeamForm
        form = TeamForm()
        form.captain_team.choices = [(sede.id_sede, sede.full_name_sede) for sede in sedi_list]
        form.uni2_team.choices = [(sede.id_sede, sede.full_name_sede) for sede in sedi_list]
        form.uni3_team.choices = [(sede.id_sede, sede.full_name_sede) for sede in sedi_list]
        form.uni4_team.choices = [(sede.id_sede, sede.full_name_sede) for sede in sedi_list]
        form.uni5_team.choices = [(sede.id_sede, sede.full_name_sede) for sede in sedi_list]

        if form.validate_on_submit():
            # Create new team and update player's team
            new_team = Team(
                name_team=form.name_team.data,
                captain_team=form.captain_team.data,
                uni2_team=form.uni2_team.data,
                uni3_team=form.uni3_team.data,
                uni4_team=form.uni4_team.data,
                uni5_team=form.uni5_team.data
            )
            session_db.add(new_team)
            session_db.flush()  # Flush to get the new team id

            # Update player's team
            player.team_player = new_team.id_team
            session_db.commit()

            flash('Team created successfully!', 'success')
            session_db.close()

            return redirect(url_for('team_view', team_id=new_team.id_team))

        session_db.close()
        return render_template('teams.html', form=form)

    except Exception as e:
        flash('Error occurred while managing teams.', 'error')
        print(e)
        return redirect(url_for('index'))

# Route for Team View page
@app.route('/teams/<int:team_id>')
def team_view(team_id):
    try:
        session_db = Session()

        # Fetch team details
        team = session_db.query(Team).filter_by(id_team=team_id).first()

        session_db.close()

        return render_template('team_view.html', team=team)

    except Exception as e:
        flash('Error occurred while fetching team details.', 'error')
        print(e)
        return redirect(url_for('index'))

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

        session_db.close()

        return render_template('venues.html', venues_data=venues_data)

    except Exception as e:
        flash('Error occurred while fetching venues data.', 'error')
        print(e)
        return redirect(url_for('scoreboard'))

if __name__ == '__main__':
    Base.metadata.create_all(engine)  # Create database tables based on Base metadata
    app.run(debug=True)
