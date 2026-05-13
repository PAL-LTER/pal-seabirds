# Copilot Working Preferences for This Repository

These instructions apply to all Copilot chat sessions in this workspace.

## Environment
- Use the existing conda environment named `seabirds`.
- Do not suggest creating a new environment unless explicitly asked.
- When running Python, prefer `conda run -n seabirds python ...`.

## Script Execution Style
- Do not use inline shell Python (for example, heredoc or one-liner embedded Python in shell commands).
- For diagnostics or quick checks, create temporary `.py` scripts in the relevant folder (for example, `cruise/_tmp_*.py`) and run them.
- Keep temporary scripts focused and easy to clean up.

## Change Style
- Prefer minimal, targeted edits over broad refactors.
- Prioritize direct data-fix work over tooling complexity unless tooling changes are explicitly requested.

## Command and Execution Defaults
- For cruise workflows, run commands from `cruise/` unless a script requires repo root.
- Prefer existing entry points over ad hoc orchestration:
	- `conda run -n seabirds python process_cruise.py`
	- `conda run -n seabirds python qc_cruise.py --dataset transect --only-failures`
	- `conda run -n seabirds python qc_cruise.py --dataset stationary --only-failures`

## Temp Script Hygiene
- Temporary diagnostics scripts must be named `_tmp_<purpose>.py` and kept in `cruise/`.
- Remove temporary scripts after results are captured, unless explicitly kept for repeated diagnostics.
- If a temp diagnostic becomes repeatedly useful, promote it to a named utility script.

## Repo Workflow Preferences
- Do not update `README.md` or broader documentation unless explicitly requested.
- Keep fixes in converter scripts where possible; avoid post-merge patching unless necessary.
- Re-run the relevant validator after each targeted fix batch and report only key deltas.

## Tasklist Maintenance
- When a new blocking issue is found, add it to `dev/qc_cleanup_tasklist.txt` with priority and a one-line acceptance check.
- Keep task priorities explicit (`P0`, `P1`, ...), and close tasks with a short note of what changed.
