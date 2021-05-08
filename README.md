# pycroED
This program is refinement tool for microED. pycroED automates Gaussian and Eos commands used in the refinement process.

### Environment
- python 3.6.9
- Gaussian (Quantum calculation software)
- Eos (Image processing software)

### Process flow
1. Throw Gaussian job
2. Result file processing
3. Generate electron density & electrostatic potential cube file
4. Generate mrc file
5. Make crystal
6. Padding
7. FFT
8. Output ascii file
9. Pick up the value at the reciprocal lattice point
10. calculate R factor

### Configuration
in pycroEDSetting.yaml
```yaml
# calculation type
#   - both
#   - density
#   - potential
calc_type       : 'both'

lattice_vector  :
    a : [7.1178, 0, 0]
    b : [0, 9.6265, 0]
    c : [-1.39567, 0, 11.81314]

# start lattice point ( voxel  unit )
#     - Eos: mrcImageCrystalCreate [ -start ]
start           : [14, 11, 9]

# crystal size
#     - Eos: mrcImageCrystalCreate [ -nx, -ny, -nz ]
crystal_size    : [9, 6, 5]
```

### Result
project.txt
```yaml
project               : project file name

gt                    : selection(gt) rule about I
num_of_lat_point_all  : number of all(all) lattice point
num_of_lat_point_gt   : number of select(gt) lattice point
r_factor_all          : R factor - all
r_factor_gt           : R factor - gt
scale_all             : R factor scaling constant s_all ;
                      ( R = Σ ||Fobs| - s_all * |Fcalc|| / Σ ||Fobs| ) 
scale_gt              : R factor scaling constant s_gt  ;
                      ( R = Σ ||Fobs| - s_gt  * |Fcalc|| / Σ ||Fobs| )
```