# Simple Folder Management

## How to Run
Refer to `config.yaml`, which should reference paths under `/work`.
In `docker-compose.yaml`, make sure you map the path you want managed to `/work`.
Run `docker-compose up`.

## Build
```
docker build -t tianlechen/sfm . && docker push tianlechen/sfm
```
Strangely building this on a M1 Mac can run successfully in WSL but not on my Synology NAS.
However, if I built it on WSL it works fine on Synology NAS.
Perhaps there's some architecture flag I should be setting 🤷
