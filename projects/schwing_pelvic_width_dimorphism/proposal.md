# Is relative pelvic width different between females and males, and by how much?

**Student:** Gregory Schwing (worked example for the onboarding primer)
**Mentor requested:** Gregory Schwing
**Email for the ClickUp invitation:** gregory.schwing@med.wayne.edu
**Dataset:** CTSpinoPelvic1K v10, https://doi.org/10.5281/zenodo.22642578
**Date:** 2026-09-07

## 1. The question

The female pelvis is wider than the male pelvis; every anatomy text says so, and forensic
anthropology sexes skeletons on it. What the texts rarely give is the size of the
difference in living adults measured the same way on the same scanner protocol, and whether
it survives normalization to the rest of the skeleton. CTSpinoPelvic1K labels the two hip
bones and the first sacral segment on one coordinate frame in 802 adults, so the width of
the pelvis and the width of the sacrum it sits on are available in every record. The
sentence I hope to write: "Relative to the width of S1, the female pelvis is X percent wider
than the male pelvis, with an effect size of d, in 738 adults over 50."

## 2. What is already known

Pelvic sexual dimorphism is the most reliable skeletal sex indicator, with the greater
sciatic notch, subpubic angle and iliac flare the classic features (Phenice 1969; Bruzek
2002). CT-based studies report bi-iliac and inlet widths larger in females by roughly 5 to
10 percent, mostly in samples of a few hundred (Tague 1989 on skeletal remains; Franklin
2014 and Decker 2011 on CT). Few normalize to a co-registered structure of the same
skeleton, and none that I know of use a single-protocol cohort of this size with the sacrum
segmented separately.

## 3. What will be measured

| measurement | from identifiers | how | unit |
|---|---|---|---|
| bi-iliac width | 30 (left hip), 31 (right hip) | left–right extent of the union of both hip labels, along the axis the affine marks L/R | mm |
| S1 width | 29 (S1) | left–right extent of the S1 label | mm |
| relative pelvic width | 30, 31, 29 | bi-iliac width divided by S1 width | none |

The extent is the number of voxel columns occupied along the left–right axis times the
voxel size on that axis, so it is a maximal width, including the iliac crests where they
are in the field of view.

## 4. Who is compared

Grouped by `sex` from `manifest.json` (393 female, 345 male; 11 "other" and 53 missing are
listed in the CSV and excluded from the test). Excluded: the 11 records with surgical
hardware (`hardware_labelled`), because eight carry hip arthroplasties, and any record whose
S1 label is absent (one). Prone and supine records are pooled for a width measured
perpendicular to gravity, which posture does not change; the CSV keeps `position` so that
claim can be checked.

## 5. Analysis plan

Means and standard deviations by sex for the absolute and relative widths; Welch's t test
on the relative width; Cohen's d as the effect size; a two-panel box-and-dot figure
(absolute, relative). If the relative difference survives, a secondary check regresses
relative width on age within each sex to see whether it drifts across the 50 to 89 range.
About 730 records analyzed after exclusions.

## 6. Outputs

`results/pelvic_width.csv` (one row per record), `results/report.txt`,
`results/pelvic_width.png`, and a 250-word write-up in `WRITEUP.md`. If the effect holds,
an abstract for the medical student research day.

## 7. Timeline and milestones

| milestone | date |
|---|---|
| environment set up, demo study reproduced | 2026-09-14 |
| measurement script runs on 10 records | 2026-09-21 |
| measurement script runs on all records, CSV committed | 2026-09-28 |
| analysis and figure | 2026-10-05 |
| write-up draft | 2026-10-12 |
| final pull request | 2026-10-19 |

## 8. What could go wrong

A hip label that is cut by the field of view at the iliac crest would under-measure the
width; I will flag records whose hip label touches the volume edge and report the analysis
with and without them. A misplaced S1 carve would distort the denominator; the dataset's
quality-control table flags 100 such records and I will report the result with those
excluded as well.
