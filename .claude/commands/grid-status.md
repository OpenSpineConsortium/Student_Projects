Check the grid and report in five lines or fewer.

1. Run `tools/grid.sh run "hostname; squeue -u \$USER -o '%.10i %.20j %.8T %.10M %.6D %R'"` (on Windows through `wsl -e bash -lc`).
2. If a job is running or pending, say which, how long, and where its log is (`logs/<name>_<id>.out` in `~/Student_Projects` on the grid).
3. If `.last_jobid` exists in the repository root, show the last 20 lines of that job's stdout and stderr with `tools/grid.sh run "cd ~/Student_Projects && tail -n 20 logs/*_<id>.out logs/*_<id>.err"`.
4. If the grid does not answer, say so and tell me to check `ssh grid hostname` in a terminal; do not retry more than twice.
