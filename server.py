import datetime
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
     
def saveClubs(clubs):
    print("CLUBS", clubs)
    clubs_to_save_to_json = {"clubs" : []}
    [clubs_to_save_to_json["clubs"].append(i) for i in clubs]
    with open('clubs.json','w') as c:
        json.dump(clubs_to_save_to_json,c)
    
def saveCompetitions(competitions):
    print("COMPETITIONS", competitions)
    competitions_to_save_to_json = {"competitions" : []}
    [competitions_to_save_to_json["competitions"].append(i) for i in competitions]
    with open('competitions.json','w') as comps:
        json.dump(competitions_to_save_to_json,comps)

app = Flask(__name__)
app.debug = True
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    print("REQUEST.FORM", request.form)
    print("REQUEST", request)
    print("REQUEST.FORM['email']", request.form['email'])
    print("REQUEST.FORM['email'][0]", request.form['email'][0])
    club_email = [club['email'] for club in clubs]
    print("club_email", club_email)
    print(request.form['email'])
    connected_club = [club for club in clubs if club["email"] == request.form["email"]]
    
    club = [club for club in clubs if club["email"] in request.form["email"]]

    print("clubs", clubs)
    print("connected_club", connected_club)
    # if connected_club != [] and request.form['email'] not in club_email:
    if connected_club != []:
        return render_template('welcome.html', connected_club=connected_club[0], clubs=clubs, club=club[0], competitions=competitions)
    else:
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    print("foundCompetition", foundCompetition)
    print("foundCompetition['date']", foundCompetition['date'])
    date_of_competition = datetime.datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
    today = datetime.datetime.today()
    print("today", today)
    if date_of_competition < today:
        flash("Sorry, this competition is in the past")
        return render_template('welcome.html', connected_club=foundClub, club=foundClub, competitions=competitions, clubs=clubs) 
    elif int(foundClub['points']) < 1:
        flash("Sorry, you don't have enough points to book a place")
        return render_template('welcome.html', connected_club=foundClub, club=foundClub, competitions=competitions, clubs=clubs)
    elif int(foundCompetition['numberOfPlaces']) < 1:
        flash("Sorry, there are no places left for this competition")
        return render_template('welcome.html', connected_club=foundClub, club=foundClub, competitions=competitions, clubs=clubs)
    else:
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

 
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    #TODO : faire une recherche avec request.form['name'] et renvoyer l'object connected_club
    print("=== REQUEST.FORM ===", request.form)
    print("=== REQUEST.FORM['name'] ===", request.form['club'])
    connected_club = [club for club in clubs if club["name"] == request.form["club"]]
    placesRequired = int(request.form['places'])
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    print("COMPETITION", competition)
    club = [club for club in clubs if club["name"] in request.form["club"]]
    print("CLUB", club)
    print("PLACESREQUIRED", placesRequired)
    print("CONNECTED_CLUB", connected_club[0])
    print("competition", competition)
    if placesRequired>=12:
        print('Achat impossible car vous ne pouvez pas acheter plus de 12 places')
        flash('Achat impossible car vous ne pouvez pas acheter plus de 12 places')        
        return render_template('welcome.html', connected_club=connected_club[0], club=club[0], competitions=competitions, clubs=clubs)
    elif placesRequired<=0:
        print('Achat impossible car vous ne pouvez pas acheter moins de 1 place')
        flash('Achat impossible car vous ne pouvez pas acheter moins de 1 place')
        return render_template('welcome.html', connected_club=connected_club[0], club=club[0], competitions=competitions, clubs=clubs)
    elif int(connected_club[0]['points'])>=placesRequired and placesRequired<=int(competition['numberOfPlaces']):
        print("Achat autorisé")
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        competition['numberOfPlaces'] = str(competition['numberOfPlaces'])
        connected_club[0]['points'] = int(connected_club[0]['points'])-placesRequired
        connected_club[0]['points'] = str(connected_club[0]['points'])
        saveClubs(clubs)
        saveCompetitions(competitions)
        flash('Great-booking complete!')
        return render_template('welcome.html', connected_club=connected_club[0], club=club[0], competitions=competitions, clubs=clubs)
    print("=== REQUEST.ARGS ===", request.args)
    print("=== REQUEST.values ===", request.values)
    print("=== REQUEST.FORM['EMAIL'] ===", request.form["email"])
    print("=== REQUEST.FORM[0][0] ===", request.form[0][0])
    connected_club = [club for club in clubs if club["name"] == request.form["club"]]
    

    # connected_club = [club for club in clubs if club["email"] in request.form["email"]][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    # placesRequired = int(request.form['places'])
    # competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    # flash('Great-booking complete!')
    return render_template('welcome.html', connected_club=connected_club, competitions=competitions, clubs=clubs)
    # return render_template('welcome.html', connected_club=connected_club, club=club, competitions=competitions)


# TODO: Add route for points display 


@app.route('/logout')
def logout():
    return redirect(url_for('index'))