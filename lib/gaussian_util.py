import subprocess


def form_chk(file_name):
    form_check_command = ['formchk', file_name + '.chk', file_name + '.fchk']
    print(' '.join(form_check_command))
    subprocess.call(form_check_command)
    print('')


def generate_cube(file_name):
    # generate cube file (3D: cube_file_size^3)
    cube_file_size = 100
    generate_density_cube_command = \
        ['cubegen', '0', 'density', file_name+'.fchk', file_name+'_density.cube', str(cube_file_size)]
    print(' '.join(generate_density_cube_command))
    subprocess.call(generate_density_cube_command)
    print('')

    generate_potential_cube_command = \
        ['cubegen', '0', 'potential', file_name+'.fchk', file_name+'_potential.cube', str(cube_file_size)]
    print(' '.join(generate_potential_cube_command))
    subprocess.call(generate_potential_cube_command)
    print('')
