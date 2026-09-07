Submit a job on the grid for: $ARGUMENTS

Do it in this order, and stop to show me before step 4.

1. Make sure the script to run exists in this repository and takes `--help`; if the job needs a new SLURM script, write it as a FILE under `slurm/` in my project folder by copying `templates/slurm_job.sh` and editing the `#SBATCH` lines (CPUs must match `--workers`, memory in GB, a realistic wall time). Never use `sbatch --wrap`, never send a script through a heredoc over ssh.
2. Commit the files and push (`git push` through WSL on Windows), then sync the grid clone with `tools/grid.sh sync`.
3. Show me the exact submit command, `tools/grid.sh submit <job script> <args>`, and what each `#SBATCH` line asks for.
4. Only after I say "submit", run it, report the job id, and add a dated line with the job id and the command to `JOURNAL.md` in my project folder.
5. Start `tools/grid.sh wait <id>` as a background command so I am told when the job ends, and do not poll in the foreground.
