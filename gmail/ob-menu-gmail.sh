#!/bin/bash
# Script to generate pipe menu
# Make sure that CACHE_FILE variables are set to the same file in both this script and ob-fetch-gmail.py
# Also make sure that both scripts are in same folder

CACHE_FILE=".ob-cache-gmail"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
COMPLIMENT="ob-fetch-gmail.py"
mailfile="${DIR}/${CACHE_FILE}"

# readlines function
# Reads N lines from input, keeping further lines in the input.
#
# Arguments:
#   $1: number N of lines to read.
#
# Return code:
#   0 if at least one line was read.
#   1 if input is empty.
# Thanks to albarji's answer on a stackoverflow question: http://http://stackoverflow.com/questions/8314499/read-n-lines-at-a-time-using-bash

function readlines () {
    local N="$1"
    local line
    local rc="1"
    # Read at most N lines
    for i in $(seq 1 $N)
    do
        # Try reading a single line
        read line
        if [ $? -eq 0 ]
        then
            # Output line
            echo $line
            rc="0"
        else
            break
        fi
    done

    # Return 1 if no lines where read
    return $rc
}
# End of readlines function

read -r UNREAD<$mailfile
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
echo "<openbox_pipe_menu>"
echo "<separator label=\"$UNREAD\"/>"
echo "<item label=\"Go to Inbox\">
       <action name=\"Execute\"><command>xdg-open https://gmail.com</command></action>
       </item>
       <separator/>"

sed 1d $mailfile|while mail=$(readlines 2) # skipping first line
do

    echo "<item label=\"$mail\"/>"
done
echo "<separator/>
    <item label=\"Refresh Inbox\">
    <action name=\"Execute\"><command>$DIR/$COMPLIMENT</command></action>
    </item>"
echo "</openbox_pipe_menu>"
