import random
from Poker.card import Card



class Deck:

	def __init__(self):
		self.cards = []
		self.build()

	def build(self):
		self.cards.append(Card("Spades", '2', "<:2s:865464492343558194>"))
		self.cards.append(Card("Spades", '3', "<:3s:865464492434391071>"))
		self.cards.append(Card("Spades", '4', "<:4s:865464492384714782>"))
		self.cards.append(Card("Spades", '5', "<:5s:865464492123750401>"))
		self.cards.append(Card("Spades", '6', "<:6s:865464492351553586>"))
		self.cards.append(Card("Spades", '7', "<:7s:865464492389302272>"))
		self.cards.append(Card("Spades", '8', "<:8s:865464492371476480>"))
		self.cards.append(Card("Spades", '9', "<:9s:865462093192232962>"))
		self.cards.append(Card("Spades", '10', "<:10s:867926783054471218>"))
		self.cards.append(Card("Spades", 'J', "<:Js:865464042121330698>"))
		self.cards.append(Card("Spades", 'Q', "<:Qs:865464041820651581>"))
		self.cards.append(Card("Spades", 'K', "<:Ks:865464041911615569>"))
		self.cards.append(Card("Spades", 'A', "<:As:865464042260660259>"))

		self.cards.append(Card("Clubs", '2', "<:2c:865462093380714507>"))
		self.cards.append(Card("Clubs", '3', "<:3c:865462093301547028>"))
		self.cards.append(Card("Clubs", '4', "<:4c:865462092860358697>"))
		self.cards.append(Card("Clubs", '5', "<:5c:865462093435240468>"))
		self.cards.append(Card("Clubs", '6', "<:6c:865462093259341825>"))
		self.cards.append(Card("Clubs", '7', "<:7c:865462093199966222>"))
		self.cards.append(Card("Clubs", '8', "<:8c:865462093126041611>"))
		self.cards.append(Card("Clubs", '9', "<:9c:865462093192232962>"))
		self.cards.append(Card("Clubs", '10', "<:10c:865462093641416734>"))
		self.cards.append(Card("Clubs", 'J', "<:Jc:865462093033898025>"))
		self.cards.append(Card("Clubs", 'Q', "<:Qc:865462093356204042>"))
		self.cards.append(Card("Clubs", 'K', "<:Kc:865462093339033600>"))
		self.cards.append(Card("Clubs", 'A', "<:Ac:865462093133512775>"))

		self.cards.append(Card("Diamonds", '2', "<:2d:865457553214668841>"))
		self.cards.append(Card("Diamonds", '3', "<:3d:865457553441161216>"))
		self.cards.append(Card("Diamonds", '4', "<:4d:865457553357799465>"))
		self.cards.append(Card("Diamonds", '5', "<:5d:865457553257136139>"))
		self.cards.append(Card("Diamonds", '6', "<:6d:865457553684561950>"))
		self.cards.append(Card("Diamonds", '7', "<:7d:865457552967860286>"))
		self.cards.append(Card("Diamonds", '8', "<:8d:865457553391353856>"))
		self.cards.append(Card("Diamonds", '9', "<:9d:865457553412325416>"))
		self.cards.append(Card("Diamonds", '10', "<:10d:865457553475239966>"))
		self.cards.append(Card("Diamonds", 'J', "<:Jd:865457553403543592>"))
		self.cards.append(Card("Diamonds", 'Q', "<:Qd:865457553512726558>"))
		self.cards.append(Card("Diamonds", 'K', "<:Kd:865457553419534346>"))
		self.cards.append(Card("Diamonds", 'A', "<:Ad:865457553454530560>"))

		self.cards.append(Card("Hearts", '2', "<:2h:865455728282304522>"))
		self.cards.append(Card("Hearts", '3', "<:3h:865455728084254721>"))
		self.cards.append(Card("Hearts", '4', "<:4h:865455728272343120>"))
		self.cards.append(Card("Hearts", '5', "<:5h:865455728391487529>"))
		self.cards.append(Card("Hearts", '6', "<:6h:865455728390438962>"))
		self.cards.append(Card("Hearts", '7', "<:7h:865455728318742528>"))
		self.cards.append(Card("Hearts", '8', "<:8h:865455728017670175>"))
		self.cards.append(Card("Hearts", '9', "<:9h:865455728495034418>"))
		self.cards.append(Card("Hearts", '10', "<:10h:865455728331063306>"))
		self.cards.append(Card("Hearts", 'J', "<:Jh:865455728344301599>"))
		self.cards.append(Card("Hearts", 'Q', "<:Qh:865455728356753408>"))
		self.cards.append(Card("Hearts", 'K', "<:Kh:865455728012427275>"))
		self.cards.append(Card("Hearts", 'A', "<:Ah:865455728339451914>"))

				

	def show(self):
		for c in self.cards:
			c.show()

	def shuffle(self):
		for i in range(len(self.cards) -1, 0, -1):
			r = random.randint(0, i)
			self.cards[i], self.cards[r], = self.cards[r], self.cards[i]

	def drawCard(self):
		return self.cards.pop()
