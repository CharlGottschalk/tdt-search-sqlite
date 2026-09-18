![Dryft SQLite Search](docs/assets/banner.png)

# SQLite Search

A [Dryft](https://usedryft.com) stack that adds ranked full-text search to your approved brain notes.
It uses SQLite FTS5 to search titles and contents, giving title matches more
weight. Indexing and searching run locally without an API key, external service
or model download. Your Markdown notes remain the source for every result.

## Dependencies

- [Dryft](https://usedryft.com) running under Python 3.12.
- SQLite FTS5 support in that Python interpreter's `sqlite3` module.

No separate database server or pip package is required. See
[dependency setup](docs/usage.md#dependency-setup) for installation commands and
an FTS5 check. Installing the `sqlite3` command-line tool alone does not add FTS5
to Python.

## Package compatibility

[Dryft](https://usedryft.com)'s platform support and this stack package's compatibility are separate.
The provider uses Python's standard library, but its current manifest declares
Linux x86_64 only. A Windows-compatible release must declare and verify Windows
support; installing Python and FTS5 alone does not change that declaration.

## Release status

Candidate version: **0.1.0**. Canonical source: [1one8/dryft-search-sqlite](https://github.com/1one8/dryft-search-sqlite).
The registry commands below are the planned public installation path; production
listing and installation are still awaiting release verification.

Local acceptance is on Linux x86_64 with Python 3.12 and Claude/Codex. macOS
and native Windows are unverified. The manifest enforces Linux x86_64/Python 3.12.
The provider runs with local OS access, so inspect its code before granting trust.

## Install

Ask your agent to install
`dryft-search-sqlite` using `/dryft-install-stack` (Claude) or
`$dryft-install-stack` (Codex). The skill inspects the registry release and guides
prerequisite checks and executable trust.

Or inspect and install through the CLI:

Run the path-based examples from a parent directory containing `workspace` and
the stack source directories. Paths are relative to that directory; adjust them
to your layout. Commands without `--workspace` run from the workspace root.

```sh
dryft stack install dryft-search-sqlite --inspect
dryft --workspace ./workspace stack install dryft-search-sqlite --trust-executable SHA256
```

Review the release, prerequisites and provider code first. Replace `SHA256`
with the inspected selected-content digest and the workspace path with your own.
[Dryft](https://usedryft.com) downloads the stack from the registry; no source clone is needed.

See the [usage guide](docs/usage.md) to build the index and start searching.

## License

Licensed under the [Apache License 2.0](LICENSE). Copyright 1one8 (Pty) Ltd.

Bundled third-party components retain their respective licenses and notices.
