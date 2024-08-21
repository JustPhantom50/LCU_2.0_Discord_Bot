
import discord
from discord.ext import tasks, commands
import datetime
import time
from discord.ext.commands.context import Context
import motor.motor_asyncio
import json
from dotenv import load_dotenv
load_dotenv()
import os

MONGO_URL = os.getenv('MONGO_URL')

# client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://lcuAdmin:wIlMckypCCOGfGO5@serverlessinstance0.82popmp.mongodb.net/?retryWrites=true&w=majority")
# db = client['lcu_db']

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client['lcu_db']


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(minutes = 1)
    async def checkLogin(self):
        timeNow = round(time.time())
        # print('Checking')
        with open("stafflogins.json", "r") as stafflogin:
            data = json.load(stafflogin)


        
        # user = user.items()
        keys = data.keys()
        values = data.values()
        for user in keys:
        
            if data['logged-in']:
                if (int(timeNow) - int(data['logged-in-at'])) >= 600:
                    data['logged-in'] = False
                    data['logged-in-at'] = None
                    with open("stafflogins.json", "w", encoding = "utf-8") as f:
                        json.dump(data, f, ensure_ascii = False, indent = 4)

                    user = self.bot.get_user(int(data['user_id']))
                    await user.send(f"You have been logged out due to your session time ending <t:{timeNow}:R>.")
                else:
                    pass
            else:
                pass

    @tasks.loop(minutes=1)
    async def check_loa_end_date(self):
        all_loas = db.loa.find()
        async for loa_findone in all_loas:
            if not loa_findone['start_date']:
                return
            else:
                current_time = datetime.datetime.now()
                if current_time > loa_findone['end_date']:
                    guild = self.bot.get_guild(loa_findone["guild_id"])
                    if guild:
                        member = guild.get_member(loa_findone["author_id"])
                        if member:
                            loadmembed = discord.Embed(title='Your LOA has expired')
                            await member.send(embed=loadmembed)

                            config = await db.settings.find_one({'guild_id': guild.id})
                            if config and 'loa_channel' in config:
                                channel = self.bot.get_channel(config['loa_channel'])
                                channelembed = discord.Embed(
                                    title='Leave Of Absence Ended',
                                    description=f"Started: {discord.utils.format_dt(loa_findone['start_date'])}\n Ended: {discord.utils.format_dt(loa_findone['end_date'])}\n Reason: {loa_findone['reason']}"
                                )
                                await channel.send(embed=channelembed)

                            await db.overall_loa.insert_one({
                                '_id': loa_findone['_id'],
                                'start_date': loa_findone['start_date'],
                                'end_date': loa_findone['end_date'],
                                'guild_id': guild.id,
                                'user_id': member.id
                            })
                            await db.loa.delete_one({'_id': loa_findone['_id']})

                            role = await db.settings.find_one({'guild_id': guild.id})
                            if role and 'loa_role' in role:
                                loa_role = guild.get_role(role['loa_role'])
                                if loa_role:
                                    await member.remove_roles(loa_role)

    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context):
        if ctx.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(ctx) and len(ctx.content.split(' ')) == 1 and ctx.content[-1] == ">" and ctx.content[0] == '<':
            await ctx.channel.send("My prefix is `-`\nTry `-help` for help with commands\nTry `-setup` to setup the bot")

        

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await guild.chunk()
        channel = self.bot.get_channel(1073714276138766336)

        em = discord.Embed(title=f"Bot Joining Logs", description=f"Guild Name: **{guild}**\nGuild ID: **{guild.id}**\nMember Count: **{guild.member_count}**\nGuild Count: **{str(len(self.bot.guilds))}**")
        await channel.send(embed=em)

        
        # Send a message to the top channel
        em = discord.Embed(title="Thank You For Adding LCU!", description=f"LCU is a fully customizable Emergency Response : Liberty County. We allow you to do such things as sessions, shutdowns, and session votes\n\nSupport server: https://discord.gg/EvcYNK53MC\nSetup Command: `-setup`\nHelp Command: `-help`", color=discord.Color.blue())
        for channel in guild.text_channels:
            try:
                await channel.send(embed=em)
                break
            except:
                pass


    @commands.Cog.listener()
    async def on_ready(self, ctx: commands.Context = None):
        self.check_loa_end_date.start()
        self.bot.uptime = int(time.time())
        self.bot.blacklists = db.blacklists.find()
        self.checkLogin.start()
        await self.bot.change_presence(activity=discord.Activity(name="-help | lcubot.xyz", type=discord.ActivityType.watching))
        
    
        print(self.bot.user.name + " is ready.")
        
    

    
async def setup(bot):
  await bot.add_cog(events(bot))


