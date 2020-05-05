#!/usr/bin/env python3

""" just playin with agate"""

import agate
import pandas as pd
from pathlib import Path

SRC_PATH = Path('data', 'wrangled', 'sf-shelter-waitlist.csv')


def main():
    df = pd.read_csv(SRC_PATH, dtype=str)
    counts = df['date'].value_counts().sort_index()
    # just get first 10 rows and last 10 rows
    counts = pd.concat([counts.head(10), pd.Series({'...': None}, name='date'), counts.tail(10)])
    vals =  [[k, v] for k, v in counts.to_dict().items()] # is there really no way to convert a Pandas series to list-of-lists?
    table = agate.Table(vals, ['date', 'count'], [agate.Text(), agate.Number()])
    table.print_bars('date', 'count')

if __name__ == '__main__':
    main()
