class PokerPlayer:
    def __init__(self, username, seatNumber):
        self._username = username
        self._seatNumber = seatNumber
        self._hand = []
        self._gameBalance = 3000
        self._playerAction = 0
        self._inGame = True

    '''Returns the player's username'''
    def username(self):
        return self._username

    '''Returns the player's seatNumber'''
    def seatNumber(self):
        return self._seatNumber

    '''Returns the player's status'''
    def getStatus(self):
        return self._inGame

    '''Sets the player's status'''
    def setStatus(self, status):
        self._inGame = status

    '''Returns the player's action'''
    def getHand(self):
        return self._hand

    '''Adds a card to the player's hand.
       A player cannot have more than 2 cards.'''
    def addCard(self, c):
        if len(self._hand) < 2:
            self._hand.append(c)

    '''Returns the player's balance'''
    def getGameBalance(self):
        return self._gameBalance

    '''Sets the Poker Player's current balance.
       opType represents the type of operation.
       1 is for addition and 0 is for subtraction.
       The player's inGame status is set to False if 
       their balance hits 0'''
    def setBalance(self, opType, amount):
        if opType:
            self._gameBalance += amount
        else:
            if self._gameBalance > 0:
                current = self._gameBalance - amount
                self._gameBalance = current if (current > 0) else 0
                if self._gameBalance == 0:
                    self.setStatus(False)

    '''Returns the player's action'''
    def getAction(self):
        return self._playerAction

    '''Sets the player's action'''
    def setAction(self, action):
        self._playerAction = action

