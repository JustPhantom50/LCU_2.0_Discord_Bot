import discord
from discord.ext import commands
import time
from cogs.utils.checks import (
    getInfo,
    getHex,
    createUrlButton,
    getColor,
    convertEmbed,
    get_embed_info,
    is_management,
)
import re
from cogs.events import db


class session(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(with_app_command=True, extras={"category": "Group"})
    async def session(self, ctx: commands.Context):
        return

    @session.command(
        description="This command sends the Server Start Up message.",
        with_app_command=True,
        extras={"category": "Main Commands"},
    )
    @is_management()
    async def startup(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)

        try:
            await ctx.message.delete()
        except:
            pass

        guild_info = await getInfo(ctx)
        timestamp = int(time.time())

        embed_info = await get_embed_info(ctx, "session")

        res1 = await db.settings.find_one(
            {"guild_id": int(ctx.guild.id)}, {"session_link": 1}
        )

        color = await getHex(str(embed_info[1]))
        print(timestamp) 
        newDescription = await convertEmbed(
            ctx,
            embed_info[0],
            embed_info[2],
            embed_info[3],
            embed_info[5],
            guild_info,
            timestamp,
            "session",
        )

        description = re.sub(r'<t:\d+:F>', f'<t:{int(time.time())}:F>', newDescription[0])

        em = discord.Embed(
            title=f"{newDescription[1]}", description=description, color=color
        )
        if (
            str(guild_info["session_banner_link"]) != "skipped"
            and str(guild_info["session_banner_link"]) != "None"
            and str(guild_info["session_banner_link"]) != None
        ):
            try:
                em.set_image(url=f"{guild_info['session_banner_link']}")
            except:
                await ctx.send(
                    f"It looks like your banner link is invalid. Please change it in `-config` so I can display it! It's currently `{guild_info['session_banner_link']}`."
                )

        if embed_info[4]:
            em.set_author(name=newDescription[3], icon_url=embed_info[4])

        if embed_info[3]:
            em.set_footer(text=newDescription[2])

        view = await createUrlButton([res1["session_link"]], ["Click to Join"])
        if view == "0x1":
            return await ctx.send(
                "Something went wrong while making the buttons, please contact support!"
            )

        member = guild_info["session_role_id"]
        try:
            if member[0] == "[" and member[0] == "]":
                member = member[1:-1]
            else:
                pass
        except:
            pass

        role = discord.utils.get(ctx.guild.roles, id=int(member))

        records1 = await db.settings.find_one({ 'guild_id': int(ctx.guild.id) }, { 'svote_here_toggle': 1 })
    
        if records1['svote_here_toggle'] != 1 and records1['svote_here_toggle'] != 0:
            await db.settings.update_one({ 'guild_id': int(ctx.guild.id) }, { '$set': {'svote_here_toggle': 1} })
        
        em2 = discord.Embed(title="Message Sent Successfuly!", description=f"", color=discord.Color.green())
        await ctx.send(embed=em2, delete_after=1, ephemeral=True)
        if records1['svote_here_toggle'] == 1:
            return await ctx.send(content=f"@here {role.mention}", embed=em, view=view, allowed_mentions=discord.AllowedMentions(roles=True, users = True, replied_user=True))
        await ctx.send(
            content=f"{role.mention}",
            embed=em,
            view=view,
            allowed_mentions=discord.AllowedMentions(
                roles=True, users=True, replied_user=True
            ),
        )

    @startup.error
    async def startup_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MessageNotFound):
            return await ctx.send("Please retry this command, message not found.")
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send("I don't have the required permissions!")

    @session.command(
        description="This command sends the Server Shutdown message.",
        with_app_command=True,
        extras={"category": "Main Commands"},
    )
    @is_management()
    async def shutdown(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)

        try:
            await ctx.message.delete()
        except:
            pass

        timestamp = int(time.time())
        guild_info = await getInfo(ctx)

        embed_info = await get_embed_info(ctx, "shutdown")

        color = await getHex(str(embed_info[1]))
        newDescription = await convertEmbed(
            ctx,
            embed_info[0],
            embed_info[2],
            embed_info[3],
            embed_info[5],
            guild_info,
            timestamp,
            "shutdown",
        )

        description = re.sub(r'<t:\d+:F>', f'<t:{int(time.time())}:F>', newDescription[0])

        em = discord.Embed(
            title=f"{newDescription[1]}", description=newDescription[0], color=color
        )
        if (
            guild_info["shutdown_banner_link"] != "skipped"
            and str(guild_info["shutdown_banner_link"]) != "None"
            and str(guild_info["shutdown_banner_link"]) != None
        ):
            try:
                em.set_image(url=f"{guild_info['shutdown_banner_link']}")
            except:
                await ctx.send(
                    f"It looks like your banner link is invalid. Please change it in `-config` so I can display it! It's currently `{guild_info['session_banner_link']}`."
                )

        if embed_info[4]:
            em.set_author(name=newDescription[3], icon_url=embed_info[4])

        if embed_info[3]:
            em.set_footer(text=newDescription[2])

        await ctx.send("Message Sent Successfuly!", delete_after=1, ephemeral=True)
        await ctx.channel.send(
            embed=em,
            allowed_mentions=discord.AllowedMentions(
                roles=True, users=True, replied_user=True
            ),
        )

    @shutdown.error
    async def shutdown_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MessageNotFound):
            return await ctx.send("Please retry this command, message not found.")
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send("I don't have the required permissions!")

    @session.command(
        description="This command sends the Session Cancel message.",
        with_app_command=True,
        extras={"category": "Main Commands"},
    )
    @is_management()
    async def vcancel(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)
        deleted = False
        guild_info = await getInfo(ctx)

        records = await db.embeds.find_one(
            {"guild_id": int(ctx.guild.id)},
            {"shutdown_description": 1, "shutdown_color": 1, "svote_title": 1},
        )
        try:
            await ctx.message.delete()
        except:
            pass

        async for message in ctx.channel.history(limit=50):
            if message.author.id == self.bot.user.id:
                if len(message.embeds) > 0:
                    if message.embeds[0].title == records["svote_title"]:
                        deleted = True

                        color = await getHex(records["shutdown_color"])

                        em = discord.Embed(
                            title=f"{ctx.guild.name} Session Canceled",
                            description=f"The session poll has been canceled by {ctx.author.mention}. Let's try again next time!\n\n**Timestamp:** <t:{int(time.time())}:F>",
                            color=color,
                        )
                        if (
                            guild_info["shutdown_banner_link"] == "skipped"
                            or guild_info["shutdown_banner_link"] == None
                        ):
                            pass
                        else:
                            try:
                                em.set_image(
                                    url=f"{guild_info['shutdown_banner_link']}"
                                )
                            except Exception:
                                await ctx.send(
                                    f"It looks like your banner link is invalid. Please change it in `-config` so I can display it! It's currently `{guild_info['session_banner_link']}`."
                                )
                        await message.edit(embed=em, view=None)
                        break

        if not deleted:
            em = discord.Embed(
                title="",
                description="Please make sure to start a SVote before running this command!",
            )
            return await ctx.send(embed=em, delete_after=4, ephemeral=True)
        elif deleted:
            await ctx.send("Message Sent Successfuly!", delete_after=1, ephemeral=True)

    @session.command(
        description="This command sends the Server Restart message.",
        with_app_command=True,
        extras={"category": "Main Commands"},
    )
    @is_management()
    async def restart(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)

        try:
            await ctx.message.delete()
        except:
            pass

        guild_info = await getInfo(ctx)
        timestamp = int(time.time())

        records = await db.settings.find_one(
            {"guild_id": int(ctx.guild.id)}, {"session_link": 1}
        )

        em = discord.Embed(
            title=f"{ctx.guild.name} Session Restart",
            description=f"{guild_info['emoji_id']} Our ingame server is restarting due to difficulties. Please rejoin using the link below!\n\nTimestamp: <t:{timestamp}:F>",
            color=await getColor(ctx, "commands_color"),
        )

        view = await createUrlButton([records["session_link"]], ["Click to Join"])
        if view == "0x1":
            return await ctx.send(
                "Something went wrong while making the buttons, please contact support!"
            )

        member = guild_info["session_role_id"]
        try:
            if member[0] == "[" and member[0] == "]":
                member = member[1:-1]
            else:
                pass
        except:
            pass

        role = discord.utils.get(ctx.guild.roles, id=int(member))
        await ctx.send("Message Sent Successfuly!", delete_after=1, ephemeral=True)
        await ctx.send(
            content=f"{role.mention}",
            embed=em,
            view=view,
            allowed_mentions=discord.AllowedMentions(
                roles=True, users=True, replied_user=True
            ),
        )

    @session.command(
        description="This command sends the Server Full message.",
        with_app_command=True,
        extras={"category": "Main Commands"},
    )
    @is_management()
    async def full(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)

        try:
            await ctx.message.delete()
        except:
            pass

        guild_info = await getInfo(ctx)
        color = await getColor(ctx, "commands_color")
        timestamp = int(time.time())

        em = discord.Embed(
            title=f"{ctx.guild.name} Server Full",
            description=f"{guild_info['emoji_id']} Our in-game server is full! Thank you all for some amazing roleplays, please remember spots will still open up. Click the button to join.\n\nTimestamp: <t:{timestamp}:F>",
            color=color,
        )

        records = await db.settings.find_one(
            {"guild_id": int(ctx.guild.id)}, {"session_link": 1}
        )

        view = await createUrlButton([records["session_link"]], ["Click to Join"])
        if view == "0x1":
            return await ctx.send(
                "Something went wrong while making the buttons, please contact support!"
            )

        await ctx.send("Message Sent Successfuly!", delete_after=1, ephemeral=True)
        await ctx.send(embed=em, view=view)


async def setup(bot):
    await bot.add_cog(session(bot))
