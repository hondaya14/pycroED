import os
import subprocess
import yaml
from .constants import *


def current_time():
    time = subprocess.run(['date'], stdout=subprocess.PIPE).stdout.decode().replace('\n', '')
    return time


def file_exist(file_path):
    return os.path.exists(file_path)


def setting_params():
    params = PycroEDSetting()
    with open(PycroEDConstants.config_file_name, mode='r') as conf:
        obj = yaml.safe_load(conf)
        params.calc_type = obj['calc_type']
        if params.calc_type == 'both':
            params.is_ed = True
            params.is_esp = True
        elif params.calc_type == 'density':
            params.is_ed = True
            params.is_esp = False
        elif params.calc_type == 'potential':
            params.is_ed = False
            params.is_esp = True
        else:
            print('error: invalid calc_typ\nplease modify calc_type { density, potential, both} in pycroEDSetting.yaml')
        params.lattice_vector = [
            obj['lattice_vector']['a'],
            obj['lattice_vector']['b'],
            obj['lattice_vector']['c'],
        ]
        params.start = obj['start']
        params.crystal_size = obj['crystal_size']
        params.f_obs_file_path = obj["f_obs_file_path"]
        if not file_exist(params.f_obs_file_path):
            print('File not exist Fobs.hkl')
            exit(0)
    return params
