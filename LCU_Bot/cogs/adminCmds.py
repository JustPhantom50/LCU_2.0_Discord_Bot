import discord
from discord.ext import commands
from discord.ui import View
from cogs.utils.checks import check_if_it_is_me, send_message
import typing
import json
from cogs.events import db
from typing import cast

class admincmd(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    @commands.check(check_if_it_is_me)
    async def testing(self, ctx: commands.Context, command=None):
        with open("cogs/data/stafflogins.json", "r") as stafflogin:
            data = json.load(stafflogin)


        for user in data:
            user = user.values()
            print(user)


        
   


    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    async def check_setup(self, ctx: commands.Context, *, id: int):
        try:
            server = self.bot.get_guild(1000207936204836965)
            role1 = discord.utils.get(server.roles, id=1059547821101023242)
            role2 = discord.utils.get(server.roles, id=1059547830680813710)
            role3 = discord.utils.get(server.roles, id=1059547839228821584)
            role4 = discord.utils.get(server.roles, id=1059547824141906042)
        except:
            server = self.bot.get_guild(1073712961253818459)
            role1 = discord.utils.get(server.roles, id=1073713086600577064)
            role2 = discord.utils.get(server.roles, id=1073713821132279808)
            role3 = discord.utils.get(server.roles, id=1073713653691457637)
        if role1 in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles or role4 in ctx.author.roles:
            records = await db.setup.find_one({"guild_id": id}, {"_id": 0})

            records2 = await db.embeds.find_one({"guild_id": id}, {"_id": 0})

            records3 = await db.settings.find_one({"guild_id": id}, {"_id": 0})
            if records == None:
                return await ctx.send("This server has not been setup yet!")
            em = discord.Embed(title=f"Setup for: {str(id)}", description="")
            em2 = discord.Embed(title=f"Embeds for: {str(id)}", description="")
            em3 = discord.Embed(title=f"Settings for: {str(id)}", description="")
            em4 = discord.Embed(title=f"Advertisement for: {str(id)}", description="")
            for record in records.items():
                if record[0] != "advertisement":
                    em.add_field(name=record[0], value=record[1])
                else:
                    em4.description = f"```{record[1]}```"
                

            for record in records2.items():
                em2.add_field(name=record[0], value=record[1])

            for record in records3.items():
                em3.add_field(name=record[0], value=record[1])
            
            await ctx.send(embed=em)
            await ctx.send(embed=em2)
            await ctx.send(embed=em3)
            try:
                await ctx.send(embed=em4)
            except:
                await ctx.send("Advertisement is too long to send in a message.")
        else:
            return

    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    @commands.check(check_if_it_is_me)
    async def devdm(self, ctx, member: discord.Member, *, message):
        em = discord.Embed(title="Development Notification", description=message)
        try:
            await member.send(embed=em)
            await ctx.send("sent")
        except:
            await ctx.send("I cant send dms to this person!")

    #This command is not to be touched by anyone or face infractions
    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    @commands.is_owner()
    async def sync(self, ctx, *, msg: typing.Optional[int] = None):
        if msg is None:
            await ctx.bot.tree.sync()
        else:
            await ctx.bot.tree.sync(guild=discord.Object(id = msg))
        await ctx.send(f"commands are synced")

    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    @commands.check(check_if_it_is_me)
    async def blacklist(self, ctx: commands.Context, member: discord.Member):

        member = self.bot.get_user(member)
        record = db.blacklists.find_one({"user_id": member})
        if ctx.author.id == member:
            return await ctx.send("You cannot blacklist yourself!")
        if record is None:
            await db.blacklists.insert_one({"user_id": member})
            await ctx.send(f"Blacklisted {member.mention}.")
        else:
            await ctx.send(f"{member.mention} is already blacklisted.")
        

    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    @commands.check(check_if_it_is_me)
    async def unblacklist(self, ctx: commands.Context, member: discord.Member):
        with open('cogs/data/blacklists.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        if member.id not in data['blacklisted_members']:
            await ctx.send(f"{member} is already not blacklisted.")
            return
        # Remove the new member ID in the data dictionary
        data["blacklisted_members"].remove(member.id)
        with open('cogs/data/blacklists.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        await ctx.send(f"Unblacklisted {member}.")
    
async def setup(bot):
    await bot.add_cog(admincmd(bot))