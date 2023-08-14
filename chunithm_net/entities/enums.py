from enum import Enum


class Difficulty(Enum):
    BASIC = 0
    ADVANCED = 1
    EXPERT = 2
    MASTER = 3
    ULTIMA = 4
    WORLDS_END = 5

    def __str__(self):
        if self.value == 5:
            return "WORLD'S END"

        return self.name

    def color(self):
        match self.value:
            case 0:
                return 0x009F7B
            case 1:
                return 0xF47900
            case 2:
                return 0xE92829
            case 3:
                return 0x8C1BE1
            case 4:
                return 0x131313
            case 5:
                return 0x0B6FF3

    def short_form(self):
        if self.value == 5:
            return "WE"
        return self.name[:3]

    def emoji(self):
        match self.value:
            case 0:
                return ":green_square:"
            case 1:
                return ":yellow_square:"  # yellow square
            case 2:
                return ":red_square:"  # red square
            case 3:
                return ":purple_square:"  # purple square
            case 4:
                return ":black_large_square:"  # black large square
            case 5:
                return ":blue_square:"  # blue square

    @classmethod
    def from_embed_color(cls, color: int):
        if color == 0x009F7B:
            return cls.BASIC
        if color == 0xF47900:
            return cls.ADVANCED
        if color == 0xE92829:
            return cls.EXPERT
        if color == 0x8C1BE1:
            return cls.MASTER
        if color == 0x131313:
            return cls.ULTIMA
        if color == 0x0B6FF3:
            return cls.WORLDS_END

        msg = f"Unknown difficulty color: {color}"
        raise ValueError(msg)

    @classmethod
    def from_short_form(cls, short_form: str):
        if short_form == "BAS":
            return cls.BASIC
        if short_form == "ADV":
            return cls.ADVANCED
        if short_form == "EXP":
            return cls.EXPERT
        if short_form == "MAS":
            return cls.MASTER
        if short_form == "ULT":
            return cls.ULTIMA
        if short_form == "WE":
            return cls.WORLDS_END

        msg = f"Unknown difficulty short form: {short_form}"
        raise ValueError(msg)


class ClearType(Enum):
    FAILED = 0
    CLEAR = 1
    FULL_COMBO = 2
    ALL_JUSTICE = 3

    def __str__(self):
        return self.name.replace("_", " ")


class Rank(Enum):
    D = 0
    C = 1
    B = 2
    BB = 3
    BBB = 4
    A = 5
    AA = 6
    AAA = 7
    S = 8
    Sp = 9
    SS = 10
    SSp = 11
    SSS = 12
    SSSp = 13

    def __str__(self) -> str:
        return self.name.replace("p", "+")

    @classmethod
    def from_score(cls, score: int):
        if score >= 1009000:
            return cls.SSSp
        if score >= 1007500:
            return cls.SSS
        if score >= 1005000:
            return cls.SSp
        if score >= 1000000:
            return cls.SS
        if score >= 990000:
            return cls.Sp
        if score >= 975000:
            return cls.S
        if score >= 950000:
            return cls.AAA
        if score >= 925000:
            return cls.AA
        if score >= 900000:
            return cls.A
        if score >= 800000:
            return cls.BBB
        if score >= 700000:
            return cls.BB
        if score >= 600000:
            return cls.B
        if score >= 500000:
            return cls.C
        return cls.D


class Possession(Enum):
    NONE = 0
    SILVER = 1
    GOLD = 2
    PLATINUM = 3
    RAINBOW = 4

    @classmethod
    def from_str(cls, s: str):
        if s == "silver":
            return cls.SILVER
        if s == "gold":
            return cls.GOLD
        if s == "platina" or s == "platinum":
            return cls.PLATINUM
        if s == "rainbow":
            return cls.RAINBOW

        return cls.NONE

    def color(self):
        match self.value:
            case 0:
                return 0xCECECE
            case 1:
                return 0x6BAAC7
            case 2:
                return 0xFCE620
            case 3:
                return 0xFFF6C5
            case 4:
                return 0x0B6FF3


class SkillClass(Enum):
    I = 1  # noqa: E741
    II = 2
    III = 3
    IV = 4
    V = 5
    INFINITE = 6

    def __str__(self):
        if self.value == 6:
            return "∞"
        return self.name


class Genres(Enum):
    ALL = 99
    POPS_AND_ANIME = 0
    NICONICO = 2
    TOUHOU_PROJECT = 3
    ORIGINAL = 5
    VARIETY = 6
    IRODORIMIDORI = 7
    GEKIMAI = 9

    def __str__(self):
        if self.value == 99:
            return "All genres"
        if self.value == 0:
            return "POPS & ANIME"
        if self.value == 2:
            return "niconico"
        if self.value == 3:
            return "東方Project"
        if self.value == 5:
            return "ORIGINAL"
        if self.value == 6:
            return "VARIETY"
        if self.value == 7:
            return "イロドリミドリ"
        if self.value == 9:
            return "ゲキマイ"
        return None
