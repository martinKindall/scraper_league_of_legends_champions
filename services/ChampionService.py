import typing
import mysql.connector as mariadb

if typing.TYPE_CHECKING:
	from dataClasses.Champion import Champion

class ChampionService:
	mariadb_connection = \
		mariadb.connect(user='python_user', password='some_pass', database='employees')

	def save(self, champion: 'Champion'):
		pass
