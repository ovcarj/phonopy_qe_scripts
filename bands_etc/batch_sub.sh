#!/bin/bash

dirnames=$(ls -d batch_*/)
submission_script_name=$1

for dirname in $dirnames
do
        cd $dirname
        sbatch $submission_script_name
        cd ..
done
