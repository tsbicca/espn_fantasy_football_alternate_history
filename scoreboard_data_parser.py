from bs4 import BeautifulSoup
import requests

def fetch_page_as_soup(url):
  page = requests.get(url)
  data = page.text
  return BeautifulSoup(data, "html.parser")

def _get_matchups(soup):
  '''
  Parses page for matchups.  Each matchup contains owner & score data for two teams.  Returns a list of html/css results
  '''
  return soup.find_all("table", attrs={'class': 'ptsBased matchup'})

def get_score(soup):
  '''
  Parses page for all scores and returns them as a list.  Scores are in same order as owners
  '''
  scores = []
  scores_soup = soup.find_all("td", attrs={'class': 'score'})
  for score in scores_soup:
    scores.append(float(score.next))
  return scores

def get_owners(soup):
  '''
  Parses page for all owners and returns them as a list
  '''
  owners = []
  owners_soup = soup.find_all("span", attrs={'class': 'owners'})
  for owner in owners_soup:
    owners.append(owner.next)
  return owners

def get_owners_from_url(url, league):
  owners_url = url.format(LEAGUE=str(league), WEEK="1")
  owners_soup = fetch_page_as_soup(owners_url)
  return get_owners(owners_soup)

def get_owner_scores(soup):
  owners = get_owners(soup)
  scores = get_score(soup)
  return dict(zip(owners, scores))

def get_matchups_for_week(soup):
  '''
  Takes the beautiful soup page and returns a dictionary of matchups with key being owner name and value being thier opponet
  '''
  matchup_results = {}
  matchups = _get_matchups(soup)
  for matchup in matchups:
    teams = get_owners(matchup)
    matchup_results[teams[0]] = teams[1]
    matchup_results[teams[1]] = teams[0]
  return matchup_results