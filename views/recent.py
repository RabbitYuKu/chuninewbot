from math import floor

import discord.ui

from api import ChuniNet
from api.record import DetailedRecentRecord, RecentRecord
from bot import ChuniBot
from cogs.botutils import UtilsCog

from .pagination import PaginationView


def split_scores_into_credits(scores: list[RecentRecord]) -> list[list[RecentRecord]]:
    credits = []
    current_credit = []
    for score in scores:
        current_credit.append(score)
        if score.track == 1:
            credits.append(current_credit)
            current_credit = []
    return credits


class RecentRecordsView(PaginationView):
    def __init__(
        self, bot: ChuniBot, scores: list[RecentRecord], chuni_client: ChuniNet
    ):
        super().__init__(items=split_scores_into_credits(scores), per_page=1)
        self.chuni_client = chuni_client
        self.page = 0
        self.max_index = len(self.items) - 1

        self.utils: UtilsCog = bot.get_cog("Utils")  # type: ignore

        self.dropdown.options = [  # type: ignore[attr-defined]
            discord.SelectOption(
                label=f"{idx + 1}. {score.title} - {score.difficulty}",
                value=f"{score.detailed.idx}",
            )
            for (idx, score) in enumerate(scores)
            if score.detailed is not None
        ][:25]

    def format_score_page(self, scores: list[RecentRecord]) -> list[discord.Embed]:
        embeds = []
        for score in scores:
            embed = (
                discord.Embed(
                    description=f"**{score.title} [{score.difficulty} {score.internal_level if not score.unknown_const else score.level}]**\n\n▸ **{score.rank}** ▸ {score.clear} ▸ {score.score}",
                    timestamp=score.date,
                    color=score.difficulty.color(),
                )
                .set_author(name=f"TRACK {score.track}")
                .set_thumbnail(url=score.jacket)
            )
            if not score.unknown_const:
                embed.set_footer(text=f"Play rating {score.play_rating:.2f}")
            embeds.append(embed)

        embeds.append(
            discord.Embed(description=f"Page {self.page + 1}/{self.max_index + 1}")
        )
        return embeds

    def format_detailed_score_page(self, score: DetailedRecentRecord) -> discord.Embed:
        embed = (
            discord.Embed(
                description=(
                    f"**{score.title} [{score.difficulty} {score.internal_level if not score.unknown_const else score.level}]**\n\n"
                    f"▸ **{score.rank}** ▸ {score.clear} ▸ {score.score} ▸ x{score.max_combo}{f'/{score.full_combo}' if score.full_combo else ''}\n"
                    f"▸ CRITICAL {score.judgements.jcrit}/JUSTICE {score.judgements.justice}/ATTACK {score.judgements.attack}/MISS {score.judgements.miss}\n"
                    f"▸ TAP {score.note_type.tap * 100:.2f}%/HOLD {score.note_type.hold * 100:.2f}%/SLIDE {score.note_type.slide * 100:.2f}%/AIR {score.note_type.air * 100:.2f}%/FLICK {score.note_type.flick * 100:.2f}%"
                ),
                color=score.difficulty.color(),
                timestamp=score.date,
            )
            .set_author(name=f"TRACK {score.track}")
            .set_thumbnail(url=score.jacket)
        )
        if not score.unknown_const:
            embed.set_footer(text=f"Play rating {score.play_rating:.2f}")
        return embed

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embeds=self.format_score_page(self.items[self.page]), view=self
        )

    @discord.ui.select(placeholder="Select a score", row=1)
    async def dropdown(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        if not isinstance(interaction.channel, discord.TextChannel):
            return
        await interaction.response.defer()

        idx = int(select.values[0])
        score = await self.chuni_client.detailed_recent_record(idx)
        score = await self.utils.annotate_song(score)
        await interaction.channel.send(
            content=f"Score of {interaction.user.mention}",
            embed=self.format_detailed_score_page(score),
        )