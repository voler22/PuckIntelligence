import datetime as dt
from Lib.data.universe import NHLUniverse
from Lib.data.nhl.player.player import NHLPlayer
from Lib.data.nhl.player.game_log import NHLSkaterGameLog

date = dt.date(2024, 11, 1)
universe = NHLUniverse(date)
player = NHLPlayer(universe, "Alex", "Ovechkin", "8471214")
player.make_bio()
player.get_skater_game_log()
universe.make()
print("nothing")

'''
import sqlite3
import sys

connection = sqlite3.connect("NHL.db")
cursor = connection.cursor()

# cursor.execute("CREATE TABLE SkaterGameStats (name TEXT, date DATE, team TEXT, versus TEXT, home INTEGER, goals INTEGER, assists INTEGER, points INTEGER, plus_minus INTEGER, pim FLOAT(10,5), ppp INTEGER,"
#               "shg INTEGER, shp INTEGER, toi FLOAT(10,5), gwg INTEGER, otg INTEGER, shots INTEGER, shifts INTEGER)")

query = "INSERT INTO SkaterGameStats VALUES('Cole Caufield', '2024-11-01', 'Montreal', 'Toronto', 1, 3, 0, 3, 3, 0,2, 0,0,15.5, 1,0,10, 25)"
cursor.execute(query)

query = "select * from SkaterGameStats"
cursor.execute(query).fetchall()
'''