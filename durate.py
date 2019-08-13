import time
import subprocess


def main(dir_, sampling_interval_sec):
    prev_size_bytes = 0

    while True:
        res = subprocess.check_output(['du', '-s', dir_])
        size_bytes, *_ = res.decode('utf8').split('\t')
        size_bytes = float(size_bytes)

        delta_bytes = size_bytes - prev_size_bytes
        rate = delta_bytes / sampling_interval_sec
        print(rate)
        prev_size_bytes = size_bytes
        time.sleep(sampling_interval_sec)


if __name__ == '__main__':
    dir_ = '.'
    sampling_interval_sec = 1.0
    main(dir_, sampling_interval_sec)
