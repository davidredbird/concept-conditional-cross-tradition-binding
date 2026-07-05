"""
Patch gradient-corpus metas that predate the sphere/contact_level/transmission schema
(Plato, Aristotle, Plotinus, Clement; TTC, Zhuangzi, Analects, Platform Sutra, faju).
Metadata only — does NOT touch text (firewall-safe). john_chinese is scripture, NOT a
gradient text, so it is intentionally left without a sphere (stays excluded from cells).
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
MD = Path(__file__).resolve().parent.parent / "corpus" / "books" / "cleaned"

# new-schema fields (sphere/contact_level/transmission always set); era/category only if absent
PATCH = {
    "plato_greek":          {"sphere": "greek",   "contact_level": "independent"},
    "aristotle_greek":      {"sphere": "greek",   "contact_level": "independent"},
    "plotinus_greek":       {"sphere": "greek",   "contact_level": "high-contact", "_era": "~3c CE",   "_category": "nondual"},
    "clement_greek":        {"sphere": "greek",   "contact_level": "high-contact", "_era": "~2-3c CE", "_category": "mixed"},
    "taote_chinese":        {"sphere": "chinese", "contact_level": "independent",  "transmission": "indigenous"},
    "zhuangzi_chinese":     {"sphere": "chinese", "contact_level": "independent",  "transmission": "indigenous", "_era": "~4c BCE", "_category": "nondual"},
    "analects_chinese":     {"sphere": "chinese", "contact_level": "independent",  "transmission": "indigenous", "_era": "~5c BCE", "_category": "dualistic"},
    "platform_sutra_chinese": {"sphere": "chinese", "contact_level": "high-contact", "transmission": "sinified-hybrid"},
    "faju_jing_chinese":    {"sphere": "chinese", "contact_level": "early-contact", "transmission": "imported", "_era": "~1c CE", "_category": "nondual"},
}

for cid, fields in PATCH.items():
    p = MD / f"{cid}.meta.json"
    m = json.loads(p.read_text(encoding="utf-8"))
    for k, v in fields.items():
        if k.startswith("_"):          # set only if absent
            m.setdefault(k[1:], v)
        else:                           # always set the new schema field
            m[k] = v
    p.write_text(json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  {cid:24s} sphere={m['sphere']} contact={m['contact_level']} cat={m.get('category')} era={m.get('era')}")
print("done")
