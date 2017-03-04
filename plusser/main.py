"""Parses CSVs and sums up a running total."""

from datetime import datetime
import os
import argparse
import tzlocal


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

    print type(args)
    return args


def show(data):
    """
    Unfurl data list and print out.

    :param list data: List of data to show
    """
    print
    for idx, line in enumerate(data):
        print '{:>3} {}'.format(idx, line)


def verify(data):
    """
    Sanity check on read CSV data.

    :param list data: Read data as list of lists
    :return: Same data but with headers removed
    :rtype: list of lists
    """
    headers = data.pop(0)
    expected = ['Date', 'Time', 'Amount', 'Location', 'Notes']
    check = [e for e in expected for h in headers if e == h]
    assert check == expected

    return data


def main():
    """Main entry point."""
    args = parse_arguments()

    with args.csv as f:
        data = [line.strip().split('|') for line in args.csv]
        data = [[ele.strip() for ele in lst] for lst in data]

    filename = data.pop(0)
    assert os.path.basename(args.csv.name) in filename

    data = verify(data)

    tz = tzlocal.get_localzone()
    lts = tz.localize(datetime.today())

    show(data)
    amounts = [int(d[2]) for d in data if len(d) == 5]
    append = [
        lts.strftime('%Y-%m-%d'), lts.strftime('%H:%M:%S %z'), '00', 'N/A',
        'Running Total: {}'.format(sum(amounts))
    ]

    print
    print append[-1]

    if args.save:
        with open(args.csv.name, 'a') as f:
            f.write(' | '.join(append) + '\n')


if __name__ == '__main__':
    main()
