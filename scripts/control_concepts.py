"""
Phase 3a CONTROL concepts — the bracketing anchors that calibrate the structural-
convergence scale (see findings/phase3a-design.md §6). DRAFT term lists, first pass —
to be refined and FROZEN via a pre-committed selection rule before the 3a pre-registration.

Tiers:
  EATING      L3 positive control — shared embodied experience (LITERAL eating only)
  DRINKING    L3 positive control — shared embodied experience (thirst/water/drink)
  SLEEP       L3 positive control (3rd experiential anchor)
  GOVERNANCE  L2 functional / convergent-evolution anchor (NOT a zero-floor)
  WARFARE     L2 functional anchor (2nd)
EATING and DRINKING should converge near each other if the experiential-universal story
holds — a built-in consistency check on the positive bracket.
(The permutation null already supplies the L1 chance floor; SELF is the universality-
gradient mid-point and lives in harmonized_concepts.)

Matching mirrors harmonized_concepts: word-boundary regex for English; diacritic-folded
substring for Greek; raw substring for Han. Known collision risks are flagged inline and
must be resolved before freezing (e.g. βασιλ matches both 'king' and 'kingdom-of-God';
αρχ matches 'rule' and 'beginning/archē'; 法/禮 carry ritual senses; metaphorical eating
like 心齋 must be excluded).
"""

from __future__ import annotations

import re
import unicodedata

# ---- English (word-boundary regex; lowercase) ----
EN = {
    "EATING": ["eat", "eats", "ate", "eating", "eaten", "food", "bread", "loaf", "loaves",
               "hunger", "hungry", "famine", "meal", "feast", "dine", "supper", "devour",
               "meat", "nourish", "nourishment", "fed", "feed"],
    "DRINKING": ["drink", "drinks", "drank", "drunk", "drinking", "thirst", "thirsty",
                 "wine", "water", "cup", "beverage"],  # water/wine/cup carry metaphor (living water, the cup, eucharist)
    "SLEEP": ["sleep", "sleeps", "slept", "asleep", "sleeping", "slumber", "dream", "dreams",
              "dreamed", "bed", "drowsy"],  # 'awake/wake/rest' excluded (spiritual senses)
    "GOVERNANCE": ["king", "kings", "reign", "reigned", "throne", "ruler", "rule", "rules",
                   "govern", "governor", "government", "law", "laws", "judge", "judges",
                   "magistrate", "authority", "prince", "royal", "realm", "decree", "statute",
                   "council", "sovereign", "nation", "citizen", "kingdom"],  # 'kingdom/law' carry religious senses in scripture
    "WARFARE": ["war", "wars", "battle", "army", "armies", "soldier", "soldiers", "weapon",
                "weapons", "sword", "swords", "fight", "fought", "enemy", "enemies", "victory",
                "slay", "slain", "spear", "shield", "warrior", "conquer", "siege", "bow", "arrows"],
}

# ---- Greek (normalized: NFD strip combining, lowercase, final sigma; substring stems) ----
GR = {
    "EATING": ["εσθι", "εφαγ", "φαγ", "τροφ", "σιτ", "αρτο", "βρω", "πειν", "δειπν",
               "τραπεζ", "γευ", "κρεα", "λιμ"],
    "DRINKING": ["πιν", "διψ", "οινο", "ποτηρ"],  # dropped ποτ (ποταμος 'river') + υδ (ὕδωρ 'water', over-fires)
    "SLEEP": ["υπν", "καθευδ", "κοιμ", "ονειρ"],  # εγειρ excluded (resurrection)
    "GOVERNANCE": ["βασιλ", "νομ", "αρχων", "πολι", "δικαι", "βουλ", "τυρανν",
                   "δημ", "κρατ", "δικαστ", "ηγεμον", "θρον"],  # dropped αρχη ('beginning'); kept αρχων ('ruler')
    "WARFARE": ["πολεμ", "μαχ", "στρατ", "οπλ", "ξιφ", "νικ", "μαχαιρ", "τοξ", "δορ", "φον"],
}

# ---- Chinese (raw substring on Han) ----
ZH = {
    "EATING": ["食", "飯", "餓", "飢", "肉", "穀", "飽", "餅", "嚼", "啖", "糧", "餐"],
    "DRINKING": ["飲", "渴", "水", "酒", "漿", "杯", "茶"],  # 水 = water (metaphor risk)
    "SLEEP": ["寐", "眠", "睡", "寢", "夢", "臥", "枕"],  # 覺 excluded (wake/enlighten collision)
    "GOVERNANCE": ["君", "王", "國", "政", "臣", "治", "民", "官", "刑", "令", "侯", "朝", "邦", "禮"],  # dropped 法 (= dharma in Buddhist texts; loses Legalist sense — flag for freeze)
    "WARFARE": ["兵", "戰", "軍", "攻", "將", "敵", "殺", "武", "勝", "劍", "弓", "矛"],  # dropped 師 ('teacher') + 甲 ('first/stem')
}

CONCEPTS = ["EATING", "DRINKING", "SLEEP", "GOVERNANCE", "WARFARE"]


def _norm_gr(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower().replace("ς", "σ")


_EN_RX = {c: re.compile(r"\b(" + "|".join(map(re.escape, terms)) + r")\b", re.I)
          for c, terms in EN.items()}


def tag(language: str, text: str) -> list[str]:
    lang = language.lower()
    if lang.startswith("greek") or lang == "el":
        n = _norm_gr(text)
        return [c for c in CONCEPTS if any(_norm_gr(t) in n for t in GR[c])]
    if "chinese" in lang or lang == "zh":
        return [c for c in CONCEPTS if any(t in text for t in ZH[c])]
    return [c for c in CONCEPTS if _EN_RX[c].search(text)]
