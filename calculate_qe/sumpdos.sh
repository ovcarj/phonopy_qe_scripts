#!/bin/bash

ntyp=$(grep ntyp pwscf.in | cut -d "=" -f 2)
species=$(grep ATOMIC_SPECIES pwscf.in -A$ntyp | tail -n $ntyp | awk '{print $1}')

for sp in $species;
do
        ls pdos.dat.pdos_atm#*$sp* > files_pdos_$sp.dat
        sumpdos.x -f files_pdos_$sp.dat > summed_pdos_$sp.dat
done
