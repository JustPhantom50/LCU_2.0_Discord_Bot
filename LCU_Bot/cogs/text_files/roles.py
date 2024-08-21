import discord
from discord.ext import commands
import time
from cogs.utils.checks import getInfo, checks, getColor, convertEmbed, get_embed_info
from cogs.events import db

class roles(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    
  @commands.hybrid_command(description="This command is used to promote any staff members who require a promotion.", with_app_command = True, extras={"category": "Infractions"})
  @commands.check(checks.check2)
  async def promote(self, ctx: commands.Context, member: discord.Member, role: discord.Role, *, reason: str = "None Was Specified"):
    await ctx.defer(ephemeral = False)
     
    guild_info = await getInfo(ctx)

    bot_member = ctx.guild.get_member(self.bot.user.id)
    top_role = discord.utils.get(ctx.guild.roles, id=bot_member.top_role.id)
    if top_role.position <= role.position:
        em = discord.Embed(title="", description="My top role is below the role your trying to promote to!")
        return await ctx.send(embed=em)
    elif ctx.author == member:
        em = discord.Embed(title="", description="You can't do that, your trying to promote yourself!")
        return await ctx.send(embed=em)
    elif ctx.author.top_role.position <= role.position:
        em = discord.Embed(title=f"{ctx.author.top_role.position} and {role.position}", description="Please make sure your top role is higher than the one your trying to add!")
        return await ctx.send(embed=em)
    elif ctx.author.top_role.position <= member.top_role.position:
        em = discord.Embed(title="", description="Your trying to promote someone that has the same or higher rank than you do!")
        return await ctx.send(embed=em)
    elif role in member.roles:
        em = discord.Embed(title="", description=f"{member.mention} already has {role.mention}.")
        return await ctx.send(embed=em)
    else:
        timestamp = int(time.time())
    
        await db.promos.insert_one({
          'user_id': member.id,
          'promo_reason': reason,
          'moderator': ctx.author.id,
          'promo_role_id': role.id,
          'guild_id': ctx.guild.id
        })
        embed_info = await get_embed_info(ctx, 'promote')

        newDescription = await convertEmbed(ctx, embed_info[0], embed_info[2], embed_info[3], embed_info[5], guild_info, timestamp, "promote")

        await member.add_roles(role)
        try:
          em = discord.Embed(title=f"{newDescription[1]}", description=f"{newDescription[0]} \n\n> **Username:** {member.mention}\n> **Reason:** {reason}\n> **Role:** {role.mention}\n> **Server**: {ctx.guild.name} \n > **Submission Date:** <t:{timestamp}:F>", color=await getColor(ctx, "promote_color"))
        except Exception as e:
          raise commands.CommandInvokeError(e)
        if embed_info[4]:
          em.set_author(name=newDescription[3], icon_url=embed_info[4])

        if embed_info[3]:
          em.set_footer(text=newDescription[2])
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
    
  @promote.error
  async def promote_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MessageNotFound):
      pass
    elif isinstance(error, commands.MissingPermissions):
      return await ctx.send("I don't have the required permissions!")
    elif isinstance(error, commands.MissingRequiredArgument):
      return await ctx.send("Please make sure you have a member, role, than a reason. Example: `-promote @person @mod Good Job`")
    elif isinstance(error, commands.BadArgument):
      return await ctx.send("Please make sure you have a member, role, than a reason. Example: `-promote @person @mod Good Job`")
    elif ctx.guild.me.guild_permissions.manage_roles is False:
       return await ctx.send("I need permission to manage roles.")

  @commands.hybrid_command(description="This command is used to search a users promotions (e.g -search_promos @user)", with_app_command = True, extras={"category": "Infractions"})
  @commands.check(checks.check1)
  async def search_promos(self, ctx: commands.Context, member: discord.Member):
    await ctx.defer(ephemeral = False)
     
    
    records_yguilds = db.promos.find({'guild_id': {'$exists': True}, 'user_id': member.id})
    records_nguilds = db.promos.find({'guild_id': {'$exists': False}, 'user_id': member.id})
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
      em = discord.Embed(title=f"", description=f"{member.mention} is not in our database", color=discord.Color.from_rgb(255, 255, 254))
      return await ctx.send(embed=em)

    em = discord.Embed(title=f"{member}", description=f"These are the users promotions", color=discord.Color.from_rgb(255, 255, 254))
    counter = 0
    for warn in result:
      counter += 1
      role = discord.utils.get(ctx.guild.roles, id=int(warn['promo_role_id']))
      em.add_field(name=f"Promotion: {counter}", value=f"Role: {role.mention}\nReason: {warn['promo_reason']}\nModerator: <@{int(warn['moderator'])}>")
    await ctx.send(embed=em)


    try:
      await ctx.message.delete()
    except:
      pass
    return

  @search_promos.error
  async def search_promos_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MessageNotFound):
      pass
    elif isinstance(error, commands.MissingPermissions):
      return await ctx.send("I don't have the required permissions!")
    elif isinstance(error, commands.MissingRequiredArgument):
      return await ctx.send("Please make sure you have a member. Example: `-search_promos @person`")
    elif isinstance(error, commands.BadArgument):
      return await ctx.send("Please make sure you have a member. Example: `-search_promos @person`")



  @commands.hybrid_command(description="This command is used to demote any staff members who require a demotion.", with_app_command = True, extras={"category": "Infractions"})
  @commands.check(checks.check2)
  async def demote(self, ctx: commands.Context, member: discord.Member, role: discord.Role, *, reason: str = "None Was Specified"):
    await ctx.defer(ephemeral = False)
     
    guild_info = await getInfo(ctx)
    guild = self.bot.get_guild(ctx.guild.id)
    bot_member = guild.get_member(self.bot.user.id)
    top_role = discord.utils.get(guild.roles, id=bot_member.top_role.id)
    if top_role.position <= role.position:
        em = discord.Embed(title="", description="My top role is below the role your trying to promote to!")
        return await ctx.send(embed=em)
    elif ctx.author == member:
        em = discord.Embed(title="", description="You can't do that, your trying to demote yourself!")
        return await ctx.send(embed=em)
    elif ctx.author.top_role.position <= role.position:
        em = discord.Embed(title="", description="Please make sure your top role is higher than the one your trying to remove!")
        return await ctx.send(embed=em)
    elif ctx.author.top_role.position <= member.top_role.position:
        em = discord.Embed(title="", description="Your trying to demote someone that has the same or higher rank than you do!")
        return await ctx.send(embed=em)
    else:
        if role not in member.roles:
          await member.add_roles(role)
        timestamp = int(time.time())
    
        await db.demos.insert_one({
          'user_id': member.id,
          'demo_reason': reason,
          'moderator': ctx.author.id,
          'demo_role_id': role.id,
          'guild_id': ctx.guild.id
        })
        embed_info = await get_embed_info(ctx, 'demote')

        newDescription = await convertEmbed(ctx, embed_info[0], embed_info[2], embed_info[3], embed_info[5], guild_info, timestamp, "demote")

        for r in reversed(member.roles):
          if r > role:
            try:
              await member.remove_roles(r)
            except Exception:
              pass

        em = discord.Embed(title=f"{newDescription[1]}", description=f"{newDescription[0]} \n\n> **Username:** {member.mention}\n> **Reason:** {reason}\n> **Role:** {role.mention}\n> **Server**: {ctx.guild.name} \n > **Submission Date:** <t:{timestamp}:F>", color=await getColor(ctx, "demote_color"))
        if embed_info[4]:
          em.set_author(name=newDescription[3], icon_url=embed_info[4])

        if embed_info[3]:
          em.set_footer(text=newDescription[2])
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
    
  @demote.error
  async def demote_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MessageNotFound):
      pass
    elif isinstance(error, commands.MissingPermissions):
      return await ctx.send("I don't have the required permissions!")
    elif isinstance(error, commands.MissingRequiredArgument):
      return await ctx.send("Please make sure you have a member, role, than a reason. Example: `-demote @person @mod Good Job`")
    elif isinstance(error, commands.BadArgument):
      return await ctx.send("Please make sure you have a member, role, than a reason. Example: `-demote @person @mod Good Job`")
    elif ctx.guild.me.guild_permissions.manage_roles is False:
       return await ctx.send("I need permission to manage roles.")

  @commands.hybrid_command(description="This command is used to search a users demotions (e.g -search_demos @user)", with_app_command = True, extras={"category": "Infractions"})
  @commands.check(checks.check1)
  async def search_demos(self, ctx: commands.Context, member: discord.Member):
    await ctx.defer(ephemeral = False)
     
    guild_info = await getInfo(ctx)
    records_yguilds = db.demos.find({'guild_id': {'$exists': True}, 'user_id': member.id})
    records_nguilds = db.demos.find({'guild_id': {'$exists': False}, 'user_id': member.id})
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
      em = discord.Embed(title=f"", description=f"{member.mention} is not in our database", color=discord.Color.from_rgb(255, 255, 254))
      return await ctx.send(embed=em)

    em = discord.Embed(title=f"{member}", description=f"These are the users demotions", color=discord.Color.from_rgb(255, 255, 254))
    counter = 0
    for warn in result:
      counter += 1
      role = discord.utils.get(ctx.guild.roles, id=int(warn['demo_role_id']))
      em.add_field(name=f"Demotion: {counter}", value=f"Role: {role.mention}\nReason: {warn['demo_reason']}\nModerator: <@{int(warn['moderator'])}>")
    await ctx.send(embed=em)

    try:
      await ctx.message.delete()
    except:
      pass
    return
  
  @search_demos.error
  async def search_demos_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MessageNotFound):
      pass
    elif isinstance(error, commands.MissingPermissions):
      return await ctx.send("I don't have the required permissions!")
    elif isinstance(error, commands.MissingRequiredArgument):
      return await ctx.send("Please make sure you have a member. Example: `-search_demos @person`")
    elif isinstance(error, commands.BadArgument):
      return await ctx.send("Please make sure you have a member. Example: `-search_demos @person`")

    


    
async def setup(bot):
  await bot.add_cog(roles(bot))