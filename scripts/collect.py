#!/usr/bin/env python3


import requests
from pathlib import Path
from datetime import datetime
from sys import stdout

SRC_URL = 'https://data.sfgov.org/api/views/w4sk-nq57/rows.csv?accessType=DOWNLOAD'
DEST_DIR = Path('data', 'collected')

def main():
    DEST_DIR.mkdir(exist_ok=True, parents=True)
    resp = requests.get(SRC_URL)
    fname = DEST_DIR.joinpath(f'{datetime.now().strftime("%Y-%m-%d_%H")}.csv')
    with open(fname, 'w') as f:
        f.write(resp.text)
        stdout.write(f"Wrote {len(resp.text)} chars to {fname}\n")


if __name__ == '__main__':
    main()
