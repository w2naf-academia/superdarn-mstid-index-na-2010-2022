#!/usr/bin/env python3
"""
Verify every DOI in this repository against the Crossref registry.

Why this exists
---------------
The reference list in README.md was once written from recollection rather than from a
bibliography, and two entries came out wrong in journal, volume, article number, and DOI.
Both bad DOIs resolved to real but unrelated papers, so a reader following either link was
sent to the wrong science with nothing to signal the error. It was caught by a human
noticing that a link opened the wrong paper.

This repository is citable and archived, so that class of error must not be able to recur
silently. The script enforces three things:

  1. Every DOI appearing anywhere in the documented files is listed in EXPECTED below.
     A newly added DOI therefore fails the check until someone states what it should be.
  2. Every DOI in EXPECTED still appears in README.md, so the table cannot go stale.
  3. Crossref's metadata for each DOI matches EXPECTED on first author, year, journal,
     volume and issue, and on the page range where Crossref supplies one.

EXPECTED holds the values Crossref reports, which are not always the values a citation
should print. Two examples in this list: Bristow et al. (1994) appeared in Journal of
Geophysical Research before the "Space Physics" split, and Crossref canonicalises the
modern name; and Radio Science article numbers (RS5012, RS4011) are not in Crossref's
page field at all. So this script checks the DOI's identity, and citation style stays a
human matter.

Usage
-----
    python tools/check_references.py             # full check, needs network
    python tools/check_references.py --offline   # coverage checks only, no network

Exit status is 0 when every check passes and 1 otherwise, so this is usable as a
pre-release gate. Only the standard library is required.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Files whose DOIs are checked. README.md is the one that must contain every entry.
SCANNED = ["README.md", "CITATION.cff", ".zenodo.json", "LICENSE-DATA"]

# doi -> what Crossref should report. See the module docstring on why these are
# Crossref's values rather than the printed citation's.
EXPECTED = {
    "10.1029/2009RS004141": dict(
        author="Blanchard", year=2009, journal="Radio Science",
        volume="44", issue="5", page=None, note="article RS5012"),
    "10.1029/93JA01470": dict(
        author="Bristow", year=1994,
        journal="Journal of Geophysical Research: Space Physics",
        volume="99", issue="A1", page="319-331", note="printed as J. Geophys. Res."),
    "10.1007/s10712-007-9017-8": dict(
        author="Chisham", year=2007, journal="Surveys in Geophysics",
        volume="28", issue="1", page="33-109", note=""),
    "10.1002/2015JA022168": dict(
        author="Frissell", year=2016,
        journal="Journal of Geophysical Research: Space Physics",
        volume="121", issue="4", page="3722-3739", note="defines the index"),
    "10.1007/BF00751350": dict(
        author="Greenwald", year=1995, journal="Space Science Reviews",
        volume="71", issue="1-4", page="761-796", note=""),
    "10.1186/s40645-019-0270-5": dict(
        author="Nishitani", year=2019,
        journal="Progress in Earth and Planetary Science",
        volume="6", issue="1", page=None, note="article 27"),
    "10.1029/2011RS004676": dict(
        author="Ribeiro", year=2011, journal="Radio Science",
        volume="46", issue="4", page=None, note="article RS4011"),
    "10.1029/98JA01288": dict(
        author="Ruohoniemi", year=1998,
        journal="Journal of Geophysical Research: Space Physics",
        volume="103", issue="A9", page="20797-20811", note=""),
}

# Award numbers funding this work, checked as literals in .zenodo.json. A typo in one is a
# funder-reporting error (A6) that nothing else in this repository would catch.
#
# These live in the record description rather than Zenodo's structured `grants` field. That
# field only accepts awards present in Zenodo's OpenAIRE-derived grant database, which covers
# the European Commission and a limited set of national funders; NASA is not in it. Supplying
# NASA's funder DOI there failed the v1.0.0 release with
# `{"errors": "Invalid value 10.13039/100000104."}`. Structured funding metadata can be added
# through the Zenodo web form after a record exists, where it is picked from their vocabulary
# rather than asserted blind.
EXPECTED_AWARDS = {
    "80NSSC23K0848",
    "80NSSC21K1772",
    "AGS-2045755",
}

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s)>\"',;]+")
UA = "check_references.py (+https://github.com/w2naf-academia/superdarn-mstid-index-na-2010-2022)"


def scan():
    """Return {doi: {files it appears in}} across SCANNED."""
    found = {}
    for name in SCANNED:
        path = REPO / name
        if not path.exists():
            continue
        for raw in DOI_RE.findall(path.read_text(encoding="utf-8")):
            found.setdefault(raw.rstrip(".,);>"), set()).add(name)
    return found


def crossref(endpoint, ident):
    req = urllib.request.Request(
        f"https://api.crossref.org/{endpoint}/{ident}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as fh:
        return json.load(fh)["message"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    ap.add_argument("--offline", action="store_true",
                    help="skip the Crossref lookups; run coverage checks only")
    args = ap.parse_args()

    found = scan()
    articles = {d: f for d, f in found.items()
                if not d.startswith("10.13039/") and "::" not in d}
    funders = {d: f for d, f in found.items() if d.startswith("10.13039/")}
    zenodo_text = (REPO / ".zenodo.json").read_text(encoding="utf-8")
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    failures = []

    print(f"Scanned {len(SCANNED)} files; found {len(articles)} article DOIs "
          f"and {len(funders)} funder ids.\n")

    # 1. Nothing unverified may appear in the files.
    print("[1] every DOI in the files is listed in EXPECTED")
    for doi in sorted(articles):
        if doi in EXPECTED:
            print(f"    ok    {doi}")
        else:
            print(f"    FAIL  {doi}  not in EXPECTED; add it with its verified metadata")
            failures.append(f"unlisted DOI {doi}")
    for doi in sorted(funders):
        print(f"    FAIL  {doi}  funder DOI in a file; Zenodo rejects these in `grants`")
        failures.append(f"unexpected funder DOI {doi}")

    # 2. The table may not go stale.
    print("\n[2] every EXPECTED DOI still appears in README.md")
    for doi in sorted(EXPECTED):
        if doi in readme:
            print(f"    ok    {doi}")
        else:
            print(f"    FAIL  {doi}  in EXPECTED but absent from README.md")
            failures.append(f"stale EXPECTED entry {doi}")

    # 2b. The award numbers must still be stated in the Zenodo record description.
    print("\n[2b] award numbers present in .zenodo.json")
    for award in sorted(EXPECTED_AWARDS):
        if award in zenodo_text:
            print(f"    ok    {award}")
        else:
            print(f"    FAIL  {award}  not stated in .zenodo.json")
            failures.append(f"missing award number {award}")

    # 3. Crossref must agree with the table.
    if args.offline:
        print("\n[3] Crossref comparison SKIPPED (--offline)")
    else:
        print("\n[3] Crossref metadata matches EXPECTED")
        for doi in sorted(EXPECTED):
            exp = EXPECTED[doi]
            try:
                m = crossref("works", doi)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as err:
                print(f"    FAIL  {doi}  lookup failed: {err}")
                failures.append(f"lookup failed {doi}")
                continue
            got = dict(
                author=(m.get("author") or [{}])[0].get("family"),
                year=(m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                journal=(m.get("container-title") or [None])[0],
                volume=m.get("volume"),
                issue=m.get("issue"),
                page=m.get("page"),
            )
            bad = [k for k in ("author", "year", "journal", "volume", "issue")
                   if str(got[k]) != str(exp[k])]
            if exp["page"] is not None and got["page"] != exp["page"]:
                bad.append("page")
            if bad:
                print(f"    FAIL  {doi}")
                for k in bad:
                    print(f"            {k}: registry {got[k]!r} != expected {exp[k]!r}")
                print(f"            registry title: {(m.get('title') or ['?'])[0][:80]}")
                failures.append(f"metadata mismatch {doi} ({', '.join(bad)})")
            else:
                print(f"    ok    {doi}  {got['author']} {got['year']}, "
                      f"{got['journal']} {got['volume']}({got['issue']})")

    print()
    if failures:
        print(f"FAILED: {len(failures)} problem(s)")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("All reference checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
