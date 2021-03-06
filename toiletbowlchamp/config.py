from datetime import datetime
from pytz import timezone

scoreboard_url = 'http://games.espn.go.com/ffl/scoreboard?leagueId={LEAGUE}&scoringPeriodId={WEEK}'
league_settings_url = 'http://games.espn.go.com/ffl/leaguesetup/settings?leagueId={LEAGUEID}'
# Datetime is set to estimated end of monday night game.  Using PST because #WestCoastBestCoast
local_timezone = timezone('America/Los_Angeles')
opening_day_date = datetime(2015, 9, 14, 23, 0, 0, tzinfo=local_timezone)