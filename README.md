# Simple Folder Management
Will probably add more details later.
For now, see [tests/test_config.yaml](tests/test_config.yaml) for example configuration.
Example configuration references paths in `tests` so run the following to see a demo:
```python
python app.py tests/test_config.yaml
```

## How to Run
In `docker-compose.yaml`, make sure you map the path you want managed to `/work`.
Your config should paths under `/work`.
Run `docker-compose up`.

## Build
```
docker build -t tianlechen/sfm . && docker push tianlechen/sfm
```
Strangely building this on a M1 Mac can run successfully in WSL but not on my Synology NAS.
However, if I built it on WSL it works fine on Synology NAS.
Perhaps there's some architecture flag I should be setting 🤷
