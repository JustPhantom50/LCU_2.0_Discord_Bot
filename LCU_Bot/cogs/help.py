import discord
from discord.ext import commands
from discord.ui import View
from discord import Interaction
import asyncio
from cogs.utils.checks import checkBlacklisted
import re
from cogs.events import db

class SettingsPanel(discord.ui.View):
    def __init__(self, ctx, bot, pages, cur_page, contents):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.bot = bot
        self.pages = pages
        self.cur_page = cur_page
        self.contents = contents

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple)
    async def back(self, ctx: Interaction, button: discord.ui.Button):
       
      try:
        records = await db.embeds.find_one({'guild_id': int(ctx.guild.id)},{'commands_color': 1})
        res = records['commands_color']
        color2 = ','.join(res)
        color2 = color2.replace("(", "").replace(")", "")
        color_list = re.split(r',\s?', color2)
        color = discord.Color.from_rgb(int(color_list[0]), int(color_list[1]), int(color_list[2]))
      except:
        color = discord.Color.blue()
      super().__init__(timeout=None)
      if self.cur_page == 1:
        self.cur_page = 5
        e = discord.Embed(title=f"{list(self.contents.keys())[self.cur_page-1]}", description=f"\n{list(self.contents.values())[self.cur_page-1]}", color=color)
        e.set_footer(text=f"Page {self.cur_page}/{self.pages}")
        return await ctx.response.edit_message(embed=e)
      else:
        self.cur_page -= 1
        e = discord.Embed(title=f"{list(self.contents.keys())[self.cur_page-1]}", description=f"\n{list(self.contents.values())[self.cur_page-1]}", color=color)
        e.set_footer(text=f"Page {self.cur_page}/{self.pages}")
        return await ctx.response.edit_message(embed=e)
      
    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def next(self, ctx: Interaction, button: discord.ui.Button):
       
      try:
        records = await db.embeds.find_one({'guild_id': int(ctx.guild.id)},{'commands_color': 1})
        res = records['commands_color']

        color2 = ','.join(res)
        color2 = color2.replace("(", "").replace(")", "")
        color_list = re.split(r',\s?', color2)
        color = discord.Color.from_rgb(int(color_list[0]), int(color_list[1]), int(color_list[2]))
      except:
        color = discord.Color.blue()
      if self.cur_page >= self.pages:
        self.cur_page = 1
        e = discord.Embed(title=f"{list(self.contents.keys())[self.cur_page-1]}", description=f"\n{list(self.contents.values())[self.cur_page-1]}", color=color)
        e.set_footer(text=f"Page {self.cur_page}/{self.pages}")
        return await ctx.response.edit_message(embed=e)
      else:
        self.cur_page += 1
        e = discord.Embed(title=f"{list(self.contents.keys())[self.cur_page-1]}", description=f"\n{list(self.contents.values())[self.cur_page-1]}", color=color)
        e.set_footer(text=f"Page {self.cur_page}/{self.pages}")
        return await ctx.response.edit_message(embed=e)

class helpc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Need help with commands? Run the help command.", with_app_command = True, extras={"category": "Other"})
    async def help(self, ctx: commands.Context):
      await ctx.defer(ephemeral = False)
      if await checkBlacklisted(ctx) == False:
        return await ctx.send("You are blacklisted from LCU. Join our support server to appeal.")
       
      contents = {"Main Commands": "",
                  "Infractions": "",
                  "Tools": "",
                  "Other": "",
                  "LOA": ""
                  }

         
      for command in self.bot.walk_commands():
        
        if command.extras.get('category'):
          if command.extras['category'] == 'Group' or command.extras['category'] == 'Staff':
            pass
          else:
            if command == None or command.description == None:
              pass
            else:
              cat = str(command.extras['category'])
              value = contents.get(cat)
              if value == None:
                pass
              else:
                value += f"`-{command}` - {command.description}\n\n"
                contents.update({cat: value})
        else:
            pass
      
      
      pages = int(len(contents))
      cur_page = 1

        
      try:
        records = db.embeds.find(
            {'guild_id': int(ctx.guild.id)},
            {'commands_color': 1}
        )
        res = records['commands_color']

        color2 = ','.join(res)
        color2 = color2.replace("(", "").replace(")", "")
        color_list = re.split(r',\s?', color2)
        color = discord.Color.from_rgb(int(color_list[0]), int(color_list[1]), int(color_list[2]))
      except:
        color = discord.Color.blue()
      e = discord.Embed(title=f"{list(contents.keys())[0]}", description=f"\n{list(contents.values())[0]}", color=color)
      e.set_footer(text=f"Page {cur_page}/{pages} You are able to edit all embeds in the settings command")#its right here
      msg = await ctx.send(embed=e, view = SettingsPanel(ctx, self.bot, pages, cur_page, contents))
      try:
        await self.bot.wait_for('interaction', timeout=800, check=lambda message: message.user == ctx.author and message.channel == ctx.channel)
      except asyncio.TimeoutError:
        last = discord.ui.Button(label="<", style=discord.ButtonStyle.primary, disabled=True)
        next = discord.ui.Button(label=">", style=discord.ButtonStyle.primary, disabled=True)
        view=View()
        view.add_item(last)
        view.add_item(next)
        await msg.edit(view=view)
        return


async def setup(bot):
  await bot.add_cog(helpc(bot))