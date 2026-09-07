Bring results back from the grid for: $ARGUMENTS

1. Run `tools/grid.sh pull <remote folder relative to the repo> <local folder>` (through `wsl -e bash -lc` on Windows). Results folders only: never pull `*.nii.gz`.
2. List what arrived with sizes.
3. Open every PNG that arrived with the Read tool and describe what it shows in one sentence each; flag anything that looks wrong (empty axes, a single point, an impossible range).
4. If a report or CSV arrived, print the report and the first five rows of the CSV, and check that one number in the report can be found in the CSV.
5. Remind me to commit the results (`git add <folder> && git commit -m "..."`) and to add a dated line to `JOURNAL.md`.
