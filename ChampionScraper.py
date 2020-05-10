from typing import List, Iterator

import requests
from bs4 import BeautifulSoup

from dataClasses.Champion import Champion

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
		championName = championCells[0].text
		return Champion(championName)

if __name__ == '__main__':
	for champ in ChampionScraper().requestAndObtainParsedChampions():
		print(champ.name)
