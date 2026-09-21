# Using SQLite Search

Run the path-based examples from a parent directory containing `workspace` and
the stack source directories. Paths are relative to that directory; adjust them
to your layout. Commands without `--workspace` run from the workspace root.

SQLite Search adds ranked full-text search over approved brain notes. It indexes
note titles and contents with SQLite FTS5 and ranks matches using BM25, with more
weight given to title matches. [ThisDamnThing](https://usethisdamnthing.com) returns current Markdown evidence for the
matching notes.

## Requirements

[ThisDamnThing](https://usethisdamnthing.com) must run under Python 3.12, with FTS5 support in that interpreter's
`sqlite3` module. The provider uses Python's standard library;
it does not bundle a separate database server, model or third-party Python runtime.

## Package compatibility

The provider itself uses portable Python APIs, but the current stack manifest
lists Linux x86_64 only. Windows support needs a compatible release with an
updated platform declaration and verification. This is separate from [ThisDamnThing](https://usethisdamnthing.com) core
platform support. The Python/FTS5 dependency check applies on Windows too; use the
Python executable from [ThisDamnThing](https://usethisdamnthing.com)'s environment.

## Dependency setup

[ThisDamnThing](https://usethisdamnthing.com) launches providers with its own Python interpreter. Installing Python 3.12
alongside a [ThisDamnThing](https://usethisdamnthing.com) installation that uses another version does not switch [ThisDamnThing](https://usethisdamnthing.com)
to 3.12. Select Python 3.12 when installing [ThisDamnThing](https://usethisdamnthing.com); for an existing installation,
check its environment before changing anything. For pipx installations,
`pipx list` shows the Python version used by each application.

The following package commands are for Ubuntu 24.04 x86_64 only. They are not
Windows installation instructions. Install missing host packages with:

```sh
sudo apt update
sudo apt install python3.12 python3.12-venv libsqlite3-0
```

Check Python and FTS5:

```sh
python3.12 --version
python3.12 -c 'import sqlite3; db = sqlite3.connect(":memory:"); db.execute("CREATE VIRTUAL TABLE probe USING fts5(body)"); print("FTS5 available")'
```

Repeat the FTS5 check with the interpreter in [ThisDamnThing](https://usethisdamnthing.com)'s environment if it differs
from `python3.12`. Expect Python 3.12 and `FTS5 available`. The check uses an
in-memory database and writes no files.

Other distributions use different package names; see the
[Python Linux installation guide](https://docs.python.org/3.12/using/unix.html).
Ubuntu's [SQLite shared-library package](https://packages.ubuntu.com/noble/libsqlite3-0)
provides the system library, but a custom Python build may use a different SQLite.
If the check fails, use a Python 3.12 build linked to an SQLite build with
[FTS5 enabled](https://www.sqlite.org/fts5.html#building_fts5_as_part_of_sqlite).
Installing the SQLite CLI or a pip package does not enable FTS5 in the interpreter
[ThisDamnThing](https://usethisdamnthing.com) already uses. No database server is needed.

## Install from the registry

In your workspace's agent session, invoke `/tdt-install-stack` in Claude or
`$tdt-install-stack` in Codex and ask to install `tdt-search-sqlite`. The skill
searches the marketplace, inspects the release and guides installation.

For the same flow in the CLI:

```sh
tdt marketplace search "sqlite search"
tdt stack install tdt-search-sqlite --inspect
tdt --workspace ./workspace stack install tdt-search-sqlite --trust-executable SHA256
tdt --workspace ./workspace brain providers
```

Review the source, version, provider code, platform requirements and any listed
prerequisites. Replace `SHA256` with the displayed selected-content digest only
after approving that content, and replace the workspace path with your own.
If the listing requires prerequisite confirmation, verify it and supply the
corresponding `--confirm-prerequisite TYPE:REF` flags. Select a particular release
with `--version VERSION` on both inspection and installation.

Registry installation requires network access. [ThisDamnThing](https://usethisdamnthing.com) downloads and validates the
release, including the provider's size and hash. Installation does not run the
provider or build an index. When invoked, the provider retains your OS access;
a subprocess is not a security sandbox.

## Build the index

Run the following commands from your [ThisDamnThing](https://usethisdamnthing.com) workspace, or add
`--workspace ./workspace` after `tdt` when working elsewhere:

```sh
tdt brain index --provider tdt-search-sqlite
```

Only approved notes are indexed. After adding, approving, editing or removing
notes, rerun the command to reconcile the index. It adds new notes, replaces
changed entries and removes deleted ones, leaving unchanged entries intact.

To discard the cache and build a fresh index:

```sh
tdt brain index --provider tdt-search-sqlite --rebuild
```

The SQLite index is a disposable core-managed cache. Your Markdown files remain
authoritative; do not edit the database directly.

## Search your notes

```sh
tdt brain search "deployment recovery" --provider tdt-search-sqlite
```

Use ordinary words. The provider takes up to 50 word tokens and searches for any
of them, ranking the results by relevance. Input is not interpreted as raw FTS
syntax, so operators, quotes and punctuation do not enable advanced query syntax.
Title matches receive more weight than body matches.

Queries do not update the index. New notes need indexing before they appear;
stale or deleted notes are excluded from results. Reindex after changing notes
if expected results are missing.

Installing this stack does not change ordinary literal search. Omit the provider
to use it:

```sh
tdt brain search "deployment"
```

If Semantic Search is also installed and indexed, combine the rankings by
repeating `--provider`:

```sh
tdt brain search "deployment recovery" --provider tdt-search-sqlite --provider tdt-search-semantic
```

Index each selected provider first. Indexing and querying run locally on demand,
without network calls, downloads, dependency installation or background services.

## Update or remove

Inspect a newer release before approving an update:

```sh
tdt stack update tdt-search-sqlite --check
```

Review the plan and new executable content, then approve through the interactive
update command or its `--approve` token, with fresh `--trust-executable SHA256`
consent for the selected content. Updates invalidate the index; build it again
before searching.

To remove the stack:

```sh
tdt stack remove tdt-search-sqlite
```

Removal deletes unchanged owned cache files and preserves your brain notes.
Edited owned assets or cache files block removal; save useful changes elsewhere
and restore the recorded originals before retrying.

## Troubleshooting

- **Provider not listed:** run `tdt stack list` and `tdt doctor` in the intended
  workspace to check installation and owned files.
- **FTS5 unavailable:** use a compatible Python build with SQLite FTS5 support.
  Installing this stack does not replace Python or its SQLite library.
- **Index missing or invalid:** run the index command with `--rebuild`.
- **Expected notes missing:** confirm the notes are approved, rerun indexing and
  search for words present in the title or body.
- **Provider error:** omit `--provider` to use literal search while resolving the
  error. [ThisDamnThing](https://usethisdamnthing.com) does not silently switch providers.
