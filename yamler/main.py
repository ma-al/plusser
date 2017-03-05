"""Parses CSVs and outputs a YAML."""

import csv
import os
import argparse
from datetime import datetime as dt

import yaml


def parse_arguments():
    """
    Get and parse the program arguments.

    :return: Parsed arguments object
    :rtype: argparse.Namespace
    """
    pars = argparse.ArgumentParser()
    pars.add_argument(
        '-s', '--save', action='store_true', help='Save all output to files')
    pars.add_argument(
        'csv',
        metavar='input_csv',
        type=argparse.FileType('r'),
        help='The CSV file to convert')

    args = pars.parse_args()
    for key, val in vars(args).iteritems():
        print '{:>6} : {}'.format(key, val)

    return args


def verify(data):
    """
    Simple checks on the read CSV data.

    :param list data: List of dictionaries
    """
    for dic in data:
        assert dic['Amount']
        assert dic['Balance']
        assert dic['Entered Date']
        assert dic['Transaction Description']

    print
    print 'Verify OK on {} records'.format(len(data))


def main():
    """Main entry point."""
    args = parse_arguments()

    with args.csv as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    verify(data)

    for idx, val in enumerate(data):
        nd = dt.strptime(val['Entered Date'], '%d/%m/%Y').strftime('%Y-%m-%d')
        new = \
            {
                'SN': idx,
                'Amount': float(val['Amount']),
                'Balance': float(val['Balance']),
                'Notes': [' '.join(val['Transaction Description'].split())],
                'Date': nd
            }
        val.update(new)
        del val['Entered Date']
        del val['Effective Date']
        del val['Transaction Description']

    if not args.save:
        print
        print yaml.dump(data, indent=2, default_flow_style=False)
        return

    path, _ = os.path.splitext(args.csv.name)
    with open(path + '.yaml', 'w') as f:
        yaml.dump(data, f, indent=2, default_flow_style=False)
        print
        print '"{}" saved. Size: {}'.format(f.name, f.tell())


if __name__ == '__main__':
    main()
