# File Integrity Monitor

A command-line tool that detects unauthorized or unexpected changes to files
in a directory by comparing cryptographic hashes against a saved baseline.

## How it works

1. Recursively scans a target directory and computes a SHA-256 hash for every
   file found.
2. On first run (or with `--update`), saves these hashes to a JSON baseline
   file.
3. On subsequent runs, re-scans the directory and compares the new hashes
   against the baseline, reporting any files that were **added**,
   **removed**, or **modified**.

## Usage

Create or update the baseline:
```bash
python hashing.py <directory> --update
```

Check current state against the existing baseline:
```bash
python hashing.py <directory>
```

Use a custom baseline file:
```bash
python hashing.py <directory> --baseline custom_baseline.json
```

## Arguments

| Argument | Required | Description |
|---|---|---|
| `directory` | Yes | Folder to scan |
| `--baseline` | No | Baseline JSON file to read/write (default: `baseline.json`) |
| `--update` | No | Force saving the current scan as the new baseline |

## Example

```bash
$ python hashing.py ./watched_folder --update
Baseline saved to baseline.json (12 files)

# ...later, after a file is edited...

$ python hashing.py ./watched_folder
Added: set()
Removed: set()
Modified: ['./watched_folder/config.yaml']
```

## Known limitations

- No error handling for unreadable files (permission-denied files will crash
  the scan rather than being skipped and reported).
- Hashing is SHA-256 only; not configurable.
- Baseline comparison only reports *which* files changed, not *how*.
