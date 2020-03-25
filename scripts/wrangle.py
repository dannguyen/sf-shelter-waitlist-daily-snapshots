#!/usr/bin/env python3

import csv
from pathlib import Path
import re
from sys import stderr

SRC_DIR = Path('data', 'collected')
DEST_PATH = Path('data', 'wrangled', 'sf-shelter-waitlist.csv')

WRANGLE_HEADERS = ('datetime', 'position', 'seniority_number', 'birthdate',
                    'changes_id', 'serial_number', 'instructions',)


def _glob_srcpaths():
    return sorted(SRC_DIR.glob('*.csv'))

def process_file(srcpath):
    dt = re.match(r'(\d{4}-\d{2}-\d{2})_(\d{2})', srcpath.name).groups()
    srcdt = f'{dt[0]} {dt[1]}:00'
    outdata = []
    for row in csv.DictReader(srcpath.open()):
        bmt, bdy, byr = row['DOB'].split('-')
        d = {
            'datetime': srcdt,
            'position': row['Position'],
            'seniority_number': row['Seniority Number'],
            'birthdate': f'{byr}-{bmt}-{bdy}',
            'changes_id': row['CHANGES ID'],
            'serial_number': row['SR #'],
            'instructions': row['Instructions'],
        }
        outdata.append(d)
    return outdata

def main():
    DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
    with open(DEST_PATH, 'w') as dest:
        outs = csv.DictWriter(dest, fieldnames=WRANGLE_HEADERS)
        outs.writeheader()
        for srcpath in _glob_srcpaths():
            outs.writerows(process_file(srcpath))

    stderr.write(f'Wrote {DEST_PATH.stat().st_size} bytes to: {DEST_PATH}\n')


if __name__ == '__main__':
    main()
