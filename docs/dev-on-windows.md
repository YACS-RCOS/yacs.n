# Windows Dev

Hi friends, so you are looking to contribute and you're on a windows
environment, here's what you'll need.

## Requirements

Make sure you have the following requirements:

1. Have Windows 10 1903 (if x64 system)
    - You can either go to Settings, Update & Security and click Check for Updates. Here's a link to for more [information](https://support.microsoft.com/en-us/help/4028685/windows-10-get-the-update).

2. Have Windows Subsystem for Linux 2 (WSL 2)
    - Windows now support Linux filesystem and commands starting 1607. For x64 systems, Version 1903 or higher supports WSL 2, which we would need. Here's a [link](https://docs.microsoft.com/en-us/windows/wsl/install-win10#install-windows-subsystem-for-linux) to learn more!

3. Have [Docker Desktop](https://www.docker.com/products/docker-desktop) installed
    - Docker Desktop has both docker and docker-compose commands that will be needed for this project! Here are guides about them:
        - [docker](https://docs.docker.com/get-started/overview/)
        - [docker-compose](https://docs.docker.com/compose/)


## Dev Start

From the project root, run `./scripts/dev-start.bat`

_See dev script here: https://github.com/YACS-RCOS/yacs.n/blob/master/scripts/dev-start.bat_
