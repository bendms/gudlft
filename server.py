import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club_email = [club['email'] for club in clubs]
    print("club_email", club_email)
    print(request.form['email'])
    connected_club = [club for club in clubs if club["email"] in request.form["email"]][0]
    club = [club for club in clubs if club["email"] in request.form["email"]]

    print("clubs", clubs)
    print("connected_club", connected_club)
    if connected_club != []:
        return render_template('welcome.html', connected_club=connected_club, clubs=clubs, club=club[0], competitions=competitions)
    else:
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    #TODO : faire une recherche avec request.form['name'] et renvoyer l'object connected_club
    print("REQUEST", request.form)
    connected_club = [club for club in clubs if club["email"] in request.form["email"]][0]
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', connected_club=connected_club, club=club, competitions=competitions)


# TODO: Add route for points display 


@app.route('/logout')
def logout():
    return redirect(url_for('index'))