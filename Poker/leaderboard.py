class Leaderboard:
    
    def __init__(self):
        self.players=[]
        self.playerdata={}
        
    def getLeaderboard(self, ctx):
        sort_byvalue=sorted(self.playerdata.items(),key=lambda x:x[1],reverse=True)
        return sort_byvalue
        # for i in sort_byvalue:
        #     await ctx.send((i[0],i[1]))

    def addplayer(self,id):
        self.players.append(id)
        self.playerdata[id]=3000

    def updateplayer(self,id,number):
        self.playerdata[id]+=number

