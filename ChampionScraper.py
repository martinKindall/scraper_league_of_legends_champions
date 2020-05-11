import re
from typing import List, Iterator

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dataClasses.Champion import Champion
from services.ChampionService import ChampionService

baseURL = 'https://leagueoflegends.fandom.com'
championsURL = "https://leagueoflegends.fandom.com/es/wiki/Lista_de_campeones"

class ChampionScraper:

	def requestAndObtainParsedChampions(self) -> Iterator['Champion']:
		response = requests.get(championsURL, timeout=10)
		content: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
		championsList: List[BeautifulSoup] = \
			content.find('table', {'class': 'sortable'})\
			.find_all('tr')[1:]
		driver = webdriver.Chrome(
			executable_path=r'C:\\webdrivers\\chromedriver.exe'
		)

		return map(
			lambda championRaw: self.parseChampion(championRaw, driver),
			championsList
		)

	def parseChampion(self, championSoup: BeautifulSoup, driver) -> 'Champion':
		championLinks = championSoup.find_all('a')
		championDetailsURL = "{}{}".format(baseURL, championLinks[1]['href'])
		return self.parseChamptionDetails(championDetailsURL, driver)

	def parseChamptionDetails(self, championDetailsURL: str, driver) -> 'Champion':
		driver.get(championDetailsURL)
		delay = 20
		try:
			flyTabs = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'flytabs_0-content-wrapper')))
			generalDetails: BeautifulSoup = BeautifulSoup(driver.page_source, "html.parser")
			detailsFromTable: BeautifulSoup = BeautifulSoup(flyTabs.get_attribute('innerHTML'), "html.parser")
			tableData = detailsFromTable \
				.find('div', {"data-tab-body": "flytabs_00"}) \
				.find_all('aside')

			name = self.getChampionName(generalDetails)
			category = self.getChampionCategory(generalDetails)
			movementSpeed = self.getMovementSpeed(tableData[1])
			attackRange = self.getAttackRange(tableData[1])
			championStyle = self.getChampionStyle(tableData[0])
			difficulty = self.getDifficulty(tableData[0])

			return Champion(
				name,
				championDetailsURL,
				category,
				int(attackRange),
				int(movementSpeed),
				int(championStyle),
				int(difficulty)
			)
		except TimeoutException:
			print("Loading took too much time!")
			exit()

	@classmethod
	def getDifficulty(cls, table: BeautifulSoup) -> str:
		championDifficulty = table.find(
				'div', {'data-source': 'difficulty'}
			).find('div', {'style': 'cursor:help;'})['title']
		return re.findall('[0-9]+', championDifficulty)[0]

	@classmethod
	def getChampionStyle(cls, table: BeautifulSoup) -> str:
		return table.find(
				'div', {'data-source': 'style'}
			).find_all('span')[1]['title']

	@classmethod
	def getAttackRange(cls, table: BeautifulSoup) -> str:
		return table.find(
				'div', {'data-source': 'range'}).find('span').text

	@classmethod
	def getMovementSpeed(cls, table: BeautifulSoup) -> str:
		return table.find(
				'div', {'data-source': 'ms'}).find('span').text

	@classmethod
	def getChampionName(cls, generalDetails: BeautifulSoup) -> str:
		return generalDetails.find('h1', {'class': 'page-header__title'}).text.lower()

	@classmethod
	def getChampionCategory(cls, generalDetails: BeautifulSoup) -> str:
		return generalDetails.find('a', {'class': 'mw-redirect'}).text.lower()


if __name__ == '__main__':
	championService = ChampionService()
	for champ in ChampionScraper().requestAndObtainParsedChampions():
		print(champ.name, champ.url, champ.category,
			  champ.attackRange, champ.movementSpeed,
			  champ.style, champ.difficulty)
		championService.save(champ)
