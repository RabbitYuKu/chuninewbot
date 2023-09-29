import importlib.util

import pytest
from bs4 import BeautifulSoup

from chunithm_net.entities.enums import ClearType, Difficulty, Rank
from chunithm_net.utils import difficulty_from_imgurl, get_rank_and_cleartype


@pytest.mark.parametrize(
    ("html", "expected"),
    [
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_clear.png">
                <!-- ◆ランク -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_rank_9.png">
            </div>
            """,
            (Rank.Sp, ClearType.CLEAR),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆ランク -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_rank_9.png">
            </div>
            """,
            (Rank.Sp, ClearType.FAILED),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_clear.png">
            </div>
            """,
            (Rank.D, ClearType.CLEAR),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
            </div>
            """,
            (Rank.D, ClearType.FAILED),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_clear.png">
                <!-- ◆ランク -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_rank_13.png">
                <img src="https://chunithm-net-eng.com/mobile/images/icon_alljustice.png">
            </div>
            """,
            (Rank.SSSp, ClearType.ALL_JUSTICE),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_clear.png">
                <!-- ◆ランク -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_rank_12.png">
                <img src="https://chunithm-net-eng.com/mobile/images/icon_fullcombo.png">
            </div>
            """,
            (Rank.SSS, ClearType.FULL_COMBO),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_absolutep.png">
                <!-- ◆ランク -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_rank_13.png">
            </div>
            """,
            (Rank.SSSp, ClearType.ABSOLUTE_PLUS_CLEAR),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_absolute.png">
                <!-- ◆ランク -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_rank_13.png">
            </div>
            """,
            (Rank.SSSp, ClearType.ABSOLUTE_CLEAR),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_hard.png">
                <!-- ◆ランク -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_rank_13.png">
            </div>
            """,
            (Rank.SSSp, ClearType.HARD_CLEAR),
        ),
        (
            """
            <div class="play_musicdata_icon clearfix">
                <!-- ◆クリア -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_catastrophy.png">
                <!-- ◆ランク -->
                <img src="https://chunithm-net-eng.com/mobile/images/icon_rank_13.png">
            </div>
            """,
            (Rank.SSSp, ClearType.CATASTROPHY_CLEAR),
        ),
    ],
)
def test_get_rank_and_cleartype(html, expected):
    bs4_features = "lxml" if importlib.util.find_spec("lxml") else "html.parser"
    soup = BeautifulSoup(html, bs4_features)
    assert get_rank_and_cleartype(soup) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("basic", Difficulty.BASIC),
        ("advanced", Difficulty.ADVANCED),
        ("expert", Difficulty.EXPERT),
        ("master", Difficulty.MASTER),
        ("worldsend", Difficulty.WORLDS_END),
        ("ultima", Difficulty.ULTIMA),
        ("ultimate", Difficulty.ULTIMA),
    ],
)
def test_difficulty_from_imgurl(value, expected):
    assert difficulty_from_imgurl(value) == expected


@pytest.mark.parametrize(
    ("value"),
    [
        "unknown",
        "basik",
        "advance",
        "worldend",
        "ultimat",
        "thembululwa",
    ],
)
def test_difficulty_from_imgurl_raises_on_unknown_difficulty(value):
    with pytest.raises(ValueError):
        difficulty_from_imgurl(value)
