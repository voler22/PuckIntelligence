from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Lib.tools as t

from Config.urls import URL_NHL_TEAM


class NHLRoster:
    """Interface to import NHL team rosters."""

    _POSITIONS = {"Forwards": 0, "Defensemen": 1, "Goalies": 2}

    def __init__(self, universe, team):
        self._universe = universe
        self._date_str = str(universe.date)
        self._url = URL_NHL_TEAM.format(team) + "/roster"
        self._roster = {}

    def make(self):
        """Make NHL team roster and create player object with corresponding
        data."""
        tables = self._get_html_tables()
        for position_ in self._POSITIONS:
            table = tables[self._POSITIONS[position_]]
            column_data_ = table.find_all("tr")
            self._add_players_to_roster(column_data_)

    def _get_html_tables(self):
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
        tables = soup.find_all("table")
        return tables

    def _add_players_to_roster(self, column_data):
        for row in column_data:
            row_data = row.find_all("td")
            individual_row = [data.text.strip() for data in row_data]
            if len(individual_row) > 0:
                row_data_ = row.find("th").find("a")
                try:
                    name_ = row_data_.text.split()
                    nhl_id_ = row_data_.attrs["href"][8:]
                    insert_values_ = [name_[0], name_[1], nhl_id_]
                    individual_row[1:1] = insert_values_
                    self._insert_player(individual_row)
                except Exception:
                    raise RuntimeError(
                        "Player cannot be added: {}".format(row_data_.text)
                    )

    def _insert_player(self, player_data):
        birth_city_, birth_state_, birth_country_ = t.format_player_birthplace(
            player_data[9]
        )
        birth_date_, age_ = t.get_birthdate_and_age(player_data[8], self._universe.date)
        self._roster[player_data[3]] = {
            "number": player_data[0],
            "first": player_data[1],
            "last": player_data[2],
            "position": player_data[4],
            "shot": player_data[5],
            "height (inches)": t.format_player_height_in_inches(player_data[6]),
            "weight (lbs)": t.format_player_weight_in_lbs(player_data[7]),
            "birth date": birth_date_,
            "age": age_,
            "birth city": birth_city_,
            "birth state": birth_state_,
            "birth country": birth_country_,
        }
