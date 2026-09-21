"""Independent stdlib SQLite FTS5 search. No network or runtime installation."""
import json
from pathlib import Path
import re
import sqlite3
import sys


def main(request):
    path = Path(request['state_path'])
    notes = {n['id']: n for n in request['notes']}
    if request['operation'] == 'index':
        if request['rebuild']:
            path.unlink(missing_ok=True)
        db = sqlite3.connect(path)
        with db:
            db.execute('CREATE VIRTUAL TABLE IF NOT EXISTS notes USING fts5(id UNINDEXED, hash UNINDEXED, title, body)')
            stored = dict(db.execute('SELECT id, hash FROM notes'))
            for key, old in stored.items():
                if key not in notes or notes[key]['sha256'] != old:
                    db.execute('DELETE FROM notes WHERE id=?', (key,))
            for key, note in notes.items():
                if stored.get(key) != note['sha256']:
                    db.execute('INSERT INTO notes VALUES (?,?,?,?)', (key, note['sha256'], note['title'], note['text']))
        db.close()
        return {'protocol_version': 1, 'indexed': len(notes)}
    if not path.exists():
        raise ValueError('Index missing; run tdt brain index --provider tdt-search-sqlite')
    db = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    # Query grammar is generated from tokens; user input is never FTS syntax.
    terms = re.findall(r'\w+', request['query'])[:50]
    expression = ' OR '.join('"' + term.replace('"', '""') + '"' for term in terms)
    rows = db.execute('SELECT id, hash FROM notes WHERE notes MATCH ? ORDER BY bm25(notes,0,0,4,1), id', (expression,)) if expression else []
    result = []
    for key, digest in rows:
        if key in notes and notes[key]['sha256'] == digest:
            result.append({'id': key, 'sha256': digest})
        if len(result) == request['limit']:
            break
    db.close()
    return {'protocol_version': 1, 'results': result}


if __name__ == '__main__':
    try:
        print(json.dumps(main(json.load(sys.stdin))))
    except Exception as exc:
        print(f'SQLite FTS5 unavailable or index invalid: {exc}; rebuild the index or use literal search.', file=sys.stderr)
        sys.exit(1)
