from Poker.card import Card
from Poker.pokerplayer import PokerPlayer

class EvaluateHand:
    def __init__(self, hand):
        self.allCards= hand
        # print(self.allCards)
    
    def printHand(self):
        for x in self.allCards:
            print(str(x.val) +str(x.suit) )

    def addCard(self, card):
        self.allCards.append(card)

    def numCards(self):
        return len(self.hand)

    def sortByRank(self):
        self.allCards.sort(key=lambda x:x.getNumVal())
        
    def sortBySuit(self):
        self.allCards.sort(key=lambda x:x.getNumSuit())
    
    def sortBySuitThenRank(self):
        self.allCards.sort(key=lambda x:x.getNumSuit())
        self.allCards.sort(key=lambda x:x.getNumVal())

    def sortByRankThenSuit(self):
        self.allCards.sort(key=lambda x:x.getNumVal())
        self.allCards.sort(key=lambda x:x.getNumSuit())

    def evaluate(self):
        rankCounter = {}
        suitCounter = {}

        for x in range(13):
            rankCounter[x]=[]

        for x in range(4):
            suitCounter[x]=[]

        for x in self.allCards:
            rankCounter[x.getNumVal()].append(x)
            suitCounter[x.getNumSuit()].append(x)

        self.sortByRankThenSuit()

        handResult=[]
        handResult=self.evaluateRoyal(rankCounter,suitCounter)

        if len(handResult)==0:
            handResult=self.evaluateStraightFlush(suitCounter)
    
        if len(handResult)==0:
            handResult=self.evaluateFourOfAKind(rankCounter)

        if len(handResult)==0:
            handResult=self.evaluateFullHouse(rankCounter)

        if len(handResult)==0:
            handResult=self.evaluateFlush(suitCounter)

        if len(handResult)==0:
            handResult=self.evaluateStraight(rankCounter)

        if len(handResult)==0:
            handResult=self.evaluateThreeOfAKind(rankCounter)

        if len(handResult)==0:
            handResult=self.evaluateTwoPair(rankCounter)

        if len(handResult)==0:
            handResult=self.evaluateOnePair(rankCounter)

        if len(handResult)==0:
            handResult=self.evaluateHighCard(rankCounter)
        
        return handResult

    def evaluateRoyal(self, rankCounter, suitCounter):
        result=[]
        if ((len(rankCounter[9])>=1 and len(rankCounter[10])>=1 and 
            len(rankCounter[11])>=1 and len(rankCounter[12])>=1 and
            len(rankCounter[0])>=1)
            and 
            (len(suitCounter[0])>4 or len(suitCounter[1])>4 or
            len(suitCounter[2])>4 or len(suitCounter[3])>4)):
            for i in range(3):
                if (self.allCards[i].getNumVal()==0):
                    for j in range(1,4-i):
                        if (self.allCards[i+j].getNumVal()==9 and self.allCards[i+j+1].getNumVal()==10 and
                            self.allCards[i+j+2].getNumVal()==11 and self.allCards[i+j+3].getNumVal()==12
                            and
                            self.allCards[i].getNumSuit() == self.allCards[i+j].getNumSuit() and
                            self.allCards[i].getNumSuit() == self.allCards[i+j+1].getNumSuit() and
                            self.allCards[i].getNumSuit() == self.allCards[i+j+2].getNumSuit() and
                            self.allCards[i].getNumSuit() == self.allCards[i+j+3].getNumSuit()):
                            result=[10]
                            break
        return result

    def evaluateStraightFlush(self, suitCounter):
        result=[]
        if (len(suitCounter[0])>4 or len(suitCounter[1])>4 or 
            len(suitCounter[2])>4 or len(suitCounter[3])>4):
            for i in range(len(self.allCards)-1, 3, -1):
                if ((self.allCards[i].getNumVal()-1 == self.allCards[i-1].getNumVal() and
                    self.allCards[i].getNumVal()-2 == self.allCards[i-2].getNumVal() and
                    self.allCards[i].getNumVal()-3 == self.allCards[i-3].getNumVal() and
                    self.allCards[i].getNumVal()-4 == self.allCards[i-4].getNumVal())
                    and
                    (self.allCards[i].getNumSuit() == self.allCards[i-1].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-2].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-3].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-4].getNumSuit())):
                    result=[9,self.allCards[i].getNumVal()]
        return result

    def evaluateFourOfAKind(self, rankCounter):
        result=[]
        for i in range(13):
            if len(rankCounter[i])==4:
                result=[8,i]
                if len(rankCounter[0])>0 and i!=0:
                    result.append(0)
                    break
                for j in range(len(rankCounter),0,-1):
                    if len(rankCounter[j-1])>0 and j!=i:
                        result.append(j)
                        break
                break
        return result        

    def evaluateFullHouse(self, rankCounter):
        result=[]
        threeOfKind=-1
        twoOfKind=-1

        for i in range(len(rankCounter), 0, -1):
            if threeOfKind<0 or twoOfKind<0:
                if len(rankCounter[i-1])>2:
                    threeOfKind=i-1
                elif len(rankCounter[i-1])>1:
                    twoOfKind=i-1
            else:
                break
        if threeOfKind >=0 and twoOfKind >=0:
            result=[7,threeOfKind,twoOfKind]
            
        return result     

    def evaluateFlush(self, suitCounter):
        result=[]

        if (len(suitCounter[0])>4 or len(suitCounter[1])>4 or
            len(suitCounter[2])>4 or len(suitCounter[3])>4):
            for i in range(len(self.allCards)-1, 3, -1):
                if (self.allCards[i].getNumSuit() == self.allCards[i-1].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-2].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-3].getNumSuit() and
                    self.allCards[i].getNumSuit() == self.allCards[i-4].getNumSuit()):
                    result=[6, self.allCards[i].getNumVal(),self.allCards[i-1].getNumVal(),
                        self.allCards[i-2].getNumVal(),self.allCards[i-3].getNumVal() ,self.allCards[i-4].getNumVal()]
                    if self.allCards[i-4].getNumVal()==0:
                        result.pop()
                        result.insert(1,0)
                    break

        return result

    def evaluateStraight(self, rankCounter):
        result=[]
        if (len(rankCounter[0])>0 and len(rankCounter[12])>0 and
            len(rankCounter[11])>0 and len(rankCounter[10])>0 and
            len(rankCounter[9])>0):
            result=[5, 0]
            return result
        for i in range(len(rankCounter), 4, -1):
            if (len(rankCounter[i-1])>0 and len(rankCounter[i-2])>0 and
                len(rankCounter[i-3])>0 and len(rankCounter[i-4])>0 and
                len(rankCounter[i-5])>0):
                result=[5,i-1]

        return result

    def evaluateThreeOfAKind(self, rankCounter):
        result=[]

        for i in range(len(rankCounter),0,-1):
            if len(rankCounter[i-1])>2:
                result =[4, i-1]
                count=0
                if len(rankCounter[0])>0 and i!=0:
                    result.append(0)
                    count+=1
                for j in range(len(rankCounter),0,-1):
                    if len(rankCounter[j-1])>0 and (j-1)!=i and count!=2:
                        result.append(j-1)
                        count+=1
                break
        return result

    def evaluateTwoPair(self, rankCounter):
        result=[]

        pairOne=-1
        pairTwo=-1

        for i in range(len(rankCounter),0,-1):
            if pairOne<0 or pairTwo<0:
                if len(rankCounter[i-1])>1 and pairOne < 0:
                    pairOne=i-1
                elif len(rankCounter[i-1])>1:
                    pairTwo=i-1
            else:
                break

        if pairOne>=0 and pairTwo >=0:
            if (pairTwo==0):
                result=[3, pairTwo, pairOne]
            else:
                result=[3, pairOne, pairTwo]

            if (len(rankCounter[0])>0 and pairOne!=0 and pairTwo!=0):
                    result.append(0)
                    return result
            for j in range(len(rankCounter),0,-1):
                if len(rankCounter[j-1])>0 and (j-1)!=pairOne and (j-1)!=pairTwo:
                    result.append(j-1)
                    break
        return result

    def evaluateOnePair(self, rankCounter):
        result=[]

        for i in range(len(rankCounter),0,-1):
            if len(rankCounter[i-1])>1:
                result=[2, i-1]
                count=0
                if len(rankCounter[0])>0 and i!=0:
                    result.append(0)
                    count+=1
                for j in range(len(rankCounter),0,-1):
                    if len(rankCounter[j-1])>0 and (j-1)!=i and count!=3:
                        result.append(j-1)
                        count+=1
                break
        return result

    def evaluateHighCard(self, rankCounter):
        result=[1]
        count=0
        if len(rankCounter[0])>0:
            result.append(0)
            count+=1

        for i in range(len(rankCounter),0,-1):
            if len(rankCounter[i-1])>0 and count!=5:
                result.append(i-1)
                count+=1

        return result
    
    def winning(self, competing, winCond):
        winners=[]
        winners2=[]
        winners3=[]

        if len(competing)==1: 
            return competing

        if winCond==10:
            return competing

        elif winCond==9:
            maxVal = max(x._winCondition[1] for x in competing)
            for x in competing:
                if x._winCondition[1] == maxVal:
                    winners.append(x)

        elif winCond==8:
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)
            
            for x in competing:
                if x._winCondition[1] == maxVal:
                    winners.append(x)
            if len(winners)>1:
                if (min(x._winCondition[2] for x in winners)==0): 
                    maxVal=0
                else:
                    maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                return winners2
                
        elif winCond==7:
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)
                
            for x in competing:
                if x._winCondition[1] == maxVal:
                    winners.append(x)
            if len(winners)>1:
                if (min(x._winCondition[2] for x in winners)==0): 
                    maxVal=0
                else:
                    maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                return winners2

        elif winCond==6:
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:
                    winners.append(x)
            
            if len(winners) >1:
                maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    if len(winners3)==1:
                        return winners3
                    else:
                        winners.clear()
                        maxVal = max(x._winCondition[4] for x in winners3)
                        for x in winners3:
                            if x._winCondition[4] == maxVal:
                                winners.append(x)
                        if len(winners)==1:
                            return winners
                        else:     
                            winners2.clear()
                            maxVal = max(x._winCondition[5] for x in winners)
                            for x in winners:
                                if x._winCondition[5] == maxVal:
                                    winners2.append(x)
                            return winners2        

        elif winCond==5:
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)          

            for x in competing:
                if x._winCondition[1]==maxVal:
                    winners.append(x)
        
        elif winCond==4:
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:
                    winners.append(x)
            
            if len(winners) >1:
                if (min(x._winCondition[2] for x in winners)==0): 
                    maxVal=0
                else:
                    maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    return winners3

        elif winCond==3:
            
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:
                    winners.append(x)
            
            if len(winners) >1:
                maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    if (min(x._winCondition[3] for x in winners2)==0): 
                        maxVal=0
                    else:
                        maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    return winners3

        elif winCond==2:
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:
                    winners.append(x)
            
            if len(winners) >1:
                if (min(x._winCondition[2] for x in winners)==0): 
                    maxVal=0
                else:
                    maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    if len(winners3)==1:
                        return winners3
                    else:
                        winners.clear()
                        maxVal = max(x._winCondition[4] for x in winners3)
                        for x in winners3:
                            if x._winCondition[4] == maxVal:
                                winners.append(x)    

        elif winCond==1:
            if (min(x._winCondition[1] for x in competing)==0): 
                maxVal=0
            else:
                maxVal = max(x._winCondition[1] for x in competing)

            for x in competing:
                if x._winCondition[1]==maxVal:
                    winners.append(x)
            
            if len(winners) >1:
                maxVal = max(x._winCondition[2] for x in winners)
                for x in winners:
                    if x._winCondition[2] == maxVal:
                        winners2.append(x)
                if len(winners2)==1:
                    return winners2
                else:
                    maxVal = max(x._winCondition[3] for x in winners2)
                    for x in winners2:
                        if x._winCondition[3] == maxVal:
                            winners3.append(x)
                    if len(winners3)==1:
                        return winners3
                    else:
                        winners.clear()
                        maxVal = max(x._winCondition[4] for x in winners3)
                        for x in winners3:
                            if x._winCondition[4] == maxVal:
                                winners.append(x)
                        if len(winners)==1:
                            return winners
                        else:     
                            winners2.clear()
                            maxVal = max(x._winCondition[5] for x in winners)
                            for x in winners:
                                if x._winCondition[5] == maxVal:
                                    winners2.append(x)
                            return winners2                      
        return winners

