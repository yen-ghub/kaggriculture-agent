---
name: set-eval-baseline
description: Add or activate a Kaggriculture baseline in evaluate.py. Use when the user asks to evaluate against, add, switch to, or select a baseline opponent.
---

# Set evaluation baseline

Update the repository's `evaluate.py` so one requested baseline is the active
opponent.

## Identify the baseline

- Prefer a baseline module name supplied by the user, with or without the
  `.py` suffix.
- If the user says "latest" without naming it, inspect `baselines/` and the
  current Git state. Select the unique newly added or newly frozen baseline;
  do not rely on modification time alone. Ask only if multiple candidates are
  genuinely ambiguous.
- Require a valid Python module filename and verify that
  `baselines/<module>.py` exists.

## Update `evaluate.py`

- Add an import in the existing baseline-import section if it is absent:

  ```python
  from baselines.<module> import agent as <alias>
  ```

- Use a clear, valid Python identifier for `<alias>`, normally
  `<module>_agent`.
- In `OPPONENTS`, comment out each currently active opponent entry and activate
  exactly one entry for the requested baseline.
- Reuse an existing import or opponent entry rather than duplicating it.
- Preserve `SEEDS`, product tracking, reporting, commented opponent choices,
  and all unrelated code.
- Do not modify `main.py`, the baseline module, or evaluation parameters unless
  the user separately requests it.

## Verify

Run the repository virtual environment's Python syntax/import check:

```powershell
.\.venv\Scripts\python.exe -m py_compile evaluate.py baselines\<module>.py
```

Then inspect the focused diff for `evaluate.py`. Do not run the full evaluation
unless the user asks. Report the active baseline and whether validation passed.
