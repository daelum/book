# Bibliography

Append one JSON object per line to `sources.jsonl` matching `research/schemas/bibliography.schema.json`.

Rules:

- Never invent DOIs, PMIDs, or URLs.
- Set `identifiers_verified` to `true` only after resolving the identifier.
- YouTube videos may be bibliography entries (`source_type: youtube`) but do not replace scientific refs for scientific claims.

Helper:

```bash
python3 scripts/research/add_bibliography.py --from-json path/to/source.json
```
