import sys, os, platform, time, re
from datetime import datetime

def _get_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def _set_timestamp(path):
    # check for file pattern
    jason_pattern= re.compile("201611(2\d)_(\d{2,2})(\d{2,2})(\d{2,2})\.jpg") # jason's file pattern
    if jason_pattern.match(path):
        # It's a pic by Jason
        print(path)
        # Get the day (1st capture group), hour (2nd capture group), minute (3rd capture group), and millisecond (4th capture group)
        # and turn into unix epoch time to set on the last modified datetime field
    creation_date = _get_creation_date(path) # not needed; just used to see what format the timestamp gets returned in
    # print(time.time()) # to get now time
    # print time.strftime("Before: %m/%d/%Y %I:%M:%S %p",time.localtime(os.stat(path).st_atime))
    # if path == 'README.md':
    #     # creation_date in this example on my linux is actually last-modified time in linux
    #     os.utime(path, (os.stat(path).st_atime, creation_date))
    #     print time.strftime("After: %m/%d/%Y %I:%M:%S %p",time.localtime(os.stat(path).st_atime))
    print(creation_date)
    return

# STARTS HERE
# Check if any arguments beside this python file are given
if len(sys.argv) <= 1:
    print('Need to pass argument')
else:
    # Retrieve file/filename from input/argument (TODO: also accept folder name eventually so can change multiple photos at once)
    # ^-- read: https://docs.python.org/3/tutorial/inputoutput.html
    # If folder, only grab .jpg(?) files (mainly want to avoid the CR2 files from echow)
    _set_timestamp(sys.argv[1])

