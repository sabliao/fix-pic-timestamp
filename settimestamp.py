import sys

def _set_timestamp():
    return print(sys.argv[1]) #filename

# Check if any arguments beside this python file are given
if len(sys.argv) <= 1:
    print('Need to pass argument')
else:
    # Retrieve file/filename from input/argument (TODO: also accept folder name eventually so can change multiple photos at once)
    # If folder, only grab .jpg(?) files (mainly want to avoid the CR2 files from echow)
    _set_timestamp()

