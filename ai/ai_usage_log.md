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
