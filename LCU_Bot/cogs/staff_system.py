import discord
from discord.ext import commands
import json
from cogs.utils.checks import check_if_it_is_me
import time

class staff(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    async def staff_login(self, ctx, password: str):
        await ctx.message.delete()
        
        try:
            server = self.bot.get_guild(1000207936204836965)
            role1 = discord.utils.get(server.roles, id=1059547821101023242)
            role2 = discord.utils.get(server.roles, id=1059547830680813710)
            role3 = discord.utils.get(server.roles, id=1142917690055471124)
            role4 = discord.utils.get(server.roles, id=1059547840839417907)
        except:
            server2 = self.bot.get_guild(1073712961253818459)
            role1 = discord.utils.get(server2.roles, id=1073713086600577064)
            role2 = discord.utils.get(server2.roles, id=1073713821132279808)
            role3 = discord.utils.get(server2.roles, id=1073713653691457637)
        if role1 in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles or role4 in ctx.author.roles or ctx.author.id == 676895030094331915 or ctx.author.id == 1117952814044434442:
            pass
        else:
            return

        with open("cogs/data/stafflogins.json", "r") as stafflogin:
            data = json.load(stafflogin)

        
        if str(ctx.author.id) in data:
            if data[str(ctx.author.id)]["password"] == str(password):
                data[str(ctx.author.id)]['logged-in'] = True
                data[str(ctx.author.id)]['logged-in-at'] = int(round(time.time()))
                with open("cogs/data/stafflogins.json", "w", encoding = "utf-8") as f:
                    json.dump(data, f, ensure_ascii = False, indent = 4)
                return await ctx.author.send(f"Successfully logged in.")
            else:
                return await ctx.author.send(f"Invalid password.")
        else:
            pass

        
        
    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    @commands.check(check_if_it_is_me)
    async def create_user(self, ctx: commands.Context, memberID: int, password: str, type: str):
        await ctx.message.delete()
        with open("cogs/data/stafflogins.json", 'r') as stafflogin:
            data = json.load(stafflogin)
        
        if str(memberID) in data:
            return await ctx.send("This person is already an existing staff member.")
        
        data[memberID] = {}
        data[memberID]['user_id'] = memberID
        data[memberID]['password'] = password
        data[memberID]['type'] = type
        data[memberID]['logged-in'] = False
        data[memberID]['logged-in-at'] = None

        with open('cogs/data/stafflogins.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        await ctx.send(f"New staff member with ID {memberID} created successfully.")


    
    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    @commands.check(check_if_it_is_me)
    async def remove_staff(self, ctx: commands.Context, user_id):
        await ctx.message.delete()
        with open('cogs/data/stafflogins.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        if f"{user_id}" in data:
            
            del data[user_id]
        else:
            return await ctx.send(f"{user_id} is not in the staff list")
        with open('cogs/data/stafflogins.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        await ctx.send(f"removed **{user_id}**.")
    
    @commands.command(description="This is a staff command", extras={"category": "Staff"})
    @commands.check(check_if_it_is_me)
    async def force_logout(self, ctx: commands.Context, user_id):
        with open('cogs/data/stafflogins.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        if f"{user_id}" in data:
            if data[user_id]['logged-in'] == False:
                return await ctx.send("user is already logged out")
            data[user_id]['logged-in'] = False
            data[user_id]['logged-in-at'] = None
        else:
            return await ctx.send(f"{user_id} is not in our database.")
        
        user = self.bot.get_user(int(user_id))
        
        with open('cogs/data/stafflogins.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        try:
            await ctx.user.send(f"{user_id} you are now logged out of LCU Staff System by force!")
        except:
            pass
        await ctx.send(f"{user_id} is now logged out.")
            



async def setup(bot):
    await bot.add_cog(staff(bot))