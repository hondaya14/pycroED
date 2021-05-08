from enum import Enum


class PycroEDConstants(str, Enum):
    config_file_name = 'pycroEDconfig.yaml'


class PycroEDSetting:
    calc_type = ''  # density, potential, both
    is_ed = False  # calculate electron density series
    is_esp = True  # calculate electrostatic potential series
    lattice_vector = []  # ax3, bx3, cx3
    start = []  # x, y, c
    crystal_size = []
    f_obs_file_path = ''  # Fobs hkl file path

    def __init__(self):
        pass
