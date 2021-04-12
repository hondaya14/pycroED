from .util import *


def throw_gaussian_job(gjf_file_name):
    print('\nGaussian job start:' + '\t' + current_time())
    try:
        if gjf_file_name.split('.')[-1] != 'gjf':
            print('Invalid file format. Specify gjf file.')
            exit(1)
    except IndexError:
        print('type gaussian job file')
        exit(1)
    
    # subprocess.call(['g16', gjf_file_name])
    print('Gaussian job end:' + '\t' + current_time() + '\n')

    file_name = gjf_file_name.split('.')[-2]
    if not is_normal_termination(file_name):
        print('Gaussian job failed.')
        exit(1)


def is_normal_termination(file_name):
    out = subprocess.run(['tail', '-1', file_name+'.log'], stdout=subprocess.PIPE)
    result = ' '.join(out.stdout.decode().split()[:2])
    if result == 'Normal termination':
        return True
    else:
        return False
