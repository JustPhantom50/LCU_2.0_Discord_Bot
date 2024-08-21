import discord
from discord.ext import commands
from discord.ui import View, Button, Select
from discord import Interaction
from cogs.utils.checks import is_management, getColor
from cogs.utils.modals import MAdvert, MCode, MEmoji, MReminderText, MServerName, MServerOwner, MSessionBanner, MShutdownBanner, MVotes, MSVoteBanner
from cogs.events import db

class config(commands.Cog):
    def __init__ (self, bot):
      self.bot = bot
      self.staff_roles_returns = []

    @commands.hybrid_command(description="This will allow you to reconfigure specific features within LCU to your liking!", with_app_command = True, extras={"category": "Other"})
    @is_management()
    async def config(self, ctx: commands.Context):
      await ctx.defer(ephemeral = False)
       
       
      #------------------------------------------------------
      usr = ctx.author.id
      chn = ctx.channel.id

      async def callback1(ctx: Interaction):
        if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)

        if select_menu1.values[0] == "1":
          await ctx.response.send_modal(MSessionBanner())
          return
        elif select_menu1.values[0] == "2":
          await ctx.response.send_modal(MShutdownBanner())
          return
        elif select_menu1.values[0] == "5":
          await ctx.response.send_modal(MSVoteBanner())
          return
        elif select_menu1.values[0] == "3":
          await ctx.response.send_modal(MEmoji())
          return
      #---------------------------------------------------
          

      async def callback2(ctx: Interaction):
        if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
        staff_roles_returns = []
        manage_roles_returns = []
        mod_roles_returns = []
        async def role1callback(ctx: Interaction):
          for role in select_role1.values:
            cstaff_Roles = discord.utils.get(ctx.guild.roles, name=str(role))
            staff_roles_returns.append(cstaff_Roles.id)
          await db.setup.update_one(
              {'guild_id': ctx.guild.id},
              {'$set': {'staff_roles_id': str(staff_roles_returns)}}
          )
          try:
            await ctx.message.delete()
          except:
            pass
          await ctx.response.send_message(content = f"Your staff roles have been updated.", ephemeral=True)

        async def role2callback(ctx: Interaction):
          if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
          
          for role in select_role2.values:
            cmanage_Roles = discord.utils.get(ctx.guild.roles, name=str(role))
            manage_roles_returns.append(cmanage_Roles.id)
          
          await db.setup.update_one(
            {'guild_id': ctx.guild.id},
            {'$set': {'management_roles_id': manage_roles_returns}}
          )
          try:
            await ctx.message.delete()
          except:
            pass
          await ctx.response.send_message(content = f"Your management roles have been updated.", ephemeral=True)

        async def role3callback(ctx: Interaction):
          if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
          shift_role = discord.utils.get(ctx.guild.roles, name=str(select_role3.values[0]))
          
          await db.setup.update_one(
            {'guild_id': ctx.guild.id},
            {'$set': {'session_role_id': shift_role.id}}
          )
          try:
            await ctx.message.delete()
          except:
            pass
          await ctx.response.send_message(content = f"Your session role has been updated.", ephemeral=True)

        async def channel1callback(ctx: Interaction):
          if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
          shift_channel = discord.utils.get(ctx.guild.channels, name=str(select_channel1.values[0]))
          
          await db.setup.update_one(
            {'guild_id': ctx.guild.id},
            {'$set': {'m_command_channel': shift_channel.id}}
          )
          try:
            await ctx.message.delete()
          except:
            pass
          await ctx.response.send_message(content = f"Your reminder command channel has been updated.", ephemeral=True)
          
          
        async def channel2callback(ctx: Interaction):
          if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
          shift_channel = discord.utils.get(ctx.guild.channels, name=str(select_channel2.values[0]))
          await db.setup.update_one(
              {'guild_id': ctx.guild.id},
              {'$set': {'ping_channel': str(shift_channel.id)}}
          )
          try:
            await ctx.message.delete()
          except:
            pass
          await ctx.response.send_message(content = f"Your staff request channel has been updated.", ephemeral=True)

        async def role4callback(ctx: Interaction):
          if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
          shift_role = discord.utils.get(ctx.guild.roles, name=str(select_role4.values[0]))
          
          await db.setup.update_one(
            {'guild_id': ctx.guild.id},
            {'$set': {'on_shift_role': shift_role.id}}
          )
          try:
            await ctx.message.delete()
          except:
            pass
          await ctx.response.send_message(content = f"Your on duty staff role has been updated.", ephemeral=True)
        async def role5callback(ctx):
          if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
          for role in select_role1.values:
            cmanage_Roles = discord.utils.get(ctx.guild.roles, name=str(role))
            mod_roles_returns.append(cmanage_Roles.id)
          await db.setup.update_one(
              {'guild_id': ctx.guild.id},
              {'$set': {'mod_roles_id': str(mod_roles_returns)}}
          )
          try:
            await ctx.message.delete()
          except:
            pass
          await ctx.response.send_message(content = f"Your moderation roles have been updated.", ephemeral=True)
          

        if select_menu2.values[0] == "1":
          
          em = discord.Embed(title=f"Please select your staff roles (Do not select your 'Management roles')", description=f"You can select up to 20 roles.", color=await getColor(ctx, "commands_color"))
          select_role1 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=10)
          select_role1.callback = role1callback
          view=View()
          view.add_item(select_role1)
          await ctx.response.send_message(embed = em, view=view)
          await self.bot.wait_for('interaction', timeout=None, check=lambda message: message.user == ctx.user and message.channel == ctx.channel)
          return
        elif select_menu2.values[0] == "2":
          em = discord.Embed(title=f"Please select your management roles (Do not select your 'Staff roles')", description=f"You can select up to 20 roles.", color=await getColor(ctx, "commands_color"))
          select_role2 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=10)
          select_role2.callback = role2callback
          view=View()
          view.add_item(select_role2)
          await ctx.response.send_message(embed = em, view=view)
          await self.bot.wait_for('interaction', check=lambda message: message.user == ctx.user and message.channel == ctx.channel)
          return
        elif select_menu2.values[0] == "3":
          em = discord.Embed(title=f"Please select you SSU/Session ping role.", description=f"This is the role that is pinged for Server Start Ups.", color=await getColor(ctx, "commands_color"))
          select_role3 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=1)
          select_role3.callback = role3callback
          view=View()
          view.add_item(select_role3)
          await ctx.response.send_message(embed = em, view=view)
          await self.bot.wait_for('interaction', check=lambda message: message.user == ctx.user and message.channel == ctx.channel)
          return
        elif select_menu2.values[0] == "4":
          em = discord.Embed(title=f"Reminder Channel", description=f"This channel will be used when reminder command is on.", color=await getColor(ctx, "commands_color"))
          select_channel1 = discord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
          select_channel1.callback = channel1callback
          view=View()
          view.add_item(select_channel1)
          await ctx.response.send_message(embed = em, view=view)
          await self.bot.wait_for('interaction', check=lambda message: message.user == ctx.user and message.channel == ctx.channel)
          return
        elif select_menu2.values[0] == "5":
          em = discord.Embed(title=f"Please select your staff request channel.", description=f"This channel will be used when a staff request is sent.", color=await getColor(ctx, "commands_color"))
          select_channel2 = discord.ui.ChannelSelect(placeholder="Select A Channel", min_values=1, max_values=1)
          select_channel2.callback = channel2callback
          view=View()
          view.add_item(select_channel2)
          await ctx.response.send_message(embed = em, view=view)
          await self.bot.wait_for('interaction', check=lambda message: message.user == ctx.user and message.channel == ctx.channel)
          return
        elif select_menu2.values[0] == "6":
          em = discord.Embed(title=f"Please select your on duty staff role.", description=f"The role used for when a staff member is on shift/duty.", color=await getColor(ctx, "commands_color"))
          select_role4 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=1)
          select_role4.callback = role4callback
          view=View()
          view.add_item(select_role4)
          await ctx.response.send_message(embed = em, view=view)
          await self.bot.wait_for('interaction', check=lambda message: message.user == ctx.user and message.channel == ctx.channel)
          return
        elif select_menu2.values[0] == "7":
          em = discord.Embed(title=f"Moderation Roles", description=f"Can be 1-20 roles.", color=await getColor(ctx, "commands_color"))
          select_role1 = discord.ui.RoleSelect(placeholder="Select A Role", min_values=1, max_values=20)
          select_role1.callback = role5callback
          view=View()
          view.add_item(select_role1)
          await ctx.response.send_message(embed = em, view=view)
          await self.bot.wait_for('interaction', timeout=None, check=lambda message: message.user == ctx.user and message.channel == ctx.channel)
          return
      #---------------------------------------------------
      async def callback3(ctx: Interaction):
        if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
        if select_menu3.values[0] == "1":
          await ctx.response.send_modal(MServerName())
          return
        elif select_menu3.values[0] == "2":
          await ctx.response.send_modal(MServerOwner())
          return
        elif select_menu3.values[0] == "3":
          await ctx.response.send_modal(MCode())
          return
        elif select_menu3.values[0] == "4":
          await ctx.response.send_modal(MReminderText())
          return
        elif select_menu3.values[0] == "5":
          await ctx.response.send_modal(MVotes())
          return
        elif select_menu3.values[0] == "6":
          await ctx.response.send_modal(MAdvert())
          return
        
      #-----------------------------------------------------
      em = discord.Embed(title="Reconfiguration", description="Here you can reconfigure the setup for LCU.\n\n**Graphics** - Banners and emojis\n**Roles and Channels** - Roles and channels for staff\n**Server Information** - In-Game information, votes, advertisements", color=await getColor(ctx, "commands_color"))
      
      button = Button(label="Graphics", style=discord.ButtonStyle.grey)
      button2 = Button(label="Roles & Channels", style=discord.ButtonStyle.grey)
      button3 = Button(label="Server Info", style=discord.ButtonStyle.grey)

      select_menu1 = Select(placeholder="Graphics", options=[
        discord.SelectOption(label="Session Banner", value="1", description="Change the session banner"),
        discord.SelectOption(label="Shutdown Banner", value="2", description="Change the shutdown banner"),
        discord.SelectOption(label="Svote Banner", value="5", description="Change the svote banner"),
        discord.SelectOption(label="Emoji", value="3", description="Change the emoji"),
      ])

      select_menu2 = Select(placeholder="Roles and Channels", options=[
        discord.SelectOption(label="Moderation Roles", value="7", description="Change the moderation roles"),
        discord.SelectOption(label="Staff Roles", value="1", description="Change the staff roles"),
        discord.SelectOption(label="Management Roles", value="2", description="Change the management roles"),
        discord.SelectOption(label="Session Role", value="3", description="Change the session role"),
        discord.SelectOption(label="On Shift Role", value="6", description="Change the on shift role"),
        discord.SelectOption(label="M Reminder Channel", value="4", description="Change the m reminder channel"),
        discord.SelectOption(label="Staff Request Channel", value="5", description="Change the staff request channel"),
      ])

      select_menu3 = Select(placeholder="Server Information", options=[
        discord.SelectOption(label="Server Name", value="1", description="Change the server roblox name"),
        discord.SelectOption(label="Server Owner", value="2", description="Change the server roblox owner"),
        discord.SelectOption(label="Code", value="3", description="Change the server roblox code"),
        discord.SelectOption(label="M Reminder Text", value="4", description="Change the m reminder text"),
        discord.SelectOption(label="Votes", value="5", description="Change the number of votes needed for svote"),
        discord.SelectOption(label="Advertisement", value="6", description="Change the advertisement"),
      ])

      button4 = Button(label="Back", style=discord.ButtonStyle.red)
      usr = ctx.author.id
      chn = ctx.channel.id
      async def callback4(ctx: Interaction):
        if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
        em = discord.Embed(title="Reconfiguration", description="Here you can reconfigure your graphics.", color=await getColor(ctx, "commands_color"))
      
        select_menu1.callback = callback1
        view = View()
        view.add_item(select_menu1)
        view.add_item(button4)
        try:
          await ctx.response.edit_message(embed=em, view=view)
        except Exception:
          pass

      async def callback5(ctx: Interaction):
        if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
        em = discord.Embed(title="Reconfiguration", description="Here you can reconfigure your roles and channels.", color=await getColor(ctx, "commands_color"))

        select_menu2.callback = callback2
        view = View()
        view.add_item(select_menu2)
        view.add_item(button4)
        try:
          await ctx.response.edit_message(embed=em, view=view)
        except Exception:
          pass

      async def callback6(ctx: Interaction):
        if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
        em = discord.Embed(title="Reconfiguration", description="Here you can reconfigure your server information.", color=await getColor(ctx, "commands_color"))

        select_menu3.callback = callback3
        view = View()
        view.add_item(select_menu3)
        view.add_item(button4)
        try:
          await ctx.response.edit_message(embed=em, view=view)
        except Exception:
          pass

      async def callback7(ctx: Interaction):
        if not ctx.user.id == usr and ctx.channel.id == chn:
                return await ctx.response.send_message("You are not the user who used the command!", ephemeral=True)
        button.callback = callback4
        button2.callback = callback5
        button3.callback = callback6
        button4.callback = callback7
        view = View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        try:
          await ctx.response.edit_message(embed=em, view=view)
        except Exception:
          pass

      button.callback = callback4
      button2.callback = callback5
      button3.callback = callback6
      button4.callback = callback7
      view = View()
      view.add_item(button)
      view.add_item(button2)
      view.add_item(button3)
      await ctx.send(embed=em, view=view)
      return
    
    @config.error
    async def config_error(self, ctx: commands.Context, error):
      if isinstance(error, commands.MessageNotFound):
        pass
      elif isinstance(error, commands.MissingPermissions):
        return await ctx.send("I don't have the required permissions!")



  

async def setup(bot):
  await bot.add_cog(config(bot))