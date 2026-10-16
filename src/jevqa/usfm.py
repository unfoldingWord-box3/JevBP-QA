"""Just enough USFM: UGNT word lists and aligned (zaln) or plain translations."""

import re
import unicodedata

from jevqa.model import Alignment, GreekVerse, GreekWord, TargetVerse

# Lines that carry headings or book metadata, never verse text.
_SKIP_LINE = re.compile(r"^\\(id|ide|usfm|h|toc\d?|mt\d?|ms\d?|mr|s\d?|sr|r|d|sp|cl|rem|sts|b)\b")
_NOTE = re.compile(r"\\(f|x|fe) .*?\\\1\*")
_TOKEN = re.compile(
    r"\\zaln-s\s*\|(?P<zs>.*?)\\\*"
    r"|(?P<ze>\\zaln-e\\\*)"
    r"|\\w\s+(?P<w>[^|\\]*?)(?:\|[^\\]*)?\\w\*"
    r"|\\\+?[a-z0-9-]+\*?\s?|\\\*"  # any other marker: dropped, text kept
)
_ATTR = re.compile(r'([\w-]+)="([^"]*)"')


def _verses(usfm: str):
    """Yield (ref, raw content) for each verse, headings and notes removed."""
    chapter, verse, buf = None, None, []
    for line in usfm.splitlines():
        line = line.strip()
        if not line or _SKIP_LINE.match(line):
            continue
        for part in re.split(r"(\\c\s+\d+|\\v\s+\d+[-\d]*)", _NOTE.sub("", line)):
            if m := re.match(r"\\c\s+(\d+)", part):
                if verse:
                    yield f"{chapter}:{verse}", " ".join(buf)
                chapter, verse, buf = m[1], None, []
            elif m := re.match(r"\\v\s+([\d-]+)", part):
                if verse:
                    yield f"{chapter}:{verse}", " ".join(buf)
                verse, buf = m[1], []
            elif verse:
                buf.append(part)
    if verse:
        yield f"{chapter}:{verse}", " ".join(buf)


def norm(word: str) -> str:
    """Comparison key for Greek words: NFC, casefolded, punctuation and elision marks removed."""
    w = unicodedata.normalize("NFC", word).casefold()
    return "".join(ch for ch in w if not unicodedata.category(ch).startswith("P") and ch not in "ʼ’᾽'")


def parse_ugnt(usfm: str) -> dict[str, GreekVerse]:
    out = {}
    for ref, content in _verses(usfm):
        words, seen = [], {}
        for m in re.finditer(r"\\w\s+([^|\\]+)\|([^\\]*)\\w\*", content):
            surface, attrs = m[1].strip(), dict(_ATTR.findall(m[2]))
            seen[surface] = seen.get(surface, 0) + 1
            words.append(GreekWord(surface, attrs.get("lemma", ""), attrs.get("strong", ""), seen[surface]))
        out[ref] = GreekVerse(ref, tuple(words))
    return out


def parse_target(usfm: str) -> dict[str, TargetVerse]:
    """Verse text, words, and Greek alignment groups (if the file is aligned)."""
    out = {}
    for ref, content in _verses(usfm):
        text, words, groups = [], [], []
        depth, open_greek, open_words = 0, [], []
        pos = 0
        for m in _TOKEN.finditer(content):
            text.append(content[pos:m.start()])
            pos = m.end()
            if m["zs"] is not None:
                a = dict(_ATTR.findall(m["zs"]))
                open_greek.append((a.get("x-content", ""), int(a.get("x-occurrence", "1"))))
                depth += 1
            elif m["ze"]:
                depth -= 1
                if depth == 0 and open_greek:
                    groups.append(Alignment(tuple(open_greek), tuple(open_words)))
                    open_greek, open_words = [], []
            elif m["w"] is not None:
                text.append(m["w"])
                if depth:
                    open_words.append(len(words))
                words.append(m["w"])
            else:
                text.append(" " if m[0].endswith(" ") else "")
        text.append(content[pos:])
        clean = re.sub(r"\s+", " ", "".join(text)).strip()
        clean = re.sub(r"\s+([,.;:!?»)\]])", r"\1", clean)
        if not words:  # plain USFM without \w markup
            words = re.findall(r"[^\W\d_][\w’'̰̂̀́-]*", clean)
        out[ref] = TargetVerse(ref, clean, tuple(words), tuple(groups))
    return out


def find_phrase(verse: GreekVerse, phrase: str, occurrence: int) -> list[GreekWord]:
    """Greek words matching a tN/TWL quote. `&` separates discontinuous parts.

    occurrence counts matches of the whole quote; -1 means every match.
    """
    parts = [[norm(w) for w in p.split()] for p in phrase.split("&")]
    parts = [[w for w in p if w] for p in parts]
    keys = [norm(w.surface) for w in verse.words]
    matches = []
    for start in range(len(keys)):
        found, i = [], start
        for k, part in enumerate(parts):
            # first part must start here; later parts may start anywhere after
            j = i if k == 0 else next((j for j in range(i, len(keys)) if keys[j:j + len(part)] == part), None)
            if j is None or keys[j:j + len(part)] != part:
                found = None
                break
            found += range(j, j + len(part))
            i = j + len(part)
        if found:
            matches.append([verse.words[x] for x in found])
    if occurrence == -1:
        return [w for m in matches for w in m]
    return matches[occurrence - 1] if 0 < occurrence <= len(matches) else []


def rendering(target: TargetVerse, greek: list[GreekWord]) -> str | None:
    """Target words aligned to any of these Greek words, in verse order; gaps shown as …"""
    if not target.alignments or not greek:
        return None
    # Occurrence counts are per exact surface form on both sides, so compare NFC surfaces, not norm().
    nfc = lambda s: unicodedata.normalize("NFC", s)
    want = {(nfc(w.surface), w.occurrence) for w in greek}
    idx = sorted({i for a in target.alignments if any((nfc(s), o) in want for s, o in a.greek) for i in a.target})
    if not idx:
        return ""  # aligned translation, but these Greek words have no target words
    out = [target.words[idx[0]]]
    for prev, i in zip(idx, idx[1:]):
        out.append(target.words[i] if i == prev + 1 else f"… {target.words[i]}")
    return " ".join(out)
