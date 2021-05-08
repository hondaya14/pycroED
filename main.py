import sys

from lib import *

# Description
# Input file
#     - gjf (gaussian input file)
#
# Output file
#     gaussian out put
#     - log, chk, fchk, cube
#     - pcube (processed cube) : Processed file
#     - mrc, pad, fft, amp, ampascii
#     - hkl
#     - result.txt (R factor)


def main():
    # setting config
    params = setting_params()

    # throw quantum calculation job
    gjf_file_name = sys.argv[1]
    file_name = gjf_file_name.split('.')[-2]
    throw_gaussian_job(gjf_file_name)

    # form chk
    form_chk(file_name)

    # cubegen
    # generate_cube(file_name)
    density_file_name = file_name + '_density'
    potential_file_name = file_name + '_potential'

    # cubepreprocess
    cube_preprocessor(density_file_name)
    cube_preprocessor(potential_file_name)

    # array2mrc
    array2mrc(density_file_name)
    array2mrc(potential_file_name)

    # cut unit cell from cube
    cut_unitcell_from_cube(density_file_name, params)
    cut_unitcell_from_cube(potential_file_name, params)

    # mrcCrystalCreate
    crystal_create(density_file_name, params)
    crystal_create(potential_file_name, params)

    # scope crystal file
    density_file_name = density_file_name + '_crystal'
    potential_file_name = potential_file_name + '_crystal'

    # padding
    padding_image(density_file_name)
    padding_image(potential_file_name)

    # mrcImageFFT
    fft(density_file_name)
    fft(potential_file_name)

    # mrcFFTExpression
    fft_expression(density_file_name)
    fft_expression(potential_file_name)

    # mrc2ascii
    mrc2ascii(density_file_name)
    mrc2ascii(potential_file_name)

    # pickup hkl
    pick_up_hkl(params.f_obs_file_path, density_file_name)
    pick_up_hkl(params.f_obs_file_path, potential_file_name)

    # R factor calculation
    calculate_r_factor(params.f_obs_file_path, density_file_name)
    calculate_r_factor(params.f_obs_file_path, potential_file_name)


def setup():
    if not file_exist(PycroEDConstants.config_file_name):
        pycroED_path = '/'.join(sys.argv[0].split('/')[:-1]) + '/'
        cp_config_command = ['cp', pycroED_path + PycroEDConstants.config_file_name, './']
        subprocess.call(cp_config_command)
        print('Finish set up')
        exit(0)
    else:
        print('Already set up.')
        exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage:\tpycroED [gjf file]\t-execute calculation\n\tpycroED setup\t\t-setup for calculation")
    else:
        if str(sys.argv[1]) == 'setup':
            setup()
        if file_exist(PycroEDConstants.config_file_name):
            main()
        else:
            print("Please setup : %pycroED setup\nAfter generating pycroEDconfig.yaml, modify its param as appropriate.")
