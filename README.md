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
4. Generate cube mrc file
5. Generate unitcell mrc file
6. Generate crystal mrc file
7. Resize crystal mrc size(x, y, z) to even if odd for fft
8. FFT
9. Expression amplitude
10. Output ascii file
11. Pick up the value at the reciprocal lattice point
12. calculate R factor
13. generate result file <a href="#result_example">(example)</a>

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

#### Determination start voxel
- generate [ project ].mrc ( = cube mrc)
- generate [ project ]_unitcell.mrc ( = unitcell mrc)
- start = (cube - unitcell) / 2

### <p id="result_example">Result</p>
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