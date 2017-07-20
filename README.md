# duetmonitor
Monitor and log print data with a Rasberry Pi; this logs basic print information to CSV. The script will detect prints starting,  start polling more frequently and take photos for a timelapse.

To install check out duetmonitor and install the scripts in your $PATH; I recommend ~/bin/. Update ``config``  and copy it to ~/.duet. Options are documented in the config file. 

Once configured run ``printmonitor`` and start a print. The script will output "Detected new print at [date of print starting]". This triggers taking photos for timelapse and creates a CSV with print data. Print data is currently limited to Layer, Bed Temp, Bed Target, Head Temp, Head Target, and Percent Complete but will be expanded.

Photos for timelapses are stored in ~/pics/ by default and are named [date-print-started]-[number].jpg. These should be automatically converted to a video when the print is done; the video will be stored in the directory configured in ``config``.

``dls`` - lists files on the Duet. Can differentiate between files and folders, prints out file sizes and indicates folders with /. Can handle files/paths with spaces. 

``ledon``/``ledoff`` - Turn LEDs on or off via CLI.

``printcontol`` - Similar to a service start/stop script. Can pause/resume/cancel a print and set LEDs to on/off/50%.

``printmonitor`` - Monitoring daemon

``functions`` - Stores functions used by other scripts

``handle_print`` - Called by ``printmonitor`` to do specific print-related tasks.

Bugs:

* May interfere with Duet Web GUI while polling

Required software:
``avconv``
