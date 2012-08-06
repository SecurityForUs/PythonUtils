# File and folder operations
import os

# Needed system information
import sys

import stat

# File handling
import io

"""
    asblocks()
    Credit: https://github.com/softlayer/softlayer-object-storage-backup/blob/master/slbackup.py
    
    Gets 'buflen' bytes amount of data from a given file (_f).  Data is stored only on request, then freed from memory.
"""
def asblocks(_f, buflen=1024):
    # Defined so 'data' is not being redefined numerous times in a call
    data = ""
    
    while True:
        data = _f.read(buflen)
        
        if data:
            yield data
        else:
            break

"""
    FileSplit()
    Splits a file into parts (up to max_size) if the filesize is >= cap_size (default: 5GB).
    
    fn       - The file to split
    max_size - The maximum size of each part (default: 2GB)
    
    Returns filename(s) of files to upload
"""
def FileSplit(fn, max_size = 2147483648):
    # We only do this if fn is bigger than cap_size (5 GB)
    cap_size = 5368709120
    
    # If we already have a file handler, read the data and close
    if isinstance(fn, file):
        data = fn.read()
        fn.close()
    else:
        # No file handler, so open it, read data and then close it
        fp = open(fn, 'rb')
        data = '' . join(asblocks(fp))
        fp.close()
    
    # Get how many bytes were read
    bytes = len(data)
    
    # If we didn't go over our filesize limit, no work needs to be done, return filename
    if bytes < cap_size:
        return [fn]
    
    # Holds a list of all the files we will be creating so we can upload them
    files = []

    # Always start our list off at <file>.00001
    id = 1

    # How many different files we will have to be writing
    chunks = bytes / max_size
    
    # If there's still a bit of bytes left unaccounted for, add another chunk to the list
    if (bytes % chunks):
        chunks += 1
    
    # So we aren't constantly creating a variable
    name = ""
    
    # pos = current position in buffer, going from 0 - bytes, in max_size steps
    for pos in xrange(0, bytes, max_size):
        # Filename: <filename>.<00000>-<99999>
        name = "%s.%s" % (fn, format(id, "05d"))
        
        # Add the new name to the list
        files.append(name)
        
        # Open the file for writing, write the amount of data, then close the file
        fp = open(name, 'wb')
        fp.write(data[pos:pos+max_size])
        fp.close()
        
        # Increment the id number accordingly
        id += 1
    
    # Return all the files created
    return files
