import glob

all_files = glob.glob('disp*')
all_files.sort()

print('#!/bin/bash')
print('')
print('phonopy -f ', end='')

for disp in all_files:
    print(f'{disp}/pwscf.out ', end='')
