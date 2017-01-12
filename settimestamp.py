import sys, os, platform, time, re, datetime
import pprint

def _set_timestamp(filename, path, time_keeper):
    # check for file pattern
    dfan_pattern= re.compile("IMG_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2}).*\.jpg") # dfan's file pattern
    jason_pattern= re.compile("(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})\.jpg") # jason's file pattern
    dfan_match  = dfan_pattern.match(filename)
    jason_match = jason_pattern.match(filename)
    if dfan_match or jason_match:
        if dfan_match:
            print("DFAN'S")
        else:
            print("JASON'S")
        match = dfan_match if dfan_match else jason_match
        # It's a pic by DFan or Jason; both can use similar way of getting timestamp 'fixed'
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
    else:
        pattern= re.compile("IMG_(\d{4})\.jpg", re.I) # eric's file pattern, case-insensitive to account for .JPG too
        match = pattern.match(filename)
        if match:
            print("ERIC'S")
            true_time = os.stat(path).st_mtime + 2*60*60 # add 2 hrs to last modified time (since echow's photos are 2 hrs behind)
            if true_time <= time_keeper['cutoff_time']:
                # update last valid timestamp
                time_keeper['last_valid_timestamp'] = true_time
            print(time.strftime("Before: %m/%d/%Y %I:%M:%S %p", time.localtime(os.stat(path).st_mtime)))
            # set timestamp of file
            os.utime(path, (os.stat(path).st_atime, time_keeper['last_valid_timestamp']))
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
    # time_keeper is just for help w/ processing eric's pics
    # cutoff_time is last minute of Sunday of our trip, Nov 27th, 2016 11:59pm
    time_keeper = {
        'last_valid_timestamp': time.mktime(datetime.datetime(2016, 11, 23, 17, 0, 0).timetuple()),
        'cutoff_time': time.mktime(datetime.datetime(2016, 11, 27, 23, 50, 59).timetuple())
    }
    if filename:
        if os.path.isfile(path):
            _set_timestamp(filename, path, time_keeper) # doesn't really make sense to pass time_keeper here, but doing so to keep code consistent
    elif dirname and os.path.isdir(dirname):
        # this is for when we pass a folder name for the argument (have to end w/ a '/' or else split thinks last part is filename)
        # only grab .jpg(?) files (mainly want to avoid the CR2 files from echow)
        for root, dirs, files in os.walk(dirname):
            for file in files:
                # 'root' is the dirname path + whichever subfolder we might be walking through
                _set_timestamp(file, os.path.join(root, file), time_keeper)

