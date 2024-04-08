#!/bin/bash

supercell_files=$(ls supercell*-*in)

for f in $supercell_files;
do
        number=$(echo $f | cut -d "-" -f 2 | cut -d "." -f 1)
        mkdir "disp-$number" 

        cp $f "disp-$number"
        cp sub.sh "disp-$number"

        cd "disp-$number"       
        sed -i -e "1d" $f
        cat ../header.in | cat - $f > tmp && mv tmp $f
        mv $f pwscf.in

        sbatch sub.sh

        cd ..
done
