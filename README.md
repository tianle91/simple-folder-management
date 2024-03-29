# Simple Folder Management
Moves folders in `dump` directory to other directories in the same base path. Will add more details later. For now, see [tests/test_config.yaml](tests/test_config.yaml) for example configuration, which references paths in `tests`.

Run the following to see a demo:
```console
root@5c9b3ad8f566:/workspaces/simple-folder-management# python app.py tests/test_config.yaml
INFO:__main__:In tests/example_directory_a, found 3 directories to be moved.
INFO:__main__:In tests/example_directory_b, found 1 directories to be moved.
INFO:__main__:In tests/example_directory_c, found 1 files to be moved.
INFO:__main__:Moving tests/example_directory_a/dump/keyword_A/ -> tests/example_directory_a/group_A_name/keyword_A
INFO:__main__:Moving tests/example_directory_a/dump/keyword_B/ -> tests/example_directory_a/group_A_name/keyword_B
INFO:__main__:Moving tests/example_directory_a/dump/keyword_C/ -> tests/example_directory_a/some_subdir/group_C/keyword_C
INFO:__main__:Moving tests/example_directory_b/dump/keyword_A/ -> tests/example_directory_b/group_A_name/keyword_A
INFO:__main__:Moving tests/example_directory_c/dump/keyword_A.txt -> tests/example_directory_c/group_A_name
```

## Run with Docker
In `docker-compose.yaml`, make sure you map the path you want managed to `/work`.
Your config should paths under `/work`.
Run `docker-compose up`.
