#!/usr/bin/env python3

from collections import defaultdict
import csv
from pathlib import Path
import re
from sys import stderr

SRC_DIR = Path('data', 'collected')
DEST_PATH = Path('data', 'wrangled', 'sf-shelter-waitlist.csv')

WRANGLE_HEADERS = ('date', 'position', 'seniority_number', 'birthdate',
                    'changes_id', 'serial_number', 'instructions', 'datetime_collected')


def glob_srcpaths():
    """
    in the (unexpected) situation that there is more than 1 file per date, this
    filters for the latest file of that date
    """

    ddict = {}
    for path in sorted(SRC_DIR.glob('*.csv')):
        dt = re.match(r'(\d{4}-\d{2}-\d{2})', path.name).groups()[0]
        if ddict.get(dt):
            stderr.write(f'WARNING: Multiple files for date: {dt}: {ddict[dt]} and {path}')
        ddict[dt] = path
    return sorted(ddict.values())


def process_file(srcpath):
    dt = re.match(r'(\d{4}-\d{2}-\d{2})_(\d{2})', srcpath.name).groups()
    srcdt = f'{dt[0]} {dt[1]}:00'
    outdata = []
    for row in csv.DictReader(srcpath.open()):
        bmt, bdy, byr = row['DOB'].split('-')
        d = {
            'date': dt[0],
            'position': row['Position'],
            'seniority_number': row['Seniority Number'],
            'birthdate': f'{byr}-{bmt}-{bdy}',
            'changes_id': row['CHANGES ID'],
            'serial_number': row['SR #'],
            'instructions': row['Instructions'],
            'datetime_collected': srcdt,

        }
        outdata.append(d)
    return outdata

def main():
    DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
    with open(DEST_PATH, 'w') as dest:
        outs = csv.DictWriter(dest, fieldnames=WRANGLE_HEADERS)
        outs.writeheader()
        for srcpath in glob_srcpaths():
            outs.writerows(process_file(srcpath))

    stderr.write(f'Wrote {DEST_PATH.stat().st_size} bytes to: {DEST_PATH}\n')


if __name__ == '__main__':
    main()
