import sys, os, platform, time, re, datetime

def _set_timestamp(filename, path):
    # check for file pattern
    jason_pattern= re.compile("(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})\.jpg") # jason's file pattern
    match = jason_pattern.match(filename)
    if match:
        # It's a pic by Jason
        # Turn components of date into epoch time to set on the last modified datetime field
        # must convert strings to numbers for datetime
        time_components = {
            'year': int(match.group(1)),
            'mon': int(match.group(2)),
            'day': int(match.group(3)),
            'hr': int(match.group(4)),
            'min': int(match.group(5)),
            'sec': int(match.group(6))
        }
        # datetime.datetime takes: year, month, day, hr, min, sec; timetuple() returns a struct_time to pass to time.mktime()
        struct = datetime.datetime(time_components['year'], time_components['mon'], time_components['day'],
            time_components['hr'], time_components['min'], time_components['sec']).timetuple()
        print(time.strftime("Before: %m/%d/%Y %I:%M:%S %p", time.localtime(os.stat(path).st_mtime)))
        os.utime(path, (os.stat(path).st_atime, time.mktime(struct)))
        print(time.strftime("After: %m/%d/%Y %I:%M:%S %p", time.localtime(os.stat(path).st_mtime)))
    return

# STARTS HERE
# Check if any arguments beside this python file are given
if len(sys.argv) <= 1:
    print('Need to pass argument')
else:
    path = sys.argv[1]
    (dirname, filename) = os.path.split(os.path.expanduser(path))
    print(dirname, filename)
    if filename:
        if os.path.isfile(path):
            _set_timestamp(filename, path)
    elif dirname and os.path.isdir(dirname):
        # this is for when we pass a folder name for the argument (have to end w/ a '/' or else split thinks last part is filename)
        # only grab .jpg(?) files (mainly want to avoid the CR2 files from echow)
        for root, dirs, files in os.walk(dirname):
            for file in files:
                if file.endswith(".jpg"):
                    # 'root' is the dirname path + whichever subfolder we might be walking through
                    _set_timestamp(file, os.path.join(root, file))

