"""Door43 sources, pinned to a commit and cached under data/raw/.

Every fetch records the commit SHA it came from in data/sources.json, so a
run can say exactly which text it checked.
"""

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

DCS = "https://git.door43.org"
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
LOCK = ROOT / "data" / "sources.json"


@dataclass(frozen=True)
class Source:
    repo: str
    ref: str  # branch or tag; resolved to a commit SHA on first fetch
    path: str | None  # single file; None for article collections (tW)
    license: str
    note: str = ""


SOURCES = {
    "ugnt": Source("unfoldingWord/el-x-koine_ugnt", "v0.34", "57-TIT.usfm", "CC BY-SA 4.0",
                   "unfoldingWord Greek New Testament; v0.34 is the version BSB and RSOB are aligned to"),
    "en_tn": Source("unfoldingWord/en_tn", "master", "tn_TIT.tsv", "CC BY-SA 4.0"),
    "en_twl": Source("unfoldingWord/en_twl", "master", "twl_TIT.tsv", "CC BY-SA 4.0"),
    "en_tw": Source("unfoldingWord/en_tw", "master", None, "CC BY-SA 4.0"),
    "en_ult": Source("unfoldingWord/en_ult", "master", "57-TIT.usfm", "CC BY-SA 4.0",
                     "source text the Masalit team translated from"),
    "bsb": Source("Worldview/en_bsb", "master", "57-TIT.usfm", "Public domain (BSB); alignment CC BY-SA 4.0",
                  "Berean Standard Bible, word-aligned to UGNT 0.34 by Worldview"),
    "hi_irv": Source("Door43-Catalog/hi_irv", "master", "57-TIT.usfm", "CC BY-SA 4.0",
                     "Indian Revised Version (Hindi), aligned to UGNT 0.13 (older than 0.34)"),
    "hi_tw": Source("Door43-Catalog/hi_tw", "master", None, "CC BY-SA 4.0"),
    "ar_nav": Source("BSOJ/ar_nav", "master", "57-TIT.usfm", "CC BY-SA 4.0 (Biblica open license; repo LICENSE.md is uW boilerplate)",
                     "New Arabic Version (Ketab El Hayat), aligned to UGNT 0.34"),
    "ar_tw": Source("BSOJ/ar_tw", "master", None, "CC BY-SA 4.0"),
    "ru_rsob": Source("ru_gl/ru_rsob", "master", "57-TIT.usfm", "CC BY-SA 4.0",
                      "Russian Simplified Open Bible, aligned to UGNT 0.34"),
    "ru_rsb": Source("Door43-Catalog/ru_rsb", "master", "57-TIT.usfm", "Public domain (1876 text); alignment CC BY-SA 4.0",
                     "Russian Synodal Bible, aligned to UGNT (2019, version not stated)"),
    "ru_tw": Source("ru_gl/ru_tw", "master", None, "CC BY-SA 4.0"),
    "mdg_ssv": Source("Nhial/mdg_ssv_tit_book", "master", "mdg_ssv_tit_book.usfm", "CC BY-SA 4.0",
                      "Masalit Titus (repo uses code mdg; ISO 639-3 for Masalit is mls), unaligned, translated from ULT"),
}


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "jevqa"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def _lock() -> dict:
    return json.loads(LOCK.read_text()) if LOCK.exists() else {}


def _resolve(src: Source) -> str:
    """Commit SHA for a branch or tag."""
    for kind in ("branches", "tags"):
        try:
            d = json.loads(_get(f"{DCS}/api/v1/repos/{src.repo}/{kind}/{src.ref}"))
            return d["commit"].get("id") or d["commit"]["sha"]  # branches use id, tags use sha
        except urllib.error.HTTPError:
            continue
    raise RuntimeError(f"cannot resolve {src.repo}@{src.ref}")


def sha(key: str) -> str:
    """Pinned commit for a source, resolving and recording it on first use."""
    lock = _lock()
    if key not in lock:
        src = SOURCES[key]
        lock[key] = {"repo": src.repo, "ref": src.ref, "sha": _resolve(src), "license": src.license, "note": src.note}
        LOCK.parent.mkdir(parents=True, exist_ok=True)
        LOCK.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n")
    return lock[key]["sha"]


def fetch(key: str, path: str | None = None) -> str:
    """Text of a source file (its default path, or `path` inside the repo), cached."""
    src = SOURCES[key]
    path = path or src.path
    dest = RAW / key / path
    if not dest.exists():
        data = _get(f"{DCS}/{src.repo}/raw/commit/{sha(key)}/{path}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    return dest.read_text(encoding="utf-8")


def fetch_optional(key: str, path: str) -> str | None:
    """Like fetch, but None when the file does not exist in the repo."""
    try:
        return fetch(key, path)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
