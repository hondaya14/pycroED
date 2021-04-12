import subprocess


def current_time():
    time = subprocess.run(['date'], stdout=subprocess.PIPE).stdout.decode().replace('\n', '')
    return time
