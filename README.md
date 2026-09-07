# OpenSpineConsortium · Student_Projects

Student research projects on the consortium's open datasets. One folder per project,
reviewed by pull request, tracked in ClickUp once approved.

**Start here:** the [OSC Primer](https://openspineconsortium.github.io/onboarding/) walks a
student with no coding experience from an empty laptop to a finished population-level study:
installing VS Code and Claude Code, getting onto the WSU grid, downloading
CTSpinoPelvic1K, running the demo study in this repository, and proposing a project of your
own.

## How a project moves

| step | who | where |
|---|---|---|
| 1. Read the primer and run the demo study | you | `examples/pelvic_width_dimorphism/` |
| 2. Write a one-page proposal from the template | you | `templates/proposal_template.md` |
| 3. Open a pull request adding `projects/<lastname>_<topic>/proposal.md` | you | GitHub, using the PR template |
| 4. Review, questions, revisions in the PR thread | mentor and you | GitHub |
| 5. Approval, merge, ClickUp invitation to the email in your PR | mentor | ClickUp |
| 6. Work in your project folder on a branch; milestones tracked in ClickUp | you | this repo and ClickUp |
| 7. Results, figure code and a write-up in the same folder; final PR | you | this repo |

The worked example, [projects/schwing_pelvic_width_dimorphism](projects/schwing_pelvic_width_dimorphism/),
is the pull request every proposal should imitate.

## Layout

```
Student_Projects/
├── README.md                     this file
├── CONTRIBUTING.md               the pull-request procedure and house rules
├── .github/PULL_REQUEST_TEMPLATE.md
├── templates/
│   ├── proposal_template.md      copy this to projects/<lastname>_<topic>/proposal.md
│   ├── CLAUDE.md                 copy this into your project folder so Claude Code knows the grid
│   ├── environment.yml           the mamba environment every project starts from
│   ├── slurm_job.sh              a SLURM job script that runs a Python script on the grid
│   └── ssh_config                the ~/.ssh/config entry that makes `ssh grid` work
├── tools/grid.sh                 run / sync / submit / wait / pull, the five remote calls a project needs
├── .claude/
│   ├── settings.json             commands Claude may run without asking (git, python, ssh grid, rsync)
│   └── commands/                 /grid-status, /grid-submit, /grid-pull, /new-project
├── examples/
│   └── pelvic_width_dimorphism/  the demo study, end to end, with its results
└── projects/
    └── <lastname>_<topic>/       one folder per project
```

## Rules that keep this repository usable

- **No imaging data in git.** CT and label volumes stay on the grid or your disk; `.gitignore`
  blocks `*.nii.gz`. Commit code, small CSVs of derived measurements, figures and text.
- **Every figure has a script that regenerates it** from the released data, with the
  environment pinned in `environment.yml`.
- **One project, one folder, one branch per piece of work.** Never commit to `main` directly.
- **Cite the dataset** you used, by its DOI, in anything you write or present.
- **Nothing heavy runs on the login node, and job scripts are files, never heredocs.**
  `templates/CLAUDE.md` says why; `tools/grid.sh` makes the right thing the easy thing.

Questions: Gregory Schwing, gregory.schwing@med.wayne.edu.
