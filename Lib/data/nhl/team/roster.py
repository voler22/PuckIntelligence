from bs4 import BeautifulSoup
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        """Fetch the HTML table(s) from the URL."""
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
        """Extract player data from the table and add it to the roster."""
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
                    self._insert(individual_row)
                except Exception:
                    raise RuntimeError(
                        "Player cannot be added: {}".format(row_data_.text)
                    )

    def _insert(self, player_data):
        """Insert player data into the roster."""
        # player = NHLPlayer(player_data)
        self._roster[player_data[0]] = {
            "first": player_data[1],
            "last": player_data[2],
            "id": player_data[3],
            "number": player_data[0],
            "position": player_data[4],
            "shot": player_data[5],
            "height (inches)": self._convert_height_to_inches(player_data[6]),
            "weight (lbs)": player_data[7],
            "birth date": self._convert_date_from_string_to_datetime(player_data[8]),
            "birthplace": self._format_birthplace(player_data[9]),
        }

    def _convert_height_to_inches(self, height):
        """Convert height from feet and inches to inches."""
        if len(height) == 5:
            feet, inches = int(height[0]), int(height[2:4])
            return 12 * feet + inches
        elif len(height) == 4:
            feet, inches = int(height[0]), int(height[2])
            return 12 * feet + inches
        raise RuntimeError("Height cannot be transformed. Height: {}.format(height)")

    def _convert_date_from_string_to_datetime(self, date):
        """Convert date from string to datetime object."""
        return dt.datetime.strptime(date, "%b %d, %Y").date()

    def _format_birthplace(self, birthplace):
        """Format the birthplace."""
        birthplace_ = birthplace.split(", ")
        try:
            return {
                "city": birthplace_[0],
                "state/province": birthplace_[1],
                "country": birthplace_[2],
            }
        except IndexError:
            return {
                "city": birthplace_[0],
                "state/province": None,
                "country": birthplace_[1],
            }
