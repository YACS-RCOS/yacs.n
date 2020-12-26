# Mac/Linux Dev

Hi friends, so you are looking to contribute and you're on a mac/linux
environment, heres what you'll need.

## Requirements

Make sure you have the following commands available, you can check with the
following.

```sh
> which docker-compose
/usr/local/bin/docker-compose
> which docker
/usr/local/bin/docker
```

See install guides here if you are missing any:

- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Dev Start

From the project root, run `./scripts/dev-start.sh`

_See dev script here: https://github.com/YACS-RCOS/yacs.n/blob/master/scripts/dev-start.sh_

## Dev Clear Volumes

If any of the following occur

- web dependencies are changed

From the project root, run `./scripts/dev-clear-volumes.sh`
