#!/usr/bin/python

"""
I wrote this to cure boredom and to better understand the Luhn algorithm.  This does a validation of numbers
to see if a given number can pass as a valid credit card number.
"""

test_data = "38520000023237"

# The last digit of the number is the checksum
checksum = test_data[-1:]

# Get the rest of the data
data = test_data[0:-1]

# We have to double every even digit from right-to-left, so we reverse the string of digits
data_rev = data[::-1]

print "Testing to see if %s is a valid card number based on mod-10..." % (test_data)
i = 0

val = 0
datastr = ""

# Loop through each digit
while i < len(data_rev):
    # If (i % 2) == 0, we're at an even position in the buffer stream
    if i % 2 == 0:
        # Get the digit at the current spot, then double it
        val = int(data_rev[i])
        val *= 2
        
        # If 'val' is a double-digit, we need to sum up both digits (i.e.: 18 = 1+8 = 9)
        if val >= 10:
            val = str(val)
            val = int(val[0]) + int(val[1])
        else:
            val = val[0]
        
        # Add the new value to the stream
        datastr = "%s%d" % (datastr, str(val))
    else:
        datastr = "%s%s" % (datastr, data_rev[i])
        
    i += 1

i = 0
j = 0

# Now we need to get the sum of all the digits
while i < len(datastr):
    j += int(datastr[i])
    i += 1

# Multiply the total sum by 9, then get the final digit of the product
i = j * 9
i = str(i)
i = i[-1:]

# If the last digit of the product above matches the last digit of the original number, success
if i == checksum:
    print "Success"
else:
    print "Failure"