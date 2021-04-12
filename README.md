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