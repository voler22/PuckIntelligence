import datetime as dt
from abc import abstractmethod

from Lib.data.nhl.league.standing import (
    LeagueStanding,
    DivisionStanding,
    ConferenceStanding,
)


class IHockeyUniverse:
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

    def _make_league(self):
        LeagueStanding_ = LeagueStanding(self)
        self.league["standing"] = LeagueStanding_.make()

        ConferenceStanding_ = ConferenceStanding(self)
        self.conference["standing"] = ConferenceStanding_.make()

        DivisionStanding_ = DivisionStanding(self)
        self.division["standing"] = DivisionStanding_.make()
