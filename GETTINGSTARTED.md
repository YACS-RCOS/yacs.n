# Intro
This file is intended to be a guide to help new developers get started working on YACS and to help avoid 
    many of the common pitfalls that people will fall into. It includes links to online tutorials,
    troubleshooting guides, as well as information on what to submit. If you run into any issues or 
    find something that would be useful to others add it to the appropiate section so that others can 
    see it.
Here is a link to the github: https://github.com/YACS-RCOS/yacs.n

# Getting Set Up
To get started you need to install Docker Desktop and Github Desktop (Not required but a very helpful tool),
    as well as ensuring that you have git installed. 
    The links to download these are below:  
        Git: https://git-scm.com/downloads
        Docker Desktop: https://www.docker.com/products/docker-desktop
        GitHub Desktop: https://desktop.github.com/
    Here are links to the already existing dev guides, though they are not very detailed:
        Getting Started on Linux/MacOS: https://github.com/YACS-RCOS/yacs.n/blob/master/docs/dev-on-mac-and-linux.md
        Getting Started on Windows: https://github.com/YACS-RCOS/yacs.n/blob/master/docs/dev-on-windows.md

Now that you have the necessary software installed, you should make sure you are able to 
    actually use it. 
    Begin by cloning the repository to your local machine. 
        Enter the folder you would like to have the repo in and enter the command: 
            git clone https://github.com/YACS-RCOS/yacs.n.git
        This should give you a clone of the master branch in your local repository.
        If this does not work, then see the Software Issues section for help on setting
        up git.

    Next, make sure you can run this repository via docker. Use the following commands:
        docker-compose -f docker-compose.yml -f docker-compose.development.yml build
        docker-compose -f docker-compose.yml -f docker-compose.development.yml up
    After doing this, you should be able to open up docker desktop and run YACS locally.
        If this does not work or you are given any errors after using these command lines, 
            see the Software Issues section for help.
    

# Software Issues
If a useful link is not listed below for the issue you are having, try to find one on your 
    own or with the help of a mentor/professor and place the link in this file for others 
    who may end up with the same problem. 

List of known problems:
    WSL 1 running instead of WSL 2 and causing issues. To fix this follow the guide in the 
        Docker Troubleshooting section on how to ugrade to WSL 2. If this does not work
        you may also have to update Ubuntu to the correct version.

Git Troubleshooting
    If you are having any issues getting git up and running, refer to the following:
        https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
        https://www.simplilearn.com/tutorials/git-tutorial/git-installation-on-windows (windows)
        https://www.youtube.com/watch?v=sJ4zr0a4GAs (mac)
    If it is installed but it is not working as it should, you probably have a relatively specific
        issue. If a link is not listed below that helps try searching up the specific error message
            https://www.geeksforgeeks.org/common-git-problems-and-their-fixes/
            https://www.gitkraken.com/learn/git/problems

Docker Troubleshooting
    If you are getting errors with Docker and WSL interaction, try the following links:
        https://docs.microsoft.com/en-us/windows/wsl/install-win10
        https://docs.microsoft.com/en-us/windows/wsl/troubleshooting
        https://alessio.franceschelli.me/posts/windows/wsl2-upgrade/
    If you are having strictly Docker issues, try the following:
        https://docs.docker.com/docker-for-windows/troubleshoot/
        https://docs.docker.com/docker-for-windows/

Remember to add any issues you run into, as well as their solutions, to this document.

# How to Begin
When you first start working on YACS, it may appear overwhelming if you have not worked on
    websites before. The first thing you should do is decide if you want to work on front 
    end or back end issues. From here you can look through the issues listed on the github
    (https://github.com/YACS-RCOS/yacs.n/issues) and decide what seems appropiately 
    challenging. It is recomended that you begin with issues that have the tag for 
    "good first issue" or "feature request", as these types of issues tend to be less
    complicated.

Much of YACS is coded in Vue Javascript. If you are not familiar with vue.js, the first 
    thing you need to do is learn it. It is relatively similar to React and Vanilla JS,
    so if you have experience in those languages you should not have much issues.
    Here are some links for helpful videos for learning the basics:
        https://www.youtube.com/watch?v=qZXt1Aom3Cs
        https://www.youtube.com/watch?v=4deVCNJq3qc
    Documentation/Cheatsheets:
        https://vuejs.org/v2/guide/
        https://www.tutorialspoint.com/vuejs/index.htm

If you are working on the backend, there are a lot of Python Libraries you may be unfamiliar with,
    such as BeautifulSoup, Regex, Flask, and Pandas. These are all relatively complicated and so
    here are links to helpful documentation for each of them.
        BeautifulSoup: 
            https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        Regex: 
            https://docs.python.org/3/howto/regex.html
        Flask: 
            https://flask.palletsprojects.com/
        Pandas: 
            https://pandas.pydata.org/docs/

If you are having any issues or are unsure of what to start with, reach out to the professor,
    a mentor, or one of the more experienced developers for assistance.


# Making Commits
First things first, it is essential to learn how to actually use git itself. It is an extremely
    useful tool that will be of great service far beyond just RCOS. Here are some quality 
    tutorials that I found extremely helpful
        https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners
        https://www.youtube.com/watch?v=8JJ101D3knE
        https://www.youtube.com/watch?v=PQsJR8ci3J0
        https://education.github.com/git-cheat-sheet-education.pdf

Before you go to commit any changes, you must make sure that ALL modifications you have made
    work as intended and do not create any fatal errors. If you end up pushing and Pull Requesting
    something that causes issues, it is not a very good look for your dev team or your github.
    Test all modifications thouruoghly to ensure there are no issues.

If you are using Github Desktop use the following guide for making commits. Otherwise, refer to
    the part directly below this one:
        https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project

When you want to commit the changes you have made, you can use the following commands:
    git checkout -b <name_of_your_branch> 
        //This line creates the branch you will commit
    git status 
        //This line will show you which files have been changed to make sure they 
            are there as you planned
    git commit * 
        OR
    git commit file1.vue file2.vue ....
        //Either of these commands work. Use the first one to commit all file changes and
            the second for specific files
    git status
        //This line will indicate whether or not the changes you wanted actually got committed
    git push --set-upstream origin <name_of_your_branch>
        //This line will put your branch on github
    
After you have done all of these commands, you can make a Pull Request. When you do this,
    you must specify what issue it closes and what your changes speciffically do. If you 
    are unsure about anything, make sure you talk to a professor, one of the mentors, or 
    reach out to a developer who has more experience on YACS. In order for your changes to
    be pulled to the main, 2 people will need to approve them. It is also possible for your
    Pull Request to be denied due to issues with how you resolved the given issue. If this
    happens, figure out what you can do differently and try it again.

# Weekly Status Updates
Use the following template for your weekly status updates. Make sure you do not miss any, as they
    account for a large portion of your grade. This is a YACS specific template, so do not refer to
    it for other projects you may work on.

    # Status Update (2021-02-10)
    Name: [ full name]
    Project: YACS
    ## What I did
    Last week I made yacs better than it was the week prior by doing xyz
    (1-2) paragraphs
    ## Plan for next week
    Make yacs even better by doing xyz
    (1-2) paragraphs
    ## Blockers
    No Blockers
        or
    Can't get [something] to work, went through xyz tutorials/documentation and getting errors xyz that I can't figure out.
    ## Links
    - https://github.com/YACS-RCOS/yacs.n/commit/18a6da62f8d9b999d0f42fa838a0515d9b57d8a0
    - more links to github commits, issues, prs, etc.
