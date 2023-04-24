**!!THIS IS FOR PROJECT MAINTAINERS ONLY!!**

---

# The Server

Direct SSH access to the server is available, use the username and password you were given to sign in like this:

`ssh <username>`[^network]

You will then be prompted for the password, type that in.

You can use `btop` to check the server's status, including current disk and memory usage. If the Github Actions fail, it could be bacause of lack of storage space. Other troubleshooting can also be done from here.

[^network]: You need to be connected to the RPI network (or on the VPN) in order to connect.

# Github Actions

Accessed through the "Actions" tab near the top of the page. To update the production website, run the "Production CD" action, which is configured in `prod-cd.yaml`. It only runs when manually triggered, so stay on top of this! Semester data updates are configured by `prod-update.yaml`.

# Semester Data

Semesters to be updated are listed in the `semester` list in the `matrix` variable, on line 14. This runs the appropriate shell script `scripts/get-<semester name>.sh`. If you need to make a new shell scripts, use the previous ones as references, the format should be very similar.
