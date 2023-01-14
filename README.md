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

## How to Run
Refer to `config.yaml`, which should reference paths under `/work`.
In `docker-compose.yaml`, make sure you map the path you want managed to `/work`.
Run `docker-compose up`.

## Build
```
docker build -t tianlechen/sfm . && docker push tianlechen/sfm
```
