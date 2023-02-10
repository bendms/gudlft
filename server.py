import datetime
import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    """Return list of club"""
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def loadCompetitions():
    """Return list of competitions"""
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
     
def saveClubs(clubs):
    clubs_to_save_to_json = {"clubs" : []}
    [clubs_to_save_to_json["clubs"].append(i) for i in clubs]
    with open('clubs.json','w') as c:
        json.dump(clubs_to_save_to_json,c)
    print("saveClubs function is called with clubs:", clubs)

    
def saveCompetitions(competitions):
    competitions_to_save_to_json = {"competitions" : []}
    [competitions_to_save_to_json["competitions"].append(i) for i in competitions]
    with open('competitions.json','w') as comps:
        json.dump(competitions_to_save_to_json,comps)
    print("saveCompetitions function is called with competitions:", competitions)

app = Flask(__name__)
app.debug = True
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    """Login page when customer can put his e-mail address and views number of points for each clubs in JSON"""
    return render_template('index.html', clubs=clubs, competitions=competitions)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    """Main page show number of points for each club and past/next competitions save into JSON"""
    club_email = [club['email'] for club in clubs]
    connected_club = [club for club in clubs if club["email"] in request.form["email"]]
    if connected_club != []:
        return render_template('welcome.html', connected_club=connected_club[0], clubs=clubs, competitions=competitions)
    else:
        flash("Sorry, unable to log in to the app. Your email address is incorrect")
        return render_template('index.html', clubs=clubs, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    """Booking view when user can choose how many tickets he wants to buy"""
    try:
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        foundClub = [c for c in clubs if c['name'] == club][0]
    except:
        flash("Sorry, this competition or club does not exist")
        return render_template('welcome.html', connected_club=club, competitions=competitions, clubs=clubs)
    date_of_competition = datetime.datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
    today = datetime.datetime.today()
    if date_of_competition < today:
        flash("Sorry, this competition is in the past")
        return render_template('welcome.html', connected_club=foundClub, competitions=competitions, clubs=clubs) 
    elif int(foundClub['points']) < 1:
        flash("Sorry, you don't have enough points to book a place")
        return render_template('welcome.html', connected_club=foundClub, competitions=competitions, clubs=clubs)
    elif int(foundCompetition['numberOfPlaces']) < 1:
        flash("Sorry, there are no places left for this competition")
        return render_template('welcome.html', connected_club=foundClub, competitions=competitions, clubs=clubs)
    else:
        return render_template('booking.html',connected_club=foundClub,competition=foundCompetition)


 
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    """This view check is connected_club is able to buy tickets, not possible if more than 12 tickets or """
    connected_club = [club for club in clubs if club["name"] == request.form["club"]]
    club = [club for club in clubs if club["name"] in request.form["club"]]
    try:
        placesRequired = int(request.form['places'])
    except ValueError:
        print('Achat impossible car vous devez indiquer le nombre de place à acheter')
        flash('Achat impossible car vous devez indiquer le nombre de place à acheter')
        return render_template('welcome.html', connected_club=club[0], competitions=competitions, clubs=clubs)
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    places_customer_wants_to_buy = {'name':competition['name'], 'date':competition['date'], 'number':placesRequired}
    places_customer_already_bought = [places for places in connected_club[0]['places'] if places['name'] == competition['name']]
    if placesRequired>=12:
        print('Achat impossible car vous ne pouvez pas acheter plus de 12 places')
        flash('Achat impossible car vous ne pouvez pas acheter plus de 12 places')        
        return render_template('welcome.html', connected_club=club[0], competitions=competitions, clubs=clubs)
    elif placesRequired<=0 or placesRequired==ValueError:
        print('Achat impossible car vous ne pouvez pas acheter moins de 1 place')
        flash('Achat impossible car vous ne pouvez pas acheter moins de 1 place')
        return render_template('welcome.html', connected_club=club[0], competitions=competitions, clubs=clubs)
    elif int(connected_club[0]['points'])>=placesRequired and placesRequired<=int(competition['numberOfPlaces']):
        sum_of_places_bought_for_this_event = 0
        places_of_connected_club = connected_club[0]['places']
        for place in places_customer_already_bought:
            if place['name'] == competition['name']:
                sum_of_places_bought_for_this_event += int(place['number'])
        if sum_of_places_bought_for_this_event + placesRequired <= 12:
            if places_of_connected_club:
                for places in places_of_connected_club:
                    if places['name'] == competition['name']:
                        places['number'] = int(places['number'])+placesRequired
                        break
                else:
                    connected_club[0]['places'].append(places_customer_wants_to_buy)
            print("Achat autorisé")
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            competition['numberOfPlaces'] = str(competition['numberOfPlaces'])
            connected_club[0]['points'] = int(connected_club[0]['points'])-placesRequired
            connected_club[0]['points'] = str(connected_club[0]['points'])
            # saveClubs(clubs)
            # saveCompetitions(competitions)
            flash('Great-booking complete!')
            return render_template('welcome.html', connected_club=club[0], competitions=competitions, clubs=clubs)
        flash('Achat impossible car vous ne pouvez pas acheter plus de 12 places')        
        return render_template('welcome.html', connected_club=club[0], competitions=competitions, clubs=clubs)

@app.route('/logout')
def logout():
    """Logout view, rediction to login page"""
    return redirect(url_for('index'))