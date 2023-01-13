# Simple Folder Management
Here's an example configuration.
```yaml
meta:
  base_dir: example
  dump_directory: dump
  managed_directory: managed
groups:
  group_A:
    name: group_A_name
    keywords:
      - keyword_A
      - keyword_B
```

For any new folders in `dump`, if any of `keyword_A, keyword_B` are in the new folder name, the new folder will be moved to `managed/group_A_name`.
