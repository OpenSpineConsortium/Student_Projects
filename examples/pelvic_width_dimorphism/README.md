# Demo study: is relative pelvic width different between females and males?

The shape every project here has, in one script: a question, a measurement from the
labels, a comparison, a figure, and a report whose numbers a script wrote.

## Run it

```bash
mamba activate osc
python examples/pelvic_width_dimorphism/measure_pelvic_width.py \
    --data /path/to/CTSpinoPelvic1K --out examples/pelvic_width_dimorphism/results --workers 8
```

`/path/to/CTSpinoPelvic1K` is the folder holding `labels/` and `manifest.json` (the
Hugging Face download, or the shared copy on the grid). About ten minutes on eight CPUs. On
the grid: `mkdir -p logs && sbatch templates/slurm_job.sh examples/pelvic_width_dimorphism/measure_pelvic_width.py --data ... --out ...`.

## What it measures

For every record, from the label volume alone: the left–right extent of the two hip bones
(identifiers 30 and 31) and of S1 (identifier 29), in mm, and their ratio. The left–right
axis is read from the affine, never assumed. Sex comes from `manifest.json`. Records with
surgical hardware are excluded.

## What it found (v10 labels, 7 September 2026)

```
records measured: 802; analysed (no hardware, S1 present): 790; female 390, male 338
bi-iliac width, mm:   female 272.9 +/- 17.7   male 283.9 +/- 18.9
S1 width, mm:         female 117.8 +/- 7.5    male 120.7 +/- 8.9
relative width:       female 2.321 +/- 0.128  male 2.357 +/- 0.138
Welch t = -3.64, p = 2.87e-04, Cohen's d = -0.27
```

![bi-iliac width by sex, absolute and relative to S1](results/pelvic_width.png)

The answer, for this measurement, is no. Male pelves are about 4 percent wider at the iliac
crests, and dividing by S1 width does not reverse that: males stay slightly wider relative
to their sacrum, a small effect but not a chance one. The classic female dimorphism lives in
the pelvic inlet, the subpubic angle and the sciatic notch, none of which a bi-iliac extent
measures. That is the lesson of the demo: the measurement decides which question you
actually asked, and an honest report says so.

## Make it yours

Change one thing at a time and rerun. Swap 30 and 31 for 32 and 33 and you measure femoral
spread. Change the axis from left–right to superior–inferior and you measure heights. Group
by `position` instead of `sex` to check that a width does not depend on posture. Group by
`has_l6` and you have a transitional-anatomy question. Ask Claude Code to make the change
and to explain the two lines it edited.

## Files

- `measure_pelvic_width.py` — the whole study
- `results/pelvic_width.csv` — one row per record: case, sex, age, position, hardware, bi-iliac mm, S1 mm, ratio
- `results/report.txt` — the numbers above, written by the script
- `results/pelvic_width.png` — the figure
