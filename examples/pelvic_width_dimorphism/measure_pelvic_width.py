"""measure_pelvic_width.py -- the demo study: is relative pelvic width different between
females and males in CTSpinoPelvic1K?

Run from the repository root, pointing at the dataset folder (the one holding labels/ and
manifest.json):

    python examples/pelvic_width_dimorphism/measure_pelvic_width.py \
        --data /path/to/CTSpinoPelvic1K --out examples/pelvic_width_dimorphism/results

On the grid, through SLURM:

    mkdir -p logs
    sbatch templates/slurm_job.sh examples/pelvic_width_dimorphism/measure_pelvic_width.py \
        --data /path/to/CTSpinoPelvic1K --out examples/pelvic_width_dimorphism/results --workers 8

WHAT IT MEASURES, per record, from the label volume alone:
  bi-iliac width   the left-right extent of the two hip bones (identifiers 30 and 31), mm
  S1 width         the left-right extent of S1 (identifier 29), mm
  relative width   bi-iliac / S1, dimensionless, so a wide pelvis on a large skeleton and a
                   wide pelvis on a small one are compared fairly
The left-right axis is read from the affine's axis codes, never assumed, so prone and supine
records are measured identically.

WHO IS COMPARED: `sex` from manifest.json (female / male; "other" and missing are kept in
the CSV but not in the test). Records with surgical hardware are excluded.

WHAT IT WRITES: results/pelvic_width.csv (one row per record), results/report.txt (the
numbers, with a Welch t test and Cohen's d) and results/pelvic_width.png. Every number in
the report comes from the CSV, and the figure is drawn from the same rows.
"""
from __future__ import annotations

import argparse
import csv
import json
from multiprocessing import Pool
from pathlib import Path

import nibabel as nib
import numpy as np

HIPS = (30, 31)      # left_hip, right_hip  (check dataset_labels.json if in doubt)
S1 = 29              # S1, carved from the sacrum


def measure(path: str):
    """Left-right extent, in mm, of the hips and of S1 in one label volume."""
    img = nib.load(path)
    lab = np.asanyarray(img.dataobj)                       # never reorient
    codes = nib.aff2axcodes(img.affine)                    # e.g. ('P', 'I', 'R')
    lr = [i for i, c in enumerate(codes) if c in "LR"][0]  # the left-right axis
    mm = img.header.get_zooms()[lr]
    others = tuple(k for k in range(3) if k != lr)

    def extent_mm(mask):
        idx = np.nonzero(mask.any(axis=others))[0]
        return float((idx.max() - idx.min() + 1) * mm) if idx.size else float("nan")

    case = Path(path).name.split("_")[0]
    return case, extent_mm(np.isin(lab, HIPS)), extent_mm(lab == S1)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="folder holding labels/ and manifest.json")
    ap.add_argument("--out", default="examples/pelvic_width_dimorphism/results")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    data, out = Path(a.data), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    man = {r["label_file"].split("/")[-1].split("_")[0]: r
           for r in json.load(open(data / "manifest.json", encoding="utf-8"))}
    files = sorted(str(p) for p in (data / "labels").glob("*_label.nii.gz"))
    print(f"{len(files)} label volumes")

    rows = []
    with Pool(a.workers) as pool:
        for k, (case, hips_mm, s1_mm) in enumerate(pool.imap_unordered(measure, files), 1):
            r = man.get(case, {})
            rel = hips_mm / s1_mm if s1_mm == s1_mm and s1_mm > 0 else float("nan")
            rows.append({"case": case, "sex": r.get("sex") or "missing", "age": r.get("age"),
                         "position": r.get("position"), "hardware": bool(r.get("hardware_labelled")),
                         "biiliac_mm": round(hips_mm, 1), "s1_mm": round(s1_mm, 1),
                         "relative_width": round(rel, 3)})
            if k % 100 == 0:
                print(f"  {k}/{len(files)}", flush=True)
    rows.sort(key=lambda r: r["case"])
    with open(out / "pelvic_width.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    # ---- the comparison --------------------------------------------------------------
    from scipy import stats
    keep = [r for r in rows if not r["hardware"] and r["relative_width"] == r["relative_width"]]
    grp = {s: [r for r in keep if r["sex"] == s] for s in ("female", "male")}
    f = np.array([r["relative_width"] for r in grp["female"]]); m = np.array([r["relative_width"] for r in grp["male"]])
    t, p = stats.ttest_ind(f, m, equal_var=False)
    d = (f.mean() - m.mean()) / np.sqrt((f.var(ddof=1) + m.var(ddof=1)) / 2)

    def ms(key, s):
        v = np.array([r[key] for r in grp[s]]); return f"{v.mean():.1f} +/- {v.std(ddof=1):.1f}"
    lines = [
        f"records measured: {len(rows)}; analysed (no hardware, S1 present): {len(keep)}; female {len(f)}, male {len(m)}",
        f"bi-iliac width, mm:   female {ms('biiliac_mm', 'female')}   male {ms('biiliac_mm', 'male')}",
        f"S1 width, mm:         female {ms('s1_mm', 'female')}   male {ms('s1_mm', 'male')}",
        f"relative width:       female {f.mean():.3f} +/- {f.std(ddof=1):.3f}   male {m.mean():.3f} +/- {m.std(ddof=1):.3f}",
        f"Welch t = {t:.2f}, p = {p:.2e}, Cohen's d = {d:.2f}",
    ]
    (out / "report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    # ---- the figure --------------------------------------------------------------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 9})
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    rng = np.random.default_rng(0)
    for ax, (key, label) in zip(axes, [("biiliac_mm", "bi-iliac width (mm)"),
                                       ("relative_width", "bi-iliac width / S1 width")]):
        data_ = [[r[key] for r in grp[s]] for s in ("female", "male")]
        ax.boxplot(data_, tick_labels=[f"female (n={len(data_[0])})", f"male (n={len(data_[1])})"],
                   widths=0.5, showfliers=False)
        for i, dd in enumerate(data_, 1):
            ax.scatter(rng.normal(i, 0.06, len(dd)), dd, s=4, alpha=0.25, color="#1c6b73")
        ax.set_ylabel(label); ax.grid(axis="y", color="#CCCCCC", lw=0.5); ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_title("(a) Absolute", loc="left"); axes[1].set_title("(b) Relative to the sacrum", loc="left")
    fig.tight_layout()
    fig.savefig(out / "pelvic_width.png", dpi=200)
    print("wrote", out / "pelvic_width.csv", out / "report.txt", out / "pelvic_width.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
