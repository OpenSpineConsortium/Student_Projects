# CLAUDE.md — how this project works (read before doing anything)

Copy this file into your project folder and edit the three paths marked EDIT. Claude Code
reads it at the start of every session, so everything here is something you will not have
to repeat.

## Who and what

I am a student on an OpenSpineConsortium project. I am learning to code; explain what a
command does in one line before running it, and prefer small scripts I can read over clever
ones. The project question and plan are in `proposal.md` in this folder.

## Where things are

- Repository root: the `Student_Projects` clone. Run scripts from the root.
- Dataset: CTSpinoPelvic1K v10. Labels and CT volumes are in
  `EDIT: /path/to/CTSpinoPelvic1K` (on the grid this is the shared copy the mentor named;
  on a laptop it is the `huggingface_hub` download). Never copy volumes into the repository.
- Results go in `results/` inside this project folder; figures in `figures/`.
- The label identifiers are in `dataset_labels.json` next to the data. Never hard-code an
  identifier from memory; read it from that file. Key ones: vertebrae 1–25 (L1–L6 = 20–25),
  sacrum 26, S1 29, hips 30–31, femora 32–33, ribs 34–46 left and 47–59 right, lumbar
  ribs 60–61, hardware 62–68.

## Rules that never bend

- **Never reorient a volume when writing a label.** Read arrays with
  `np.asanyarray(img.dataobj)` and write them back with the same affine and header.
- **Never assume an axis.** Volumes are stored P,I,R; find the left–right or
  superior–inferior axis from `nib.aff2axcodes(img.affine)` every time.
- **Never commit `*.nii.gz`.** `.gitignore` blocks it; do not work around it.
- **Never edit a result by hand.** If a number is wrong, fix the script and rerun it.
- **Read `KNOWN_ISSUES.md`** from the dataset before any analysis: a null Castellvi grade
  means ungraded, not normal; exclude hardware records from gap measurements; do not pool
  prone and supine; nine four-lumbar records carry the transitional segment under the S1
  identifier.

## The environment

Python lives in a mamba environment created from `templates/environment.yml`:

    mamba env create -f templates/environment.yml -n osc
    mamba activate osc

On the grid, create it once in my home directory. If a package is missing, add it to the
`environment.yml` in this folder and tell me, rather than installing it ad hoc.

## The grid (WSU HPC, SLURM)

- Login node: `EDIT: youraccessid@grid.wayne.edu`. Never run heavy work on the login node;
  anything over a minute or over a few GB of memory goes through `sbatch`.
- Job scripts follow `templates/slurm_job.sh`: `#SBATCH -q primary`, one node, a CPU count,
  memory in GB, a wall time, and `--output=logs/%x_%j.out`. Create `logs/` before submitting.
- Draft the job script and show it to me; **I run `sbatch` myself**. After submission, I
  will paste `squeue -u $USER` and the log tail; help me read them.
- Parallelize over records with `multiprocessing.Pool` and match `--cpus-per-task` to the
  pool size. A single 802-record pass that reads every label volume takes about 10–15
  minutes on 8 CPUs.
- Scratch space is per job; write results to my project folder, not to `/tmp`.

## How I want to work

- One script per question, named for what it produces (`measure_pelvic_width.py`,
  `plot_pelvic_width.py`).
- Every script prints what it wrote. Every figure has a caption in the script's docstring.
- When you are unsure what a label contains, look at the volume (unique identifiers, voxel
  counts) rather than guessing.
- Keep `JOURNAL.md` in this folder updated with a dated line whenever something worked or
  failed; I will paste it into my methods later.
