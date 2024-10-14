from Config.urls import URL_NHL_PLAYER
from Config.teams import NHL_TEAMS_FOR_DRAFT
from bs4 import BeautifulSoup
import Lib.tools as t
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from typing import Any


class NHLPlayer:
    _BIO_CLASS = "sc-gUhVhA kPFQTO"

    def __init__(
        self, universe: dict[str, Any], first_name: str, last_name: str, nhl_id: str
    ) -> None:
        self._universe = universe
        self._first_name = first_name
        self._last_name = last_name
        self._nhl_id = nhl_id
        self._url = URL_NHL_PLAYER.format(
            self._first_name.lower(), self._last_name.lower(), self._nhl_id
        )
        self._player = {
            "profile": {},
        }

    def make(self):
        """Make NHL player bio."""
        bio_html = self._get_html_content()
        self._make_player_bio(bio_html)

    def _get_html_content(self):
        driver = webdriver.Chrome()
        try:
            driver.get(self._url)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            html = driver.page_source
        finally:
            driver.quit()
        soup = BeautifulSoup(html, "html.parser")
        bio = soup.find("div", class_=self._BIO_CLASS)
        return bio

    def _make_player_bio(self, bio_html):
        bio_fields = bio_html.find_all("div")
        for field in bio_fields:
            list = field.text.split(": ")
            if list[0] == "Height":
                self._player["profile"]["height (inches)"] = (
                    t.format_player_height_in_inches(list[1])
                )
            elif list[0] == "Weight":
                self._player["profile"]["weight (lbs)"] = t.format_player_weight_in_lbs(
                    list[1]
                )
            elif list[0] == "Born":
                (
                    self._player["profile"]["birth_date"],
                    self._player["profile"]["age"],
                ) = t.get_birthdate_and_age(list[1], self._universe.date)
            elif list[0] == "Birthplace":
                (
                    self._player["profile"]["birth city"],
                    self._player["profile"]["birth state"],
                    self._player["profile"]["birth country"],
                ) = t.format_player_birthplace(list[1])
            elif list[0] == "Shoots":
                self._player["profile"]["shot"] = list[1]
            elif list[0] == "Draft":
                self._player["profile"]["draft"] = self._format_draft(list[1])
            else:
                print(
                    "Field '{}' not found for {} {}.".format(
                        list[0], self._first_name, self._last_name
                    )
                )

    def _format_draft(self, draft):
        if draft == "Undrafted":
            return draft
        draft_list_ = draft.split(", ")
        year = int(draft_list_[0])
        team = draft_list_[1][0:3]
        overall = int(re.sub(r"[^0-9]", "", draft_list_[1]))
        round = int(re.sub(r"[^0-9]", "", draft_list_[2]))
        pick = int(re.sub(r"[^0-9]", "", draft_list_[3]))
        return {
            "year": year,
            "team": NHL_TEAMS_FOR_DRAFT[team],
            "overall": overall,
            "round": round,
            "pick": pick,
        }
