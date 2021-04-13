import subprocess


def array2mrc(file_name):
    result = subprocess.run(['head', '-6', file_name+'.cube'], stdout=subprocess.PIPE).stdout.decode()
    lines = result.split('\n')
    x_length = str(bohr2angstrom(float(lines[3].split()[1])))
    y_length = str(bohr2angstrom(float(lines[4].split()[2])))
    z_length = str(bohr2angstrom(float(lines[5].split()[3])))
    array2mrc_command = \
        ['array2mrc', '-i', file_name+'.pcube', '-o', file_name+'.mrc', '-mm', '2',
         '-lm3', x_length, y_length, z_length]
    print(' '.join(array2mrc_command))
    subprocess.call(array2mrc_command)
    print('')


def bohr2angstrom(bohr):
    return bohr * 0.529177249


def crystal_create(file_name):
    # acetaminophen parameter
    lattice_vector_a = [7.1178, 0, 0]
    lattice_vector_b = [0, 9.6265, 0]
    lattice_vector_c = [-1.39567, 0, 11.81314]

    start = [0, 0, 0]

    crystal_size_x = 5
    crystal_size_y = 5
    crystal_size_z = 5
    mrc_image_crystal_create_command = \
        ['mrcImageCrystalCreate', '-i', file_name+'.mrc', '-o', file_name+'_crystal.mrc',
         '-A', str(lattice_vector_a[0]), str(lattice_vector_a[1]), str(lattice_vector_a[2]),
         '-B', str(lattice_vector_b[0]), str(lattice_vector_b[1]), str(lattice_vector_b[2]),
         '-C', str(lattice_vector_c[0]), str(lattice_vector_c[1]), str(lattice_vector_c[2]),
         '-start', ' '.join(map(str, start)),
         '-nx', str(crystal_size_x), '-ny', str(crystal_size_y), '-nz', str(crystal_size_z)]
    print(' '.join(mrc_image_crystal_create_command))
    subprocess.call(mrc_image_crystal_create_command)
    print(' ')
