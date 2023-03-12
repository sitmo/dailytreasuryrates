# Daily Treasury Rates Downloader

A simple command line tool for downloading or updating daily US interest rates (Par Yield Curve Rates) from the US Department of the Treasury.


## Installation

To install run:

~~~
> pip install dailytreasuryrates
~~~

## Usage

To create or update the file `rates.csv` with the latest treasury rates, run the following command:


~~~
> dailytreasuryrates rates.csv
~~~

This will look for the `rates.csv` file in the current folder and append any new data that is available for download on the US treasury site. You can also specify a fully qualitied path like `C:\dataset\myrates.csv` if you want to maintain the rates files at a different location.

A common usage for the rates-file it to load it into Python with Pandas for processing:

~~~
import pandas as pd

df = pd.read_csv('rates.csv', parse_dates=["Date"]).set_index("Date")
~~~


## Output format details
The output file is a `csv` file.

~~~
Date,1 Mo,2 Mo,3 Mo,4 Mo,6 Mo,1 Yr,2 Yr,3 Yr,5 Yr,7 Yr,10 Yr,20 Yr,30 Yr
1990-01-02,,,7.83,,7.89,7.81,7.87,7.9,7.87,7.98,7.94,,8.0
1990-01-03,,,7.89,,7.94,7.85,7.94,7.96,7.92,8.04,7.99,,8.04
...
2023-03-06,4.75,4.79,4.93,5.02,5.22,5.05,4.89,4.61,4.27,4.16,3.98,4.14,3.92
2023-03-07,4.8,4.88,5.04,5.12,5.32,5.22,5.0,4.66,4.31,4.17,3.97,4.11,3.88
~~~

* The first columns contains the date in `yyyy-mm-dd` format. 
* Dates are sorted in ascending order.
* The first date is Jan 2nd 1990.
* The number of tenors has grown over time. E.g. in 1990 there was no `1 Month` and `2 Month` tennor, but now there is. These missing values for older dates have empty string in the csv file, as can be seen in the snipped above.


## Download details

Data gets downloaded from the U.S. DEPARTMENT OF THE TREASURY
: Daily Treasury Par Yield Curve Rates


[https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily\_treasury\_yield\_curve](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve)