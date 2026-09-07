# projects/

One folder per project, named `<lastname>_<topic>` in lower case, for example
`schwing_pelvic_width_dimorphism`. A project folder holds:

```
projects/<lastname>_<topic>/
├── proposal.md      the approved proposal (the pull request that started the project)
├── CLAUDE.md        copied from templates/ and edited for this project
├── JOURNAL.md       dated notes: what was tried, what worked, what did not
├── *.py             the scripts, one per output, run from the repository root
├── results/         per-record CSVs and reports written by the scripts
├── figures/         figures written by the scripts
└── WRITEUP.md       the abstract-length summary, then the draft
```

Proposals arrive as pull requests that add `proposal.md` only. Everything else arrives in
later pull requests, each naming the ClickUp task it closes.
