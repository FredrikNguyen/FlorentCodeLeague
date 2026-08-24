# Packaging and submission

`bots/candidate/` is the upload tree. `bots/baseline/` is the frozen local
comparator. Generated snapshots and archives are ignored.

## Validate

```bash
make check
make smoke
make eval-regression
make eval-local
make remote-gate
```

The candidate must contain a literal `Player` class in `main.py`, pure Python
source only, no more than 500 files, at most 50 MB unpacked, and at most 5 MB in
the final ZIP.

## Package

```bash
make package SLUG=release
```

The package command:

1. copies `bots/candidate/` to an ignored timestamped directory under
   `bots/versions/`;
2. validates file count, size, and native-extension restrictions;
3. creates a ZIP under `artifacts/submissions/`;
4. writes a JSON manifest containing the archive hash, size, Git revision, and
   working-tree status.

Inspect the manifest and ensure the recorded working tree was clean.

## Upload

Uploading does not activate the bot:

```bash
uv run python scripts/submit_candidate.py \
  artifacts/submissions/FILE.zip \
  --name karrigan-release \
  --confirm
```

The wrapper refuses to write without `--confirm` and stores the CLI response in
the ignored `reports/` directory.

## Activate

After the platform reports the upload as ready:

```bash
uv run fcode submission list --json
uv run python scripts/activate_submission.py VERSION --confirm
```

Activation is a separate confirmed operation. The wrapper records the prior
submission list, activation response, and resulting status under `reports/`.

## Observe or roll back

Capture current account, ladder, match, and submission data with:

```bash
make live-snapshot
```

Keep the previous active version available. If the new version shows crashes,
timeouts, command failures, or a material live regression, reactivate that
known-good version with the same guarded activation command.
