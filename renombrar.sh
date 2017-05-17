#!/bin/bash
cd ~/remote/RAID/Downloads/newpctfinished/
rename -v 's/(.*)\/(.*)/$1.avi/;' */*.avi
rename -v 's/(.*)\/(.*)/$1.mkv/;' */*.mkv
#rm -r */
