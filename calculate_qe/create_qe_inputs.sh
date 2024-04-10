#!/bin/bash

structure_filename=$1

echo "--------"
echo "Creating a single-point SCF input for $structure_filename..."

cp header_pw.in pwscf.in

python get_pw_structure.py $structure_filename

cat structure_pw.dat >> pwscf.in

echo "SCF input created!"

echo "Creating a band structure SCF input for $structure_filename..."

cp header_pw.in pwbands.in
sed -i s/'scf'/'bands'/ pwbands.in
sed -i -n '/K_POINTS/q;p' pwbands.in

cat structure_pw.dat >> pwbands.in

python get_pw_kpath.py $structure_filename

cat kpath.dat >> pwbands.in

echo "Band structure input created!"

echo "Creating a pp_bands.in input for $structure_filename..."

prefix=$(grep "prefix" header_pw.in | cut -d "'" -f 2)

cat <<EOT > pp_bands.in
&bands
   prefix  = 'out/$prefix',
   lsym = .FALSE.,
   filband = '$prefix-bands.dat',
/
EOT

echo "pp_bands.in created!"

echo "Creating a projwfc.in input for $structure_filename..."

cat <<EOT > projwfc.in
&PROJWFC
    prefix= $prefix,
    outdir= './out'
    filpdos= 'pdos.dat'
/
EOT

echo "projwfc.in created!"

echo "Finished creating inputs for $structure_filename!"
echo "--------"
