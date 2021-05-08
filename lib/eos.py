import subprocess
from .util import *


def array2mrc(file_name):
    if file_exist(file_name + '.mrc'): return
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
    print()


def bohr2angstrom(bohr):
    return bohr * 0.5291772083


def cut_unitcell_from_cube(file_name, params):
    if file_exist(file_name + '_unitcell.mrc'): return
    # acetaminophen parameter
    lattice_vector_a = params.lattice_vector[0]
    lattice_vector_b = params.lattice_vector[1]
    lattice_vector_c = params.lattice_vector[2]

    start = params.start
    crystal_size_x, crystal_size_y, crystal_size_z = 1, 1, 1

    mrc_image_crystal_create_command = \
        ['mrcImageCrystalCreate', '-i', file_name + '.mrc', '-o', file_name + '_unitcell.mrc',
         '-A', str(lattice_vector_a[0]), str(lattice_vector_a[1]), str(lattice_vector_a[2]),
         '-B', str(lattice_vector_b[0]), str(lattice_vector_b[1]), str(lattice_vector_b[2]),
         '-C', str(lattice_vector_c[0]), str(lattice_vector_c[1]), str(lattice_vector_c[2]),
         '-start', str(start[0]), str(start[1]), str(start[2]),
         '-nx', str(crystal_size_x), '-ny', str(crystal_size_y), '-nz', str(crystal_size_z)]
    print(' '.join(mrc_image_crystal_create_command))
    subprocess.call(mrc_image_crystal_create_command)
    print()


def crystal_create(file_name, params):
    if file_exist(file_name + '_crystal.mrc'): return
    # acetaminophen parameter
    lattice_vector_a = params.lattice_vector[0]
    lattice_vector_b = params.lattice_vector[1]
    lattice_vector_c = params.lattice_vector[2]

    start = params.start

    crystal_size_x, crystal_size_y, crystal_size_z = 9, 6, 5

    mrc_image_crystal_create_command = \
        ['mrcImageCrystalCreate', '-i', file_name+'.mrc', '-o', file_name+'_crystal.mrc',
         '-A', str(lattice_vector_a[0]), str(lattice_vector_a[1]), str(lattice_vector_a[2]),
         '-B', str(lattice_vector_b[0]), str(lattice_vector_b[1]), str(lattice_vector_b[2]),
         '-C', str(lattice_vector_c[0]), str(lattice_vector_c[1]), str(lattice_vector_c[2]),
         '-start', str(start[0]), str(start[1]), str(start[2]),
         '-nx', str(crystal_size_x), '-ny', str(crystal_size_y), '-nz', str(crystal_size_z)]
    print(' '.join(mrc_image_crystal_create_command))
    subprocess.call(mrc_image_crystal_create_command)
    print()


def padding_image(file_name):
    # TODO: Default params x3 original image
    result = subprocess.run(['mrcInfo', '-i', file_name + '.mrc'], stdout=subprocess.PIPE).stdout.decode()
    nx = 500
    ny = 500
    nz = 500
    mrc_image_3d_pad_command = \
        ['mrcImage3DPad', '-i', file_name+'.mrc', '-o', file_name+'.pad',
         '-Nx', nx, '-Ny', ny, '-Nz', nz, '-M', '3', '-m', '1']
    print(' '.join(mrc_image_3d_pad_command))
    subprocess.call(mrc_image_3d_pad_command)
    print()


def fft(file_name):
    if file_exist(file_name + '.fft'): return
    mrc_image_fft_command = ['mrcImageFFT', '-i', file_name+'.mrc', '-o', file_name+'.fft']
    print(' '.join(mrc_image_fft_command))
    subprocess.call(mrc_image_fft_command)
    print()


def fft_expression(file_name):
    if file_exist(file_name + '.amp'): return
    mrc_fft_expression_command = ['mrcFFTExpression', '-i', file_name+'.fft', '-o', file_name+'.amp',
                                  '-m', '0']
    print(' '.join(mrc_fft_expression_command))
    subprocess.call(mrc_fft_expression_command)
    print()


def mrc2ascii(file_name):
    if file_exist(file_name + '.ampascii'): return
    mrc2ascii_command = ['mrc2ascii', '-i', file_name+'.amp', '-o', file_name+'.ampascii']
    print(' '.join(mrc2ascii_command))
    subprocess.call(mrc2ascii_command)
    print()
