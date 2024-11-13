from abc import ABC
from typing import Any
from Lib.data.nhl.player.player import NHLPlayer


class INHLGameLog(ABC):
    def __init__(
        self, universe: dict[str, Any], first_name: str, last_name: str, nhl_id: str, html_source: str
    ):
        self.Player = NHLPlayer(universe, first_name, last_name, nhl_id)
        self._html_source = html_source


class NHLSkaterGameLog(INHLGameLog):
    _SKATER_GAME_LOG_CLASS = ""

    def __init__(self, universe: dict[str, Any], first_name: str, last_name: str, nhl_id: str):
        super().__init__(universe, first_name, last_name, nhl_id, html_source)








class NHLGoalieGameLog(INHLGameLog):
    def __init__(self, universe: dict[str, Any], first_name: str, last_name: str, nhl_id: str):
        super().__init__(universe, first_name, last_name, nhl_id, html_source)
