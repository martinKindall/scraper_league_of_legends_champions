from typing import List, Iterator

import requests
from bs4 import BeautifulSoup

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
		response = requests.get(championDetailsURL, timeout=10)
		details: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
		name = details.find('h1', {'class': 'page-header__title'}).text.lower()
		category = details.find('a', {'class': 'mw-redirect'}).text.lower()

		return Champion(name, championDetailsURL, category)


if __name__ == '__main__':
	for champ in ChampionScraper().requestAndObtainParsedChampions():
		print(champ.name, champ.url, champ.category)
