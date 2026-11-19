"""Read existing counters without incrementing them; keep last known values on failure."""
import concurrent.futures
import datetime
import json
import pathlib
import time
import subprocess

KEYS = ['plays', 'done', 'share', 'message-share', 'story', 'from-challenge', 'subscribe'] + [f'score-{i}' for i in range(11)] + [f'miss-r{i}' for i in range(1, 11)]
DEST = pathlib.Path(__file__).resolve().parents[1] / 'ugaday-vk/stats-data.json'

def read_counter(key):
    url = f'https://abacus.jasoncameron.dev/get/foodhacklab-ugaday-vk/{key}'
    for attempt in range(3):
        try:
            result = subprocess.run(['curl', '-sS', '--max-time', '12', '-w', '\n%{http_code}', url], capture_output=True, text=True, check=True)
            body, status = result.stdout.rsplit('\n', 1)
            if status == '404':
                return 0
            if status != '200':
                raise ValueError(f'HTTP {status}')
            value = json.loads(body)['value']
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError('Invalid counter')
            return value
        except (subprocess.SubprocessError, OSError, ValueError, KeyError):
            pass
        if attempt < 2:
            time.sleep(2 ** attempt)
    return None

def main():
    previous = json.loads(DEST.read_text()) if DEST.exists() else {}
    values = previous.get('values', {})
    timestamps = previous.get('timestamps', {})
    failed = []
    fresh = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = {}
        for key in KEYS:
            futures[pool.submit(read_counter, key)] = key
            time.sleep(.55)
        for future in concurrent.futures.as_completed(futures):
            key = futures[future]
            value = future.result()
            if value is None:
                failed.append(key)
            else:
                values[key] = value
                timestamps[key] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                fresh += 1
            print(f'{key}: {value}', flush=True)
    if not fresh:
        raise RuntimeError('All reads failed; preserve the previous published snapshot')
    payload = dict(namespace='foodhacklab-ugaday-vk', updatedAt=max(timestamps.values()), values=values, timestamps=timestamps, failed=failed)
    DEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
    print(f'Refreshed {fresh}/{len(KEYS)} counters; kept previous values for {failed}')

if __name__ == '__main__':
    main()
