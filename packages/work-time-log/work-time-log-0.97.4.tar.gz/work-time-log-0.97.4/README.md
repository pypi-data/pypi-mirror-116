# Work time log

`work` allows manual time tracking via a CLI that works similarly to `git`:

1. Text files are used for storage. This makes it easy to track the log with `git`.
2. The `work status` is global, meaning any terminal can be used to check or update it.
3. Hashes are used to verify that the log was not modified by another tool.

## Release history

- 0.9: Category and message
    + Entries can now have an optional category and message.
    + Both can be added when stopping a run or adding an entry.
    + When listing entries, these fields can be displayed.

## Changelog

- 0.97.4
    + `list`
        * `--include-active` now counts active run in total
        * `--only-time` now merges touching entries for output
        * `--with-breaks` now shows breaks in separate lines
    + `switch`: Updated help text for new syntax
    + `recess`: Clearer error message when removing nonexistent day
    + completions: Global flags no longer suggested after sub-commands
    + packaging: Test modules now omitted from package
