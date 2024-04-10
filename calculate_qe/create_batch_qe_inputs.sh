#/bin/bash

structures_names="MPOSCAR-*"
structure_filenames=$(ls $structures_names)

for structure_filename in $structure_filenames 
do
        dirname="batch_$structure_filename"

        echo "Creating QE inputs in $dirname..."
        
        mkdir -p $dirname

        cp $structure_filename create_qe_inputs.sh get_pw_kpath.py get_pw_structure.py header_pw.in sub* plot_bands.py $dirname

        cd $dirname
        bash create_qe_inputs.sh $structure_filename
        cd ..

done
