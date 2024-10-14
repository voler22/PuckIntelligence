from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from Config.urls import URL_NHL_STANDING


class INHLStanding(ABC):
    """Interface to import NHL standings."""

    def __init__(self, universe, standing_type):
        self._universe = universe
        self._date_str = str(universe.date)
        self._url = URL_NHL_STANDING.format(self._date_str, standing_type)

    @abstractmethod
    def make(self):
        """Abstract method to be implemented in subclasses."""
        raise NotImplementedError

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

    def _get_column_names(self, table):
        """Extract column names from the table header."""
        column_names_html = table.find_all("th")
        column_names = [title.text.strip() for title in column_names_html]
        column_names = column_names[0:19]  # Limit to first 19 columns
        column_names[1] = "Clinched"  # Rename second column
        return column_names

    def _get_teams_by_ranking(self, table):
        """Extract the teams' names from the ranking part of the table."""
        column_names_html = table.find_all("th")
        column_names = [title.text.strip() for title in column_names_html]
        return column_names[19:]  # Return team rankings from column 19 onwards

    def _make(self, table, column_names, teams_ranked):
        """Generate DataFrame for the standings."""
        df = self._initialize_table(column_names)
        return self._prepare_data(df, table, teams_ranked)

    def _initialize_table(self, column_names):
        """Create an empty DataFrame with column names."""
        return pd.DataFrame(columns=column_names)

    def _prepare_data(self, df, table, teams_ranked):
        """Populate the DataFrame with data from the table."""
        column_data = table.find_all("tr")
        for row in column_data:
            row_data = row.find_all("td")
            row_data_as_list = [data.text.strip() for data in row_data]
            if len(row_data_as_list) != 0:
                length = len(df)
                team = teams_ranked[length]
                row_data_as_list.insert(2, team)  # Insert team name at index 2
                df.loc[length] = row_data_as_list
        return df


class NHLLeagueStanding(INHLStanding):
    """Import NHL league standings."""

    def __init__(self, universe):
        super().__init__(universe, "league")

    def make(self):
        """Make NHL league standings."""
        table = self._get_html_tables()[0]
        column_names = self._get_column_names(table)
        teams_ranked = self._get_teams_by_ranking(table)
        return self._make(table, column_names, teams_ranked)


class NHLConferenceStanding(INHLStanding):
    """Import NHL conference standings."""

    _CONFERENCES = {"Eastern": 0, "Western": 1}

    def __init__(self, universe):
        super().__init__(universe, "conference")

    def make(self):
        """Make NHL conference standings."""
        tables = self._get_html_tables()
        for conference, index in self._CONFERENCES.items():
            table = tables[index]
            column_names = self._get_column_names(table)
            teams_ranked = self._get_teams_by_ranking(table)
            standing = self._make(table, column_names, teams_ranked)
            self._save(conference, standing)

    def _save(self, conference, standing):
        """Save the standings to the universe."""
        self._universe.conference[conference]["standing"] = standing


class NHLDivisionStanding(INHLStanding):
    """Import NHL division standings."""

    _DIVISIONS = {"Atlantic": 0, "Metropolitan": 1, "Central": 2, "Pacific": 3}

    def __init__(self, universe):
        super().__init__(universe, "division")

    def make(self):
        """Make NHL division standings."""
        tables = self._get_html_tables()
        for division, index in self._DIVISIONS.items():
            table = tables[index]
            column_names = self._get_column_names(table)
            teams_ranked = self._get_teams_by_ranking(table)
            standing = self._make(table, column_names, teams_ranked)
            self._save(division, standing)

    def _save(self, division, standing):
        """Save the standings to the universe."""
        self._universe.division[division]["standing"] = standing
