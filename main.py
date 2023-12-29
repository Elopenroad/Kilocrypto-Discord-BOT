import discord
from discord.ext import commands
import settings

intents = discord.Intents.all()
intents.reactions = True
intents.members =True
bot = commands.Bot(command_prefix='!' , intents=intents , help_command=None)

logger = settings.logging.getLogger("bot")


def run():
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        await bot.load_extension('cogs.checking')
        await bot.load_extension('cogs.help')
        await bot.load_extension('cogs.trade')

        await bot.tree.sync()


    bot.run(settings.DISOCRD_API_SECRET , root_logger=True)



if __name__ == "__main__":
    run()