# duetmonitor
Tools to remotely monitor and control 3D printer with a Duet-based control board. These expect to be placed in your $PATH; I recommend putting them in ~/bin/ on a machine running Octoprint.

These scripts source ~/.duet to get the IP address of the printer; this will be used for any global configuration going forward.

The currently checked-in scripts are my initial tests/monitoring tools and are very basic. I plan to expand on them going forward.

dls - lists files on the Duet. Can differentiate between files and folders, prints out file sizes and indicates folders with /. Can handle files/paths with spaces.

ledon/ledoff - my printer has LEDs hooked up to a fan header. This turns the LEDs on or off. This will likely be merged into a seperate tool shortly.

printcontol - functionally similar to a service start/stop script. Can pause/resume/cancel a print and set LEDs to on/off/50%.

printmonitor - "Daemon" in the form of a looping script. Calls handle_printing for all the interesting stuff.

printstatus - Logs status, but different status than printmonitor.


I'm working on making this a more complete suite - I'd like to execute macros direct off the Duet via CLI, manage files, have persistient logs of print statistics, and add some form of timelapse feature.
