"""
Phase 2d — HARMONIZED concept operationalization (the frozen, pre-registerable
dictionary). Replaces the scattered per-gate-prep Option-A dicts with ONE canonical
source so every test uses identical concept definitions across all languages — a
precondition for cross-test comparison and for using Bible×Quran as a per-language
baseline (Δ_T = CCB_T − baseline).

MASTER SCOPE per concept (each language's term-list is derived from these facets):

  ULTIMATE     the absolute / ground-of-being / the divine / highest reality —
               named absolute (God/Allah/Dao/Brahman/the One/Buddha-nature/the Real),
               the divine, the supreme/first principle.
  SUBSTRATE    the formless non-being ground AND its modes:
               (a) emptiness/void, (b) non-being/the unmanifest, (c) the hidden/
               unseen ground, (d) impermanence/transience, (e) dissolution/
               annihilation. *Harmonized in 2d to cover all five facets in every
               language* (was technical-emptiness-only in the exploratory phase).
  AWARENESS    consciousness / mind / intellect / cognition / contemplation / gnosis.
  WORLD        the cosmos / phenomena / all-things / creation / beings.
  SELF         self / ego / soul / person / I / body.
  RECOGNITION  liberation / awakening / enlightenment / realization / salvation /
               beatific or unitive attainment.
  NONSEP       non-duality / oneness / unity / identity / fusion.

Cross-concept harmonization decisions (documented DoF):
  - Arabic فناء (fanaʾ, annihilation) -> SUBSTRATE (dissolution facet); بقاء
    (subsistence-in-God) stays RECOGNITION.
  - Hebrew הבל (hevel, vanity/transience) -> SUBSTRATE (impermanence facet).
  - Greek ματαιοτης (LXX Ecclesiastes 'vanity') -> SUBSTRATE.
  - English adds scriptural-emptiness vocab (vanity/breath/perish/the unseen/...).
  - Removed from SUBSTRATE: Japanese 理/性 (Confucian principle/nature — not
    emptiness); kept Greek υλη (matter-as-substratum, with caveat).

Precision caveat: broader terms (breath, perish, the-unseen) can over-tag mundane
content; terms kept tradition-distinctive where possible. Hidden-DoF caveat applies.
"""

from __future__ import annotations

import re
import unicodedata

# ---- normalization (per script) ----
_AR_TASHKEEL = re.compile(r"[ً-ْٰـ]")
_HE_NIQQUD = re.compile(r"[֑-ׇ]")
_HE_FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}


def _norm_ar(t):
    t = _AR_TASHKEEL.sub("", t)
    return t.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي")


def _norm_he(t):
    t = _HE_NIQQUD.sub("", t)
    return "".join(_HE_FINALS.get(c, c) for c in t)


def _norm_gr(t):
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower().replace("ς", "σ")


# match mode per language: "regex" (Latin), "substr" (CJK/Devanagari), or normalized substr
_MATCH = {
    "english": "regex", "french": "regex", "spanish": "regex",
    "classical_chinese": "substr", "japanese": "substr", "hindi": "substr",
    "arabic": ("substr", _norm_ar), "hebrew": ("substr", _norm_he), "greek": ("substr", _norm_gr),
}

# ---- harmonized term-lists: TERMS[language][concept] = [terms] ----
TERMS: dict[str, dict[str, list[str]]] = {
    "classical_chinese": {
        "ULTIMATE": ["道", "真如", "第一義", "法身", "佛性", "如來", "天"],
        "SUBSTRATE": ["空", "虛", "無", "無為", "緣起", "無常", "寂滅", "幻", "無形"],
        "AWARENESS": ["識", "覺", "念", "智慧", "明", "心", "意"],
        "WORLD": ["世間", "世界", "萬物", "諸法", "輪迴", "三界", "天下"],
        "SELF": ["無我", "我", "身", "己"],
        "RECOGNITION": ["涅槃", "解脫", "解脱", "菩提", "覺悟", "漏盡", "證", "得道"],
        "NONSEP": ["不二", "一如", "平等", "齊物"],
    },
    "japanese": {
        "ULTIMATE": ["道", "天命", "仏", "佛", "如来", "如來", "法身", "阿弥陀", "弥陀", "本願", "誠", "太極", "上帝"],
        "SUBSTRATE": ["空", "無", "虚", "無為", "無常", "寂", "滅", "儚", "幻"],
        "AWARENESS": ["心", "意識", "智慧", "悟", "覚", "念", "信心", "知", "明", "思"],
        "WORLD": ["世界", "世間", "万物", "萬物", "天下", "衆生", "諸法", "三界"],
        "SELF": ["自己", "自身", "己", "我", "身"],
        "RECOGNITION": ["涅槃", "解脱", "往生", "成仏", "成佛", "菩提", "悟り", "至誠"],
        "NONSEP": ["不二", "一如", "一体", "一體", "一味"],
    },
    "hindi": {
        "ULTIMATE": ["राम", "हरि", "ब्रह्म", "ईश्वर", "ईस्वर", "भगवान", "प्रभु", "साहिब", "साईं",
                     "गोविन्द", "गोबिंद", "परमात्मा", "परमातमा", "अलख", "निरंजन"],
        "SUBSTRATE": ["सून्य", "शून्य", "निरगुन", "निर्गुण", "माया", "अव्यक्त", "निराकार", "नश्वर", "क्षणिक", "लय", "अभाव"],
        "AWARENESS": ["मन", "ग्यान", "ज्ञान", "सुरति", "सुरत", "सुमिरन", "ध्यान", "बुद्धि", "बिबेक", "विवेक", "चेत", "बोध"],
        "WORLD": ["जगत", "संसार", "संसा", "सृष्टि", "लोक", "भव"],
        "SELF": ["आतम", "आत्मा", "जीव", "अहंकार", "अहं", "देह", "काया", "पिंड"],
        "RECOGNITION": ["मोक्ष", "मुक्ति", "मुकति", "निर्वान", "निरवान", "भक्ति", "भगति", "दरसन", "दर्शन", "मिलन", "सहज"],
        "NONSEP": ["अद्वैत", "अभेद", "समता", "अनन्य", "लीन", "एकै"],
    },
    "arabic": {  # normalized (no tashkeel; alef/ya folded)
        "ULTIMATE": ["الله", "الحق", "الحقيقه", "الذات", "الالهيه", "الربوبيه", "الاسماء", "الواجب"],
        "SUBSTRATE": ["العدم", "العماء", "الغيب", "البطون", "الفناء", "الزوال", "الهلاك", "الخلاء", "الامكان"],
        "AWARENESS": ["العقل", "القلب", "المعرفه", "الشهود", "المشاهده", "البصيره", "العلم", "الذوق"],
        "WORLD": ["العالم", "الكون", "الاكوان", "الخلق", "المخلوق", "الموجودات", "الطبيعه"],
        "SELF": ["النفس", "الروح", "الانا", "العبد"],
        "RECOGNITION": ["البقاء", "الكشف", "التجلي", "الوصول", "الفتح", "الولايه", "النجاه"],
        "NONSEP": ["التوحيد", "الوحده", "الاتحاد", "الجمع"],
    },
    "hebrew": {  # normalized (no niqqud; finals folded)
        "ULTIMATE": ["אלהים", "הבורא", "הקדוש ברוך", "השם", "אדני", "יהוה", "אין סוף", "המקום", "רבונו"],
        "SUBSTRATE": ["העדר", "אפס", "תהו", "הבל", "כליון", "אפיסה", "חומר"],
        "AWARENESS": ["שכל", "דעת", "בינה", "חכמה", "מחשבה", "הכרה", "השגה", "הבנה", "מוחין"],
        "WORLD": ["עולמ", "בריאה", "יקומ", "טבע", "נבראימ", "מציאות"],
        "SELF": ["נפש", "נשמה", "עצמ", "גופ", "רוח", "אנכי"],
        "RECOGNITION": ["גאולה", "דבקות", "תשובה", "שלמות", "דבק", "השגת"],
        "NONSEP": ["יחוד", "אחדות", "ביטול", "התכללות"],
    },
    "greek": {  # normalized (diacritic-free, lowercase, final-sigma folded)
        "ULTIMATE": ["θεο", "αγαθο", "θειο", "δημιουργ", "το εν", "το πρωτον"],
        "SUBSTRATE": ["στερησι", "απειρ", "ανειδε", "μη ον", "φθορα", "κενωσι", "κενο", "ματαιοτη"],  # 2026-05-24: dropped υλη (matter — violates the non-being master scope, opposite pole from emptiness); added κενο (void)
        "AWARENESS": ["νουσ", "νοησ", "διανοι", "αισθησ", "γνωσ", "θεωρι", "συνειδ", "φρονησ"],
        "WORLD": ["κοσμο", "φυσι", "αισθητ", "τα οντα", "το παν"],
        "SELF": ["ψυχ", "σωμα", "εγω", "ζωον"],
        "RECOGNITION": ["ενωσι", "εκστασι", "επιστροφ", "σωτηρι", "ομοιωσι"],
        "NONSEP": ["απλοτη", "ομου", "ταυτον"],
    },
    "french": {
        "ULTIMATE": [r"\btao\b", r"\bla voie\b", r"\bdieu\b", r"\bbrahma", r"\babsolu", r"\bsuprême",
                     r"\bseigneur\b", r"\bbien[- ]?aimé", r"\bépoux\b", r"\bdivin", r"\btrès[- ]?haut"],
        "SUBSTRATE": [r"\bvide\b", r"\bnéant", r"\bnon[- ]?être", r"\bnon[- ]?agir", r"\bsans nom",
                      r"\babîme", r"\bsans forme", r"\bvanité", r"\bpérissable", r"\banéantissement", r"\béphémère"],
        "AWARENESS": [r"\bconscience", r"\besprit\b", r"\bintelligence", r"\bentendement", r"\bcontemplation",
                      r"\bconnaissance", r"\bperception", r"\bintellect", r"\blumière"],
        "WORLD": [r"\bmonde\b", r"\bunivers", r"\btoutes choses", r"\bcréation", r"\bcréatures?", r"\bciel et",
                  r"\bêtres\b", r"\bphénomène"],
        "SELF": [r"\bsoi[- ]?même", r"\ble moi\b", r"\bego\b", r"\bla personne\b", r"\ble corps\b", r"\bmon âme\b"],
        "RECOGNITION": [r"\bunion\b", r"\blibération", r"\bdélivrance", r"\billumination", r"\bréalisation",
                        r"\bsalut\b", r"\bextase", r"\bravissement", r"\bdéification", r"\bbéatitude"],
        "NONSEP": [r"\bunité\b", r"\bnon[- ]?dualité", r"\bindistinct", r"\bfusion\b", r"\bne faire qu['’]un", r"\bun seul\b"],
    },
    "spanish": {
        "ULTIMATE": [r"\bDios\b", r"\bel Señor\b", r"\bdivin", r"\babsoluto\b", r"\bla Divinidad\b",
                     r"\bel Amado\b", r"\bel Esposo\b", r"\bCristo\b", r"\bsumo bien\b"],
        "SUBSTRATE": [r"\bnada\b", r"\bvacío\b", r"\babismo\b", r"\bno[- ]?ser\b", r"\baniquila", r"\bvanidad",
                      r"\bperecedero", r"\binforme\b", r"\bdisoluci"],
        "AWARENESS": [r"\bconciencia\b", r"\balma\b", r"\bentendimiento\b", r"\bmente\b", r"\bcontemplaci",
                      r"\bconocimiento\b", r"\brazón\b", r"\bintelecto\b", r"\bespíritu\b"],
        "WORLD": [r"\bmundo\b", r"\buniverso\b", r"\bcriaturas?\b", r"\bcreación\b", r"\btodas las cosas\b", r"\blo creado\b"],
        "SELF": [r"\bsí mismo\b", r"\bel yo\b", r"\bego\b", r"\bla persona\b", r"\bel cuerpo\b", r"\bpropia voluntad\b"],
        "RECOGNITION": [r"\bunión\b", r"\béxtasis\b", r"\barrobamiento\b", r"\btransformaci", r"\bsalvación\b",
                        r"\bdeificaci", r"\bperfección\b", r"\bgracia\b"],
        "NONSEP": [r"\bunidad\b", r"\buno\b", r"\bfusión\b", r"\bindistint", r"\bno hay distinción\b"],
    },
    "english": {
        "ULTIMATE": [r"\btao\b", r"\bthe way\b", r"\bsuchness\b", r"\bbuddha[- ]?nature\b", r"\bdharma[- ]?body\b",
                     r"\btathagata\b", r"\bgod\b", r"\blord\b", r"\bdivine\b", r"\bbrahman\b", r"\bthe absolute\b",
                     r"\bthe supreme\b", r"\bthe eternal\b", r"\bthe holy\b", r"\bthe real\b", r"\bheaven\b"],
        "SUBSTRATE": [r"\bemptiness\b", r"\bvoid\b", r"\bnon[- ]?being\b", r"\bthe formless\b", r"\bthe nameless\b",
                      r"\bimpermanen", r"\bcessation\b", r"\bnon[- ]?action\b", r"\bvanity\b", r"\bmeaningless\b",
                      r"\bfleeting\b", r"\bvapou?r\b", r"\bbreath\b", r"\bperish", r"\bpass(es|ing)? away\b",
                      r"\btransien", r"\bthe unseen\b", r"\bdissolution\b", r"\bannihilat", r"\bnothingness\b"],
        "AWARENESS": [r"\bconsciousness\b", r"\bawareness\b", r"\bmind\b", r"\bmindful", r"\bthought\b", r"\bthinking\b",
                      r"\bwisdom\b", r"\bclarity\b", r"\billumination\b", r"\bintellect", r"\bintelligence\b",
                      r"\bperception\b", r"\bunderstanding\b", r"\bspirit\b", r"\bknowing\b"],
        "WORLD": [r"\bworld\b", r"\bmyriad\b", r"\bten thousand things\b", r"\ball things\b", r"\ball dharmas\b",
                  r"\bsamsara\b", r"\bthree realms\b", r"\bcreation\b", r"\bbeings\b", r"\bheaven and earth\b",
                  r"\buniverse\b", r"\bphenomen"],
        "SELF": [r"\bnon[- ]?self\b", r"\bthe self\b", r"\bself\b", r"\bego\b", r"\bthe body\b", r"\bthe soul\b", r"\bthe person\b"],
        "RECOGNITION": [r"\bnirvana\b", r"\bnibbana\b", r"\bliberation\b", r"\bbodhi\b", r"\bawakening\b", r"\benlightenment\b",
                        r"\brealization\b", r"\bsalvation\b", r"\bdeliverance\b", r"\bdeathless\b", r"\bfreedom\b"],
        "NONSEP": [r"\bnon[- ]?dual", r"\boneness\b", r"\bunity\b", r"\bsameness\b", r"\bequality\b", r"\bundivided\b", r"\bbecome one\b"],
    },
}

CONCEPTS = ["ULTIMATE", "SUBSTRATE", "AWARENESS", "WORLD", "SELF", "RECOGNITION", "NONSEP"]


def tag(language: str, text: str) -> list[str]:
    """Harmonized concept tags for `text` in `language`."""
    lang = "classical_chinese" if language in ("classical_chinese", "chinese") else language
    terms = TERMS.get(lang)
    if terms is None:
        return []
    mode = _MATCH[lang]
    if mode == "regex":
        return [c for c, pats in terms.items() if any(re.search(p, text, re.IGNORECASE) for p in pats)]
    if isinstance(mode, tuple):           # normalized substring (ar/he/gr)
        norm = mode[1]; t = norm(text)
        return [c for c, ts in terms.items() if any(norm(x) in t for x in ts)]
    return [c for c, ts in terms.items() if any(x in text for x in ts)]  # plain substring (zh/ja/hi)
