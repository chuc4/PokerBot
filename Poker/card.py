class Card:
	def __init__(self, suit, val, emote):
		self.suit = suit
		self.val = val
		self.emote = emote

	def show(self):
		return self.emote

