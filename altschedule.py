from data_utils import *
from config import *

owners = get_owners_from_url(scoreboard_url, leagueID)
alt_team = prompt_for_team(owners)
season_schedule, season_scores = construct_season_data(scoreboard_url, alt_team, owners, leagueID)
display_alt_history(season_schedule, season_scores, owners, alt_team)