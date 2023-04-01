import logging

import aiohttp
import discord
from discord import Webhook
from discord.ext import commands
from discord.ext.commands import Context

from api.exceptions import (
    ChuniNetException,
    MaintenanceException,
    InvalidTokenException,
)
from bot import ChuniBot, cfg


class EventsCog(commands.Cog, name="Events"):
    def __init__(self, bot: ChuniBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, MaintenanceException):
            await ctx.send(
                "CHUNITHM-NET is currently undergoing maintenance. Please try again later.",
                mention_author=False,
                delete_after=5,
            )
        elif isinstance(error, InvalidTokenException):
            await ctx.send(
                "Your CHUNITHM-NET cookie is invalid. Please use `c>login` in DMs to log in.",
                mention_author=False,
                delete_after=5,
            )
        elif isinstance(error, ChuniNetException):
            await ctx.send(
                "An error occurred while communicating with CHUNITHM-NET. Please try again later (or re-login).",
                mention_author=False,
                delete_after=5,
            )
        elif (
            isinstance(error, commands.BadArgument)
            or isinstance(error, commands.BadUnionArgument)
            or isinstance(error, commands.MissingRequiredArgument)
            or isinstance(error, commands.MissingPermissions)
            or isinstance(error, commands.BotMissingPermissions)
            or isinstance(error, commands.MaxConcurrencyReached)
            or isinstance(error, commands.NoPrivateMessage)
            or isinstance(error, commands.PrivateMessageOnly)
        ):
            await ctx.send(str(error), mention_author=False, delete_after=5)
        else:
            await ctx.send(
                "An error occurred while executing the command.",
                mention_author=False,
                delete_after=5,
            )
            logging.getLogger("discord").error(
                "Exception in command %s", ctx.command, exc_info=error
            )
            if webhook_url := cfg.get("ERROR_REPORTING_WEBHOOK"):
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(webhook_url, session=session)

                    embed = discord.Embed(
                        title=f"Error in command {ctx.command}",
                        description=f"```{error}```",
                    )
                    await webhook.send(
                        username=self.bot.user.display_name,
                        avatar_url=self.bot.user.display_avatar.url,
                        embed=embed,
                        allowed_mentions=discord.AllowedMentions.none(),
                    )


async def setup(bot: ChuniBot):
    await bot.add_cog(EventsCog(bot))