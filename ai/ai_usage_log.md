# AI Usage Log — mstid_index

This log records substantive AI-assisted sessions in this repository.

Required per the University of Scranton AI Policy, the HamSCI Generative AI Use Agreement, and
NASA and NSF guidance on generative AI in funded research. NAF's contribution to this work is
supported by NASA 80NSSC23K0848, NSF AGS-2045755, and NASA 80NSSC21K1772.

**The data in `data/` predates any AI involvement.** It was computed by `DARNtids` and exported
from MongoDB on 23 October 2023. No AI tool has touched the index values, and none has recomputed
them. AI assistance in this repository is confined to documentation and to keeping the plotting
script running on current Python releases.

**`superdarn_mstid_plot.py` was written by N. A. Frissell.** Entries below record later edits to
it, each of which is listed line by line.

---

<!-- Newest entries at the bottom. -->

## [2026-08-31 20:43 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: Bring the repository up to date for a Zenodo data release, so a collaborator
  can cite it and describe the MSTID index in her own paper. Directed by NAF. Tracked as
  w2naf-academia/MSTID-Climatology-Paper-2026-Project#52.
- **Sections/Files Affected**:
  - `README.md`: rewritten and expanded from 33 lines to roughly 430. New material: a description
    of what the SuperDARN MSTID index is and how it is derived, a full data dictionary, the radar
    and season tables, interpretation guidance, known limitations, provenance, and a reference
    list. The stale `w2naf/mstid_index` clone URL was corrected to `w2naf-academia/mstid_index`.
  - `superdarn_mstid_plot.py`: seven forward-compatibility edits, listed under Verification below.
  - `requirements.txt`: version floors added for the eight packages, matching the environment the
    committed `output/` was reproduced against.
  - `ai/ai_usage_log.md`: this file, new.
  - `data/` and `output/` were **not** modified.
- **Nature of Contribution**: Documentation drafting, and small code edits for forward
  compatibility. No change to any scientific method, threshold, or result.
- **Human Review Status**: Pending review. NAF set the objective and the scope; he has not yet read
  the README text or the code diff.
- **Verification**:
  - The script was run end to end before any edit, and again after, against the full twelve-season
    dataset on Python 3.13.11 with matplotlib 3.10.8, NumPy 2.2.6, SciPy 1.14.1, pandas 2.3.3, and
    xarray 2025.12.0. Both runs completed successfully.
  - The post-edit run reproduces the committed `output/`. All 14 PNGs are **pixel-identical**
    (maximum per-channel difference 0). Sixteen of the 24 CSVs are byte-identical apart from their
    generation timestamp. The other eight are the reduced-index files, whose headers are identical
    and whose numbers agree to 1.78e-15, roughly eight times float64 epsilon, from accumulation
    order in `numpy`. The committed `output/` was therefore left in place rather than replaced with
    a churned copy.
  - The seven code edits, each verified against the documentation of the library concerned:
    1. `mpl.cm.get_cmap('cet_CET_C6')` to `mpl.colormaps['cet_CET_C6']`. `get_cmap` was deprecated
       in matplotlib 3.7 and is removed in 3.11.
    2. `sp.nanmedian` to `np.nanmedian`. `scipy.nanmedian` was removed in SciPy 1.3, so this line
       would have raised `AttributeError` on any run with `reduction_type='median'`. The default is
       `'mean'`, so it had never been reached.
    3. `datetime.datetime.utcnow()` to `datetime.datetime.now(datetime.timezone.utc)`, at two
       sites, both writing the "Generated on" line of a CSV header. `utcnow` is deprecated as of
       Python 3.12. `.replace(tzinfo=None)` preserves the header's existing text format.
    4. `param.rstrip('_reducedIndex')` to `param.removesuffix('_reducedIndex')`. `str.rstrip`
       strips a character set. It returns the intended result for the one parameter in use and
       would silently truncate a parameter name ending in any of `_rediucnIx`.
    5. `xr.concat(ds, dim='index')` given an explicit `join='outer'`. xarray warns that the default
       will become `join='exact'`, which these per-radar datasets cannot satisfy, since their date
       coordinates differ in length.
    6. `np.nanmin(...)` wrapped in `float(...)` at three sites computing `min_orig_rti_fraction`.
    7. A new `native()` helper applied to `dsr.attrs` on load. Items 6 and 7 address the same
       regression: NumPy 2 changed scalar repr, so a NumPy float in an attribute dictionary renders
       as `np.float64(0.25)`, and these dictionaries are printed verbatim into the CSV headers. The
       headers now match the committed files exactly.
  - The description of the index in the README was written against
    [Frissell et al. (2016)](https://doi.org/10.1002/2015JA022168) section 2.2, against the
    implementation in `DARNtids` (`darntids/classify.py`, the `intSpect` / `meanSubIntSpect` /
    `_by_rtiCnt` computation, and `darntids/more_music.py` for the filter parameters
    `numtaps=101`, `cutoff_low=0.0003 Hz`, `cutoff_high=0.0012 Hz`), and against the parameter
    explanations already present in this repository's own CSV headers. It was then checked for
    consistency against the corresponding methods text of the paper in preparation, which is not
    reproduced here.
  - The dataset's identity with the run used by that paper was confirmed by content rather than by
    name: `diff -rq` reports the 240 files in
    `data/mongo_out/mstid_GSMR_fitexfilter_rtiThresh-0.25/guc/` byte-identical to the same-named
    directory in the paper's code repository.
- **Still open**: `LICENSE`, `CITATION.cff`, and `.zenodo.json` are not yet written, and the README
  carries bracketed placeholders for the license, the use terms, and the Zenodo DOI. These need
  NAF's decisions before they can be filled in.
- **Git Hash**: 5c95758

## [2026-08-31 20:52 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: Same session as the entry above, continued after NAF answered the three
  open release questions.
- **NAF's decisions** (all three, his recommended-option choices, 2026-08-31):
  1. **License**: GPL-3.0 for the code, CC-BY-4.0 for the data.
  2. **Use terms**: attribution as the only condition, plus a courtesy notice that carries no
     obligation. This retires the previous "contact NAF before using this code or data" line.
  3. **Zenodo authorship**: N. A. Frissell alone. The `DARNtids` and `pyDARNmusic` lineage is
     credited by citing that software, which the README and `CITATION.cff` both do.
- **Sections/Files Affected**: `LICENSE` (new, GPL-3.0), `LICENSE-DATA` (new, CC-BY-4.0),
  `CITATION.cff` (new), `.zenodo.json` (new), `README.md` (the Rules of the road, Citation, and
  License sections; all license placeholders resolved).
- **Nature of Contribution**: Drafting of release metadata, to NAF's stated decisions.
- **Human Review Status**: Pending review. NAF made the three decisions; he has not read the
  resulting files.
- **Verification**:
  - `LICENSE` is a byte-identical copy of the GPL-3.0 text already in
    `MSTID-Climatology-Paper-2026` and `DARNtids` (md5 `1ebbd3e34237af26da5dc08a4e440464` in all
    three), rather than a transcription from memory.
  - `LICENSE-DATA` **references** the canonical CC-BY-4.0 legal code at creativecommons.org rather
    than reproducing it. Reproducing a license text from memory risks a subtly wrong legal
    instrument (W12), and a reference cannot drift from the canonical version.
  - `.zenodo.json` parses as JSON; `CITATION.cff` parses as YAML with `cff-version: 1.2.0`.
  - NAF's ORCID `0000-0002-8398-4222` was taken from the author block of `overleaf/main.tex`, and
    his affiliation from `\affiliation{1}` there.
  - The three grant identifiers in `.zenodo.json` are the ones named in the project's governance
    file: NASA 80NSSC23K0848, NASA 80NSSC21K1772, NSF AGS-2045755.
- **Still open**: the Zenodo DOI itself. The README carries `[DOI to be assigned at release]` in
  two places (W13) until the record exists. Minting it means enabling the Zenodo webhook and
  pushing a version tag, which is irreversible and needs NAF's explicit authorization at the time
  (R3).
- **Git Hash**: 4b1227d

## [2026-08-31 21:05 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: NAF asked whether the required SuperDARN data acknowledgment from
  <https://vt.superdarn.org/data-acknowledgement> had been included, and whether any radars were
  missed. It had not been. Add it.
- **Sections/Files Affected**: `README.md`: new `## Required acknowledgment` section, a table-of-
  contents entry, and the Rules of the road sentence updated to name the acknowledgment as a
  condition of use alongside attribution.
- **Nature of Contribution**: Correction of an omission in the previous session's README.
- **Human Review Status**: Pending review. NAF supplied the statement text and identified the gap.
- **What was wrong**: the previous session's README carried a two-sentence paraphrase naming the
  ten funding countries and linking the data policy. It dropped every per-radar operator and award
  clause, which is the substantive part of the requirement.
- **Verification**:
  - The block in the README is **character-for-character identical** to the statement NAF supplied,
    checked programmatically after whitespace normalization for the Markdown blockquote wrapping.
  - **All ten radars in the bundle are covered by the statement**, checked by matching each radar's
    full name against the text: Prince George, Saskatoon, Kapuskasing, Goose Bay, Christmas Valley
    West, Christmas Valley East, Fort Hays West, Fort Hays East, Blackstone, Wallops Island. None
    missing, and the statement names no radar absent from the dataset.
  - **`AGU-2426201` for Wallops Island was left exactly as supplied and not corrected.** It is
    likely a typo for `AGS-`: the two sibling awards in the same statement are `AGS-2426199` and
    `AGS-2426200`, and NSF Geosciences awards carry the `AGS` prefix. Silently altering a required
    verbatim statement is the wrong call, so it stands and is flagged to NAF to confirm with
    Virginia Tech. The README tells the reader the generator is the authority and to re-check it
    before submitting.
  - The generator page could not be fetched for independent confirmation: it builds the statement
    client-side, so the text is absent from the served HTML.
- **Related finding, not acted on**: `overleaf/main.tex` line 363 carries an **older version of
  this same statement**, with superseded operators and award numbers (Virginia Tech `AGS-1935110`,
  Dartmouth `AGS-1341925`, Saskatoon and Prince George attributed to "the University of
  Saskatchewan" rather than SuperDARN Canada, no award for Wallops Island, and "Fort Hays" rather
  than the two named radars). `MSTID-Climatology-Paper-2026/README.md` line 296 carries only a
  one-line thanks to the SuperDARN community. Both were reported to NAF rather than edited, since
  the manuscript's Acknowledgments are flagged in its own draft note as pending the author list.
- **Git Hash**: [to be added after commit]
