# Getting started, from an empty laptop

Seven steps you do; everything after that Claude does with you. Budget an afternoon, plus
the two business days the grid takes to create an account.

## 1. Three installs

| what | macOS / Linux | Windows |
|---|---|---|
| Visual Studio Code | [code.visualstudio.com](https://code.visualstudio.com/) | same |
| Git | `xcode-select --install` (macOS) or your package manager | [git-scm.com](https://git-scm.com/download/win), keep "Git Bash" checked |
| Claude Code | `curl -fsSL https://claude.ai/install.sh \| bash` | PowerShell: `irm https://claude.ai/install.ps1 \| iex` |

Then install the **Claude Code** extension inside VS Code. Ask your mentor which Claude plan
the lab uses before buying anything.

## 2. Clone this repository and open it

```bash
git clone https://github.com/OpenSpineConsortium/Student_Projects.git
cd Student_Projects
code .
```

(You need to be a collaborator: email your GitHub username to
gregory.schwing@med.wayne.edu with the subject "Student_Projects access".)

## 3. Start Claude and type `/onboard`

In the VS Code terminal (`Ctrl` + `` ` ``), type `claude`, sign in when the browser opens,
then type:

```
/onboard
```

Claude reads `CLAUDE.md` at the root of this repository, which carries the whole lab
workflow, and the `/onboard` command walks you through everything below: it checks your
tools, sets up the grid connection, builds your environment on the grid as a job, fetches
the dataset, runs the demo study, and then helps you choose a project from
`projects/IDEAS.md` and write the proposal. You can stop and resume at any step; it checks
what is already done.

The three grid steps need you, because they involve your university identity.

## 4. Get a grid account

The WSU Grid is the university's HPC cluster. Apply with your AccessID through the
C&IT High Performance Computing pages, [tech.wayne.edu/kb/high-performance-computing](https://tech.wayne.edu/kb/high-performance-computing)
(the "Grid account request" form), naming **Gregory Schwing** as sponsor, and email him
that you applied. Accounts are usually created within two business days. Questions:
hpc@wayne.edu, (313) 577-4743.

## 5. Set up Google Authenticator

The grid uses Google Authenticator (not Microsoft Authenticator) for its second factor.
Install the app on your phone, connect to the WSU VPN, log in to
[ondemand.grid.wayne.edu](https://ondemand.grid.wayne.edu) with your AccessID and
password, open **Interactive Apps → 2FA Setup**, launch it, and scan the QR code with the
app. From then on a password login to the grid asks for the six-digit code.
Instructions with screenshots: [How do I set up and use Google Authenticator for the Grid?](https://services.wayne.edu/TDClient/277/Portal/KB/Article/20242)

## 6. Make an SSH key, so the code is asked only once

Claude drives the grid with non-interactive `ssh` commands, and those cannot answer a
two-factor prompt. An SSH key logs you in without password or code. `/onboard` runs these
for you, but they are here so you know what happens:

```bash
ssh-keygen -t ed25519 -C "youraccessid@wayne.edu"        # Enter at every prompt
ssh-copy-id youraccessid@grid.wayne.edu                    # password + Authenticator code, once
ssh -o BatchMode=yes youraccessid@grid.wayne.edu hostname  # prints "warrior" with no prompt
```

and a `~/.ssh/config` entry (`templates/ssh_config`) so that `ssh grid` is enough. On
Windows, Claude runs `ssh` from Git Bash or WSL; the key lives in that home directory.

## 7. Tell Claude your AccessID, and let it finish

Back in `/onboard`, give Claude your AccessID. It will test the connection, clone this
repository on the grid, submit a job that builds the `osc` environment
(`templates/make_env.sh`), submit a job that downloads the dataset labels and manifest
(`templates/get_dataset.sh`, 1.1 GB, or use the lab's shared copy if your mentor gives you
a path), run the demo study on ten records and then on all 802, and open
`projects/IDEAS.md` with you to choose a project.

## What "done" looks like

- `ssh -o BatchMode=yes grid hostname` prints `warrior`
- `ssh grid "source ~/miniforge3/etc/profile.d/conda.sh && conda activate osc && python -c 'import nibabel'"` prints nothing
- `~/data/CTSpinoPelvic1K/labels` on the grid holds 802 files
- `examples/pelvic_width_dimorphism/results/report.txt` on the grid matches the one in
  this repository to the second decimal
- a branch `proposal/<lastname>-<topic>` with `proposal.md`, opened as a pull request

If any step fails, paste the error to Claude and say which step you were on. If Claude is
stuck, email your mentor with the same paste.
