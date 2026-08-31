# SuperDARN MSTID Index: Data and Plotting Tools

Twelve Northern Hemisphere winters (2010--2011 through 2021--2022) of the SuperDARN
Medium-Scale Traveling Ionospheric Disturbance (MSTID) index, computed for ten North American
SuperDARN radars, together with the script that produces climatology and stack plots from it.

The index quantifies how much MSTID-band (roughly 14 to 56 min period) fluctuation appears in a
radar's ground-scatter field within a 2 h daytime window, expressed as a departure from that
radar's own seasonal-mean spectrum. It was defined by
[Frissell et al. (2016)](https://doi.org/10.1002/2015JA022168), section 2.2, and is computed here
by the [DARNtids](https://github.com/w2naf-academia/DARNtids) SuperDARN TID Analysis Toolkit.

**Maintainer:** Nathaniel A. Frissell (W2NAF), Department of Physics and Engineering, The
University of Scranton, <nathaniel.frissell@scranton.edu>

---

## Contents

- [Citation](#citation)
- [Required acknowledgment](#required-acknowledgment)
- [Rules of the road](#rules-of-the-road)
- [Quick start](#quick-start)
- [What the SuperDARN MSTID index is](#what-the-superdarn-mstid-index-is)
  - [How SuperDARN observes MSTIDs](#how-superdarn-observes-mstids)
  - [How the index is derived](#how-the-index-is-derived)
  - [How to interpret a value](#how-to-interpret-a-value)
  - [The reduced index](#the-reduced-index)
- [Repository layout](#repository-layout)
- [Radars and seasons](#radars-and-seasons)
- [Data dictionary](#data-dictionary)
- [Known limitations](#known-limitations)
- [Provenance](#provenance)
- [Software environment](#software-environment)
- [References](#references)
- [License](#license)

---

## Citation

If you use this dataset or code, please cite both the dataset and the paper that defines the index:

> Frissell, N. A. (2026). *SuperDARN MSTID Index, North American sector, 2010--2022* [Data set].
> Zenodo. [DOI to be assigned at release]

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff), which GitHub and Zenodo both read.

> Frissell, N. A., Baker, J. B. H., Ruohoniemi, J. M., Greenwald, R. A., Gerrard, A. J.,
> Miller, E. S., & West, M. L. (2016). Sources and characteristics of medium-scale traveling
> ionospheric disturbances observed by high-frequency radars in the North American sector.
> *Journal of Geophysical Research: Space Physics*, 121(4), 3722--3739.
> <https://doi.org/10.1002/2015JA022168>

Please also cite the software that produced the index:

> `DARNtids`: SuperDARN TID Analysis Toolkit. <https://github.com/w2naf-academia/DARNtids>
> [version and DOI to be assigned]

## Required acknowledgment

Any publication using this dataset must carry the following statement, which covers all ten radars
in the bundle. It is the output of the
[SuperDARN acknowledgment generator](https://vt.superdarn.org/data-acknowledgement) with one typo
corrected: the generator prints `AGU-2426201` for the Wallops Island award, and the correct
identifier is `AGS-2426201`. Check the generator before submitting, because operators and award
numbers change.

> The authors acknowledge the use of SuperDARN data. SuperDARN is a collection of radars funded by
> national scientific funding agencies of Australia, Canada, China, France, Italy, Japan, Norway,
> South Africa, United Kingdom, and the United States of America. The Blackstone, Fort Hays East,
> Fort Hays West, Goose Bay, and Kapuskasing radars are maintained and operated by Virginia Tech
> with support from NSF under AGS-2426200. The Christmas Valley East and Christmas Valley West
> radars are maintained and operated by Dartmouth College with support from NSF under AGS-2426199.
> The Prince George and Saskatoon radars are maintained and operated by SuperDARN Canada. SuperDARN
> Canada operations are supported by funding from the Canada Foundation for Innovation (CFI), the
> Canadian Space Agency's (CSA) Geospace Observatory (GO) Canada program, and Innovation
> Saskatchewan. The Wallops Island radar is maintained and operated by JHU Applied Physics
> Laboratory with support from NSF under AGS-2426201.

Use of SuperDARN data is also subject to the
[SuperDARN data policy](https://superdarn.ca/data-policy).

## Rules of the road

The data are open under CC BY 4.0 and the software under GPL-3.0, so the conditions on use are
attribution and the SuperDARN acknowledgment: cite the dataset and the paper that defines the
index, and carry the statement above.

Beyond that, a courtesy. If you are building a study on this index, we would like to hear what you
are working on. The reason is practical rather than proprietary: the index has real limitations
(see [Known limitations](#known-limitations)), the record is being extended and reprocessed, and a
short exchange can save you from an analysis the data will not support. Write to
<nathaniel.frissell@scranton.edu>. This is an invitation, and nothing in the license depends on it.

## Quick start

```bash
git clone https://github.com/w2naf-academia/mstid_index.git
cd mstid_index

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

python superdarn_mstid_plot.py
```

The script reads the netCDF files under `data/`, writes per-season CSV summaries and figures into
`output/`, and takes a few minutes. Everything already in `output/` was produced by exactly this
command, so a fresh run overwrites it with equivalent content.

To use the data without the plotting script, read the CSV files directly:

```python
import pandas as pd

df = pd.read_csv(
    'data/mongo_out/mstid_GSMR_fitexfilter_rtiThresh-0.25/guc/'
    'sdMSTIDindex_20181101_20190501_bks.csv',
    comment='#', index_col='datetime_ut', parse_dates=True,
)
mstid_index = df['meanSubIntSpect_by_rtiCnt']
```

The `.nc` files carry the same values plus per-radar metadata (latitude, longitude, MongoDB
collection of origin) as netCDF attributes, and are what `superdarn_mstid_plot.py` reads.

---

## What the SuperDARN MSTID index is

MSTIDs are quasi-periodic F-region plasma density fluctuations with horizontal wavelengths of
several hundred kilometers and periods of 15 to 60 min. The daytime midlatitude winter MSTIDs
measured here are largely driven by gravity waves propagating up from the lower and middle
atmosphere, which makes them a useful ionospheric tracer of stratospheric and mesospheric
dynamics.

### How SuperDARN observes MSTIDs

SuperDARN is a network of over-the-horizon radars operating between 8 and 20 MHz
([Chisham et al., 2007](https://doi.org/10.1007/s10712-007-9017-8);
[Greenwald et al., 1995](https://doi.org/10.1007/BF00751350);
[Nishitani et al., 2019](https://doi.org/10.1186/s40645-019-0270-5)). The radars complete a full
field-of-view scan every one to two minutes, which resolves MSTID periods of 15 to 60 min
comfortably.

The index is built from **ground scatter**: radar returns from signals that pass through the
ionosphere, reflect from the ground, and return along the reverse path. A passing MSTID modulates
the electron density gradients that refract the signal, which moves the skip focusing distance and
produces travelling bands of enhanced and reduced ground-scatter power. Those bands are the
signature the index measures. Observations are mapped to the ionospheric refraction point using the
ground-scatter mapping equation of
[Bristow et al. (1994)](https://doi.org/10.1029/93JA01470).

### How the index is derived

Each value in this dataset covers one radar and one 2 h observational window. The processing chain
is as follows.

1. **Despeckle.** Raw FITACF ground-scatter power is passed through a boxcar median filter, which
   replaces each range-beam cell by the median of its neighbors within a 3 x 3 x 3
   (time x beam x range) window. A cell is kept only when at least 40% of that neighborhood contains
   valid scatter ([Ribeiro et al., 2011](https://doi.org/10.1029/2011JA016933);
   [Ruohoniemi & Baker, 1998](https://doi.org/10.1029/98JA01288)). This step also recomputes the
   ground- versus ionospheric-scatter flag, applying the criterion of
   [Blanchard et al. (2009)](https://doi.org/10.1029/2008JA013980) in the linearized form used by
   standard SuperDARN processing.

2. **Define the windows.** Four 2 h windows are defined per radar per day, beginning at 14, 16, 18,
   and 20 UTC. These times fall within daylight over North America, so the index describes daytime
   conditions only. A season runs from 1 November through 30 April.

3. **Quality control.** A window is kept only if the radar has no operational gap longer than
   10 min, at least 25% of the window contains ground scatter, and no observing cell lies within
   the solar terminator. Rejected windows appear in the data files with a null index and a
   `reject_code` giving the reason. The range extent contributing to each window is selected
   automatically from the available backscatter, and surviving data are linearly interpolated first
   in beam and then in time (to 60 s resolution) to fill small gaps.

4. **Band-pass filter.** Each range-beam time series is filtered to the MSTID band with a 101-tap
   finite-impulse-response filter (Blackman window, cutoffs 0.0003 and 0.0012 Hz, so nominal
   periods of about 14 to 56 min). Because the filter is short relative to the 2 h window, its
   realized -3 dB passband is narrower, roughly 15 to 43 min.

5. **Spectrum.** The filtered series is linearly detrended, tapered with a Hann window, and Fourier
   transformed. The magnitude spectra of all contributing range-beam cells are summed to give one
   spectral curve *S*(*f*) for the window.

6. **Subtract the seasonal mean and normalize.** A mean spectrum *S̄*(*f*) is formed from every
   window for that radar in that season, which accounts for differences in sensitivity between
   radars and between winters. The index is the mean-subtracted spectrum summed over the
   non-negative frequency bins, divided by the number of ground-scatter cells *N*<sub>gs</sub> that
   contributed:

   ```
   I = (1 / N_gs) * SUM over f_k >= 0 of [ S(f_k) - S_mean(f_k) ]
   ```

   The frequency bins *f*<sub>k</sub> lie on a uniform grid common to every window and radar, so
   *I* is proportional to the frequency integral of the mean-subtracted spectrum.

The quantity *I* is the SuperDARN MSTID index, stored in these files as
**`meanSubIntSpect_by_rtiCnt`**. The name is literal: the seasonal-**mean-sub**tracted
**int**egrated **spect**rum, divided **by** the **r**ange-**t**ime-**i**ntensity backscatter
**c**ou**nt**.

Two thresholds in step 3 differ from the original
[Frissell et al. (2016)](https://doi.org/10.1002/2015JA022168) implementation: the ground-scatter
requirement is 25% here against 67.5% there. The threshold was lowered to retain windows during the
low-ground-scatter conditions near solar minimum, which the twelve-winter record spans and the
original four-winter study did not. This is the meaning of `rtiThresh-0.25` in the data path. The
normalization by cell count in the equation above is part of the index as originally implemented,
although the published description mentions only the mean subtraction and the frequency
integration.

### How to interpret a value

Because *S̄*(*f*) is a per-radar, per-season average, **the index measures each radar's departure
from its own winter background**:

- **Zero** means MSTID-band activity typical for that radar in that winter.
- **Positive** means more MSTID-band activity than that radar's seasonal norm.
- **Negative** means less.

Two consequences follow, and both matter for how the data can be used.

**Compare values within a single radar and season.** There, the index is directly comparable from
window to window and day to day. Across radars or across winters, each value carries its own
baseline: 0.01 at Blackstone in 2015--2016 and 0.01 at Saskatoon in 2018--2019 both mean "one
hundredth above my own seasonal norm," and those two norms differ. Cross-radar work needs a
separate normalization, such as the standardization used by the reduced index below.

**The within-season trend survives the subtraction.** The reference spectrum is one average over
the whole season, so the seasonal decline of MSTID activity from midwinter to spring reported by
Frissell et al. (2016) remains in the index. Any analysis of departures from the seasonal cycle
needs to remove that cycle explicitly.

Typical magnitudes are small: the plotting script uses a color scale of -0.025 to +0.025, and the
full distribution across the record spans roughly -0.05 to +0.05.

The data files also carry a `category_manu` label of `mstid` or `quiet`, which is the automatic
classification applied by `DARNtids`. It is a sign test on this index, with windows at or above
zero labeled `mstid`.

### The reduced index

`superdarn_mstid_plot.py` also computes a **reduced index**, which collapses the ten radars to one
number per day. The steps are: average the four windows of each day for each radar, average across
radars, standardize the resulting daily series to zero mean and unit variance within the season,
and smooth with a centered 4-day rolling mean. The standardization is what makes the reduced index
comparable between seasons.

Reduced-index files are written to
`output/meanSubIntSpect_by_rtiCnt/<season>_meanSubIntSpect_by_rtiCnt_reducedIndex.csv`, with three
columns: `reduced_index` (standardized daily value), `n_good_df` (how many radar-window values
contributed that day, a data-quality weight), and `smoothed` (the 4-day rolling mean). The
generating parameters are recorded in each file's header.

---

## Repository layout

```
mstid_index/
├── superdarn_mstid_plot.py    Climatology, histogram, and stack plots
├── requirements.txt
├── data/
│   └── mongo_out/mstid_GSMR_fitexfilter_rtiThresh-0.25/guc/
│       ├── sdMSTIDindex_<season>_<radar>.nc     120 files, read by the script
│       └── sdMSTIDindex_<season>_<radar>.csv    120 files, same content as text
└── output/                   Regenerated by the script; committed for reference
    ├── meanSubIntSpect_by_rtiCnt/
    │   ├── <season>_meanSubIntSpect_by_rtiCnt.csv               Wide table, one column per radar
    │   ├── <season>_meanSubIntSpect_by_rtiCnt_reducedIndex.csv  Daily network-mean index
    │   ├── meanSubIntSpect_by_rtiCnt.png                        Twelve-winter climatology
    │   ├── meanSubIntSpect_by_rtiCnt_histograms.png
    │   └── radars.csv                                           Radar coordinates
    └── stackplots/mstid_index_reduced/
        └── <season>_stack_mstid_index_reduced.png
```

`<season>` is `YYYYMMDD_YYYYMMDD` for the 1 November to 1 May interval, for example
`20181101_20190501`. `<radar>` is the three-letter SuperDARN radar code.

The `guc` directory name records the analysis configuration used by `DARNtids`.

## Radars and seasons

Ten radars, four in the high-latitude Canadian chain and six in the midlatitude US chain, listed
west to east within each group. Coordinates are the geographic location of the center of each
radar's MSTID detection region, as recorded in the data files.

| Code | Radar | Chain | Lat (°N) | Lon (°E) |
|---|---|---|---|---|
| `pgr` | Prince George | High latitude | 53.98 | -122.59 |
| `sas` | Saskatoon | High latitude | 52.16 | -106.53 |
| `kap` | Kapuskasing | High latitude | 49.39 | -82.32 |
| `gbr` | Goose Bay | High latitude | 53.32 | -60.46 |
| `cvw` | Christmas Valley West | Midlatitude | 43.271 | -120.358 |
| `cve` | Christmas Valley East | Midlatitude | 43.271 | -120.358 |
| `fhw` | Fort Hays West | Midlatitude | 38.859 | -99.389 |
| `fhe` | Fort Hays East | Midlatitude | 38.859 | -99.389 |
| `bks` | Blackstone | Midlatitude | 37.10 | -77.95 |
| `wal` | Wallops Island | Midlatitude | 37.93 | -75.47 |

`cvw`/`cve` and `fhw`/`fhe` are co-located twin radars pointing in different directions, which is
why each pair shares a detection-region center point.

Twelve winter seasons, each 1 November to 1 May:

`20101101_20110501` · `20111101_20120501` · `20121101_20130501` · `20131101_20140501` ·
`20141101_20150501` · `20151101_20160501` · `20161101_20170501` · `20171101_20180501` ·
`20181101_20190501` · `20191101_20200501` · `20201101_20210501` · `20211101_20220501`

## Data dictionary

Each row of `sdMSTIDindex_<season>_<radar>.csv` is one 2 h observational window. Rows are present
for every window in the season, including rejected ones, where the spectral columns are empty and
`reject_code` gives the reason.

### Window identification and geometry

| Column | Description |
|---|---|
| `datetime_ut` | UTC time at the start of the 2 h observation window |
| `lat`, `lon` | Geographic latitude and longitude of the center of the detection region |
| `slt` | Solar mean time at that point |
| `mlt` | Magnetic local time at that point |
| `gscat` | Scatter selection at analysis: 0 all backscatter, 1 ground backscatter only, 2 ionospheric only, 3 all backscatter carrying a ground-scatter flag |
| `height_km` | Assumed reflection-point height |
| `terminator_fraction` | Number of radar cells in daylight divided by the number in darkness |

### Data quality

| Column | Description |
|---|---|
| `good_period` | `True` when the window passed quality control |
| `reject_code` | Why a window was rejected; see the table below |
| `orig_rti_cnt` | *N*<sub>gs</sub>: number of cells in the window with a backscatter measurement |
| `orig_rti_possible` | Total number of possible cells in the window |
| `orig_rti_fraction` | `orig_rti_cnt / orig_rti_possible`; the 25% acceptance threshold applies here |
| `orig_rti_mean`, `orig_rti_median`, `orig_rti_std` | Statistics of the measured power values in the window |

| `reject_code` | Meaning |
|---|---|
| 0 | Good period, not rejected |
| 1 | High terminator fraction (dawn or dusk in the observational window) |
| 2 | No data |
| 3 | Poor data quality, including low RTI fraction and failed quality check |
| 4 | Other, including no RTI fraction and no terminator fraction |

### Spectral parameters

| Column | Description |
|---|---|
| `intSpect` | Power spectral density integrated over all radar cells and spectral bins after band-pass filtering |
| `meanSubIntSpect` | `intSpect` computed after subtracting the radar-season mean spectrum |
| `intSpect_by_rtiCnt` | `intSpect / orig_rti_cnt` |
| **`meanSubIntSpect_by_rtiCnt`** | **`meanSubIntSpect / orig_rti_cnt`. This is the SuperDARN MSTID index.** |
| `category_manu` | Automatic classification: `mstid`, `quiet`, or `None` |

### MUSIC wave parameters

Where MUSIC processing ran, the file carries the properties of up to two detected signals, ordered
by descending strength in the MUSIC wavenumber spectrum. Columns are prefixed `sig_001_` and
`sig_002_`.

| Suffix | Description |
|---|---|
| `kx`, `ky` | North-south and east-west wavenumber [1/(2π km)] |
| `k` | Horizontal wavenumber [1/(2π km)] |
| `lambda_km` | Horizontal wavelength [km] |
| `azm_deg` | Propagation azimuth [degrees clockwise from geographic north] |
| `freq_Hz` | Frequency of maximum MSTID-band power spectral density [Hz] |
| `period_min` | Period of the strongest MSTID in the window [min] |
| `vel_mps` | Horizontal phase velocity [m/s] |
| `max` | Wavenumber spectral density at the peak |
| `area` | Number of pixels of the Karr plot in the detected region |

These wave parameters are sparse across the record. Studies needing them should check coverage for
the specific radars and dates of interest before relying on them.

## Known limitations

- **Daytime only.** The four windows span 14 to 22 UTC, which is daylight over North America.
  Nighttime MSTIDs, which have a different generation mechanism, are outside this dataset.
- **Relative, not absolute.** See [How to interpret a value](#how-to-interpret-a-value).
- **Uneven coverage.** Ground scatter depends on the ionospheric state, the operating frequency,
  and the scattering properties of the surface, so it is most favorable in fall and winter daylight
  and thinnest near solar minimum. The 2020--2021 and 2021--2022 winters are the most sparsely
  sampled of the twelve, principally because of extended radar outages. The `reject_code` column
  distinguishes an outage from a window rejected on data quality, and any analysis sensitive to
  sampling should use it.
- **The terminator criterion is the most aggressive of the three quality-control tests**, removing
  roughly twice as many candidate windows as the ground-scatter threshold does.
- **Single processing chain.** These files come from one `DARNtids` run against FITACF 2.5 data.
  They have not been reprocessed against FITACF3.

## Provenance

The index values in `data/` were computed by `DARNtids` from SuperDARN FITACF data, stored in a
MongoDB database named `mstid_GSMR_fitexfilter`, and exported to netCDF and CSV by
`mongo_to_csv.py` on 23 October 2023. Each data file's header records its source collection, the
export script, the host, and the export timestamp. The `guc` and `rtiThresh-0.25` path components
identify the analysis configuration.

Everything in `output/` is regenerated by `superdarn_mstid_plot.py` from the files in `data/`. The
committed copies are there so a reader can see the product without running anything.

SuperDARN FITACF data for these radars are available from the SuperDARN data mirrors maintained by
the Federated Research Data Repository and the British Antarctic Survey, subject to the SuperDARN
data policy.

## Software environment

`requirements.txt` lists the Python packages needed. The script has been run successfully on
Python 3.13 with matplotlib 3.10, NumPy 2.2, SciPy 1.14, pandas 2.3, and xarray 2025.12, and
reproduces the committed `output/` to floating-point round-off, with the figures pixel-identical.

## References

- Blanchard, G. T., Sundeen, S., & Baker, K. B. (2009). Probabilistic identification of
  high-frequency radar backscatter from the ground and ionosphere based on spectral characteristics.
  *Journal of Geophysical Research*, 114, A12231. <https://doi.org/10.1029/2008JA013980>
- Bristow, W. A., Greenwald, R. A., & Samson, J. C. (1994). Identification of high-latitude acoustic
  gravity wave sources using the Goose Bay HF radar. *Journal of Geophysical Research*, 99(A1),
  319--331. <https://doi.org/10.1029/93JA01470>
- Chisham, G., et al. (2007). A decade of the Super Dual Auroral Radar Network (SuperDARN): Scientific
  achievements, new techniques and future directions. *Surveys in Geophysics*, 28, 33--109.
  <https://doi.org/10.1007/s10712-007-9017-8>
- Frissell, N. A., et al. (2016). Sources and characteristics of medium-scale traveling ionospheric
  disturbances observed by high-frequency radars in the North American sector. *Journal of
  Geophysical Research: Space Physics*, 121(4), 3722--3739. <https://doi.org/10.1002/2015JA022168>
- Greenwald, R. A., et al. (1995). DARN/SuperDARN: A global view of the dynamics of high-latitude
  convection. *Space Science Reviews*, 71, 761--796. <https://doi.org/10.1007/BF00751350>
- Nishitani, N., et al. (2019). Review of the accomplishments of mid-latitude Super Dual Auroral
  Radar Network (SuperDARN) HF radars. *Progress in Earth and Planetary Science*, 6, 27.
  <https://doi.org/10.1186/s40645-019-0270-5>
- Ribeiro, A. J., et al. (2011). A new approach for identifying ionospheric backscatter in
  midlatitude SuperDARN HF radar observations. *Journal of Geophysical Research*, 116, A10323.
  <https://doi.org/10.1029/2011JA016933>
- Ruohoniemi, J. M., & Baker, K. B. (1998). Large-scale imaging of high-latitude convection with Super
  Dual Auroral Radar Network HF radar observations. *Journal of Geophysical Research*, 103(A9),
  20797--20811. <https://doi.org/10.1029/98JA01288>

## Related repositories

- [DARNtids](https://github.com/w2naf-academia/DARNtids): the SuperDARN TID Analysis Toolkit that
  computes this index.
- [pyDARNmusic](https://github.com/w2naf-academia/pyDARNmusic): the MUSIC algorithm library
  `DARNtids` depends on for the wave-parameter columns.

## License

This repository carries two licenses, one for the data and one for the software.

| What | License | File |
|---|---|---|
| `data/` and `output/` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [`LICENSE-DATA`](LICENSE-DATA) |
| `superdarn_mstid_plot.py` | [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html) | [`LICENSE`](LICENSE) |

Copyright (c) 2023--2026 Nathaniel A. Frissell.

CC BY 4.0 matches the terms under which the SuperDARN MSTID index is released alongside the paper
in preparation. GPL-3.0 matches
[`DARNtids`](https://github.com/w2naf-academia/DARNtids),
[`pyDARNmusic`](https://github.com/w2naf-academia/pyDARNmusic), and the analysis package for that
paper.

These licenses cover the derived index computed here. The underlying SuperDARN FITACF observations
remain subject to the [SuperDARN data policy](https://superdarn.ca/data-policy).

## Contact

Questions, corrections, and notice of intended use are welcome. Open an issue or write to
Nathaniel A. Frissell, <nathaniel.frissell@scranton.edu>.
