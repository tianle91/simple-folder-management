# Simple Folder Management
Here's an example configuration.
```yaml
meta:
  base_dir: example
  dump_dir: dump
  managed_dir: managed
  cron: '* * * * *'
groups:
  group_A:
    name: group_A_name
    keywords:
      - keyword_A
      - keyword_B
```
Every minute, for any new folders in `dump`, if any of `keyword_A, keyword_B` are in the new folder name, the new folder will be moved to `managed/group_A_name`.
