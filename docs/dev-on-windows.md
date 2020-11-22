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

## Troubleshooting/Tips

If you have the requirements and follow the dev start instructions, you should be all set. But, in case you run into an error, here are some common ones and how to get past them: 

1. If you are not sure where to check your Windows version:

    - <img src="https://github.com/YACS-RCOS/yacs.n/blob/master/docs/screenshots/verCheck.png" width=375>

2. When you run `./scripts/dev-start.bat` if you get this error:
    - <img src="https://github.com/YACS-RCOS/yacs.n/blob/master/docs/screenshots/errorDockerCompose.JPG" width = 500>
    - This means that either you did not download Docker Desktop, or you need to change the settings in Docker Desktop. Open your Docker and go to Settings. Make sure it looks like this
    - <img src="https://github.com/YACS-RCOS/yacs.n/blob/master/docs/screenshots/solutionDockerCompose.JPG" width = 500>

3. If you get this error when you run `./scripts/dev-start.bat`:
    - <img src="https://github.com/YACS-RCOS/yacs.n/blob/master/docs/screenshots/errorNoCommandUp.JPG" width = 550>
    - Open to Windows Powershell, navigate to the root directory yacs.n, and run this:
    - `docker-compose -f docker-compose.yml -f docker-compose.development.yml up`
    - When this finishes running, it will tell you where to go to see the running version of YACS in the output text at the bottom
