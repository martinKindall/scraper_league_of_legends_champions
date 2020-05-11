

class Champion:

	def __init__(
			self,
			name: str,
			url: str,
			category: str,
			attackRange: int,
			movementSpeed: int,
			style: int,
			difficulty: int):
		self.name = name
		self.url = url
		self.category = category
		self.attackRange = attackRange
		self.movementSpeed = movementSpeed
		self.style = style
		self.difficulty = difficulty
