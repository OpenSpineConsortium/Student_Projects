Start a new project folder for: $ARGUMENTS

1. Ask me for my last name and a two-or-three-word topic if they are not in the arguments, and form the folder name `projects/<lastname>_<topic>` in lower case with underscores.
2. Create a branch `proposal/<lastname>-<topic>` from `main`.
3. Create the folder with: `proposal.md` copied from `templates/proposal_template.md`, `CLAUDE.md` copied from `templates/CLAUDE.md` with the EDIT lines filled from what I tell you, `JOURNAL.md` with today's date and one line, and empty `results/` and `figures/` folders (with a `.gitkeep` each).
4. Walk me through the proposal one section at a time, asking one question per section, and write my answers into `proposal.md` in full sentences. For section 3, insist on label identifiers, an axis and a unit for every measurement, and check the identifiers against `dataset_labels.json` if the dataset is on this machine.
5. When every section is filled, show me the whole proposal, then commit it with the message `Proposal: <title>` and push the branch. Tell me to open the pull request on GitHub and fill in the template, including the email for my ClickUp invitation.
