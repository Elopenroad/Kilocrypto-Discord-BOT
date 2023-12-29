import discord
from discord.ext import commands ,tasks
from peewee import *
from pycoingecko import CoinGeckoAPI
from database_settings import Coins , User

db = SqliteDatabase('database.db')
db.connect()


class TradeSignal(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.daily_trade.start()
        self.cg = CoinGeckoAPI()
        self.data = self.cg.get_search_trending()
        self.lastchanges = None
        self.position = None
        self.coinName = None
        self.top = {}

    @tasks.loop(hours=1)
    async def daily_trade(self):
        coins = self.data['coins']
        max_change_coin = None
        max_change = -float('inf')  # Initialize with negative infinity

        for coin in coins:
            coin_id = coin['item']['id']
            coinPrice = self.cg.get_price(ids=f'{coin_id}', vs_currencies='usd', include_market_cap=True, include_24hr_vol=True, include_24hr_change=True, include_last_updated_at=True)
            coinChanges = coinPrice[f'{coin_id}']['usd_24h_change']
            if '-' not in str(coinChanges):
                print(f'The coin name : {coin_id}')
                self.top[coin_id] = coinChanges  # Store coinChanges in the dictionary
            if coinChanges > max_change:
                max_change = coinChanges
                max_change_coin = coin_id
        if max_change_coin is not None:
            if "-" not in str(max_change):  
                # Sort the self.top dictionary by coinChanges (values) in descending order
                sorted_top = dict(sorted(self.top.items(), key=lambda x: x[1], reverse=True))

                # Create a formatted string of the top-performing coins with their changes
                top_coins_str = "\n".join([f"{coin}: \n```{changes}%```" for coin, changes in sorted_top.items()])

                embed = discord.Embed(color=discord.Color.blue(), title="BOT TRADES").set_image(url="https://cdn.dribbble.com/users/192882/screenshots/4659605/dribbble-animation.gif")
                embed.add_field(name="**Best signal**", value=f"**{max_change_coin}**\n**Changes last 24 hours :** ```{max_change}%```", inline=True)
                embed.add_field(name='**Top signals(In order)**', value=f"**{top_coins_str}**", inline=True)

                query = User.select()
                for user in query:
                    try:
                        userDm = await self.bot.fetch_user(user)
                        if userDm:
                            await userDm.send(embed=embed)
                        else:
                            print(f"User with ID {user} not found.")
                    except Exception as e:
                        print(f"An error occurred: {str(e)}")

                
async def setup(bot):
    await bot.add_cog(TradeSignal(bot))