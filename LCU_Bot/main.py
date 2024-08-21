import discord
import os
from discord.ext import commands
from cogs.utils.checks import check_if_it_is_me, load_env
import sentry_sdk
import json
import importlib
from cogs.utils import checks

sentry_sdk.init(
        dsn="https://bdd74ab2b48f403580613b913f2a4bec@o4505332868513792.ingest.sentry.io/4505332869955584",

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
)
class Bot(commands.AutoShardedBot):#autosharded
    async def is_owner(self, user: discord.User):
        with open('cogs/data/stafflogins.json', 'r+') as file:
            data = json.load(file)
            author_id = str(user.id)
        if author_id in data:
            if str(data[author_id]['type']) == "ownership" or str(data[author_id]['type']) == "developer" or author_id == 676895030094331915:
                return True
            else:
                return False
    async def setup_hook(self) -> None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                
        await bot.load_extension('cogs.utils.hot_reload')
        print('All cogs loaded successfully!')


intent = discord.Intents.default()
intent.message_content = True
intent.members = True
bot = Bot(command_prefix=load_env.prefix(), intents=intent, chunk_guilds_at_startup=False, help_command=None, allowed_mentions=discord.AllowedMentions(replied_user=True, everyone=True, roles=True))
    
@bot.before_invoke
async def before_invoke(ctx: commands.Context):
    if await checks.checkBlacklisted(ctx):
        raise commands.CheckFailure("You are blacklisted from using this bot.")
    if ctx.channel.type == discord.ChannelType.private:
        raise commands.NoPrivateMessage("This command cannot be used in private messages.")
    elif not ctx.guild:
        raise commands.NoPrivateMessage("This command cannot be used in private messages.")
    if ctx.guild.chunked == False or not ctx.guild.chunked:
        await ctx.guild.chunk()
    

bot.run(load_env.token())