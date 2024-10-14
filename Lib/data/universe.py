import datetime as dt
from abc import abstractmethod, ABC

from Lib.data.nhl.league.standing import (
    NHLLeagueStanding,
    NHLDivisionStanding,
    NHLConferenceStanding,
)
from Lib.data.nhl.team.roster import NHLRoster
from Config.teams import NHL_TEAMS


class IHockeyUniverse(ABC):
    """Interface for hockey data collector"""

    @abstractmethod
    def make(self):
        """Forming the hockey universe data"""
        raise NotImplementedError


class NHLUniverse(IHockeyUniverse):
    def __init__(self, date: dt.date):
        self.date = date
        self.league = {}
        self.conference = {"Eastern": {}, "Western": {}}
        self.division = {
            "Atlantic": {},
            "Metropolitan": {},
            "Central": {},
            "Pacific": {},
        }
        self.teams = {
            "Anaheim": {},
            "Boston": {},
            "Buffalo": {},
            "Calgary": {},
            "Carolina": {},
            "Chicago": {},
            "Colorado": {},
            "Columbus": {},
            "Dallas": {},
            "Detroit": {},
            "Edmonton": {},
            "Florida": {},
            "Los Angeles": {},
            "Minnesota": {},
            "Montreal": {},
            "Nashville": {},
            "New Jersey": {},
            "NY Islanders": {},
            "NY Rangers": {},
            "Ottawa": {},
            "Philadelphia": {},
            "Pittsburgh": {},
            "San Jose": {},
            "Seattle": {},
            "St. Louis": {},
            "Tampa Bay": {},
            "Toronto": {},
            "Utah": {},
            "Vancouver": {},
            "Vegas": {},
            "Washington": {},
            "Winnipeg": {},
        }

    def make(self):
        """Makes NHL universe data for a specific date and saves
        it in the hockey universe object.

        Returns
        -------
        None
        """
        self._make_league()
        self._make_teams()

    def _make_league(self):
        LeagueStanding = NHLLeagueStanding(self)
        self.league["standing"] = LeagueStanding.make()

        ConferenceStanding = NHLConferenceStanding(self)
        self.conference["standing"] = ConferenceStanding.make()

        DivisionStanding = NHLDivisionStanding(self)
        self.division["standing"] = DivisionStanding.make()

    def _make_teams(self):
        for team in NHL_TEAMS:
            Roster = NHLRoster(self, NHL_TEAMS[team])
            Roster.make()
            self.teams[team]["roster"] = Roster._roster
