import discord
from discord.ext import commands
from discord.ui import View
from discord import Interaction
from cogs.utils.checks import startSetup, role_select, channel_select, setupCheck, convertInto
from cogs.events import db


class MSessionBanner(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="Session Banner")

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer(ephemeral=False)
      answer = str(self.answer)

      self.stop()
      
        

class MShutdownBanner(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="Shutdown Banner", placeholder="")
    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)

      self.stop()
      
class MSVoteBanner(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="SVote Banner", placeholder="")

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)

      self.stop()
      
class MEmoji(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="Emoji", placeholder="Must be a custom emoji.")

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)

      self.stop()

      
class MServerName(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="Server Name")

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)

      self.stop()

      

class MServerOwner(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="Server Owner")

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)
      
      self.stop()

      

class MCode(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="ER:LC Server Code")

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)
       
      self.stop()

      

class MReminderText(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="M Command Text", style=discord.TextStyle.paragraph)

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)
      
      self.stop()

      

class MVotes(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="Votes", placeholder = "Must be a number")

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = self.answer
      
      self.stop()

      

class MAdvert(discord.ui.Modal, title='Setup'):

    answer = discord.ui.TextInput(label="Advertisement", style=discord.TextStyle.paragraph)

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)
      
      self.stop()


class MNickname(discord.ui.Modal, title='Setup'):
    answer = discord.ui.TextInput(label="LCU's nickname", style=discord.TextStyle.short)

    async def on_submit(self, ctx: Interaction):
      await ctx.response.defer()
      answer = str(self.answer)
      
      self.stop()
      

#-------------------------------------------------------------------------------------------------------------------
#-----------------------------------------main code-----------------------------------------------------------------

class mainButtons(discord.ui.View):
    def __init__(self, type, user_id):
      super().__init__(timeout=None)
      self.type = type
      self.user_id = user_id
      self.value = None
      self.ctx = None

    @discord.ui.button(label="Input", style=discord.ButtonStyle.green)
    async def input(self, ctx: Interaction, button: discord.ui.Button):
      type = self.type
      if ctx.user.id != self.user_id:
        try:
          return await ctx.response.send_message("You aren't the user who initiated the command!", ephemeral=True)
        except:
          return await ctx.followup.send("You aren't the user who initiated the command!", ephemeral=True)
        
      await ctx.response.send_modal(type)
      await type.wait()
      self.value = str(type.answer)
      self.stop()
      
      
    @discord.ui.button(label="Skip", style=discord.ButtonStyle.blurple)
    async def skip(self, ctx: Interaction, button: discord.ui.Button):
      if ctx.user.id != self.user_id:
        try:
          return await ctx.response.send_message("You aren't the user who initiated the command!", ephemeral=True)
        except:
          return await ctx.followup.send("You aren't the user who initiated the command!", ephemeral=True)
      self.ctx = ctx
      self.value = "skip"
      self.stop()
      
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, ctx: Interaction, button: discord.ui.Button):
      if ctx.user.id != self.user_id:
        try:
          return await ctx.response.send_message("You aren't the user who initiated the command!", ephemeral=True)
        except:
          return await ctx.followup.send("You aren't the user who initiated the command!", ephemeral=True)
      
      try:
        await db.setup.delete_one({'guild_id': ctx.guild.id})
        await db.embeds.delete_one({'guild_id': ctx.guild.id})
        await db.settings.delete_one({'guild_id': ctx.guild.id})
      except Exception:
        pass

      try:
        await ctx.message.delete()
      except:
        pass
      self.value = "cancel"
      self.stop()

class setup_command(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    

  @commands.hybrid_command(description="This will allow you to setup the bot to your liking.", with_app_command = True, extras={"category": "Other"})
  @commands.check(setupCheck)
  async def setup(self, ctx: commands.Context):
    await ctx.defer(ephemeral = False)
     
    
    em = discord.Embed(title="", description="**ATTENTION:** Please make sure I have administative permissions and I'm above the roles you will be selecting.", color=discord.Color.green())
    em.set_footer(text='LCU - Setup')
    continueB = discord.ui.Button(label="Continue", style=discord.ButtonStyle.green)
    view=View()
    view.add_item(continueB)
    msg = await ctx.send(embed=em, view=view)
    inter = await self.bot.wait_for('interaction', timeout=None, check=lambda message: message.user == ctx.author and message.channel == ctx.channel)

    
    #--------------------session banner
  
    while True:
        em = discord.Embed(title="Session Banner", description="Links have to start with: `https://cdn.discordapp.com/attachments/` or `https://media.discordapp.net/attachments/`.")
        view = mainButtons(MSessionBanner(), ctx.author.id)
        helpButton = discord.ui.Button(label="Help", style=discord.ButtonStyle.blurple)
        view.add_item(helpButton)
        async def helpCallback(interaction):
          await interaction.response.send_message("https://www.youtube.com/watch?v=nA_iUkx2-T4", ephemeral=True)
        helpButton.callback = helpCallback
        msg = await inter.response.edit_message(embed=em, view=view)
        await view.wait()

        
        if view.value == "cancel":
            return await self.canceled(ctx)
        elif view.value == "skip":
            await view.ctx.response.defer()
            session_banner = "skipped"
            break
        else:
            view.value = str(view.value)
            if view.value.startswith("https://cdn.discordapp.com/attachments/") or view.value.startswith("https://media.discordapp.net/attachments/"):
                session_banner = str(view.value)
                break
            else:
                embed = discord.Embed(title="INVALID!", description="INVALID, it must be from `https://cdn.discordapp.com/attachments/` or `https://media.discordapp.net/attachments/`", color=discord.Color.red())
                await ctx.send(embed=embed, delete_after=5)
                continue



    #-------------------------shutdown banner
    while True:
        em = discord.Embed(title="Shutdown Banner", description="Links have to start with: `https://cdn.discordapp.com/attachments/` or `https://media.discordapp.net/attachments/`.")
        view = mainButtons(MShutdownBanner(), ctx.author.id)
        helpButton = discord.ui.Button(label="Help", style=discord.ButtonStyle.blurple)
        view.add_item(helpButton)
        async def helpCallback(interaction):
          await interaction.response.send_message("https://www.youtube.com/watch?v=nA_iUkx2-T4", ephemeral=True)
        helpButton.callback = helpCallback
        msg = await inter.original_response()
        await msg.edit(embed=em, view=view)
        await view.wait()

        
        if view.value == "cancel":
            return await self.canceled(ctx)
        elif view.value == "skip":
            await view.ctx.response.defer()
            shutdown_banner = "skipped"
            break
        else:
            view.value = str(view.value)
            if view.value.startswith("https://cdn.discordapp.com/attachments/") or view.value.startswith("https://media.discordapp.net/attachments/"):
                shutdown_banner = str(view.value)
                break
            else:
                embed = discord.Embed(title="INVALID!", description="INVALID, it must be from `https://cdn.discordapp.com/attachments/` or `https://media.discordapp.net/attachments/`", color=discord.Color.red())
                await ctx.send(embed=embed, delete_after=5)
                continue
    
    #-----------------------svote banner
    while True:
        em = discord.Embed(title="SVote Banner", description="Links have to start with: `https://cdn.discordapp.com/attachments/` or `https://media.discordapp.net/attachments/`.")
        view = mainButtons(MSVoteBanner(), ctx.author.id)
        helpButton = discord.ui.Button(label="Help", style=discord.ButtonStyle.blurple)
        view.add_item(helpButton)
        async def helpCallback(interaction):
          await interaction.response.send_message("https://www.youtube.com/watch?v=nA_iUkx2-T4", ephemeral=True)
        helpButton.callback = helpCallback
        msg = await inter.original_response()
        await msg.edit(embed=em, view=view)
        await view.wait()

        if view.value == "cancel":
            return await self.canceled(ctx)
        elif view.value == "skip":
            await view.ctx.response.defer()
            svote_banner = "skipped"
            break
        else:
            view.value = str(view.value)
            if view.value.startswith("https://cdn.discordapp.com/attachments/") or view.value.startswith("https://media.discordapp.net/attachments/"):
                svote_banner = str(view.value)
                break
            else:
                embed = discord.Embed(title="INVALID!", description="INVALID, it must be from `https://cdn.discordapp.com/attachments/` or `https://media.discordapp.net/attachments/`", color=discord.Color.red())
                await ctx.send(embed=embed, delete_after=5)
                continue
  
    #---------------------emoji
    
    while True:
        em = discord.Embed(title="Custom Emoji", description="This emoji must be custom to your server.")
        view = mainButtons(MEmoji(), ctx.author.id)
        helpButton = discord.ui.Button(label="Help", style=discord.ButtonStyle.blurple)
        view.add_item(helpButton)
        async def helpCallback(interaction):
          await interaction.response.send_message("https://www.youtube.com/watch?v=nA_iUkx2-T4", ephemeral=True)
        helpButton.callback = helpCallback
        msg = await inter.original_response()
        await msg.edit(embed=em, view=view)
        await view.wait()

        
        if view.value == "cancel":
            return await self.canceled(ctx)
        elif view.value == "skip":
            await view.ctx.response.defer()
            emoji = ""
            break
        else:
            view.value = str(view.value)
            if not view.value.startswith("<") and not view.value.endswith(">"):
              embed = discord.Embed(title="INVALID!", description="INVALID, it must start with < and end with >. Example: <emojiname:emojiid>", color=discord.Color.red())
              await ctx.send(embed=embed, delete_after=5)
              continue
            else:
              emoji = str(view.value)
              break

    #----------------------mod roles
    em = discord.Embed(title=f"Please select your moderator roles(Do not select your Management roles).", description=f"These are used in the `-mod` command and do not have any permission within the bot. Can be 1-20 roles.")
    select = role_select(1, 25, ctx.author.id)
    view = View()
    view.add_item(select)
    await msg.edit(embed=em, view=view)
    await select.view_obj.wait()
    await msg.edit(view=None)
    mod_roles = select.roles

    #---------------------staff roles
    em = discord.Embed(title=f"Please select all your staff roles(Do not select your Management roles).", description=f"This is your general staff roles like 'Staff Team', etc. Can be 1-20 roles.")
    select1 = role_select(1, 25, ctx.author.id)
    view = View()
    view.add_item(select1)
    await select.interaction.response.edit_message(embed=em, view=view)
    await select1.view_obj.wait()
    await msg.edit(view=None)
    staff_roles = select1.roles

    #---------------------management roles
    em = discord.Embed(title=f"Please select your management roles.", description=f"These are your highest ranking roles like 'Management Team' or 'Ownership'. Can be 1-20 roles.")
    select = role_select(1, 25, ctx.author.id)
    view = View()
    view.add_item(select)
    await select1.interaction.response.edit_message(embed=em, view=view)
    await select.view_obj.wait()
    await msg.edit(view=None)
    manage_roles = select.roles

    #--------------------ssu ping role
    em = discord.Embed(title=f"Please select your Session/SSU Ping Role", description=f"The role you use to ping for sessions. Choose **1** role.")
    select1 = role_select(1, 1, ctx.author.id)
    view = View()
    view.add_item(select1)
    await select.interaction.response.edit_message(embed=em, view=view)
    await select1.view_obj.wait()
    await msg.edit(view=None)
    ssu_ping_role = select1.roles

    #--------------------on duty role
    em = discord.Embed(title=f"Please select your on-duty staff role/roles.", description=f"The role used for when a staff member is on shift/duty. Choose **1** role.")
    select = role_select(1, 1, ctx.author.id)
    view = View()
    view.add_item(select)
    await select1.interaction.response.edit_message(embed=em, view=view)
    await select.view_obj.wait()
    await msg.edit(view=None)
    on_duty_role = select.roles

    #-------------------reminders channel
    em = discord.Embed(title=f"Please select your reminders channel", description=f"This channel will be used when reminders are on.")
    select1 = channel_select(1, 1, ctx.author.id)
    view = View()
    view.add_item(select1)
    await select.interaction.response.edit_message(embed=em, view=view)
    await select1.view_obj.wait()
    await msg.edit(view=None)
    reminders_channel = select1.channels

    #-------------------staff requets channel
    em = discord.Embed(title=f"Please provide your staff requests channel", description=f"This channel will be used when a staff request is sent.")
    select = channel_select(1, 1, ctx.author.id)
    view = View()
    view.add_item(select)
    await select1.interaction.response.edit_message(embed=em, view=view)
    await select.view_obj.wait()
    await select.interaction.response.defer()
    await msg.edit(view=None)
    staff_requests_channel = select.channels

    #------------------nickname
    
    while True:
        em = discord.Embed(title="Bot Nickname", description="This will be LCU's nickname.")
        view = mainButtons(MNickname(), ctx.author.id)
        await msg.edit(embed=em, view=view)
        await view.wait()

       
        if view.value == "cancel":
            return await self.canceled(ctx)
        elif view.value == "skip":
            await view.ctx.response.defer()
            break
        else:
          view.value = str(view.value)
          try:
            await ctx.guild.me.edit(nick=view.value)
          except:
            embed = discord.Embed(title="ERROR!", description="Please provide a valid name. It might be too big or has special characters in it.", color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=5)
            continue
          break

    #-----------------server name
    em = discord.Embed(title="Server Name", description="This will be your server's name.")
    view = mainButtons(MServerName(), ctx.author.id)
    await msg.edit(embed=em, view=view)
    await view.wait()

    
    if view.value == "cancel":
      return await self.canceled(ctx)
    elif view.value == "skip":
      await view.ctx.response.defer()
      server_name = "Server Name"
    else:
      server_name = str(view.value)
    
    #------------------server owner
    em = discord.Embed(title="Server Owner", description="This should be the username or nickname of the server owner.")
    view = mainButtons(MServerOwner(), ctx.author.id)
    await msg.edit(embed=em, view=view)
    await view.wait()

    
    if view.value == "cancel":
      return await self.canceled(ctx)
    elif view.value == "skip":
      await view.ctx.response.defer()
      server_owner = "Server Owner"
    else:
      server_owner = str(view.value)
    
    #----------------Server code
    em = discord.Embed(title="Server Code", description="This should be your ER:LC Private Server Code.")
    view = mainButtons(MCode(), ctx.author.id)
    await msg.edit(embed=em, view=view)
    await view.wait()

 
    if view.value == "cancel":
      return await self.canceled(ctx)
    elif view.value == "skip":
      await view.ctx.response.defer()
      server_code = "code"
    else:
      server_code = str(view.value)
      if " " in server_code:
        server_code = server_code.replace(" ", "") 
      else:
        server_code = server_code
    
    #---------------votes
    while True:
      em = discord.Embed(title="Amount of Votes", description="This will be the amount of votes required to continue a SVote.")
      view = mainButtons(MVotes(), ctx.author.id)
      await msg.edit(embed=em, view=view)
      await view.wait()
      
      if view.value == "cancel":
        return await self.canceled(ctx)
      elif view.value == "skip":
        await view.ctx.response.defer()
        votes = 5
        break
      else:

        try:
          votes = int(view.value)
        except Exception:

          embed = discord.Embed(title="ERROR!", description="Please provide a number (e.g 1, 2, 3)", color=discord.Color.red())
          await ctx.send(embed=embed, delete_after=5)
          continue

  
        break

    #---------------reminders text
    em = discord.Embed(title="Reminder Text", description="This will be your ingame server reminder text.") 
    view = mainButtons(MReminderText(), ctx.author.id)
    await msg.edit(embed=em, view=view)
    await view.wait()

   
    if view.value == "cancel":
      return await self.canceled(ctx)
    elif view.value == "skip":
      await view.ctx.response.defer()
      reminders_text = ":m Come join our server for fun!"
    else:
      reminders_text = str(view.value)

    #--------------advert
    em = discord.Embed(title="Advertisement", description="This will be your server's advertisement.")
    view = mainButtons(MAdvert(), ctx.author.id)
    await msg.edit(embed=em, view=view)
    await view.wait()

   
    if view.value == "cancel":
      return await self.canceled(ctx)
    elif view.value == "skip":
      await view.ctx.response.defer()
      advert = "This is our wonderful server!"
    else:
      advert = str(view.value)

    try:
      await msg.delete()
    except:
      pass

    await startSetup(ctx, session_banner=session_banner, shutdown_banner=shutdown_banner, svote_banner=svote_banner, emoji=emoji, mod_roles=mod_roles, staff_roles=staff_roles, manage_roles=manage_roles, ssu_ping_role=ssu_ping_role, on_duty_role=on_duty_role, reminders_channel=reminders_channel, staff_requests_channel=staff_requests_channel, server_name=server_name, server_owner=server_owner, server_code=server_code, votes=votes, reminders_text=reminders_text, advert=advert)
    
  async def canceled(self, ctx: Interaction):
    em = discord.Embed(title="Canceled!", description="Your setup is canceled", color=discord.Color.red())
    
    await ctx.channel.send(embed=em)


  @setup.error
  async def setup_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MessageNotFound):
      pass
    elif ctx.guild.me.guild_permissions.administrator is False:
      try:
        return await ctx.send("Please give me Administrator perms as I tend to work better!")
      except:
        pass
    elif ctx.guild.me.guild_permissions.manage_roles is False:
      try:
        return await ctx.send("I need permission to manage roles!")
      except:
        pass
    elif isinstance(error, commands.MissingPermissions):
      try:
        return await ctx.send("I don't have the required permissions!")
      except:
        pass
    
async def setup(bot):
  await bot.add_cog(setup_command(bot)) 