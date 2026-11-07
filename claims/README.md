# Claims verification register

- `register.jsonl` — one claim per line (`research/schemas/claim.schema.json`)
- `verification-log.jsonl` — append-only audit of status changes

Statuses: `unverified` | `supported` | `contested` | `rejected` | `educational_only`

PED / peptide / GLP-1 literacy claims that must not become beginner protocols should use `educational_only` and/or `deep_dive_flags: ["harm_reduction", "beginner_unsafe"]`.

Manuscript rule: claims may be linked to YouTube-backed `insight_ids` for internal verification, but chapter prose must never name or cite those channels/people.

```bash
python3 scripts/research/export_claims.py
python3 scripts/research/verify_claim.py --claim-id CLAIM --status supported --evidence-class B
```
