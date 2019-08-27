import time
import re
import sys
import subprocess


RATE_UNITS = ['B/s', 'kB/s', 'MB/s', 'GB/s']

SIZE_UNITS = ['B', 'kB', 'MB', 'GB']

def humanize(rate_b, units=RATE_UNITS):
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

    return [
        '%.2f %s' % (rate, unit) for rate, unit in zip(rates, units[:len(rates)])
    ]


def _run(pid):
    proc = subprocess.Popen(['pmap', '-x', pid], stdout=subprocess.PIPE)
    lines = proc.stdout.read().strip().splitlines()
    proc.wait()
    summary_line = lines[-1]
    m = re.match('total kB\s+(\d+)\s+(\d+)\s+', summary_line)
    if m:
        size_kbytes = float(m.group(2))
        return size_kbytes * 1024.
    else:
        return 0


def main(pid, sampling_interval_sec):
    prev_size_bytes = 0

    start = time.time()
    while True:
        size_bytes = _run(pid)

        delta_bytes = size_bytes - prev_size_bytes
        rate = delta_bytes / sampling_interval_sec

        prev_size_bytes = size_bytes

        print('\t'.join(
            ['%.2f' % (time.time() - start)] +
            humanize(rate, RATE_UNITS) +
            [humanize(size_bytes, SIZE_UNITS)[-1]]
        ))
        time.sleep(sampling_interval_sec)


if __name__ == '__main__':
    pid = sys.argv[1]
    try:
        main(pid, 1.0)
    except KeyboardInterrupt:
        print('Exiting...')
        sys.exit(0)