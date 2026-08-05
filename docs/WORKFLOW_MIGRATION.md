# Migrating from the old multi-agent harness

The full ZIP already contains the optimized layout. When merging these files into an older checkout, remove the obsolete orchestration files:

```bash
rm -rf .codex/agents .codex/skills
rm -f configs/codex_harness.toml
rm -f scripts/codex_luna_doctor.py scripts/setup_codex_v1_catalog.py
rm -f scripts/codex_v1.sh scripts/codex_v2_visible.sh
```

Then copy the new files into the repository root and run:

```bash
make refresh-start
make chatgpt-plan REQUEST="Plan the next implementation milestone"
make static
```

The new default is one Luna XHigh Codex process. No V1/V2 subagent workaround is needed.
