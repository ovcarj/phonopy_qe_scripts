##!/bin/bash

dirnames=$(ls -d batch_*/)
bash_script_name=$1

for dirname in $dirnames
do
        cd $dirname
        source $bash_script_name
        cd ..
done
