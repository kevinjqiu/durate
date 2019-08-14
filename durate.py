import time
import subprocess


def get_rate_display(rate_b):
    rate_units = ['B/s', 'kB/s', 'MB/s', 'GB/s']

    rates = [rate_b]
    rate_kb = rate_b / 1024.
    if rate_kb > 1:
        rates.append(rate_kb)

        rate_mb = rate_kb / 1024.
        if rate_mb > 1:
            rates.append(rate_mb)

            rate_gb = rate_mb / 1024.
            if rate_gb > 1:
                rates.append(rate_gb)

    return '\t'.join([
        '{} {}'.format(rate, unit) for rate, unit in zip(rates, rate_units[:len(rates)])
    ])


def main(dir_, sampling_interval_sec):
    prev_size_bytes = 0

    while True:
        res = subprocess.check_output(['du', '-s', dir_])
        size_bytes, *_ = res.decode('utf8').split('\t')
        size_bytes = float(size_bytes)

        delta_bytes = size_bytes - prev_size_bytes
        rate = delta_bytes / sampling_interval_sec

        prev_size_bytes = size_bytes

        print(get_rate_display(rate))
        time.sleep(sampling_interval_sec)


if __name__ == '__main__':
    dir_ = '.'
    sampling_interval_sec = 1.0
    main(dir_, sampling_interval_sec)
