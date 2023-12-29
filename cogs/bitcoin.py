import discord
from discord.ext import commands , tasks
from pycoingecko import CoinGeckoAPI
from database_settings import User



class Bitcoin(commands.Cog):

    def __init__(self , bot):
        self.bot = bot
        self.bitcoin.start()
        self.checkpricedoge.start()
        self.lastminutechanges = None
        self.position = False
        
    @tasks.loop(hours=12)
    async def bitcoin(self):
        changes = None  
        cg = CoinGeckoAPI()
        data = cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True)
        data2 = data['bitcoin']
        changes = data2['usd_24h_change']
        print(changes)
        usd = data2['usd']
        print(self.position)
        if self.position == False:
            if '-' in str(changes):
                print(changes)

            else:
                query = User.select()
                for user in query:
                    print(user.ids)
                    userDM = await self.bot.fetch_user(user)
                    print(userDM)
                    if userDM:
                        print("userDM")
                        embed = discord.Embed(color=discord.Color.blue(),title=f'Professional BTC Trading Signal').set_image(url='https://media.discordapp.net/attachments/1132933928802586674/1157314793649225788/brandmark-design-1024x0_1.png?ex=651828e4&is=6516d764&hm=b197675c009f4c11ea09706a20a0a8e7d0a193c133d958aafbff0bf75a422cb4&=&width=537&height=403')
                        embed.add_field(name='**BTC**' , value=f"**Open Position :{usd}** \n ```{changes}```")
                        await userDM.send(embed=embed)
                        self.position = True
        self.lastminutechanges = changes

    @tasks.loop(minutes=1)
    async def checkpricedoge(self):
        changes = None
        if self.position:
            cg = CoinGeckoAPI()
            data = cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True)
            data2 = data['bitcoin']
            changes = data2['usd_24h_change']
            usd = data2['usd']
            str_number2 = str(changes)
            if self.lastminutechanges is not None and str(self.lastminutechanges)[5] > str_number2[5]:
                query = User.select()
                for user in query:
                    userDM = await self.bot.fetch_user(user)
                    if userDM is not None:
                        embed = discord.Embed(color=discord.Color.blue(),title=f'BTC position closed').set_image(url='https://media.discordapp.net/attachments/1132933928802586674/1157314793649225788/brandmark-design-1024x0_1.png?ex=651828e4&is=6516d764&hm=b197675c009f4c11ea09706a20a0a8e7d0a193c133d958aafbff0bf75a422cb4&=&width=537&height=403')
                        embed.add_field(name='**BTC**' , value=f"**{usd}** \n ```{changes}```")
                        await userDM.send(embed=embed)
                        self.position = False
            else:
                print("We are in profit and making money...")
        self.lastminutechanges = changes  

async def setup(bot):
    await bot.add_cog(Bitcoin(bot))
