import sys
import subprocess

from lib import *


def main():
    # throw quantum calculation job
    gjf_file_name = sys.argv[1]
    file_name = gjf_file_name.split('.')[-2]

    throw_gaussian_job(gjf_file_name)

    # form chk
    form_chk(file_name)

    # cubegen

    # cubepreprocess
    # arra2mrc
    # mrcCrystalCreate
    # padding
    # mrcImageFFT
    # mrcFFTExpression
    # mrc2ascii
    # pickuphkl
    # R factor calculation


if __name__ == "__main__":
    main()
