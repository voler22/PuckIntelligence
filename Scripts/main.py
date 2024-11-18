import datetime as dt
from Lib.data.universe import NHLUniverse
from Lib.data.nhl.player.player import NHLPlayer
from Lib.data.nhl.player.game_log import NHLSkaterGameLog

date = dt.date(2024, 11, 16)
universe = NHLUniverse(date)
player = NHLPlayer(universe, "Cole", "Caufield", "8481540")
player.make_profile()
log = NHLSkaterGameLog(date, player._player["profile"], player._html_content)
log_ = log.get_yesterday_game_log()
print("")

"""
import sqlite3
import sys

connection = sqlite3.connect("NHL.db")
cursor = connection.cursor()

# cursor.execute("CREATE TABLE SkaterGameStats (date DATE, first_name TEXT, last_name TEXT, nhl_id INTEGER, age FLOAT(10, 5), birth_city TEXT, birth_state TEXT, birth_country TEXT, height INTEGER, 
weight INTEGER, shot TEXT, draft_year INTEGER, draft_team TEXT, draft_overall INTEGER, draft_round INTEGER, draft_round_pick INTEGER, team TEXT, opponent TEXT, home INTEGER, goals INTEGER,  
assists INTEGER, points INTEGER, plus_minus INTEGER, penalty_minutes INTEGER, pp_goals INTEGER, pp_assists INTEGER, pp_points INTEGER, sh_goals INTEGER,", sh_assists INTEGER, sh_points INTEGER,
game_winning_goals INTEGER, ot_goals INTEGER, shots INTEGER, shooting_percentage FLOAT(10, 5), shifts INTEGER, time_on_ice FLOAT(10, 5)")

query = "INSERT INTO SkaterGameStats VALUES('Cole Caufield', '2024-11-01', 'Montreal', 'Toronto', 1, 3, 0, 3, 3, 0,2, 0,0,15.5, 1,0,10, 25)"
cursor.execute(query)

query = "select * from SkaterGameStats"
cursor.execute(query).fetchall()
"""
