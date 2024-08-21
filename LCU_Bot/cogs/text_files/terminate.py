import discord
from discord.ext import commands
import time
from cogs.utils.checks import getInfo, checks, getColor
from cogs.events import db

class terminate(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Terminate a staff member", with_app_command = True, extras={"category": "Infractions"})
    @commands.check(checks.check2)
    async def terminate(self, ctx: commands.Context, member: discord.Member, *, reason: str):
        await ctx.defer(ephemeral=False)
         
        guild_info = await getInfo(ctx)
        

        if ctx.author == member:
            em = discord.Embed(title="", description="If you want to terminate yourself go ahead, I will not allow it!") #:skull:
            return await ctx.send(embed=em)
        else:
            timestamp = int(time.time())
            doc = {
                'user_id': member.id,
                'term_reason': reason, 
                'moderator': ctx.author.id,
                'guild_id': ctx.guild.id
            }
            await db.terminations.insert_one(doc)
            
            em = discord.Embed(title=f"{guild_info['emoji_id']} Staff Termination", description=f"You have been terminated by the HR Team in **{ctx.guild.name}**. \n\n> **Username:** {member.mention}\n> **Reason:** {reason}\n > **Submission Date:** <t:{timestamp}:F>", color=await getColor(ctx, "demote_color"))
            #em.set_footer(text=f"Your Punishment ID is: {warn_id}")
            await ctx.send(embed=em)
            try:
                await member.send(embed=em)
            except Exception:
                await ctx.send("I can't send a message to this user!")
            try:
                await ctx.message.delete()
            except:
                pass
            return
        
    @commands.hybrid_command(description="This command is used to search a users terminations (e.g -search_terminations @user)", with_app_command = True, extras={"category": "Infractions"})
    @commands.check(checks.check1)
    async def search_terminations(self, ctx: commands.Context, member: discord.Member):
        await ctx.defer(ephemeral = False)
         
         
        records_yguilds = db.terminations.find({'guild_id': {'$exists': True}, 'user_id': member.id})
        records_nguilds = db.terminations.find({'guild_id': {'$exists': False}, 'user_id': member.id})
        result = []
        async for record in records_nguilds:
            result.append(record)

        async for item in records_yguilds:
            key = item["guild_id"]
            if int(key) == int(ctx.guild.id):
                result.append(item)
            else:
                pass

        if not records_yguilds and not records_nguilds:
            em = discord.Embed(title="", description=f"{member.mention} has no terminations.")
            return await ctx.send(embed=em)

        em = discord.Embed(title=f"{member}", description=f"{member}'s Terminations", color=discord.Color.from_rgb(255, 255, 254))
        counter = 0
        for warn in result:
            counter += 1
            em.add_field(name=f"Termination {counter}", value=f"Reason: {warn['term_reason']}\nModerator: <@{int(warn['moderator'])}>")
        await ctx.send(embed=em)

        try:
            await ctx.message.delete()
        except:
            pass
        return
    
    @terminate.error
    async def terminate_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MessageNotFound):
            pass
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send("I don't have the required permissions!")
        


async def setup(bot):
    await bot.add_cog(terminate(bot))