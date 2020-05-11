from typing import List, Iterator

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dataClasses.Champion import Champion

baseURL = 'https://leagueoflegends.fandom.com'
championsURL = "https://leagueoflegends.fandom.com/es/wiki/Lista_de_campeones"

class ChampionScraper:

	def requestAndObtainParsedChampions(self) -> Iterator['Champion']:
		response = requests.get(championsURL, timeout=10)
		content: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
		championsList: List[BeautifulSoup] = \
			content.find('table', {'class': 'sortable'})\
			.find_all('tr')[1:]

		return map(
			self.parseChampion,
			championsList
		)

	def parseChampion(self, championSoup: BeautifulSoup) -> 'Champion':
		championCells: List[BeautifulSoup] = championSoup.find_all('td')
		championLinks = championSoup.find_all('a')
		championDetailsURL = "{}{}".format(baseURL, championLinks[1]['href'])
		return self.parseChamptionDetails(championDetailsURL)

	def parseChamptionDetails(self, championDetailsURL: str) -> 'Champion':
		driver = webdriver.Chrome(
			executable_path=r'C:\\webdrivers\\chromedriver.exe'
		)
		driver.get(championDetailsURL)
		delay = 20
		try:
			flyTabs = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'flytabs_0-content-wrapper')))
			generalDetails: BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
			detailsFromTable: BeautifulSoup = BeautifulSoup(flyTabs.get_attribute('innerHTML'), "html.parser")
			name = generalDetails.find('h1', {'class': 'page-header__title'}).text.lower()
			category = generalDetails.find('a', {'class': 'mw-redirect'}).text.lower()
			tableData = detailsFromTable \
				.find('div', {"data-tab-body": "flytabs_00"}) \
				.find_all('aside')
			attackRange = tableData[1].find(
				'span',
				id=lambda idAttr: idAttr is not None and "attackrange_" in idAttr.lower()
			)
			return Champion(name, championDetailsURL, category)
		except TimeoutException:
			print("Loading took too much time!")


if __name__ == '__main__':
	for champ in ChampionScraper().requestAndObtainParsedChampions():
		print(champ.name, champ.url, champ.category)
