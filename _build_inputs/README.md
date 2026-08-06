# _build_inputs

Scratch folder for staging reference documents during skill build sessions.
Files dropped here are read by Claude Code or other build agents but never
committed to the repo (this folder is in .gitignore).

Typical contents during an active build session:
- Design spec (the canonical reference)
- Build spec (operational instructions and kickoff prompts)
- Any reference docs the build session needs (predecessor specs, etc.)

Clean out the files after a build cycle ends. Keep the folder itself.
