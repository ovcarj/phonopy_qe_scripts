#!/bin/bash

dirnames=$(ls -d batch_*/)
python_script_name=$1

for dirname in $dirnames
do
        cd $dirname
        python $python_script_name
        cd ..
done
