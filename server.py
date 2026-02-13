import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def saveClubs():
    with open('clubs.json', 'w') as c:
        json.dump({'clubs': clubs}, c, indent=4)

def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def saveCompetitions():
    with open('competitions.json', 'w') as comps:
        json.dump({'competitions': competitions}, comps, indent=4)

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club_list = [club for club in clubs if club['email'] == request.form['email']]
    if not club_list:
        flash("Email invalide")
        return redirect(url_for('index'))
        #return render_template('error.html', message="Email invalide"), 500
        #return render_template('welcome.html', club=None, competitions=competitions)
    return render_template('welcome.html', club=club_list[0], competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        competition_date = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
        if competition_date < datetime.now():
            flash("Competition is past")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
            #return render_template('error.html', message="Competition is past"), 500
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    try: 
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    except IndexError:
        flash("Competition invalide")
        return render_template('welcome.html', club=None, competitions=competitions)

    try:
        club = [c for c in clubs if c['name'] == request.form['club']][0]
    except IndexError:
        flash("Club invalide")
        return render_template('welcome.html', club=None, competitions=competitions)

    placesRequired = int(request.form['places'])

    if placesRequired > int(club["points"]):
        flash("Not enough points")
        return render_template('welcome.html', club=club, competitions=competitions)


    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces'])-placesRequired)
    club["points"] = str(int(club["points"]) - placesRequired)
    saveClubs()
    saveCompetitions()

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))