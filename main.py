import sys
import subprocess

from lib import *


def main():
    # throw quantum calculation job
    gjf_file_name = sys.argv[1]
    file_name = gjf_file_name.split('.')[-2]

    # throw_gaussian_job(gjf_file_name)

    # form chk
    # form_chk(file_name)

    # cubegen
    # generate_cube(file_name)
    density_file_name = file_name + '_density'
    potential_file_name = file_name + '_potential'

    # cubepreprocess
    # cube_preprocessor(density_file_name)
    # cube_preprocessor(potential_file_name)

    # array2mrc
    # array2mrc(density_file_name)
    # array2mrc(potential_file_name)

    # mrcCrystalCreate
    crystal_create(density_file_name)
    crystal_create(potential_file_name)

    # padding
    
    # mrcImageFFT
    # mrcFFTExpression
    # mrc2ascii
    # pickup hkl
    # R factor calculation


if __name__ == "__main__":
    main()
