# UI Design Review -- Safe Cleanup Tool

A Week-10 **design review** for the PySide6 window you've already started
in `main.py`, plus a few suggestions to align with the three-layer pattern
from `demo_ui_and_polish.py`. **This is a review of work you've done, not
a request to start over.** Use what helps; ignore what doesn't.

## Where your project stands today

You're further along than most of the class:

- `Config_Data.py` -- the builders (`freeze_transforms`,
  `delete_non_deformer_history`, `delete_all_history`, `safe_cleanup`) +
  the `BUILDERS` map + the `create_element(data)` dispatcher.
- `Data_Driven_Config.py::CLEANUP_CONFIG` -- a static list of operations.
- `main.py::run_cleanup_pipeline()` -- the driver loop that walks
  `CLEANUP_CONFIG` and dispatches each entry.
- `main.py::CleanupWindow(QtWidgets.QWidget)` -- a working PySide6
  window with a "Safe Cleanup Mode" checkbox, a "Run Cleanup" button,
  and a `run_cleanup()` method that operates on the current selection.
- `main.py::launch_ui()` -- a re-entrant launcher that closes any prior
  window before showing a new one. Nice touch.

So you already have a UI. The Week-10 question for you isn't *"build a
UI"* -- it's *"is the UI cleanly separated from the data and the
logic?"*. The rest of this memo is a small set of refactor suggestions
to push it from "working" to "lesson-aligned".

## The shape we're aiming at (recap)

```
UI  ->  DATA  ->  LOGIC
```

See `demo_ui_and_polish.py` (sections 1, 4, 5). The three layers are:

| Layer | Responsibility                              | In your code today          |
|-------|---------------------------------------------|-----------------------------|
| UI    | Draw controls. No queries. No work.         | `CleanupWindow.__init__`    |
| DATA  | Read each control into one settings dict.   | (missing -- inlined below)  |
| LOGIC | Take a settings dict, do the Maya work.     | `CleanupWindow.run_cleanup` |

Right now `run_cleanup()` reads the selection, builds a dict, and calls
`create_element()` all in one place. That's fine for a small tool, but
it's the spot the lesson asks you to split.

## Suggested settings dict shape

Your tool is a cleanup pipeline, so the natural settings dict is:

```python
{
    "freeze_transforms":      True,   # bool -- run freeze step?
    "delete_history":         True,   # bool -- run history step?
    "preserve_deformers":     True,   # bool -- safe vs. full history delete
    "use_selection":          True,   # bool -- operate on cmds.ls(sl=True)
                                       #         (False = walk CLEANUP_CONFIG)
    "debug":                  True,   # bool -- mirrors Config_Data.DEBUG
}
```

This lines up almost exactly with your existing `SAFE_CLEANUP_DEFAULTS`
dict, plus one toggle for "selection vs. preset list" and a `debug`
flag. Every key here maps to one widget in the UI and one query in
`read_settings()`.

## Suggested UI layout (top to bottom)

You already have one checkBox -- this just expands it. The Qt analogues
of the cmds-style controls used in the demo:

| Setting              | Widget                       |
|----------------------|------------------------------|
| `freeze_transforms`  | `QtWidgets.QCheckBox`        |
| `delete_history`     | `QtWidgets.QCheckBox`        |
| `preserve_deformers` | `QtWidgets.QCheckBox`        |
| `use_selection`      | `QtWidgets.QCheckBox`        |
| `debug`              | `QtWidgets.QCheckBox`        |
| Run                  | `QtWidgets.QPushButton`      |
| Report               | `QtWidgets.QPlainTextEdit`   |

A vertical `QVBoxLayout` (what you already have) is exactly right;
just add the rest of the widgets and store them on `self.` so a
`read_settings()` method can query them.

## Concrete refactor suggestions

These are small, mechanical, and you can do them one at a time. Each
keeps your existing UI working.

1. **Split `run_cleanup` into a bridge + logic pair.** Rename your
   current `run_cleanup` to `_on_run` (the *bridge*), and pull the
   per-object work into `do_the_work(settings)` -- a free function (or
   a method) that takes the settings dict and calls
   `Config_Data.safe_cleanup` / `freeze_transforms` etc. The bridge
   becomes 3 lines: gather settings, hand to logic, catch errors.

2. **Add a `read_settings(self)` method** that returns the dict above by
   querying every `self.*_checkbox`. Nothing else.

3. **Use the existing `safe_cleanup()` from `Config_Data.py`** as the
   primary path. You wrote it already; the UI should just hand it a
   data dict and let your dispatcher do its job. Don't re-implement
   freeze/history calls in the UI class.

4. **Wire `debug` to your module-level flag.** `Config_Data.DEBUG =
   settings["debug"]` before you dispatch -- you already check `DEBUG`
   in every builder, so this gives the checkbox real teeth.

5. **(Optional) Honour `use_selection`.** If on, walk the current
   selection and dispatch one entry per object. If off, fall back to
   `run_cleanup_pipeline()` so the preset `CLEANUP_CONFIG` still works.

## Must-have vs. nice-to-have

**Must-have** (for the grading rubric):
- All three layers separated; no Maya work inside the UI class beyond a
  one-line bridge call.
- At least 4 working controls (you already have 1; add 3 more checkboxes
  per the table above and you're there).
- A "Run" button that calls `safe_cleanup()` (or the dispatcher) via a
  settings dict.
- A `default_settings()` (or `SAFE_CLEANUP_DEFAULTS`) that matches what
  `read_settings()` produces.
- Friendly error path: `cmds.warning(...)` on bad input -- you're
  already doing this in every builder, just make sure the bridge
  catches `ValueError` too.

**Nice-to-have** (extra polish):
- A `QPlainTextEdit` "report" panel so each operation logs a line.
- A "Clear history" / "Selection count" status label that updates on
  selection change.
- A shelf-button installer following Section 8 of the demo.
- JSON preset save/load via `QFileDialog` so you can ship preset
  cleanup profiles alongside `CLEANUP_CONFIG`.

## How to use the starter file in this PR

`cleanup_ui_starter.py` is a parallel scaffold -- it does **not**
replace your `main.py`. Think of it as a clean reference you can
compare against, or copy bits out of:

- `default_settings()` and `do_the_work()` are **written** and call
  straight into your existing `safe_cleanup` / `freeze_transforms` /
  `delete_*_history` builders. No duplicate logic.
- `build_ui()` and `read_settings()` are **stubbed** with TODOs in the
  shape of a `cmds`-based window, so you can either:
    - Fold the same widget list into your existing `CleanupWindow`
      class (recommended -- you've already done the PySide6 work), or
    - Adopt the `cmds`-based version if you'd rather match David's /
      Lillian's example more directly. Both are graded equally.

## Resources

- **`tool_skeleton.py`** -- the blank version of this pattern.
- **`demo_ui_and_polish.py`** -- read sections 1, 4, 5 first; section 8
  for the shelf-button finish.
- **`scene_builder/` package** -- the recommended multi-file layout if
  you want to split UI and logic across files.

Questions? Comment on this PR or message me.
