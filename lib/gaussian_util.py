import subprocess
from .util import *


def form_chk(file_name):
    if file_exist(file_name + '.fchk'): return
    form_check_command = ['formchk', file_name + '.chk', file_name + '.fchk']
    print(' '.join(form_check_command))
    subprocess.call(form_check_command)
    print('')


def generate_cube(file_name, params, calc_type):
    if file_exist(file_name + '_' + calc_type + '.cube'): return
    # generate cube file (3D: cube_file_size^3)
    cube_file_size = params.cube_size

    generate_density_cube_command = \
        ['cubegen', '0', calc_type, file_name+'.fchk', file_name + '_' + calc_type + '.cube', str(cube_file_size)]
    print(' '.join(generate_density_cube_command))
    subprocess.call(generate_density_cube_command)
    print('')

