from flask import Flask, render_template, redirect, url_for, flash, session, request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField,RadioField,widgets,SelectMultipleField,IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
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

class Rickrolls(Base):
    __tablename__ = 'rickrolls'
    id_rr = Column(Integer, primary_key=True)
    user_rr = Column(Integer, ForeignKey('players.id_player'))
    user = relationship("Player")

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

def not_zero(form, field):
    if field.data == "0":
        raise ValidationError("Field cannot be zero.")

class PointsForm(FlaskForm):
    bonus = SelectField("Select Bonus",validators=[InputRequired()])
    multiplier = IntegerField('Insert Multiplier', validators=[InputRequired(), not_zero])
    sedi = SelectMultipleField('Scegli le sedi',option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False),coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PointsForm, self).__init__(*args, **kwargs)
        session_db = Session()
        # Dynamically populate sede choices from database session_db.query(Sede).all()
        self.sedi.choices = [(str(sede.id_sede), sede.tag_sede,sede.logo_sede) for sede in session_db.query(Sede).all() ]
        self.bonus.choices = [(str(bonus.id_bonus),bonus.description_bonus) for bonus in session_db.query(Bonus).all()]


# Sanitization function using bleach
def sanitize_input(input_str):
    # Allow only specific HTML tags and attributes as needed
    # Example: Allow <b> and <i> tags
    cleaned_input = bleach.clean(input_str, tags=[], attributes={})
    return cleaned_input.strip()

# Hashing function using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        redirect(url_for('profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Sanitize inputs
        name = sanitize_input(form.name.data)
        sede_id = int(form.sede.data)  # Convert selected sede to integer (assuming it's stored as str)
        
        # Hash password
        hashed_password = hash_password(form.password.data)
        
        # Save to database using SQLAlchemy
        try:
            session_db = Session()
            # Insert into players table
            new_player = Player(
                name_player=name,
                sede_player=sede_id,
                password_player=hashed_password
            )
            session_db.add(new_player)
            session_db.flush()
            session_db.commit()
            new_player = session_db.merge(new_player)
            
            flash(f'Registration successful for {name} at {new_player.sede.tag_sede}!', 'success')
            return redirect(url_for('login'))  # Redirect to registration page after successful registration
        
        except Exception as e:
            session_db.rollback()
            flash('Error occurred while registering. Please try again.', 'danger')
            print(str(e))
            flash(str(e))
        finally:
            session_db.close()
    
    return render_template('register.html', form=form, session=session)

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        redirect(url_for('profile'))
        
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
                resp = redirect(url_for('index'))  # Redirect to index or dashboard page after login
                resp.set_cookie('is_admin','0')
                return resp
            else:
                flash('Invalid username or password. Please try again.', 'danger')

        except Exception as e:
            session_db.rollback()
            flash('Error occurred while logging in. Please try again.', 'danger')
            print(str(e))

        finally:
            session_db.close()

    return render_template('login.html', form=form, session=session)

# Example route for index or dashboard page (to be added to app.py)
@app.route('/index')
@app.route('/')
def index():
    if request.cookies.get('is_admin') != '0':
        player_id = session.get('user_id')
        if player_id:
            session_db = Session()
            # Insert into players table
            new_rr = Player(
                user_rr=player_id
            )
            session_db.add(new_rr)
            session_db.flush()
            session_db.commit()
            player = session_db.query(Player).filter_by(id_player=player_id).first()
        resp = redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUXbmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXA%3D')  # Redirect to index or dashboard page after login
        resp.set_cookie('is_admin','0')
        return resp
    resp = make_response(render_template('index.html',session=session))
    resp.set_cookie('is_admin','0')
    return resp

# Example route for the scoreboard page (to be added to app.py)
@app.route('/scoreboard')
def scoreboard():
    try:
        session_db = Session()
        # Fetch team details
        teams = session_db.query(Team).all()
        return render_template('scoreboard.html', teams=teams, session=session)
    except Exception as e:
        flash('Error occurred while fetching scoreboard.', 'danger')
        print(str(e))
        return redirect(url_for('index'))
    finally:
        session_db.close()


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
                return render_template('teams.html', form=form, session=session)
            
            if session["user_sede"] in form.universities.data:
                flash('Non puoi scegliere la tua sede!', 'danger')
                return render_template('teams.html', form=form, session=session)
            
            name = sanitize_input(form.name_team.data)
            if len(name.strip()) < 1:
                flash('Nome team non valido!', 'danger')
                return render_template('teams.html', form=form, session=session)\
            
            session['temp_set'] = True
            session['temp_name'] = form.name_team.data
            session['temp_team'] = form.universities.data
            return redirect(url_for('cap'))
        return render_template('teams.html', form=form, session=session)

    except Exception as e:
        flash('Error occurred while managing teams.', 'danger')
        print(e.__str__())
        session['temp_set'] = False
        session['temp_name'] = None
        session['temp_team'] = None
        return redirect(url_for('index'))
    finally:
        session_db.close()

@app.route('/cap', methods=['GET', 'POST'])
def cap():
    try:
        session_db = Session()
        player_id = session.get('user_id')
        player = session_db.query(Player).filter_by(id_player=player_id).first()

        if player.team_player:
            flash('Player already has a team', 'danger')
            team_id = player.team_player
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

        return render_template('captain.html', form=captain_form, session=session)

    except Exception as e:
        flash('Error occurred while managing teams.', 'danger')
        print(str(e), 'danger')
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
        # Fetch team details
        team = session_db.query(Team).filter_by(id_team=team_id).first()
        owner = session_db.query(Player).filter_by(team_player=team_id).first()

        return render_template('team_view.html', team=team, owner=owner, session=session)

    except Exception as e:
        flash('Error occurred while fetching team details.', 'danger')
        print(str(e))
        return redirect(url_for('index'))
    finally:
        session_db.close()

@app.template_filter('get_uni_score')
def get_uni_score(sede_id):
    try:
        session_db = Session()
        if session_db.query(Point).filter_by(sede_id_point=sede_id).count() == 0:
            return 0
        points = session_db.query(Point).filter_by(sede_id_point=sede_id).all()
        if not points:
            return 0
        return sum([point.bonus.value_bonus*point.multiplier_point for point in points])
    except Exception as e:
        print(str(e))
        return 0xbadc0ffe
    finally:
        session_db.close()

@app.template_filter('get_team_score')
def get_team_score(team_id):
    try:
        session_db = Session()
        team = session_db.query(Team).filter_by(id_team=team_id).first()
        if not team:
            return 0
        return get_uni_score(team.captain_team)*2 + get_uni_score(team.uni2_team) + get_uni_score(team.uni3_team) + get_uni_score(team.uni4_team) + get_uni_score(team.uni5_team)
    except Exception as e:
        print(str(e))
        return 0xbadc0ffe
    finally:
        session_db.close()

# Route for Team View page
@app.route('/profile')
def profile():
    if not session.get('user_id'):
        redirect(url_for('login'))
    try:
        session_db = Session()
        player_id = session.get('user_id')
        player = session_db.query(Player).filter_by(id_player=player_id).first()

        if not player.team_player:
            flash('Player doesn\'t have a team', 'danger')
            return redirect(url_for('team'))
        
        team_id = player.team_player

        # Fetch team details
        team = session_db.query(Team).filter_by(id_team=team_id).first()
        return render_template('profile.html', team=team, session=session,player=player)

    except Exception as e:
        flash('Error occurred while fetching team details.', 'danger')
        print(str(e))
        return redirect(url_for('index'))
    finally:
        session_db.close()

# Route for Bonus page
@app.route('/bonus')
def bonus():
    try:
        session_db = Session()
        bonuses = session_db.query(Bonus).all()
        return render_template('bonus.html', bonuses=bonuses, session=session)

    except Exception as e:
        flash('Error occurred while fetching bonus data.', 'danger')
        print(str(e))
        return redirect(url_for('index'))
    finally:
        session_db.close()


@app.route('/points/<key>', methods=['GET', 'POST'])
def points(key):
    if hash_password(key) != "68490bd6a741e44734e2c96f36093dd1f3dd4cb13cc6ad4b1070e618a482aa4a":
        return redirect(url_for("index"))
    
    form = PointsForm()
    if form.validate_on_submit():
        bonus = form.bonus.data
        multiplier = int(form.multiplier.data)
        sedi = form.sedi.data
        
        try:
            for sede in sedi:
                session_db = Session()
                # Querying the database to find the user by name and password
                newPoint = Point(
                    bonus_id_point = bonus,
                    multiplier_point = multiplier,
                    sede_id_point=sede
                )
                session_db.add(newPoint)
                session_db.flush()
                session_db.commit()

        except Exception as e:
            session_db.rollback()
            flash('Error occurred while logging in. Please try again.', 'danger')
            print(str(e))

        finally:
            session_db.close()

    return render_template('points.html', form=form, session=session)
    

@app.route('/logs')
def logs():
    try:
        session_db = Session()
        points = session_db.query(Point).all()
        return render_template('logs.html', points=points, session=session)

    except Exception as e:
        flash('Error occurred while fetching points data.', 'danger')
        print(str(e))
        return redirect(url_for('index'))
    finally:
        session_db.close()

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
        return render_template('venues.html', venues_data=venues_data, session=session)

    except Exception as e:
        flash('Error occurred while fetching venues data.', 'danger')
        print(str(e))
        return redirect(url_for('scoreboard'))
    finally:
        session_db.close()

if __name__ == '__main__':
    Base.metadata.create_all(engine)  # Create database tables based on Base metadata
    app.run(debug=True)
