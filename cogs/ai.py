from discord.ext import commands, tasks
import discord
import requests
import json
from database_settings import User
class Ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai.start()
    @tasks.loop(hours=24)
    async def ai(self):
        url = 'https://www.chatbase.co/api/v1/chat'
        headers = {
            'Authorization': 'Bearer c2529c04-dfbc-4d81-8cae-84230518824c',
            'Content-Type': 'application/json'
        }
        data = {
            "messages": [
            {"content": f"How was the market and crypto today tell me about the prices and changes", "role": "user"}
            ],
            "chatbotId": "FZrg-dx5AkER0dUEpTRmo",
            "stream": False,
            "temperature": 0
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        json_data = response.json()

        if response.status_code == 200:
            query = User.select()
            for user in query:
                if user:
                    userDM = await self.bot.fetch_user(user)
                    await userDM.send(f"**{json_data['text']}**")

        else:
            print('Error:' + json_data['message'])

async def setup(bot):
    await bot.add_cog(Ai(bot))
