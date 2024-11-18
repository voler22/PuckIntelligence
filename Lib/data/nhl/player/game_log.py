from abc import ABC
from typing import Any
from Config.teams import NHL_TEAMS_ACRONYMS
import Lib.tools as tools
import datetime as dt


class INHLGameLog(ABC):
    _GAME_LOG_ID = "GAME_LOGS-tabpanel"

    def __init__(
        self,
        date: dt.date,
        profile: dict[str, Any],
        html_content: str,
    ):
        self.profile = profile
        self._html_content = html_content
        self._date = date

    def _get_last_log_in_html(self):
        logs = self._html_content.find("div", id=self._GAME_LOG_ID)
        return logs.find_all("tr")[1]

    def _get_home_away(self, content: str) -> int:
        if content == "@":
            return 0
        return 1


class NHLSkaterGameLog(INHLGameLog):
    def __init__(
        self,
        date: dt.date,
        profile: dict[str, Any],
        html_content: str,
    ):
        super().__init__(date, profile, html_content)

    def get_yesterday_game_log(self) -> dict[str, Any]:
        """Get yesterday's game log if any."""
        content = self._get_last_log_in_html()
        content_date = tools.format_game_log_date(content.find("th").text)
        if self._date == content_date:
            return self._get_game_log(content)

    def _get_game_log(self, content: str) -> dict[str, Any]:
        content_header = content.find("th")
        content_fields = content.find_all("td")
        return {
            "DATE": str(tools.format_game_log_date(content_header.text)),
            "FIRST_NAME": self.profile["first_name"],
            "LAST_NAME": self.profile["last_name"],
            "NHL_ID": self.profile["nhl_id"],
            "AGE": self.profile["age"],
            "BIRTH_CITY": self.profile["birth city"],
            "BIRTH_STATE": self.profile["birth state"],
            "BIRTH_COUNTRY": self.profile["birth country"],
            "HEIGHT_INCHES": self.profile["height (inches)"],
            "WEIGHT_LBS": self.profile["weight (lbs)"],
            "SHOT": self.profile["shot"],
            "DRAFT_YEAR": self.profile["draft"]["year"],
            "DRAFT_TEAM": self.profile["draft"]["team"],
            "DRAFT_OVERALL": self.profile["draft"]["overall"],
            "DRAFT_ROUND": self.profile["draft"]["round"],
            "DRAFT_PICK": self.profile["draft"]["pick"],
            "TEAM": NHL_TEAMS_ACRONYMS[content_fields[0].text],
            "OPPONENT": NHL_TEAMS_ACRONYMS[content_fields[1].text[-3:]],
            "HOME_GAME": int("@" not in content_fields[1].text),
            "GOALS": int(content_fields[2].text),
            "ASSISTS": int(content_fields[3].text),
            "POINTS": int(content_fields[4].text),
            "PLUS_MINUS": int(content_fields[5].text),
            "PIM": int(content_fields[6].text),
            "PPG": int(content_fields[7].text),
            "PPA": int(content_fields[8].text) - int(content_fields[7].text),
            "PPP": int(content_fields[8].text),
            "SHG": int(content_fields[9].text),
            "SHA": int(content_fields[10].text) - int(content_fields[9].text),
            "SHP": int(content_fields[10].text),
            "GWG": int(content_fields[11].text),
            "OTG": int(content_fields[12].text),
            "SHOTS": int(content_fields[13].text),
            "SHOOTING_PERCENTAGE": self._get_shooting_percentage(int(content_fields[2].text), int(content_fields[13].text)),
            "NUMBER_SHIFTS": int(content_fields[14].text),
            "TIME_ON_ICE": tools.get_time_on_ice(
                content_fields[15].text
            ),
        }

    def _get_shooting_percentage(self, goals: int, shots: int) -> float:
        if shots > 0:
            return goals/shots
        return 0.0


class NHLGoalieGameLog(INHLGameLog):
    def __init__(
        self,
        date: dt.date,
        profile: dict[str, Any],
        html_content: str,
    ):
        super().__init__(date, profile, html_content)
