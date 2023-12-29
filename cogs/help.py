import discord
from discord.ext import commands
import Paginator

class HelpCommand(commands.Cog):

    def __init__(self , bot):
        self.bot = bot

    @commands.hybrid_command(description='Help command')
    async def help(self , ctx):
        embeds = [
            discord.Embed(color=discord.Color.from_rgb(185,139,212), title="**Brochure**",description="**🤖 Kilocrypto : Kilocrypto is your ultimate companion in the world of cryptocurrency trading. This powerful Discord bot utilizes a plethora of professional trading strategies and connects to a cutting-edge AI system to provide you with the best crypto trading signals. Whether you're a seasoned trader or just starting, CryptoTrader Bot is here to help you navigate the volatile crypto markets.**"),
            discord.Embed(color=discord.Color.from_rgb(200,3,218), title="**Key Features**",description="""**

📈 Professional Trading Strategies: Our bot is equipped with a wide range of proven trading strategies used by professionals in the crypto industry. From day trading to long-term investments, we've got you covered.\n

🤖 AI Market Analysis: Powered by state-of-the-art AI technology, our bot continuously analyzes the cryptocurrency market to identify trends and opportunities. It selects the most promising strategies to optimize your trading success.\n

📅 Daily Updates: CryptoTrader Bot sends you daily messages, including the latest crypto signals, AI market analysis reports, and professional Bitcoin trade signals. Stay informed and make informed decisions.\n

📣 Announcements: Get instant updates on the latest changes and developments in our server and on our website. We keep you in the loop with the most important news and updates.\n

🌐 Website Access: For in-depth information, resources, and additional details, visit our website [insert_website_url_here]. Explore comprehensive guides, tutorials, and FAQs to make the most of CryptoTrader Bot.**"""),

        discord.Embed(color=discord.Color.from_rgb(210,238,3), title="**Support and Assistance**",description="""**🌟 Join the Crypto Revolution with CryptoTrader Bot!

Explore the crypto world with confidence, backed by data-driven strategies and AI intelligence. Elevate your trading game today and start making informed decisions.

For more information, visit our website at [insert_website_url_here] or type !help for a list of commands.

https://discord.gg/G3w6YYnC5w**""").set_footer(text='https://discord.gg/G3w6YYnC5w'),]
                                      
        await Paginator.Simple(timeout=None).start(ctx, pages=embeds)
                   
        
async def setup(bot):
    await bot.add_cog(HelpCommand(bot))