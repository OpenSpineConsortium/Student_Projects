Onboard me as a new student. Work through the steps below in order. Before each step check
whether it is already done and say so; never redo finished work. Explain each command in
one line before running it. Stop and ask when a step needs something only I can do (a
password, a phone code, my AccessID). Optional argument: $ARGUMENTS (my AccessID, if I gave it).

## Step 1. Laptop tools
Run `git --version`, `claude --version`, `ssh -V`, and `python --version` or `mamba --version`.
Tell me which are missing and how to install each (GETTING_STARTED.md step 1). On Windows,
note whether we are in Git Bash, PowerShell or WSL, and use Git Bash or `wsl -e bash -lc`
for every `ssh`, `scp` and `rsync` from here on.

## Step 2. Grid connection
1. Ask for my WSU AccessID if it is not in the arguments. Confirm I have a grid account
   (GETTING_STARTED step 4) and Google Authenticator set up (step 5); if not, stop here and
   tell me exactly what to do, then resume when I say so.
2. If `~/.ssh/id_ed25519` does not exist, run `ssh-keygen -t ed25519 -C "<accessid>@wayne.edu" -N "" -f ~/.ssh/id_ed25519`.
3. If `~/.ssh/config` has no `Host grid` block, append `templates/ssh_config` with my
   AccessID filled in (and on Windows do the same in the WSL home if WSL is used).
4. Tell me the next command will ask for my grid password and then my six-digit
   Authenticator code, once, then run `ssh-copy-id -i ~/.ssh/id_ed25519.pub grid`.
5. Test: `ssh -o BatchMode=yes grid hostname` must print `warrior` with no prompt. If it
   prompts, the key was not installed; show me `~/.ssh/authorized_keys` on the grid.

## Step 3. The repository and the environment on the grid
1. `ssh -o BatchMode=yes grid "test -d ~/Student_Projects || git clone https://github.com/OpenSpineConsortium/Student_Projects.git"`
   (a private repo; if the clone asks for credentials, tell me to run
   `gh auth login` or set up a GitHub token on the grid, and explain in two lines).
2. `ssh -o BatchMode=yes grid "cd ~/Student_Projects && git pull -q && mkdir -p logs"`.
3. If `ssh grid "ls ~/miniforge3/envs/osc ~/mambaforge/envs/osc 2>/dev/null"` finds nothing,
   show me `templates/make_env.sh`, then on my word submit it:
   `ssh -o BatchMode=yes grid "cd ~/Student_Projects && sbatch templates/make_env.sh"` and
   wait for it with `tools/grid.sh wait <jobid>` in the background. It installs Miniforge
   if needed and creates the `osc` environment from `templates/environment.yml`.
4. Verify: `ssh grid "source ~/miniforge3/etc/profile.d/conda.sh 2>/dev/null || source ~/mambaforge/etc/profile.d/conda.sh; conda activate osc && python -c 'import nibabel, numpy, scipy; print(nibabel.__version__)'"`.

## Step 4. The dataset on the grid
Ask whether my mentor gave me a path to a shared copy. If yes, record it. If no, show me
`templates/get_dataset.sh`, then on my word submit it; it downloads the v10 labels and
metadata (1.1 GB) from Hugging Face into `~/data/CTSpinoPelvic1K`. CT volumes (195 GB)
only with `CT=1`, and only if the project needs images rather than labels. Verify
`ssh grid "ls ~/data/CTSpinoPelvic1K/labels | wc -l"` prints 802 and that
`manifest.json`, `dataset_labels.json` and `KNOWN_ISSUES.md` are there.

## Step 5. The demo study
Run it on ten records first, as a job, then on all 802:
`/grid-submit examples/pelvic_width_dimorphism/measure_pelvic_width.py --data ~/data/CTSpinoPelvic1K --out examples/pelvic_width_dimorphism/results_mine --workers 8 --limit 10`
then the same without `--limit`. Pull the results back with `/grid-pull` and compare my
`report.txt` with the committed one; the first two decimals should agree. Open the figure
and explain each panel to me in two sentences.

## Step 6. Choose a project
Read `projects/IDEAS.md`. Ask me three questions: what I studied (anatomy, statistics,
programming, none), how many weeks I have, and whether I have a GPU allocation. Propose
three entries that fit, one sentence each on why, and let me choose or bring my own. Then
run `/new-project <topic>` to create the folder, the branch, the filled `CLAUDE.md` and the
proposal interview. Remind me to open the pull request with the email for my ClickUp
invitation.

## Step 7. Hand-off
Write today's date and what was completed to `projects/<me>/JOURNAL.md`. Print the
"What done looks like" checklist from `GETTING_STARTED.md` with a tick or a cross on each
line, and tell me what to email my mentor (GitHub username, AccessID, the PR link).
