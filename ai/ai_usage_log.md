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
  - NAF's ORCID `0000-0002-8398-4222` and his affiliation were taken from an authoritative source
    in the project rather than recalled.
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
- **Related finding, not acted on**: two other documents in this project carry an older revision of
  this same acknowledgment. Both were reported to NAF and left unedited, since sequencing changes to
  them is his. The specifics are recorded in the project's private AI usage log, because they concern
  the internal state of an unpublished manuscript (A4).
- **Git Hash**: 1787ff6

## [2026-08-31 21:14 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: Resolve the `AGU-2426201` question raised in the entry above.
- **NAF's decision** (2026-08-31), verbatim: *"Yes, it should be AGS-2426201"*. NAF is a SuperDARN
  co-investigator and is authoritative on this; the assistant had flagged the prefix as a probable
  typo and declined to change it unilaterally.
- **Sections/Files Affected**: `README.md`, the Wallops Island clause of the required
  acknowledgment (`AGU-2426201` to `AGS-2426201`) and the paragraph introducing the block.
- **Nature of Contribution**: Applying a correction NAF authorized.
- **Human Review Status**: Reviewed. NAF made the call on this specific identifier.
- **Verification**: The introductory paragraph no longer claims the block is verbatim generator
  output. It now states plainly that the generator prints `AGU-2426201`, that the correct identifier
  is `AGS-2426201`, and that this is the one place the block departs from the generator. A reader
  who diffs our statement against the generator's output will find the difference already
  explained rather than looking like an error on our part. The remaining text is unchanged and
  still matches the generator character for character.
- **Still open**: the corresponding update to the other documents noted in the previous entry
  remains reported and unacted on, pending NAF.
- **Git Hash**: 0ff5a21

## [2026-09-01 14:49 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: Audit the data dictionary against the actual data files before the release,
  and close the gaps it found.
- **Sections/Files Affected**: `README.md`, the Quick start netCDF paragraph (now an eleven-row
  global-attribute table) and the Data dictionary preamble and `datetime_ut` row.
- **Nature of Contribution**: Verification, and documentation of what it found.
- **Human Review Status**: Pending review.
- **What the audit found**:
  - **All 41 CSV columns are documented.** Checked by extracting the header row of a data file and
    matching every column against the backticked names in the README, with the `sig_00N_` prefix
    convention expanded. No column is missing, and nothing is documented that the files do not
    contain.
  - **One genuine gap**: the netCDF files name the time coordinate `date` where the CSV files call
    it `datetime_ut`. A user opening a `.nc` and looking for `datetime_ut` would not find it. This
    is the only name that differs between the two formats, confirmed by set comparison of the CSV
    header against the netCDF variable list. Now stated in the preamble and in the `datetime_ut`
    row, with the stored units and the decoded dtype.
  - **The netCDF global attributes were under-documented**, described only as "per-radar metadata
    (latitude, longitude, MongoDB collection of origin)". There are eleven, and they are the
    per-file provenance record. Now a table.
- **Corrections made to my own drafting in the same pass**: a first attempt wrote "the netCDF files
  carry 40 variables", taken from an `ncdump` regex. `xarray` reports 42, since the file has 40 data
  variables on two coordinates (`date` and `radar`). The text was corrected to name the 40 measured
  quantities and the two coordinates separately. A first attempt also listed seven global attributes
  where there are eleven, having transcribed from an `ncdump` excerpt rather than from
  `xarray.open_dataset(...).attrs`. Both numbers in the committed text were then re-verified
  programmatically against a data file.
- **Git Hash**: c8411c5

## [2026-09-01 14:52 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: Pre-push review of this public repository, at NAF's instruction to push.
- **Sections/Files Affected**: `ai/ai_usage_log.md`, three passages in the entries above.
- **Nature of Contribution**: Governance correction.
- **Human Review Status**: Pending review.
- **What was wrong**: this log is in a **public** repository, and three passages written in earlier
  entries carried internal detail about an unpublished manuscript in a **private** repository:
  superseded grant numbers from its acknowledgment, the fact that its author list is unsettled,
  file-and-line pointers into the private tree, and the path of the manuscript source. That is the
  category A4 prohibits sending outward, and the project's own visibility policy keeps
  session-by-session AI detail internal until the manuscript's disclosure paragraph is final.
- **What changed**: the substance of what AI did **to this repository** is unchanged and complete.
  The cross-repository specifics were replaced with a statement that they exist and are recorded in
  the project's private log. Nothing was deleted to make the record look cleaner; the finding is
  still here, pointing at where its detail lives.
- **Verification**: a grep for `overleaf`, `main.tex`, `author list`, the two superseded award
  numbers, `lws_hemispheres`, and the private analysis host now returns nothing across `README.md`
  and `ai/`. The one remaining hit, `mongo_to_csv.py` in the README provenance section, is already
  public: it is named in the comment header of all 120 CSV files in `data/`.
- **Git Hash**: 87a8862

## [2026-09-01 15:07 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: NAF found that the first reference in the README carried a DOI resolving to a
  different paper, and instructed a careful check of all of them.
- **Sections/Files Affected**: `README.md`, four locations: two inline citations in the "How the
  index is derived" step 1, and two entries in the References list.
- **Nature of Contribution**: Correction of fabricated citation metadata produced by an earlier
  entry in this same log.
- **Human Review Status**: NAF identified the error. The corrections are pending his review.
- **What was wrong, and why**: the References section was written from the assistant's own
  recollection of these papers rather than from `references.bib`, the project's curated
  bibliography, which was available and correct the whole time. Two entries were wrong in journal,
  volume, article number, **and** DOI:

  | | As published in the README | Correct |
  |---|---|---|
  | Blanchard, Sundeen & Baker (2009) | *J. Geophys. Res.*, 114, A12231, `10.1029/2008JA013980` | *Radio Science*, 44(5), RS5012, `10.1029/2009RS004141` |
  | Ribeiro et al. (2011) | *J. Geophys. Res.*, 116, A10323, `10.1029/2011JA016933` | *Radio Science*, 46(4), RS4011, `10.1029/2011RS004676` |

  Both wrong DOIs resolve to real but unrelated papers: `10.1029/2008JA013980` is Sitnov, Swisdak
  & Divin (2009), "Dipolarization fronts as a signature of transient reconnection in the
  magnetotail", and `10.1029/2011JA016933` is Clilverd et al. (**2012**), a THEMIS substorm
  precipitation study. A reader following either link would have been sent to the wrong science
  with no indication of an error. This is a W12 violation: citation metadata was asserted without
  being traced to a source.
- **Verification of the whole reference list**: every DOI in `README.md`, `CITATION.cff`,
  `.zenodo.json`, and `LICENSE-DATA` was extracted programmatically and resolved against the
  **Crossref REST API**, comparing first author, year, journal, volume, and issue against what the
  README asserts. **All eight article DOIs now agree with the registry.** Page ranges were checked
  separately for the five entries Crossref supplies them for (Bristow 319--331, Chisham 33--109,
  Frissell 3722--3739, Greenwald 761--796, Ruohoniemi 20797--20811), all matching. Three entries are
  article-number citations for which Crossref reports no page range (Blanchard RS5012, Ribeiro
  RS4011, Nishitani 27); those values come from `references.bib`. The two Crossref Funder Registry
  identifiers in `.zenodo.json` were also resolved: `10.13039/100000104` is NASA and
  `10.13039/100000001` is NSF.
- **Scope of the error**: a grep across the whole project confirms the two bad DOIs appeared
  **only** in this README, in the four places now fixed. `references.bib` and the manuscript were
  always correct, and the manuscript renders its citations from the bibliography rather than by
  hand, so nothing else was affected.
- **Git Hash**: 925a625

## [2026-09-01 15:16 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: State the season window explicitly, following NAF's decision that this bundle
  stays on 1 November.
- **NAF's decision** (2026-09-01), his own framing: keep the bundle at 1 November and *"state the
  difference explicitly in the README, since the bundle is a frozen 2023 export with its own
  provenance"*, adding that *"this particular repo is supporting a different paper than the
  manuscript we are developing here."*
- **Sections/Files Affected**: `README.md`. A new interpretation caveat, "The season window is part
  of the index definition", in the How to interpret a value section; the season window stated on the
  season list; a new Known limitations entry; and the License rationale for CC BY 4.0 rewritten so it
  no longer leans on a different paper's release terms.
- **Nature of Contribution**: Documentation, from an analysis run this session.
- **Human Review Status**: Pending review. NAF made the decision; he has not read the new text.
- **Why this matters to a user of the bundle**: the index is an anomaly against a per-radar,
  per-season **mean spectrum**, so the season window is not a coverage choice. It sets the reference
  the values are measured against. Changing the window changes every value for the same radar, day,
  and hour.
- **Verification**: the mechanism was confirmed in the `DARNtids` source, where the reference is the
  mean over all accepted windows for a radar and season (`darntids/classify.py`,
  `all_spect_mean = np.mean(all_spect_df, axis=1)`), and then measured. Comparing this bundle
  against a 1 August export of the same index, over the **110 overlapping radar-seasons** and
  restricted to windows both contain: **no radar-season is bit-identical**, the median worst-case
  difference is **27% of this bundle's own standard deviation** for that radar-season, the worst is
  **157%** (`pgr`, 2011--2012), and the correlation stays high (median Pearson *r* = 0.9997, minimum
  0.990). So the shape of the series survives and individual values do not.
- **A correction to my own first reading**: a single-radar spot check (`bks`, 2018--2019) showed a
  difference of only about 1% of the spread, which would have supported a much weaker caveat. That
  radar-season is atypical. The 110-radar-season sweep was run before anything was written, and it
  is what the README reflects.
- **Deliberately not in the README**: the magnitudes above, and any description of the other
  analysis's season window. That comparison bundle is a concurrent session's unreviewed work in a
  private repository, so quoting numbers from it in a public README would give them a standing they
  have not earned (W12) and would disclose the internal state of an unpublished manuscript (A4). The
  README states the mechanism, which is certain from the source code, and says a differently
  windowed product is a different set of numbers. The measurements are recorded here and in the
  project's private log.
- **Git Hash**: 65a9a32

## [2026-09-01 15:29 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5[1m]`, via Claude Code
- **Session Purpose**: Follow NAF's rename of this repository from `mstid_index` to
  `superdarn-mstid-index-na-2010-2022`, updating every reference that points at it.
- **NAF's instruction** (2026-09-01): *"I renamed it and I am not worried about redirects. Change
  all local references."* The name was chosen from options proposed this session; the rename was
  done deliberately **before** the Zenodo DOI, because Zenodo stamps the repository name into the
  record and the archive filename.
- **Why the rename**: `mstid_index` had become ambiguous. `DATA_INVENTORY.md` in the paper repo
  already uses `mstid_index_nh`, `mstid_index_nh_1aug`, and `mstid_index_sh` as three distinct
  archive themes, and the bare name pointed at four different things. The new name states the
  instrument, the quantity, the sector, and the span.
- **Sections/Files Affected**: `README.md` (the clone command, the `cd` that follows it, and the
  root of the repository-layout tree) and `CITATION.cff` (`repository-code`).
- **Nature of Contribution**: Mechanical reference update.
- **Human Review Status**: Pending review. NAF performed the rename and directed the update.
- **Verification**:
  - Three surviving occurrences of the old string were checked individually and **deliberately
    left**, because they are not references to the repository: `mstid_index` as a Python variable
    name in the README's usage example, and `output/stackplots/mstid_index_reduced/` plus the
    stackplot filenames under it, which are real directory and file names the plotting script
    produces. Confirmed against the filesystem rather than assumed.
  - The repository's own AI usage log was **not** rewritten. Its earlier entries name
    `mstid_index` because that was the repository's name when the work was done. Editing them to
    read as though the current name had always applied would falsify the record that A1 exists to
    keep.
  - `git remote get-url origin` now returns the new URL, and a fetch against it succeeds with
    `origin/main` matching local `HEAD`.
- **Git Hash**: e9ea304

## [2026-09-01 15:38 UTC]

- **Tool**: Claude (Anthropic), `claude-opus-5`, via Claude Code
- **Session Purpose**: NAF: *"There needs to be an appropriate Claude acknowledgment in the
  README.md."* Write the AI disclosure for this public data release.
- **Sections/Files Affected**: `README.md`, a new `## AI assistance` section placed before the
  License section, with a table-of-contents entry; `.zenodo.json`, a closing paragraph appended to
  the record description.
- **Nature of Contribution**: Drafting a disclosure of the assistant's own contribution.
- **Human Review Status**: **Pending NAF's sign-off, and that sign-off is required.** Per A2 the
  disclosure wording is drafted by the assistant and must be reviewed and adopted by the author
  before release. Treat the current text as a draft until he says otherwise.
- **What the disclosure says**: it leads with what AI did **not** touch, because that is the reader's
  first question about an AI-assisted data repository: the index values in `data/` were computed by
  `DARNtids` and exported in October 2023, before any AI involvement; no AI tool has computed,
  recomputed, or altered them; `output/` was not regenerated with one; and
  `superdarn_mstid_plot.py` was written by NAF. It then lists the five things the tool was used for
  (README drafting, release metadata, the seven forward-compatibility script edits, the
  `requirements.txt` floors, and the verification work), states that NAF set the objectives, made
  every scientific and licensing decision, and is responsible for the content, and states that an AI
  tool is not and cannot be an author (A3).
- **Why the Crossref check is named in the disclosure**: a reader of an AI-assisted README has good
  reason to worry about invented citations, so the disclosure says plainly that every DOI in the
  repository was resolved against the Crossref API and compared on author, year, journal, volume, and
  issue. That is a fact a data user can act on.
- **The disclosure points at this log**, which is public in this repository, and says it records the
  errors the tool made and how they were caught. That is deliberate: a disclosure that only lists
  successes is not a disclosure.
- **A judgment call for NAF to overrule if he wants**: the README does **not** name the specific
  fabricated-citation incident (the two wrong DOIs in the Blanchard and Ribeiro entries, which NAF
  caught). A2 says a disclosure should meet the requirement, be direct, and stop, and the detail
  lives one click away in this log. If NAF would rather the README name it explicitly, that is a
  two-sentence change.
- **`.zenodo.json`**: the same disclosure in one paragraph, because the Zenodo record is the citable
  deliverable and A2's requirement attaches to the deliverable rather than only to the source
  repository. Validated as JSON after editing.
- **Git Hash**: ec8db6c
