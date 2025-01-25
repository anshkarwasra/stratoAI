



import discord
import json
from datetime import datetime,timezone
from discord.ext import commands, tasks
import httpx,base64
import io
from mira_sdk import CompoundFlow
from mira_sdk import MiraClient
import dotenv
import os 


dotenv.load_dotenv()




client = MiraClient(config={"API_KEY": os.getenv("DISCORD_BOT_KEY")})



version = "0.1.0"


if version:
    flow_name= f"anshkarwasra/discord-bot-file-generator/{version}"
else:
    flow_name = "anshkarwasra/discord-bot-file-generator"










class MyClient(commands.Bot):   
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # Set a custom status
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="for @mentions | Type @bot help"
        ))
    

    async def handleFileAttach(self,message,channel,response_text):
        """
            handels the file attachment
        """
        print(response_text[7:-2])
        jsonFormat = json.loads(response_text[7:-3])
        fileToAttach = discord.File(
            io.BytesIO(jsonFormat["content"].encode()),
            filename=f'{jsonFormat["fileName"]}.{jsonFormat['fileExtension']}'
        )
        response_embed = discord.Embed(
            description="the requested file is ready!",
            color=discord.Color.blurple(),
            
        )
        response_embed.set_footer(text=f"Requestd by {message.author.name}")
        await channel.send(file=fileToAttach,embed=response_embed)
    async def send_regular_response(self, message, channel, response_text):
        """Handle regular text responses"""
        response_embed = discord.Embed(
            description=response_text,
            color=discord.Color.green()
        )
        response_embed.set_footer(text=f"Requested by {message.author.name}")
        await channel.send(
            f"{message.author.mention}",
            embed=response_embed
        )

    async def on_message(self, message):
        if self.user == message.author:  # Ignore self messages
            return

        channel = message.channel
        error_log_channel = self.get_channel(1261997710265946182)
        
        if self.user in message.mentions:
            user_message = message.content[21:]
            
            

            # Handle help command
            tempMessage = user_message.strip()
            if tempMessage.lower()[3:] == "help":
                help_embed = discord.Embed(
                    title="Bot Help",
                    description="Here's how to use me:",
                    color=discord.Color.blue()
                )
                help_embed.add_field(
                    name="Basic Usage", 
                    value="Just mention me (@bot) followed by your question/prompt",
                    inline=False
                )
                help_embed.add_field(
                    name="Examples",
                    value="• @bot What is quantum computing?\n• @bot Write a poem about space",
                    inline=False
                )
                await channel.send(embed=help_embed)
                return

           

            # Show typing indicator while processing
            async with channel.typing():
                try:
                    # Handle empty messages
                    if not user_message:
                        await channel.send(f"{message.author.mention} Please provide a message along with the mention!")
                        return

                    print(f"Processing request from {message.author}: {user_message}")
                
                    response = client.flow.execute(flow_name,{
                        'user_message': user_message
                    })
                    if(response['first_flow']):
                        await self.handleFileAttach(message,channel,response['second_flow'])
                    else:
                        await self.send_regular_response(message, channel, response['second_flow'] )

                except Exception as e:
                    error_data = {
                        "status": "error",
                        "message": str(e),
                        "text": "an error occurred in your genAI's backend please resolve it asap",
                        "user": str(message.author),
                        "channel": str(channel),
                        "prompt": user_message,
                        "timestamp": str(message.created_at)
                    }
                    
                    await channel.send(json.dumps(error_data, indent=2))
                    await channel.send(
                        f"{message.author.mention} Sorry, I encountered an error. Please try again later."
                    )
    
    

   



intents = discord.Intents.default()
intents.messages = True

bot = MyClient(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run('MTMzMjUyMDg0ODc3MDMzNDc1MQ.GRvMp5.tlKPwGknyAuNLRPdj_FKdJnEqmpy1VILLFmFGM')