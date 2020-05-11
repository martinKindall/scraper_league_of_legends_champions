import typing
import mysql.connector as mariadb
from dotenv import load_dotenv
import os

load_dotenv()


if typing.TYPE_CHECKING:
	from dataClasses.Champion import Champion

class ChampionService:
	tableName = os.getenv("DB_TABLE_NAME")
	mariadb_connection = mariadb.connect(
		user=os.getenv("DB_USER"),
		password=os.getenv("DB_PASS"),
		database=os.getenv("DB_NAME"))
	cursor = mariadb_connection.cursor()

	def save(self, champion: 'Champion'):
		self.cursor.execute(
			"INSERT INTO {} (name, url, category, movementSpeed, attackRange, championStyle, difficulty)"
			" VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")"
			" ON DUPLICATE KEY UPDATE"
			" name=VALUES(name), "
			" url=VALUES(url), "
			" category=VALUES(category), "
			" movementSpeed=VALUES(movementSpeed), "
			" attackRange=VALUES(attackRange), "
			" championStyle=VALUES(championStyle), "
			" difficulty=VALUES(difficulty) ".format(
				self.tableName,
				champion.name,
				champion.url,
				champion.category,
				champion.movementSpeed,
				champion.attackRange,
				champion.style,
				champion.difficulty
			)

		)
		self.mariadb_connection.commit()
