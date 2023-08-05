import discord

from . import utils as vbu
from .. import __version__


class BotStats(vbu.Cog):

    @vbu.command()
    @vbu.checks.is_config_set('bot_info', 'enabled')
    @vbu.bot_has_permissions(send_messages=True)
    async def info(self, ctx: vbu.Context):
        """
        Gives you information about the bot, including some important links, such as its invite.
        """

        # Get the info embed
        bot_info = self.bot.config.get("bot_info", {})
        info_embed = vbu.Embed(
            description=bot_info.get("content", "").format(bot=self.bot),
        ).set_author_to_user(
            self.bot.user,
        )

        # See if we have images
        if bot_info.get("thumbnail"):
            info_embed.set_thumbnail(bot_info["thumbnail"])
        if bot_info.get("image"):
            info_embed.set_image(bot_info["image"])

        # Make up our buttons
        links = bot_info.get("links", dict())
        buttons = []
        if (invite_link := self.get_invite_link()):
            buttons.append(vbu.Button(label="Invite", url=invite_link, style=vbu.ButtonStyle.LINK))
        for label, info in links.items():
            buttons.append(vbu.Button(emoji=info.get("emoji") or None, label=label, url=info['url'], style=vbu.ButtonStyle.LINK))
        components = vbu.MessageComponents.add_buttons_with_rows(*buttons)

        # And send
        return await ctx.send(embed=info_embed, components=components, wait=False)

    def get_invite_link(self):
        """
        Get the invite link for the bot.
        """

        if not self.bot.config.get("oauth", {}).get("enabled", True):
            return None
        oauth = self.bot.config.get("oauth", {}).copy()
        permissions = discord.Permissions.none()
        for i in oauth.pop('permissions', list()):
            setattr(permissions, i, True)
        oauth['permissions'] = permissions
        return self.bot.get_invite_link(**oauth)

    @vbu.command()
    @vbu.bot_has_permissions(send_messages=True)
    @vbu.checks.is_config_set('oauth', 'enabled')
    async def invite(self, ctx: vbu.Context):
        """
        Gives you the bot's invite link.
        """

        await ctx.send(f"<{self.get_invite_link()}>", embeddify=False)

    @vbu.command()
    @vbu.bot_has_permissions(send_messages=True)
    @vbu.checks.is_config_set('bot_listing_api_keys', 'topgg_token')
    async def vote(self, ctx: vbu.Context):
        """
        Gives you a link to vote for the bot.
        """

        bot_user_id = self.bot.user.id
        output_strings = []
        if self.bot.config.get('bot_listing_api_keys', {}).get("topgg_token"):
            output_strings.append(f"<https://top.gg/bot/{bot_user_id}/vote>")
        if self.bot.config.get('bot_listing_api_keys', {}).get("discordbotlist_token"):
            output_strings.append(f"<https://discordbotlist.com/bots/{bot_user_id}/upvote>")
        if not output_strings:
            return await ctx.send("Despite being enabled, the vote command has no vote links to provide :/")
        return await ctx.send("\n".join(output_strings), embeddify=False)

    async def get_stats_embed(self):
        """
        Get the stats embed - now as a function so I can use it in multiple places.
        """

        # Get creator info
        try:
            creator_id = self.bot.config["owners"][0]
            creator = self.bot.get_user(creator_id) or await self.bot.fetch_user(creator_id)
        except IndexError:
            creator_id = None
            creator = None

        # Make embed
        embed = vbu.Embed(use_random_colour=True)
        embed.set_footer(f"{self.bot.user} - VoxelBotUtils v{__version__}", icon_url=self.bot.user.avatar_url)
        if creator_id:
            embed.add_field("Creator", f"{creator!s}\n{creator_id}")
        embed.add_field("Library", f"Discord.py {discord.__version__}")
        if self.bot.shard_count != len((self.bot.shard_ids or [0])):
            embed.add_field(
                "Approximate Guild Count",
                f"{int((len(self.bot.guilds) / len(self.bot.shard_ids or [0])) * self.bot.shard_count):,}",
            )
        else:
            embed.add_field("Guild Count", f"{len(self.bot.guilds):,}")
        embed.add_field("Shard Count", f"{self.bot.shard_count or 1:,}")
        embed.add_field("Average WS Latency", f"{(self.bot.latency * 1000):.2f}ms")

        # Get topgg data
        if self.bot.config.get('bot_listing_api_keys', {}).get("topgg_token"):
            params = {"fields": "points,monthlyPoints"}
            headers = {"Authorization": self.bot.config['bot_listing_api_keys']['topgg_token']}
            async with self.bot.session.get(f"https://top.gg/api/bots/{self.bot.user.id}", params=params, headers=headers) as r:
                try:
                    data = await r.json()
                except Exception:
                    data = {}
            if "points" in data and "monthlyPoints" in data:
                embed.add_field(
                    "Bot Votes",
                    f"[Top.gg](https://top.gg/bot/{self.bot.user.id}): {data['points']:,} ({data['monthlyPoints']:,} this month)",
                )

        # Get discordbotlist data
        if self.bot.config.get('bot_listing_api_keys', {}).get("discordbotlist_token"):
            async with self.bot.session.get(f"https://discordbotlist.com/api/v1/bots/{self.bot.user.id}") as r:
                try:
                    data = await r.json()
                except Exception:
                    data = {}
            if "upvotes" in data and "metrics" in data:
                content = {
                    "name": "Bot Votes",
                    "value": f"[DiscordBotList.com](https://discordbotlist.com/bots/{self.bot.user.id}): {data['metrics'].get('upvotes', 0):,} ({data['upvotes']:,} this month)"
                }
                try:
                    current_data = embed.get_field_by_key("Bot Votes")
                    content['value'] = current_data['value'] + '\n' + content['value']
                    embed.edit_field_by_key("Bot Votes", **content)
                except KeyError:
                    embed.add_field(**content)
            elif "upvotes" in data:
                content = {
                    "name": "Bot Votes",
                    "value": f"[DiscordBotList.com](https://discordbotlist.com/bots/{self.bot.user.id}): {data['upvotes']:,}"
                }
                try:
                    current_data = embed.get_field_by_key("Bot Votes")
                    content['value'] = current_data['value'] + '\n' + content['value']
                    embed.edit_field_by_key("Bot Votes", **content)
                except KeyError:
                    embed.add_field(**content)

        return embed

    @vbu.command(aliases=['status', 'botinfo'], add_slash_command=False)
    @vbu.bot_has_permissions(send_messages=True, embed_links=True)
    async def stats(self, ctx: vbu.Context):
        """
        Gives you the stats for the bot.
        """

        embed = await self.get_stats_embed()
        await ctx.send(embed=embed)


def setup(bot: vbu.Bot):
    x = BotStats(bot)
    bot.add_cog(x)
