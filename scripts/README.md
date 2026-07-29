# Scripts

Optional helper scripts for maintaining the training repository.

Examples:

* validating links;
* checking that generated notebooks are not committed accidentally;
* building slides;
* rendering example outputs used in the training.


## Placeholder Replacement

Use `fill_placeholders.py` to replace double-brace placeholder values after
creating a new repository from this template.

```bash
scripts/fill_placeholders.py template-values.yml --dry-run
scripts/fill_placeholders.py template-values.yml --strict
```

The values file can be JSON or a simple YAML file with one `KEY: value` entry
per line. The script only edits text-like files and skips `.git`, build
directories, notebook checkpoints, and Quarto output directories.
