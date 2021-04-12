import subprocess


def form_chk(file_name):
    print('formchk file_name' + '.chk' + file_name + 'fchk')
    subprocess.call(['formchk', file_name + '.chk', file_name + 'fchk'])
    print('')


def generate_cube(input_file):
    pass