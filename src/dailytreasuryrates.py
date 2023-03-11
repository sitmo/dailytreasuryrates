import argparse
import logging
import pathlib
import datetime
import pandas as pd
from string import Template
import pkg_resources

url_template = Template(
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/"
    "daily-treasury-rates.csv/${year}/all?type=daily_treasury_yield_curve&field_tdr_date_value=${year}&page&_format=csv"
)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='dailytreasuryrates',
        description='Downloads and/or updates daily treasury rates.'
    )

    parser.add_argument(
        'filename',
        default="daily-treasury-rates.csv",
        nargs='?',
        help="Output file, default is 'daily-treasury-rates.csv' in the current directory."
    )

    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO
    )

    return parser.parse_args()


def load_cache():
    logging.info(f"Reading cache")
    stream = pkg_resources.resource_stream(__name__, 'cache.csv')
    df = pd.read_csv(stream, parse_dates=["Date"]).set_index("Date").sort_index()
    logging.debug(f"Read {len(df)} lines.")
    logging.debug(f"Last date is {df.index[-1]}.")
    return df


def load_file(filename):
    logging.info(f"Reading file {filename}")
    df = pd.read_csv(filename, parse_dates=["Date"]).set_index("Date").sort_index()
    logging.debug(f"Read {len(df)} lines.")
    logging.debug(f"Last date is {df.index[-1]}.")
    return df


def load_url(url):
    logging.debug(f"Reading url {url}")
    df = pd.read_csv(url, parse_dates=["Date"]).set_index("Date").sort_index()
    logging.debug(f"Read {len(df)} lines.")
    logging.debug(f"Last date is {df.index[-1]}.")
    return df


def cli():
    args = parse_args()

    logging.basicConfig(level=args.loglevel)
    start_download_year = 1990
    df = None

    # If the file exist,then first read the lines
    if pathlib.Path(args.filename).is_file():
        df = load_file(args.filename)
    else:
        logging.info(f"{args.filename} does not yet exist.")
        df = load_cache()

    if isinstance(df, pd.DataFrame):
        start_download_year = max(start_download_year, df.index[-1].year)

    today = datetime.date.today()
    for y in range(start_download_year, today.year + 1):
        logging.info(f"Downloading year: {y}")
        url = url_template.substitute(year=y)
        df_new = load_url(url)

        # Add all rows from df that don't currently exist in df_new
        if isinstance(df, pd.DataFrame):
            df = pd.concat([df_new, df[~df.index.isin(df_new.index)]])
        else:
            df = df_new

    # Sort dates
    df = df.sort_index()

    # Save to disk
    logging.info(f"Writing results to {args.filename}")
    df.to_csv(args.filename)
    logging.info(f"Done!")


if __name__ == "__main__":
    cli()
