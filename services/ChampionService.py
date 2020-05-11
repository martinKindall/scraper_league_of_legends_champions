import typing
import mysql.connector as mariadb
from dotenv import load_dotenv
import os

load_dotenv()


if typing.TYPE_CHECKING:
	from dataClasses.Champion import Champion

class ChampionService:
	mariadb_connection = mariadb.connect(
		user=os.getenv("DB_USER"),
		password=os.getenv("DB_PASS"),
		database=os.getenv("DB_PASS"))

	def save(self, champion: 'Champion'):
		pass
