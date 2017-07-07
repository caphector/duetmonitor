# duetmonitor
Tools to monitor and log print data with a Rasberry Pi. It logs basic print information to CSV. The script will detect prints starting, then start polling more frequently and take photos with a webcam.

To install check out duetmonitor and install the scripts in your $PATH. Edit the config file and copy it to ~/.duet. The config options are documented in the config file. 

Once configured run ``printmonitor`` and start a print. The script will output "Detected new print at [date of print starting]". This triggers taking photos for timelapse and creates a CSV with print data. Print data is currently limited to Layer, Bed Temp, Bed Target, Head Temp, Head Target, and Percent Complete but will be expanded.

Photos for timelapses are stored in ~/pics/ by default and are named [date-print-started]-[number].jpg. Converting these to a video can be done with avconv - this command should do it. ``avconv -r 10 -i ~/pics/[date-print-started]-%4d.JPG -r 10 libx264 -q:v 3  ~/timelapse.mp4``. I plan to add automatic timelapse processing.

``dls`` - lists files on the Duet. Can differentiate between files and folders, prints out file sizes and indicates folders with /. Can handle files/paths with spaces. 

``ledon``/``ledoff`` - Turn LEDs on or off via CLI.

``printcontol`` - Similar to a service start/stop script. Can pause/resume/cancel a print and set LEDs to on/off/50%.

``printmonitor`` - Monitoring daemon

``functions`` - Stores functions used by other scripts

``handle_print`` - Called by ``printmonitor`` to do specific print-related tasks.

Bugs:

* No actions are triggered when prints finish
* Does not handle a connection interruption during a print - it will consider this a new print
* API usage may interfere with Duet Web GUI connectivity since the firmware can only handle one API connection at a time
