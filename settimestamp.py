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

def _set_timestamp(filename):
    # check for file pattern
    jason_pattern= re.compile("(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})\.jpg") # jason's file pattern
    match = jason_pattern.match(filename)
    if match:
        # It's a pic by Jason
        # Turn components of date into epoch time to set on the last modified datetime field
        # time.struct_time takes: year, month, day, hr, min, sec, weekday, day in year, is DST
        struct = time.struct_time(tm_year=match.group(1), tm_mon=match.group(2), tm_mday=match.group(3),
            tm_hour=match.group(4), tm_min=match.group(5), tm_sec=match.group(6), tm_isdst=0)
        print(time.mktime(struct))
    # creation_date = _get_creation_date(path) # not needed; just used to see what format the timestamp gets returned in
    # print(time.time()) # to get now time
    # print time.strftime("Before: %m/%d/%Y %I:%M:%S %p",time.localtime(os.stat(path).st_atime))
    # os.utime(path, (os.stat(path).st_atime, creation_date))
    return

# STARTS HERE
# Check if any arguments beside this python file are given
if len(sys.argv) <= 1:
    print('Need to pass argument')
else:
    # Retrieve file/filename from input/argument (TODO: also accept folder name eventually so can change multiple photos at once)
    # ^-- read: https://docs.python.org/3/tutorial/inputoutput.html
    # If folder, only grab .jpg(?) files (mainly want to avoid the CR2 files from echow)
    path = sys.argv[1]
    has_folder_in_path = re.compile("^.*\/*.*\/(.*\..*)$").match(path)
    if has_folder_in_path:
        print(has_folder_in_path.group(1))
        _set_timestamp(has_folder_in_path.group(1))
    else:
        _set_timestamp(path) # pass in path as filename

