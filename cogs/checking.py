import discord
from discord.ext import commands, tasks
from pycoingecko import CoinGeckoAPI
from peewee import *
from database_settings import User
from datetime import datetime, timedelta 
import time

db = SqliteDatabase('database.db')
db.connect()


class CheckOut(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.check_expire.start()


    @commands.hybrid_command()
    async def announcements(self, ctx ,*, message):
        if ctx.author.guild_permissions.administrator == True:
            query = User.select()
            for user in query:
                userDM = await self.bot.fetch_user(user.ids)
                await ctx.send(message)
                await userDM.send(message)
        else:
            await ctx.send('Really?')

    @commands.hybrid_group(cog_name='database')
    async def database(self , ctx):
        if ctx.author.guild_permissions.administrator == True:
            await ctx.send('This is the main group command.')
        else:
            await ctx.send('Really?')
    @database.command()
    async def add(self, ctx, username: str , days:int ):
        if ctx.author.guild_permissions.administrator == True:
            try:
                existing_user = User.select().where(User.username == username).first()
                if existing_user:
                    await ctx.send(f"Error: User {username} already exists in the database")
                    return
                
                member = discord.utils.get(ctx.guild.members, name=username)
                
                if member:
                    trial_end_date = datetime.utcnow() + timedelta(days=days)
                    User.create(ids=member.id, username=username , trial_expiration=trial_end_date)
                    await ctx.send(f"User has been added to members. Username: {username}, User ID: {member.id} ")
                else:
                    await ctx.send(f"Error: User {username} not found in the server")
            except Exception as e:
                print("Error:", e)
                await ctx.send("An error occurred while adding the user to the database")
        else:
            await ctx.send('Really?')
    @database.command()
    async def delete(self, ctx, username: str):
        if ctx.author.guild_permissions.administrator == True:
            try:
                print("Delete command triggered")  # Debugging print
                user = User.select(User.username, User.ids).where(User.username == username).get()
                user_id = user.ids  # Retrieve the user's ID
                user.delete_instance()  # Delete the user from the database
                await ctx.send(f"User {username} (ID: {user_id}) has been removed")
            except User.DoesNotExist:
                await ctx.send("User does not exist in the database")
        else:
            await ctx.send('Really?')

    @database.command()
    async def members(self , ctx):
        query = User.select()
        userList = []
        for user in query:
            userList.append(f"{user.username} : {user.trial_expiration}")
        user_list_str = '\n'.join(userList)
        embed = discord.Embed(title="**List of Users**" ,description=f"**{user_list_str}\n**")
        await ctx.send(embed=embed)




    def check_expired_users(self):
        current_time = datetime.utcnow()
        expired_users = User.select().where(User.trial_expiration < current_time)
        for user in expired_users:
            user.delete_instance()
            print(f"User {user.username} (ID: {user.ids}) has been removed due to trial expiration.")

    @tasks.loop(minutes=1)
    async def check_expire(self):
        self.check_expired_users()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed( title="👋 Welcome to the Kiocrypto Bot Community! 🤖",color=discord.Color.blue() , description="""**We're thrilled to have you on board. Get ready to supercharge your crypto trading journey with us. 🚀

Explore the latest crypto signals, expert analysis, and insider tips. Our AI-powered bot is here to help you make informed decisions and thrive in the world of cryptocurrency.

Feel free to introduce yourself, ask questions, or dive right into the action. We're a friendly bunch here, and we're always excited to connect with fellow crypto enthusiasts.

If you have any questions or need assistance, don't hesitate to reach out. Type !help to get started and discover all the exciting features CryptoTrader Bot has to offer.

Happy trading, and may your crypto adventures be profitable! 💰💎

Cheers,
Kiloprypto Bot 🤖**""").set_image(url='https://media.discordapp.net/attachments/1132933928802586674/1157314113349894304/brandmark-design_5.png?ex=65182842&is=6516d6c2&hm=b576255cad095cb009714d0bd3cad6da4bcc864601dacc6b3978928eb6a4ea88&=&width=605&height=403')
        await member.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CheckOut(bot))
