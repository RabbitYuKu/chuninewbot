import re
from logging import Logger
from typing import TypedDict

import httpx
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from chunithm_net.consts import INTERNATIONAL_JACKET_BASE, JACKET_BASE
from database.models import Song, SongJacket

# There's this really stupid thing where CHUNITHM/ONGEKI has the original game name
# in the artist for songs from other IPs, but maimai doesn't. For song title/artist lookup
# to work properly across all games, we need to strip the original game name from the artist.
RE_GAME_NAME = re.compile(r"「.+」$")


class SongJacketInsertCols(TypedDict):
    song_id: int
    jacket_url: str


def is_url(value: str):
    return value.startswith(("http://", "https://"))


async def update_jackets(
    logger: Logger, async_session: async_sessionmaker[AsyncSession]
):
    client = httpx.AsyncClient()

    jackets: list[SongJacketInsertCols] = []
    song_title_artist_lookup: dict[str, Song] = {}

    async with async_session() as session:
        songs = (await session.scalars(select(Song))).all()

    for song in songs:
        if song.id < 8000:
            song_title_artist_lookup[
                f"{song.title}:{RE_GAME_NAME.sub('', song.artist).rstrip()}"
            ] = song

        if song.jacket is None:
            continue

        if is_url(song.jacket):
            jackets.append({"song_id": song.id, "jacket_url": song.jacket})
        else:
            jackets.append(
                {
                    "song_id": song.id,
                    "jacket_url": f"{JACKET_BASE}/{song.jacket}",
                }
            )
            jackets.append(
                {
                    "song_id": song.id,
                    "jacket_url": f"{INTERNATIONAL_JACKET_BASE}/{song.jacket}",
                }
            )

    for game in ("maimai", "chunithm", "ongeki"):
        zetaraku_songs = (
            await client.get(f"https://dp4p6x0xfi5o9.cloudfront.net/{game}/data.json")
        ).json()

        for song in zetaraku_songs["songs"]:
            # We are not doing jacket song lookups for WORLD'S END/LUNATIC automatically because
            # holy fuck it's a massive can of worms.
            if song["category"] in ("WORLD'S END", "LUNATIC"):
                continue

            search_key = (
                song["title"] + ":" + RE_GAME_NAME.sub("", song["artist"]).rstrip()
            )

            if (db_song := song_title_artist_lookup.get(search_key)) is None:
                continue

            logger.info(
                f"Mapped {db_song.artist} - {db_song.title} to Zetaraku {game} entry {song['artist']} - {song['title']}."
            )

            jackets.append(
                {
                    "song_id": db_song.id,
                    "jacket_url": f"https://dp4p6x0xfi5o9.cloudfront.net/{game}/img/cover/{song['imageName']}",
                }
            )

    official_maimai = (
        await client.get("https://maimai.sega.jp/data/maimai_songs.json")
    ).json()

    for song in official_maimai:
        search_key = song["title"] + ":" + RE_GAME_NAME.sub("", song["artist"]).rstrip()

        if (db_song := song_title_artist_lookup.get(search_key)) is None:
            continue

        logger.info(
            f"Mapped {db_song.artist} - {db_song.title} to official maimai entry {song['artist']} - {song['title']}."
        )

        jackets.append(
            {
                "song_id": db_song.id,
                "jacket_url": f"https://maimaidx.jp/maimai-mobile/img/Music/{song['image_url']}",
            }
        )
        jackets.append(
            {
                "song_id": db_song.id,
                "jacket_url": f"https://maimaidx-eng.com/maimai-mobile/img/Music/{song['image_url']}",
            }
        )

    async with async_session() as session:
        logger.info("Upserting %d jacket URLs.", len(jackets))

        insert_stmt = insert(SongJacket)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=[SongJacket.jacket_url],
            set_={
                "song_id": insert_stmt.excluded.song_id,
            },
        )
        await session.execute(upsert_stmt, jackets)
        await session.commit()

    await client.aclose()
