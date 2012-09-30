#!/usr/bin/python

"""
I wrote this to cure boredom and to better understand the Luhn algorithm.  This does a validation of numbers
to see if a given number can pass as a valid credit card number.
"""

test_data = "38520000023237"

checksum = test_data[-1:]
data = test_data[0:-1]
data_rev = data[::-1]

print "Testing to see if %s is a valid card number based on mod-10..." % (test_data)
i = 0

val = 0
datastr = ""

while i < len(data_rev):
    if i % 2 == 0:
        val = int(data_rev[i])
        val *= 2
        val = str(val)
        
        if len(val) == 2:
            val = int(val[0]) + int(val[1])
        else:
            val = int(val[0])
            
        datastr = "%s%s" % (datastr, str(val))
    else:
        datastr = "%s%s" % (datastr, data_rev[i])
        
    i += 1

i = 0
j = 0

while i < len(datastr):
    j += int(datastr[i])
    i += 1

i = j * 9
i = str(i)
i = i[-1:]

if i == checksum:
    print "Success"
else:
    print "Failure"