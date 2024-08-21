# import discord
# from discord.ext import commands
# from discord import Interaction
# from cogs.utils.checks import getInfo, checks, log_command
# from cogs.events import db

# class MAutoReply(discord.ui.Modal, title='Configuration'):
#     trigger = discord.ui.TextInput(label="Keyword", placeholder="ex: Hello")
#     response = discord.ui.TextInput(label="Response", style=discord.TextStyle.paragraph, placeholder="ex: Hello there, how may I help?")
#     async def on_submit(self, ctx: Interaction):
#         trigger = str(self.trigger).strip()
#         response = str(self.response)
#         if response.find('@everyone') != -1 or response.find('@here') != -1:
#           return await ctx.response.send_message("You can not ping everyone or here with Auto-Replies!")
#         records = db.auto_reply.find({"guild_id": ctx.guild.id}, {"key_word": 1})
#         async for item in records:
#           item = list(item.values())
#           if trigger == item[0]:
#               return await ctx.response.send_message(f"That keyword already exists, please make a new one!", ephemeral=True)
#         await db.auto_reply.insert_one({'guild_id': ctx.guild.id, 'key_word': trigger, 'response': response})
#         await ctx.response.send_message(f"Keyword `{trigger}` has been added!", ephemeral=True)

# class MDeleteAutoReply(discord.ui.Modal, title='Configuration'):
#     trigger = discord.ui.TextInput(label="Keyword", placeholder="Type the keyword.")
#     async def on_submit(self, ctx: Interaction):
#           trigger = str(self.trigger).strip()
          
#           records = db.auto_reply.find_one({"guild_id": ctx.guild.id, "key_word": trigger}, {"key_word": 1})
#           if records == None:
#               return await ctx.response.send_message(f"That keyword does not exist!", ephemseral=True)
#           else:

#               await db.auto_reply.delete_one({"guild_id": ctx.guild.id, "key_word": trigger})
#               return await ctx.response.send_message(f"Keyword `{trigger}` has been deleted!", ephemeral=True)


# class SettingsPanel(discord.ui.View):
#     def __init__(self, ctx, bot):
#       super().__init__(timeout=None)
#       self.ctx = ctx
#       self.bot = bot

#     @discord.ui.button(label="Add", style=discord.ButtonStyle.green)
#     async def add(self, ctx: Interaction, button: discord.ui.Button):
#       await ctx.response.send_modal(MAutoReply())
#       return

#     @discord.ui.button(label="Search", style=discord.ButtonStyle.blurple)
#     async def search(self, ctx: Interaction, button: discord.ui.Button):
#       em = discord.Embed(title="Current Keywords", description="", color=discord.Color.blue())
#       records = db.auto_reply.find({"guild_id": ctx.guild.id}, {"key_word": 1, "response": 1})
#       async for item in records:
#           em.add_field(name=item['key_word'], value=item['response'])
#       await ctx.response.edit_message(embed=em)
      
#     @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
#     async def delete(self, ctx: Interaction, button: discord.ui.Button):
#       await ctx.response.send_modal(MDeleteAutoReply())
#       return

# class replies(commands.Cog):
#     def __init__(self, bot):
#       self.bot = bot

      
#     @commands.hybrid_command(description="Manage Your Auto Replies", with_app_command = True, extras={"category": "Tools"})
#     @commands.check(checks.check2)
#     async def manage_replies(self, ctx: commands.Context):
#         guild_info = await getInfo(ctx)
#         await ctx.defer(ephemeral = False)
#         await log_command(ctx, self.bot)
#         em = discord.Embed(title="Configuration for Auto-Replies", description="Here you can modify your auto replies for your server.", color=discord.Color.blue())
#         view = SettingsPanel(ctx, self.bot)
#         await ctx.send(embed=em, view=view)
#         return
    
#     @manage_replies.error
#     async def manage_replies_error(self, ctx: commands.Context, error):
#       if isinstance(error, commands.MessageNotFound):
#         pass
#       elif isinstance(error, commands.MissingPermissions):
#         return await ctx.send("I don't have the required permissions!")



    
# async def setup(bot):
#   await bot.add_cog(replies(bot))