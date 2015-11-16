from config import *
from datetime import datetime
from scoreboard_data_parser import *
import re

def prompt_for_team(owners):
  print("Owners: ")
  for num, owner in enumerate(owners):
    print("{0}: {1}".format(num, owner))
  selection = int(input("Enter number of the team for which you wish to view the alternate history:  "))
  try:
    return owners[selection]
  except IndexError:
    print("Invalid entry")
    prompt_for_team()

def current_week():
  current_time = datetime.now(local_timezone)
  days = (current_time - opening_day_date).days
  return (days // 7) + 1 # aka weeks, add 1 to account for opening week

def construct_season_data(alt_team, owners, league):
  '''
  Function scrapes each score page.  Return two datasets:
  seasons_schedule is a dictionary where key is the owner and value is a list that is the owners schedule. Schedule is
  modified so that when the alt team is replaced the team being evaluated.
  season_scores is a list.  List index + 1 is the number of the NFL week.  Each index contains a dictionary where the
  key is the owner and value is the score
  '''
  season_scores = []
  season_schedule = {}

  for owner in owners:
    season_schedule[owner] = []

  for week in range(1, current_week() + 1):
    url = scoreboard_url.format(LEAGUE=str(league), WEEK=str(week))
    soup = fetch_page_as_soup(url)
    matchups = get_matchups_for_week(soup)
    week_scores = get_owner_scores(soup)
    season_scores.append({})

    '''
    Constructs a list containing the matchups for each owner.  Exception is for when the matchup would be alternate owner.
    In that case we sub in the current owner to simulate owner vs alternate team matchup
    '''
    for owner in owners:
      if matchups[owner] == alt_team:
        season_schedule[owner].append(owner)
      else:
        season_schedule[owner].append(matchups[owner])

    for owner in owners:
      season_scores[week - 1][owner] = week_scores[owner]

  return season_schedule, season_scores

def display_alt_history(season_schedule, season_scores, owners, alt_team):
  for team in owners:
    wins = 0
    losses = 0
    if team != alt_team:
      print("If {0} had {1}'s schedule:".format(alt_team, team))
      for week, result in enumerate(season_scores):
        opponent = season_schedule[team][week]
        alt_team_score = result[alt_team]
        opponent_score = result[opponent]
        if alt_team_score > opponent_score:
          outcome = "win"
          wins = wins + 1
        else:
          outcome = "loss"
          losses = losses + 1
        print("  Week {0} vs {1}: {2} ({3} - {4})".format(week + 1, opponent, outcome, alt_team_score, opponent_score))
      print("Alternate History Record: {0}-{1}".format(wins, losses))

def leagueID_from_url(url):
  search_string = 'leagueId\=(.*?)\&'
  result = re.search(search_string, url)
  if result:
    return result.group(1)
  else:
    raise Exception("Unable To Find League ID")