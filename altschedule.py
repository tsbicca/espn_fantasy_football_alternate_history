from data_utils import *
from config import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_bootstrap3 import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/', methods=['POST'])
def league_url_submission():
  url = request.form['leagueURL']
  try:
    id = leagueID_from_url(url)
    return redirect("/league/{0}".format(id))
  except:
    '''todo: handle case when URL is bad'''


@app.route('/league/<int:leagueid>', methods=['GET'])
def choose_owner(leagueid):
  owners = get_owners_from_url(leagueID)
  return render_template("owners.html", owners=owners, league=leagueID)

@app.route('/league/<int:leagueid>/<int:ownerid>', methods=['GET'])
def alternate_schedules(leagueid, ownerid):
  owners = get_owners_from_url(leagueID)
  alt_owner = owners[ownerid]
  season_schedule, season_scores = construct_season_data(alt_owner, owners, leagueID)
  return render_template("schedules.html", season_schedule=season_schedule, season_scores=season_scores, owners=owners, alt_owner=alt_owner)


'''
owners = get_owners_from_url(scoreboard_url, leagueID)
alt_team = "taylor sbicca"
season_schedule, season_scores = construct_season_data(scoreboard_url, alt_team, owners, leagueID)
display_alt_history(season_schedule, season_scores, owners, alt_team)
'''

if __name__ == '__main__':
  app.debug = True
  app.run()