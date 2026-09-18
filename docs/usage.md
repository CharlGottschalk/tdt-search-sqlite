# Using SQLite Search

Run the path-based examples from a parent directory containing `workspace` and
the stack source directories. Paths are relative to that directory; adjust them
to your layout. Commands without `--workspace` run from the workspace root.

SQLite Search adds ranked full-text search over approved brain notes. It indexes
note titles and contents with SQLite FTS5 and ranks matches using BM25, with more
weight given to title matches. [Dryft](https://usedryft.com) returns current Markdown evidence for the
matching notes.

## Requirements

[Dryft](https://usedryft.com) must run under Python 3.12, with FTS5 support in that interpreter's
`sqlite3` module. The provider uses Python's standard library;
it does not bundle a separate database server, model or third-party Python runtime.

## Package compatibility

The provider itself uses portable Python APIs, but the current stack manifest
lists Linux x86_64 only. Windows support needs a compatible release with an
updated platform declaration and verification. This is separate from [Dryft](https://usedryft.com) core
platform support. The Python/FTS5 dependency check applies on Windows too; use the
Python executable from [Dryft](https://usedryft.com)'s environment.

## Dependency setup

[Dryft](https://usedryft.com) launches providers with its own Python interpreter. Installing Python 3.12
alongside a [Dryft](https://usedryft.com) installation that uses another version does not switch [Dryft](https://usedryft.com)
to 3.12. Select Python 3.12 when installing [Dryft](https://usedryft.com); for an existing installation,
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

Repeat the FTS5 check with the interpreter in [Dryft](https://usedryft.com)'s environment if it differs
from `python3.12`. Expect Python 3.12 and `FTS5 available`. The check uses an
in-memory database and writes no files.

Other distributions use different package names; see the
[Python Linux installation guide](https://docs.python.org/3.12/using/unix.html).
Ubuntu's [SQLite shared-library package](https://packages.ubuntu.com/noble/libsqlite3-0)
provides the system library, but a custom Python build may use a different SQLite.
If the check fails, use a Python 3.12 build linked to an SQLite build with
[FTS5 enabled](https://www.sqlite.org/fts5.html#building_fts5_as_part_of_sqlite).
Installing the SQLite CLI or a pip package does not enable FTS5 in the interpreter
[Dryft](https://usedryft.com) already uses. No database server is needed.

## Install from the registry

In your workspace's agent session, invoke `/dryft-install-stack` in Claude or
`$dryft-install-stack` in Codex and ask to install `dryft-search-sqlite`. The skill
searches the marketplace, inspects the release and guides installation.

For the same flow in the CLI:

```sh
dryft marketplace search "sqlite search"
dryft stack install dryft-search-sqlite --inspect
dryft --workspace ./workspace stack install dryft-search-sqlite --trust-executable SHA256
dryft --workspace ./workspace brain providers
```

Review the source, version, provider code, platform requirements and any listed
prerequisites. Replace `SHA256` with the displayed selected-content digest only
after approving that content, and replace the workspace path with your own.
If the listing requires prerequisite confirmation, verify it and supply the
corresponding `--confirm-prerequisite TYPE:REF` flags. Select a particular release
with `--version VERSION` on both inspection and installation.

Registry installation requires network access. [Dryft](https://usedryft.com) downloads and validates the
release, including the provider's size and hash. Installation does not run the
provider or build an index. When invoked, the provider retains your OS access;
a subprocess is not a security sandbox.

## Build the index

Run the following commands from your [Dryft](https://usedryft.com) workspace, or add
`--workspace ./workspace` after `dryft` when working elsewhere:

```sh
dryft brain index --provider dryft-search-sqlite
```

Only approved notes are indexed. After adding, approving, editing or removing
notes, rerun the command to reconcile the index. It adds new notes, replaces
changed entries and removes deleted ones, leaving unchanged entries intact.

To discard the cache and build a fresh index:

```sh
dryft brain index --provider dryft-search-sqlite --rebuild
```

The SQLite index is a disposable core-managed cache. Your Markdown files remain
authoritative; do not edit the database directly.

## Search your notes

```sh
dryft brain search "deployment recovery" --provider dryft-search-sqlite
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
dryft brain search "deployment"
```

If Semantic Search is also installed and indexed, combine the rankings by
repeating `--provider`:

```sh
dryft brain search "deployment recovery" --provider dryft-search-sqlite --provider dryft-search-semantic
```

Index each selected provider first. Indexing and querying run locally on demand,
without network calls, downloads, dependency installation or background services.

## Update or remove

Inspect a newer release before approving an update:

```sh
dryft stack update dryft-search-sqlite --check
```

Review the plan and new executable content, then approve through the interactive
update command or its `--approve` token, with fresh `--trust-executable SHA256`
consent for the selected content. Updates invalidate the index; build it again
before searching.

To remove the stack:

```sh
dryft stack remove dryft-search-sqlite
```

Removal deletes unchanged owned cache files and preserves your brain notes.
Edited owned assets or cache files block removal; save useful changes elsewhere
and restore the recorded originals before retrying.

## Troubleshooting

- **Provider not listed:** run `dryft stack list` and `dryft doctor` in the intended
  workspace to check installation and owned files.
- **FTS5 unavailable:** use a compatible Python build with SQLite FTS5 support.
  Installing this stack does not replace Python or its SQLite library.
- **Index missing or invalid:** run the index command with `--rebuild`.
- **Expected notes missing:** confirm the notes are approved, rerun indexing and
  search for words present in the title or body.
- **Provider error:** omit `--provider` to use literal search while resolving the
  error. [Dryft](https://usedryft.com) does not silently switch providers.
